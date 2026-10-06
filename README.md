# 🌐 SWAINJOHN Master Repository
### Spatial Workflows Attribute Ingestion Node Jurisdictional Observatory Highways Nexus
### Core Data Ingestion Node Gateway: soggy.gov | Compliance Standard: SOP-COMP-004
### Unique Entity Identifier (UEI): FR6FF67LSVJ3 | CAGE Code: 6UR15 | EIN: 33-4888003

---

## I. PROJECT SPECIFICATION
SWAINJOHN (Spatial Workflows Attribute Ingestion Node Jurisdictional Observatory Highways Nexus) is an independent public trust protection services district operating as a self-contained Governance Node functioning as an authoritative cryptographic overlay. 

By hard-coding compliance into a deterministic runtime environment, the platform replaces traditional, bureaucrat-led systems with Runtime Cryptographic Enforcement (RCE). The system ingests outbound data streams from connected municipal and agency footprints exclusively at the core root government domain (SOGGY.GOV), delivering un-bribable data constants directly to federal agency Offices of Inspectors General (OIGs) to eliminate institutional friction, legal-industry capture, and data-poisoning threat vectors.

---

## II. MASTER DIRECTORY MATRIX
The portfolio is structured across four dedicated, contextually aligned subfolders to isolate production binaries from administrative files:

```text
SWAINJOHN_MASTER_PORTFOLIO/
│
├── README.md                                   # This master system directory documentation
├── verify_acronym.py                           # Python token alignment validation script
│
├── 📁 01_PRODUCTION_SOURCE_CODE/
│   ├── swainjohn_nexus_core.py                 # Form SOGGY-011 Sequential Byte-Stream Filter
│   └── omb_m2521_compliance_crosswalk.py       # CISA OMB M-25-21 incident automation mapping
│
├── 📁 02_DATABASE_AND_STORAGE_LAYERS/
│   ├── swainjohn_overlay_nodes.sql            # PostGIS spatial schema (SRID 2229)
│   └── setup_encrypted_storage.sh              # LUKS bare-metal block device partition setup
│
├── 📁 03_ORCHESTRATION_AND_CI_CD/
│   ├── Dockerfile                              # Hardened Alpine low-privilege runtime sandbox
│   ├── login_gov_proxy.yaml                    # America.gov / Login.gov proxy sidecar deployment
│   └── swainjohn_nexus_ci.yml                  # Automated GitHub Actions validation pipeline
│
└── 📁 04_LEGAL_GOVERNANCE_AND_FEDERAL_FILINGS/
    ├── california_sos_articles_amendment.txt   # Form AMND-NP block-anchored charter amendments
    ├── swainjohn_restated_bylaws.txt           # Mandatory constitutional disclaimers and Purge rules
    ├── gsa_eoffer_modification_addendum.txt    # GSA eOffer technical catalog redline attachment
    └── cisa_domain_authorization_letter.txt    # Official soggy.gov domain registrar request letter
```

---

## III. SECURITY & CRITICAL INFRASTRUCTURE HARDENING

*   **FIPS 140-3 Cryptographic Provenance:** Enforces raw sequential byte-stream header parsing via rigid 12/16/32/32 metadata envelopes (Form SOGGY-011) at the compiler level, requiring asymmetric digital signatures via the ECDSA secp256k1 curve processed inside a physical HSM verified at Level 4 parameters with a 5.0-second maximum clock skew fence.
*   **The GAO-15-593SP Reflex Trigger:** Continually audits all incoming contract transactional records and PostGIS spatial coordinates against the GAO Fraud Risk Framework. Any measured variance delta passing a strict ±1.5% threshold triggers an Automated Condition Subsequent, automatically inflating the asset impedance multiplier to 999.00, air-gapping the local compromised court system, and firing automated webhooks to initiate an immediate Title 23 Section 4(f) FHWA funding lockout within 60 minutes.
*   **Active Physical Site Protection (NODE-DATA-001):** Edge-node computing vaults are encased in industrially sealed, NEMA 4X brushed stainless steel enclosures lined with a light-sensitive optical fiber loop mesh. Any physical casing breach breaks the circuit ground to execute a hardware zeroization loop that wipes the internal HSM and private signature keys within 15 milliseconds. Local thermal climbs crossing a 65°C+ ceiling execute a permanent thermal key-destruction sequence.
*   **Total Institutional Immunization:** In accordance with 42 CFR Part 50 Subpart F, any recorded conflict crossing a strict \$5,000 threshold triggers an automated key self-revocation loop. Corporate bylaws permanently bar active Integrated State Bar members and sitting judicial bench officers from holding voting seats or data-validation keys.
*   **The 14 Multi-Agency Registered Docket Keys:** Automated cross-jurisdictional compliance is monitored live across exactly 14 registered federal tracking dockets, hard-coded directly into the platform context matrices:
    1. `OJP-2026-BJS-0012` (Bureau of Justice Statistics)
    2. `BJS-2026-0004` (BJS Core Tracking Loop)
    3. `GRANT14608593` (Federal Grant Allocation)
    4. `EPA-HQ-OW-2025-0093` (EPA Office of Water)
    5. `EPA-HQ-OW-2021-0602` (EPA WOTUS Spatial Baseline)
    6. `EPA-HQ-OW-2023-0346` (EPA Jurisdictional Boundaries)
    7. `GSA-GSA-2026-0002-0007` (GSA MAS Schedule)
    8. `FAR-2025-0014` (Procurement Integrity Key)
    9. `GSAR-2026-0003` (GSA Acquisition Manual Oversight)
    10. `EIB-2026-0133-0001` (Export-Import Bank Infrastructure)
    11. `OMB-3064-0225` (OMB Regulatory Compliance)
    12. `CFTC-2026-2806` (Commodity Futures Trading Commission)
    13. `RIN-3038-AF79` (RIN System Audit Pipeline)
    14. `NEH-HR-2026-0411` (NEH Section 106 Historic Preservation)

