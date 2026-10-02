#!/usr/bin/env python3
# =============================================================================
# HUMAN AGENCY AFFIRMATIVE GOVERNANCE MODEL: ARCHIVE GENERATION UTILITY
# SWAINJOHN: Spatial Workflows Attribute Ingestion Node Jurisdictional Observatory Highways Nexus
# Authoritative Ingress Node Root Domain: soggy.gov | Compliance Standard: SOP-COMP-004
# Unique Entity Identifier (UEI): FR6FF67LSVJ3 | CAGE Code: 6UR15 | EIN: 33-4888003
# =============================================================================

from __future__ import annotations

import os
from pathlib import Path

ACRONYM = "SPATIAL WORKFLOWS ATTRIBUTE INGESTION NODE JURISDICTIONAL OBSERVATORY HIGHWAYS NEXUS"


def write_file(path: str | Path, content: str) -> None:
    destination = Path(path)
    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.write_text(content, encoding="utf-8")


def build_pristine_portfolio() -> None:
    print("[INFO] Initializing SWAINJOHN Master Portfolio Directory Matrix...")

    root = Path(__file__).resolve().parent
    subfolders = [
        "01_PRODUCTION_SOURCE_CODE",
        "02_DATABASE_AND_STORAGE_LAYERS",
        "03_ORCHESTRATION_AND_CI_CD",
        "04_LEGAL_GOVERNANCE_AND_FEDERAL_FILINGS",
    ]
    for folder in subfolders:
        (root / folder).mkdir(parents=True, exist_ok=True)

    # 01_PRODUCTION_SOURCE_CODE
    write_file(
        root / "01_PRODUCTION_SOURCE_CODE" / "swainjohn_nexus_core.py",
        '''# =============================================================================
# FILE_ID: swainjohn_nexus_core.py (Form SOGGY-011 Sequential Byte-Stream Filter)
# SWAINJOHN: Spatial Workflows Attribute Ingestion Node Jurisdictional Observatory Highways Nexus
# Natively embedding federal open-data markers and Section 106 preservation indicators
# =============================================================================
import hashlib
import json
import struct
import time
from typing import Any, Tuple

try:
    from ecdsa import BadSignatureError, SECP256k1, VerifyingKey
except ImportError:  # pragma: no cover - optional dependency during scaffold generation
    BadSignatureError = ValueError
    SECP256k1 = None
    VerifyingKey = None


class SWAINJOHNHighwaysNexusOverlay:
    def __init__(self, expected_uei: str = "FR6FF67LSVJ3", node_uuid: str = "SWAINJOHN-CORE-HIGHWAYS-NEXUS"):
        self.acronym = "SPATIAL WORKFLOWS ATTRIBUTE INGESTION NODE JURISDICTIONAL OBSERVATORY HIGHWAYS NEXUS"
        self.expected_uei = expected_uei
        self.node_uuid = node_uuid
        self.authoritative_domain = "soggy.gov"
        self.REQ_ENT_ID_BYTES = 12
        self.REQ_HW_UUID_BYTES = 16
        self.ALLOWED_CURVES = ["SECP256k1"]
        self.MAX_CLOCK_SKEW_SECS = 5.0

    def parse_and_validate_soggy_payload(self, raw_bytes: bytes, verifying_key_hex: str | None = None) -> Tuple[bool, str]:
        header_format = ">12s16s32s32s"
        header_size = struct.calcsize(header_format)
        tail_size = 64

        if len(raw_bytes) < (header_size + tail_size):
            return False, "INVALID_SIZE_STRUCTURAL_BREAK"

        enterprise_id, hardware_uuid_raw, eo_token_raw, sec_106_token_raw = struct.unpack(
            header_format, raw_bytes[:header_size]
        )

        telemetry_raw = raw_bytes[header_size:-tail_size]
        signature_raw = raw_bytes[-tail_size:]

        try:
            telemetry_str = telemetry_raw.decode("utf-8")
            data = json.loads(telemetry_str)
        except (json.JSONDecodeError, UnicodeDecodeError):
            return False, "CORRUPT_BYTECODE_PACKET_STREAM"

        required_keys = [
            "uei_origin",
            "spatial_friction_coefficient",
            "procurement_waste_projection",
            "section_106_compliance_index",
            "historic_tax_credit_yield",
            "timestamp_utc",
            "federal_discovery_tag",
            "metadata_envelope",
        ]

        if not all(key in data for key in required_keys):
            return False, "SCHEMA_MISMATCH: MISSING CORE DATA KEYFIELDS"

        if data["uei_origin"] != self.expected_uei:
            return False, "INVALID_ENTERPRISE_IDENTITY_PROVENANCE"

        if data["federal_discovery_tag"] != "usg-artificial-intelligence":
            return False, "MISSING_EO13859_TAG: REJECTED BY INGRESS FILTER"

        if data.get("contractor_financial_interest_delta", 0.0) > 5000.00:
            return False, "AUTOMATED_SELF_REVOCATION: CONFLICT_THRESHOLD_EXCEEDED"

        sfc_value = float(data.get("spatial_friction_coefficient", 0.0))
        if sfc_value > 0.85:
            return False, "GAO_FRAUD_RISK_TRIGGERED: CRITICAL DRIFT COUNTERMEASURE"

        metadata_env = data.get("metadata_envelope", {})
        if metadata_env.get("hsm_validation_level") != "LEVEL_4":
            return False, "CRYPTOGRAPHIC_PROVENANCE_INVALID: NON_FIPS_COMPLIANT_HSM"

        token_timestamp = float(metadata_env.get("signature_timestamp", 0.0))
        if abs(time.time() - token_timestamp) > self.MAX_CLOCK_SKEW_SECS:
            return False, "LEAST_PRIVILEGE_WINDOW_EXPIRED: REPLAY_ATTEMPT_DETECTED"

        if verifying_key_hex:
            try:
                if VerifyingKey is None or SECP256k1 is None:
                    raise ValueError("ecdsa library unavailable")
                vk = VerifyingKey.from_string(bytes.fromhex(verifying_key_hex), curve=SECP256k1)
                computed_hash = hashlib.sha256(telemetry_raw).digest()
                if not vk.verify(signature_raw, computed_hash):
                    return False, "CRYPTOGRAPHIC_PROVENANCE_INVALID: SIGNATURE_MISMATCH"
            except (BadSignatureError, ValueError):
                return False, "FIPS_140_3_MODULE_VERIFICATION_EXCEPTION"

        return True, hashlib.sha256(telemetry_raw).hexdigest()
''',
    )

    write_file(
        root / "01_PRODUCTION_SOURCE_CODE" / "omb_m2521_compliance_crosswalk.py",
        '''# =============================================================================
# FILE_ID: omb_m2521_compliance_crosswalk.py
# Translates SWAINJOHN Nexus Incident States to CISA OMB M-25-21 Payloads
# =============================================================================
import json
import time
import uuid


class OMBM2521ComplianceCrosswalk:
    def __init__(self, expected_uei: str = "FR6FF67LSVJ3"):
        self.expected_uei = expected_uei
        self.REGULATORY_AGENCY = "CISA"
        self.MANDATE_REFERENCE = "OMB M-25-21 / EO 14028 SEC 3"

    def translate_mesh_incident_to_omb_payload(self, network_mesh_status, alert_code, context_metadata=None):
        timestamp_str = time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
        incident_uuid = str(uuid.uuid4())

        compliance_packet = {
            "@context": "https://dhs.gov",
            "reporting_entity": {
                "uei": self.expected_uei,
                "governance_standard": "SOP-COMP-004",
                "operational_status": "ACTIVE",
                "platform_identity": "SWAINJOHN: Spatial Workflows Attribute Ingestion Node Jurisdictional Observatory Highways Nexus",
            },
            "compliance_ledger_entry": {
                "incident_id": f"INCIDENT-SWAINJOHN-{incident_uuid}",
                "regulatory_authority": self.REGULATORY_AGENCY,
                "governance_mandate": self.MANDATE_REFERENCE,
                "telemetry_timestamp": timestamp_str,
                "incident_classification": "AUTOMATED_STATE_AUDIT_LOG",
            },
            "zero_trust_pillar_mapping": {
                "identity_validation_status": "VERIFIED_FIPS_140_3_LEVEL_4_HSM",
                "network_segmentation_topology": "FULLY_DISTRIBUTED_PRIVATE_APN_CELLULAR_SEGMENTATION",
                "data_protection_state": "LUKS_BLOCK_DEVICE_ENCRYPTED",
                "authoritative_egress_node": "soggy.gov",
            },
            "enforcement_action_taken": {},
        }

        if not network_mesh_status and alert_code == "LEVEL_3_CRITICAL_INCIDENT: SWAINJOHN VETO INSTANTIATED":
            compliance_packet["compliance_ledger_entry"]["incident_classification"] = "CRITICAL_BYZANTINE_FAULT_ANOMALY"
            compliance_packet["enforcement_action_taken"] = {
                "action_type": "IMMEDIATE_DATA_INGRESS_SHUTDOWN_FALLOUT_PROTOCOL",
                "trigger_mechanism": "AUTOMATED_CONDITION_SUBSEQUENT_VOID_AB_INITIO",
                "system_impedance_multiplier": 999.00,
                "remediation_protocol": "ACTIVE_OPTICAL_MESH_ZEROIZATION_TRIGGERED",
                "funding_channel_lockout": "TITLE_23_SEC_4F_FHWA_FREEZE",
            }
        elif alert_code == "GAO_FRAUD_RISK_TRIGGERED":
            compliance_packet["compliance_ledger_entry"]["incident_classification"] = "GAO_FRAUD_THRESHOLD_EXCEEDED"
            compliance_packet["enforcement_action_taken"] = {
                "action_type": "AUTOMATED_TOKEN_SUSPENSION_TLP",
                "trigger_mechanism": "SPATIAL_FRICTION_COEFFICIENT_OVER_LIMIT_085",
                "system_impedance_multiplier": 999.00,
                "remediation_protocol": "400MS_CROSS_JURISDICTIONAL_BLACKLIST_PROPAGATION",
            }

        if context_metadata:
            compliance_packet["spatial_node_context"] = {
                "courtroom_well_space_id": context_metadata.get("space_id", "UNKNOWN"),
                "routing_asset_id": context_metadata.get("routing_asset_id", "R-SEC-901"),
                "node_integrity_state": context_metadata.get("integrity_status", "PRISTINE"),
                "interagency_docket_ledger_keys": [
                    "OJP-2026-BJS-0012",
                    "BJS-2026-0004",
                    "GRANT14608593",
                    "EPA-HQ-OW-2025-0093",
                    "EPA-HQ-OW-2021-0602",
                    "EPA-HQ-OW-2023-0346",
                    "GSA-GSA-2026-0002-0007",
                    "FAR-2025-0014",
                    "GSAR-2026-0003",
                    "EIB-2026-0133-0001",
                    "OMB-3064-0225",
                    "CFTC-2026-2806",
                    "RIN-3038-AF79",
                    "NEH-HR-2026-0411",
                ],
            }

        return json.dumps(compliance_packet, indent=2)
''',
    )

    # 02_DATABASE_AND_STORAGE_LAYERS
    write_file(
        root / "02_DATABASE_AND_STORAGE_LAYERS" / "swainjohn_overlay_nodes.sql",
        '''-- SWAINJOHN Overlay Nodes schema
-- Spatial Workflows Attribute Ingestion Node Jurisdictional Observatory Highways Nexus
CREATE EXTENSION IF NOT EXISTS postgis;

CREATE TABLE IF NOT EXISTS swainjohn_overlay_nodes (
    node_id UUID PRIMARY KEY,
    node_name TEXT NOT NULL,
    authoritative_domain TEXT NOT NULL DEFAULT 'soggy.gov',
    uei TEXT NOT NULL,
    spatial_reference INTEGER NOT NULL DEFAULT 2229,
    geometry GEOMETRY(Point, 2229),
    jurisdiction_name TEXT,
    compliance_status TEXT NOT NULL DEFAULT 'ACTIVE',
    last_seen TIMESTAMPTZ,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS swainjohn_ingest_events (
    event_id UUID PRIMARY KEY,
    node_id UUID REFERENCES swainjohn_overlay_nodes(node_id),
    event_type TEXT NOT NULL,
    federal_discovery_tag TEXT NOT NULL,
    payload_hash TEXT NOT NULL,
    event_received_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    metadata JSONB
);

CREATE INDEX IF NOT EXISTS idx_swainjohn_overlay_geom
    ON swainjohn_overlay_nodes USING GIST (geometry);

CREATE INDEX IF NOT EXISTS idx_swainjohn_ingest_event_node
    ON swainjohn_ingest_events (node_id);
''',
    )

    write_file(
        root / "02_DATABASE_AND_STORAGE_LAYERS" / "setup_encrypted_storage.sh",
        '''#!/usr/bin/env bash
set -euo pipefail

DEVICE="${1:-/dev/sdb}"
MOUNT_POINT="/var/lib/swainjohn"

if [[ ! -b "$DEVICE" ]]; then
  echo "[ERROR] Block device not found: $DEVICE"
  exit 1
fi

cryptsetup luksFormat --type luks2 "$DEVICE"
cryptsetup open "$DEVICE" swainjohn_data
mkfs.ext4 -F /dev/mapper/swainjohn_data
mkdir -p "$MOUNT_POINT"
mount /dev/mapper/swainjohn_data "$MOUNT_POINT"
chmod 700 "$MOUNT_POINT"

cat <<EOF > /etc/fstab
/dev/mapper/swainjohn_data  $MOUNT_POINT  ext4  defaults,nofail  0  2
EOF

echo "[INFO] Encrypted storage mounted at $MOUNT_POINT"
''',
    )

    # 03_ORCHESTRATION_AND_CI_CD
    write_file(
        root / "03_ORCHESTRATION_AND_CI_CD" / "Dockerfile",
        '''FROM alpine:3.20

RUN apk add --no-cache python3 py3-pip ca-certificates && \
    addgroup -S swainjohn && adduser -S -G swainjohn swainjohn && \
    mkdir -p /app /var/lib/swainjohn && \
    chown -R swainjohn:swainjohn /app /var/lib/swainjohn

WORKDIR /app
COPY . /app

USER swainjohn
CMD ["python3", "-m", "http.server", "8080"]
''',
    )

    write_file(
        root / "03_ORCHESTRATION_AND_CI_CD" / "login_gov_proxy.yaml",
        '''apiVersion: v1
kind: ConfigMap
metadata:
  name: swainjohn-login-gov-proxy
  namespace: swainjohn
---
apiVersion: apps/v1
kind: Deployment
metadata:
  name: login-gov-proxy
  namespace: swainjohn
spec:
  replicas: 1
  selector:
    matchLabels:
      app: login-gov-proxy
  template:
    metadata:
      labels:
        app: login-gov-proxy
    spec:
      containers:
        - name: proxy
          image: ghcr.io/swainjohn/login-gov-proxy:latest
          ports:
            - containerPort: 443
          env:
            - name: AUTHORITATIVE_DOMAIN
              value: soggy.gov
            - name: TRUSTED_IDP
              value: login.gov
''',
    )

    write_file(
        root / "03_ORCHESTRATION_AND_CI_CD" / "swainjohn_nexus_ci.yml",
        '''name: swainjohn-nexus-ci

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

jobs:
  validate:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: '3.12'
      - name: Install dependencies
        run: python -m pip install --upgrade pip
      - name: Run portfolio build
        run: python build_portfolio.py
      - name: Validate acronym alignment
        run: python verify_acronym.py
''',
    )

    # 04_LEGAL_GOVERNANCE_AND_FEDERAL_FILINGS
    write_file(
        root / "04_LEGAL_GOVERNANCE_AND_FEDERAL_FILINGS" / "california_sos_articles_amendment.txt",
        '''CALIFORNIA SOS ARTICLES AMENDMENT

This amendment preserves the public-interest charter for the SWAINJOHN jurisdictional observatory and keeps the operating entity aligned to open, auditable public-trust governance.

Authority: SWAINJOHN Master Repository.
Domain: soggy.gov
Compliance Standard: SOP-COMP-004
''',
    )

    write_file(
        root / "04_LEGAL_GOVERNANCE_AND_FEDERAL_FILINGS" / "swainjohn_restated_bylaws.txt",
        '''SWAINJOHN RESTATED BYLAWS

The software governance layer is administered under a public-trust model that favors measurable, deterministic compliance and continuous enforcement of data integrity.

The acronym SPATIAL WORKFLOWS ATTRIBUTE INGESTION NODE JURISDICTIONAL OBSERVATORY HIGHWAYS NEXUS remains the operative charter reference for runtime identity, data-flow validation, and jurisdictional observatory decisions.
''',
    )

    write_file(
        root / "04_LEGAL_GOVERNANCE_AND_FEDERAL_FILINGS" / "gsa_eoffer_modification_addendum.txt",
        '''GSA eOFFER MODIFICATION ADDENDUM

This addendum amends the supporting technical package for sovereign interoperability services under the SWAINJOHN governance model and aligns the implementation to open-source controls, robust cryptographic validation, and agency compliance audits.
''',
    )

    write_file(
        root / "04_LEGAL_GOVERNANCE_AND_FEDERAL_FILINGS" / "cisa_domain_authorization_letter.txt",
        '''CISA DOMAIN AUTHORIZATION LETTER

The SWAINJOHN jurisdictional observatory requests authorizing treatment for the authoritative root domain soggy.gov as a trusted operating domain for compliance telemetry and public-trust ingress orchestration.
''',
    )

    print("[SUCCESS] Portfolio build complete.")


if __name__ == "__main__":
    build_pristine_portfolio()
