import hashlib
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

import ingest_arcgis_layer


LAYER_URL = "https://sampleserver.example/arcgis/rest/services/Telemetry/FeatureServer/0"


class FakeResponse:
    def __init__(self, payload):
        self.payload = json.dumps(payload).encode("utf-8")

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        return False

    def read(self):
        return self.payload


def feature(object_id, x, y):
    return {
        "attributes": {"OBJECTID": object_id, "status": "sample"},
        "geometry": {
            "x": x,
            "y": y,
            "spatialReference": {"wkid": 4326},
        },
    }


class IngestArcGISLayerTests(unittest.TestCase):
    def setUp(self):
        self.temporary_directory = tempfile.TemporaryDirectory()
        self.output = Path(self.temporary_directory.name) / "features.jsonl"
        self.metadata = {
            "objectIdField": "OBJECTID",
            "maxRecordCount": 2,
            "spatialReference": {"wkid": 4326},
        }

    def tearDown(self):
        self.temporary_directory.cleanup()

    def test_fetches_geometry_in_pages_and_stages_traceable_records(self):
        first_feature = feature(1, -77.0, 38.9)
        del first_feature["geometry"]["spatialReference"]
        responses = [
            self.metadata,
            {"objectIds": [3, 1, 2]},
            {"features": [first_feature, feature(2, -76.9, 38.8)]},
            {"features": [feature(3, -76.8, 38.7)]},
        ]
        with patch.object(
            ingest_arcgis_layer,
            "urlopen",
            side_effect=[FakeResponse(payload) for payload in responses],
        ) as mocked_urlopen:
            count = ingest_arcgis_layer.ingest_layer(LAYER_URL, self.output, page_size=2)

        self.assertEqual(count, 3)
        records = [json.loads(line) for line in self.output.read_text(encoding="utf-8").splitlines()]
        self.assertEqual([record["object_id"] for record in records], [1, 2, 3])
        self.assertEqual(records[0]["source_url"], LAYER_URL)
        self.assertEqual(records[0]["geometry"]["x"], -77.0)
        self.assertEqual(records[0]["spatial_reference"], {"wkid": 4326})
        self.assertEqual(records[0]["geometry_srid"], 4326)
        self.assertEqual(len({record["object_id_inventory_sha256"] for record in records}), 1)
        self.assertTrue(records[0]["retrieved_at_utc"].endswith("+00:00"))
        canonical_feature = json.dumps(first_feature, sort_keys=True, separators=(",", ":"), ensure_ascii=False)
        self.assertEqual(records[0]["sha256"], hashlib.sha256(canonical_feature.encode("utf-8")).hexdigest())
        self.assertEqual(mocked_urlopen.call_count, 4)
        first_query = mocked_urlopen.call_args_list[1].args[0].full_url
        second_query = mocked_urlopen.call_args_list[2].args[0].full_url
        third_query = mocked_urlopen.call_args_list[3].args[0].full_url
        self.assertIn("returnIdsOnly=true", first_query)
        self.assertIn("objectIds=1%2C2", second_query)
        self.assertIn("objectIds=3", third_query)
        self.assertNotIn("resultOffset", second_query)
        self.assertIn("returnGeometry=true", second_query)

    def test_rejects_non_https_and_non_feature_layer_urls(self):
        with self.assertRaisesRegex(ingest_arcgis_layer.ArcGISIngestionError, "HTTPS"):
            ingest_arcgis_layer.fetch_features("http://example.org/FeatureServer/0")
        with self.assertRaisesRegex(ingest_arcgis_layer.ArcGISIngestionError, "FeatureServer layer"):
            ingest_arcgis_layer.fetch_features("https://example.org/MapServer/0")

    def test_service_errors_do_not_replace_existing_output(self):
        self.output.write_text("previous\n", encoding="utf-8")
        with patch.object(
            ingest_arcgis_layer,
            "urlopen",
            return_value=FakeResponse({"error": {"message": "not authorized"}}),
        ):
            with self.assertRaisesRegex(ingest_arcgis_layer.ArcGISIngestionError, "not authorized"):
                ingest_arcgis_layer.ingest_layer(LAYER_URL, self.output)
        self.assertEqual(self.output.read_text(encoding="utf-8"), "previous\n")

    def test_refuses_partial_output_when_feature_limit_is_exceeded(self):
        self.output.write_text("previous\n", encoding="utf-8")
        responses = [
            self.metadata,
            {"objectIds": [1, 2]},
        ]
        with patch.object(
            ingest_arcgis_layer,
            "urlopen",
            side_effect=[FakeResponse(payload) for payload in responses],
        ):
            with self.assertRaisesRegex(ingest_arcgis_layer.ArcGISIngestionError, "maximum of 1"):
                ingest_arcgis_layer.ingest_layer(LAYER_URL, self.output, page_size=2, max_features=1)
        self.assertEqual(self.output.read_text(encoding="utf-8"), "previous\n")

    def test_missing_ids_during_fetch_fail_closed(self):
        self.output.write_text("previous\n", encoding="utf-8")
        responses = [
            self.metadata,
            {"objectIds": [1, 2]},
            {"features": [feature(1, -77.0, 38.9)]},
        ]
        with patch.object(
            ingest_arcgis_layer,
            "urlopen",
            side_effect=[FakeResponse(payload) for payload in responses],
        ):
            with self.assertRaisesRegex(ingest_arcgis_layer.ArcGISIngestionError, "missing 1 inventoried"):
                ingest_arcgis_layer.ingest_layer(LAYER_URL, self.output, page_size=2)
        self.assertEqual(self.output.read_text(encoding="utf-8"), "previous\n")

    def test_resolves_crs_from_query_or_layer_metadata_and_rejects_unknown(self):
        query_reference = {"wkid": 32611}
        query_metadata = {"objectIdField": "OBJECTID"}
        feature_without_reference = feature(1, 0, 0)
        del feature_without_reference["geometry"]["spatialReference"]
        resolved, srid = ingest_arcgis_layer._resolve_spatial_reference(
            feature_without_reference, query_reference, query_metadata
        )
        self.assertEqual(resolved, query_reference)
        self.assertEqual(srid, 32611)

        with self.assertRaisesRegex(ingest_arcgis_layer.ArcGISIngestionError, "could not resolve"):
            ingest_arcgis_layer._resolve_spatial_reference(
                feature_without_reference, None, query_metadata
            )


if __name__ == "__main__":
    unittest.main()