---

## IV. DEPLOYMENT & LOCAL EXECUTION
To generate the local file tree layout and extract your full-text documents with byte-perfect precision, drop the installation script into your machine shell:
```bash
python3 build_portfolio.py
```
To run the automated alignment scanner and verify that the acronym matches character-for-character with zero token drift across your files, execute:
```bash
python3 verify_acronym.py
```

## Local text-file ingestion

The local ingestion utility processes `.txt` files under
`04_LEGAL_GOVERNANCE_AND_FEDERAL_FILINGS/` with bounded parallel file readers
and writes sorted, deterministic JSON Lines to
`02_DATABASE_AND_STORAGE_LAYERS/local_documents.jsonl`:

```bash
python3 ingest_local_documents.py
```

Use `--source PATH`, `--output PATH`, and `--workers N` to override the defaults.
Each record contains only the source-relative path, the SHA-256 of the exact
source bytes, and the UTF-8 content. The utility does not access a network or
database, connect to agency systems, or infer agency identities, docket IDs,
legal validity, or provenance. It operates only on local text files and is not
an autonomous agent or an actual agency docket ingestion service.

## Read-only ArcGIS feature ingestion

`ingest_arcgis_layer.py` reads a paginated ArcGIS FeatureServer layer over
HTTPS and stages the features as JSON Lines in
`02_DATABASE_AND_STORAGE_LAYERS/arcgis_features.jsonl`:

```bash
python3 ingest_arcgis_layer.py \
  --layer-url "https://public.example.gov/arcgis/rest/services/Telemetry/FeatureServer/0"
```

Override the staging path with `--output PATH`; tune `--page-size N` (up to
2000) and the safety cap `--max-features N` as needed. The layer must be
readable by the caller and support standard object-ID queries. The importer
first captures the service's object-ID inventory, then requests explicit ID
batches and rejects duplicate, unexpected, or missing IDs rather than relying
on offset pagination. Each output record preserves the source layer URL,
retrieval time, object ID inventory hash, attributes, original ArcGIS geometry,
resolved spatial reference, numeric geometry SRID, and a SHA-256 hash of the
canonical feature response. It resolves CRS from feature geometry, query
response, or layer metadata, and fails if none is valid. The object-ID
inventory is not an atomic service snapshot: concurrent edits to feature
attributes or geometry during retrieval can still produce a mixed-time result.
This is a local staging import only: it sends
read-only metadata/query requests, does not edit Esri services or write to
PostGIS, and does not establish parcel boundaries, legal status, jurisdiction,
or telemetry provenance. Use only layers and fields you are authorized to
access; private services requiring authentication are not supported by this
initial integration.

## Courthouse indoor GIS schema

`02_DATABASE_AND_STORAGE_LAYERS/swainjohn_indoor_mapping.sql` adds an
idempotent PostGIS schema for facilities, ordered indoor levels, polygonal
spaces, point nodes, and routable edges. Mark a courtroom well explicitly
with `space_type = 'courtroom_well'`; its representative routing point can be
stored as a `node_type = 'courtroom_well'` node linked to that space. The
schema includes source URL/object ID, retrieval time, and source hash fields
for traceability when records come from the read-only ArcGIS staging workflow.

Apply the SQL after PostGIS is installed in the target database. Source
geometries are retained without forcing the existing regional SRID 2229;
`spatial_reference` stores the source ArcGIS spatial-reference JSON and
`geometry_srid` must match `ST_SRID(geometry)`; database checks reject known
WKID/SRID mismatches. For custom WKT systems without a WKID, staged geometries
use SRID 0 and keep the WKT in the source reference. Reproject to a common CRS
explicitly before cross-layer spatial analysis. This schema defines data
storage and routing topology only; it does not assign legal jurisdiction or
determine access permissions, and it is not automatically populated by the
ArcGIS JSONL staging command.
