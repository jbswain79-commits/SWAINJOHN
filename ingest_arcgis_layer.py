#!/usr/bin/env python3
"""Read ArcGIS Feature Service features into a traceable local JSONL staging file."""

from __future__ import annotations

import argparse
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import sys
import tempfile
from typing import Any
from urllib.error import HTTPError, URLError
from urllib.parse import urlencode, urlsplit
from urllib.request import Request, urlopen


DEFAULT_OUTPUT = Path(__file__).resolve().parent / "02_DATABASE_AND_STORAGE_LAYERS" / "arcgis_features.jsonl"
DEFAULT_PAGE_SIZE = 500
MAX_PAGE_SIZE = 2000
DEFAULT_MAX_FEATURES = 5000
REQUEST_TIMEOUT_SECONDS = 30


class ArcGISIngestionError(Exception):
    """An expected failure while reading ArcGIS data or writing staged output."""


def _validate_layer_url(layer_url: str) -> str:
    parsed = urlsplit(layer_url)
    if parsed.scheme != "https" or not parsed.netloc or parsed.query or parsed.fragment:
        raise ArcGISIngestionError(
            "layer URL must be an HTTPS ArcGIS Feature Service layer URL without query or fragment"
        )
    if not parsed.path.rstrip("/").lower().endswith("/featureserver/0") and "/featureserver/" not in parsed.path.lower():
        raise ArcGISIngestionError("layer URL must identify a FeatureServer layer, for example .../FeatureServer/0")
    return layer_url.rstrip("/")


def _request_json(url: str, params: dict[str, str]) -> dict[str, Any]:
    request_url = f"{url}?{urlencode(params)}"
    request = Request(
        request_url,
        headers={
            "Accept": "application/json",
            "User-Agent": "SWAINJOHN-read-only-ArcGIS-ingester/1.0",
        },
    )
    try:
        with urlopen(request, timeout=REQUEST_TIMEOUT_SECONDS) as response:
            payload = json.load(response)
    except (HTTPError, URLError, TimeoutError, OSError, json.JSONDecodeError) as exc:
        raise ArcGISIngestionError(f"ArcGIS request failed: {exc}") from exc
    if not isinstance(payload, dict):
        raise ArcGISIngestionError("ArcGIS returned a non-object JSON response")
    if "error" in payload:
        error = payload["error"]
        if isinstance(error, dict):
            detail = error.get("message", "unknown ArcGIS service error")
            if error.get("details"):
                detail = f"{detail}: {'; '.join(map(str, error['details']))}"
        else:
            detail = str(error)
        raise ArcGISIngestionError(f"ArcGIS service error: {detail}")
    return payload


def _metadata(layer_url: str) -> dict[str, Any]:
    metadata = _request_json(layer_url, {"f": "json"})
    object_id_field = metadata.get("objectIdField")
    if not isinstance(object_id_field, str) or not object_id_field:
        raise ArcGISIngestionError("layer metadata does not declare an objectIdField")
    return metadata


def _spatial_reference_id(spatial_reference: dict[str, Any]) -> int:
    value = spatial_reference.get("latestWkid") or spatial_reference.get("wkid")
    if isinstance(value, int) and not isinstance(value, bool) and value >= 0:
        return value
    if isinstance(spatial_reference.get("wkt"), str):
        return 0
    raise ArcGISIngestionError("spatial reference has no valid WKID or WKT definition")


def _resolve_spatial_reference(
    feature: dict[str, Any],
    response_spatial_reference: Any,
    metadata: dict[str, Any],
) -> tuple[dict[str, Any], int]:
    geometry = feature.get("geometry")
    candidates = [
        geometry.get("spatialReference") if isinstance(geometry, dict) else None,
        response_spatial_reference,
        metadata.get("spatialReference"),
    ]
    extent = metadata.get("extent")
    if isinstance(extent, dict):
        candidates.append(extent.get("spatialReference"))

    for candidate in candidates:
        if not isinstance(candidate, dict):
            continue
        try:
            return candidate, _spatial_reference_id(candidate)
        except ArcGISIngestionError:
            continue
    raise ArcGISIngestionError("could not resolve a valid spatial reference from feature, query, or layer metadata")


def fetch_features(
    layer_url: str, page_size: int = DEFAULT_PAGE_SIZE, max_features: int = DEFAULT_MAX_FEATURES
) -> tuple[dict[str, Any], list[tuple[dict[str, Any], Any]], str]:
    """Read and reconcile features against a captured object-ID inventory."""
    layer_url = _validate_layer_url(layer_url)
    if not 1 <= page_size <= MAX_PAGE_SIZE:
        raise ArcGISIngestionError(f"page size must be between 1 and {MAX_PAGE_SIZE}")
    if max_features < 1:
        raise ArcGISIngestionError("maximum feature count must be at least 1")

    metadata = _metadata(layer_url)
    object_id_field = metadata["objectIdField"]
    service_limit = metadata.get("maxRecordCount")
    if isinstance(service_limit, int) and service_limit > 0:
        page_size = min(page_size, service_limit)

    inventory = _request_json(
        f"{layer_url}/query",
        {"f": "json", "where": "1=1", "returnIdsOnly": "true"},
    )
    object_ids = inventory.get("objectIds")
    if not isinstance(object_ids, list):
        raise ArcGISIngestionError("ArcGIS ID inventory response does not contain an objectIds array")
    if any(not isinstance(object_id, (int, str)) or isinstance(object_id, bool) for object_id in object_ids):
        raise ArcGISIngestionError("ArcGIS ID inventory contains an unsupported object ID")
    if len(object_ids) != len(set(object_ids)):
        raise ArcGISIngestionError("ArcGIS ID inventory contains duplicate object IDs")
    if len(object_ids) > max_features:
        raise ArcGISIngestionError(
            f"query exceeds the configured maximum of {max_features} features; increase --max-features explicitly"
        )

    object_ids.sort(key=lambda object_id: (type(object_id).__name__, object_id))
    inventory_hash = hashlib.sha256(
        json.dumps(object_ids, separators=(",", ":"), ensure_ascii=False).encode("utf-8")
    ).hexdigest()
    features_by_id: dict[int | str, tuple[dict[str, Any], Any]] = {}
    for start in range(0, len(object_ids), page_size):
        requested_ids = object_ids[start : start + page_size]
        page = _request_json(
            f"{layer_url}/query",
            {
                "f": "json",
                "objectIds": ",".join(map(str, requested_ids)),
                "outFields": "*",
                "returnGeometry": "true",
                "orderByFields": f"{object_id_field} ASC",
            },
        )
        page_features = page.get("features")
        if not isinstance(page_features, list):
            raise ArcGISIngestionError("ArcGIS query response does not contain a features array")
        if page.get("exceededTransferLimit") is True:
            raise ArcGISIngestionError("ArcGIS exceeded the transfer limit for an explicit object-ID batch")
        for feature in page_features:
            attributes = feature.get("attributes") if isinstance(feature, dict) else None
            object_id = attributes.get(object_id_field) if isinstance(attributes, dict) else None
            if object_id not in requested_ids:
                raise ArcGISIngestionError("ArcGIS returned an object ID absent from the captured inventory batch")
            if object_id in features_by_id:
                raise ArcGISIngestionError(f"ArcGIS returned duplicate feature for object ID {object_id}")
            features_by_id[object_id] = (feature, page.get("spatialReference"))

    missing_ids = set(object_ids) - features_by_id.keys()
    if missing_ids:
        sample_ids = sorted(missing_ids, key=lambda object_id: (type(object_id).__name__, object_id))[:10]
        raise ArcGISIngestionError(
            f"ArcGIS feature response is missing {len(missing_ids)} inventoried object ID(s): {sample_ids}"
        )
    return metadata, [features_by_id[object_id] for object_id in object_ids], inventory_hash


def _feature_record(
    layer_url: str,
    metadata: dict[str, Any],
    feature: dict[str, Any],
    response_spatial_reference: Any,
    retrieved_at: str,
    inventory_hash: str,
) -> dict[str, Any]:
    attributes = feature.get("attributes")
    if not isinstance(attributes, dict):
        raise ArcGISIngestionError("feature is missing its attributes object")
    object_id_field = metadata["objectIdField"]
    if object_id_field not in attributes:
        raise ArcGISIngestionError(f"feature is missing object ID field {object_id_field}")
    spatial_reference, geometry_srid = _resolve_spatial_reference(
        feature, response_spatial_reference, metadata
    )
    source_json = json.dumps(feature, sort_keys=True, separators=(",", ":"), ensure_ascii=False)
    return {
        "source_url": layer_url,
        "retrieved_at_utc": retrieved_at,
        "object_id": attributes[object_id_field],
        "sha256": hashlib.sha256(source_json.encode("utf-8")).hexdigest(),
        "object_id_inventory_sha256": inventory_hash,
        "spatial_reference": spatial_reference,
        "geometry_srid": geometry_srid,
        "attributes": attributes,
        "geometry": feature.get("geometry"),
    }


def _write_jsonl_atomically(output: Path, records: list[dict[str, Any]]) -> None:
    temporary_path: Path | None = None
    try:
        output.parent.mkdir(parents=True, exist_ok=True)
        with tempfile.NamedTemporaryFile(
            mode="w",
            encoding="utf-8",
            newline="\n",
            dir=output.parent,
            prefix=f".{output.name}.",
            suffix=".tmp",
            delete=False,
        ) as temporary:
            temporary_path = Path(temporary.name)
            for record in records:
                temporary.write(json.dumps(record, ensure_ascii=False, separators=(",", ":")))
                temporary.write("\n")
            temporary.flush()
            os.fsync(temporary.fileno())
        os.replace(temporary_path, output)
        temporary_path = None
    except OSError as exc:
        raise ArcGISIngestionError(f"cannot write output {output}: {exc}") from exc
    finally:
        if temporary_path is not None:
            try:
                temporary_path.unlink(missing_ok=True)
            except OSError:
                pass


def ingest_layer(
    layer_url: str,
    output: Path,
    page_size: int = DEFAULT_PAGE_SIZE,
    max_features: int = DEFAULT_MAX_FEATURES,
) -> int:
    normalized_url = _validate_layer_url(layer_url)
    metadata, features, inventory_hash = fetch_features(normalized_url, page_size, max_features)
    retrieved_at = datetime.now(timezone.utc).isoformat()
    records = [
        _feature_record(
            normalized_url,
            metadata,
            feature,
            response_spatial_reference,
            retrieved_at,
            inventory_hash,
        )
        for feature, response_spatial_reference in features
    ]
    _write_jsonl_atomically(Path(output), records)
    return len(records)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Read a public/readable ArcGIS Feature Service layer into local JSONL; no edits are sent."
    )
    parser.add_argument(
        "--layer-url",
        required=True,
        help="HTTPS URL of a FeatureServer layer, such as https://host/arcgis/rest/services/name/FeatureServer/0",
    )
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT, help="local JSONL output path")
    parser.add_argument("--page-size", type=int, default=DEFAULT_PAGE_SIZE, help=f"page size (1-{MAX_PAGE_SIZE})")
    parser.add_argument("--max-features", type=int, default=DEFAULT_MAX_FEATURES, help="hard limit on features read")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    try:
        count = ingest_layer(args.layer_url, args.output, args.page_size, args.max_features)
    except ArcGISIngestionError as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1
    print(f"Staged {count} ArcGIS feature(s) to {args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
