# SWAINJOHN Experimental Preview
### Spatial Workflows Attribute Ingestion Node Jurisdictional Observatory Highways Nexus

> **Experimental preview only.** This repository contains prototypes and
> illustrative materials; it is not a production system and is not affiliated
> with or endorsed by a government agency. Names, domains, standards, entity
> identifiers, docket numbers, and legal or operational documents appearing
> here are project examples, not evidence of registration, authorization,
> compliance, legal status, or agency activity.

---

## PROJECT SUPPORT MATERIALS

**New to this repo?** Start here: [GitHub Navigation Guide](docs/GITHUB_NAVIGATION_GUIDE.md)

This guide provides:
- A structured workflow for understanding project scope and architecture
- How to navigate the repo effectively
- Tips for evaluating experimental systems like SWAINJOHN
- Best practices for hackathon participation and agent evaluation

The guide is especially useful if you're exploring this repo as part of an MCP (Model Context Protocol) project or AI agent evaluation.

## MCP SERVER SKELETON

This repository now includes an initial MCP-compatible server layer to support registry-style experimentation without overstating production readiness.

The MCP server skeleton lives in:
- `src/swainjohn_nexus/mcp_server.py`
- `docs/MCP_SERVER.md`

It is intentionally a minimal skeleton focused on:
- validating packet headers
- evaluating spatial drift compliance
- exposing a small, reviewable tool surface for future MCP integration

It is a roadmap toward registry submission, not a claim of full registry completion.

---

## PUBLIC SECTOR MODERNIZATION, GIS WORKFLOW DESIGN, AND AI EVALUATION

SWAINJOHN is designed as a local-first, experimental prototype for public-sector data modernization. It reflects patterns used in public-sector GIS work, local data ingestion pipelines, and AI evaluation frameworks that are increasingly relevant to government technology teams and modern innovation cohorts.

The repository sits at the intersection of three important areas:

1. Public sector GIS and civic data workflows
   SWAINJOHN explores spatial and operational data patterns that resemble the kinds of information systems used in local government, planning, facilities management, and public-service workflows. It incorporates schema design, routing logic, and local staging patterns that align with civic and geospatial modernization efforts.

2. Local-first data ingestion and staging
   The project emphasizes controlled, transparent ingestion of data from local files and read-only external sources. This is an important pattern for public-sector environments where teams need to assess, validate, and stage information before broader operational adoption, while maintaining visibility into provenance, schema constraints, and system boundaries.

3. AI evaluation and operational workflow assessment
   The repository also supports the broader practice of evaluating AI and automation workflows. It does so by documenting evaluation-oriented patterns: system boundaries, local validation, structured ingestion, and explicit limitations. This aligns with AI governance and public-sector AI frameworks that stress trustworthy deployment, measurable success, and clear evaluation criteria.

Together, these themes reflect the kind of work that appears in government technology ecosystems: structured data pipelines, spatial and civic information systems, and evaluation-aware AI experimentation. The project is intentionally designed as an illustrative prototype rather than a production system, which makes it useful for learning, assessment, and early-stage modernization work without overstating operational authority or legal status.

This approach is well aligned with the types of technical patterns found in public-sector GIS, government data models, and AI evaluation repositories, including:
- local and read-only ingestion pipelines
- spatial schema and routing design
- structured data staging for public-service workflows
- documented evaluation criteria for prototype systems

The project is not intended to represent an agency system or official government service. Instead, it functions as a demonstrator for disciplined prototype thinking: local-first, transparent, schema-driven, reviewable, and explicitly bounded in scope.

This framing supports both technical portfolio development and relevance to programs such as TechForce, where participants are expected to show practical experience with modernization work, government-aligned systems, and AI-enabled operational evaluation.

---

## I. PROJECT SCOPE
SWAINJOHN is an experimental collection of local data-staging utilities,
spatial schema examples, and a small packet-header parser and TCP listener.
The local document importer reads files on the machine; the ArcGIS importer
makes read-only HTTPS requests to a layer explicitly supplied by the operator.
These tools do not connect to government systems, transmit data to agencies,
enforce policy, establish legal status, or provide an authoritative data
service.

The project is not production-ready. Treat generated portfolio and legal
documents as illustrative samples only; review them before any use outside a
local experiment.

---

## II. REPOSITORY CONTENTS

The repository contains experimental Python utilities, their tests, example
schemas and documents, and CI workflows. The numbered folders below contain
illustrative artifacts; they are not deployed services or verified agency
materials.

```text
src/swainjohn_nexus/        # Experimental parser and TCP listener package
src/swainjohn_nexus/mcp_server.py  # Initial MCP server skeleton
tests/                      # Unit tests for utilities and package
01_PRODUCTION_SOURCE_CODE/   # Illustrative sample source artifacts
02_DATABASE_AND_STORAGE_LAYERS/ # Example schemas and local ingestion outputs
03_ORCHESTRATION_AND_CI_CD/ # Example deployment and CI configuration artifacts
04_LEGAL_GOVERNANCE_AND_FEDERAL_FILINGS/ # Illustrative document samples
.github/workflows/          # Test and CodeQL workflows
build_portfolio.py          # Generates illustrative portfolio files
ingest_local_documents.py   # Local text-file staging utility
ingest_arcgis_layer.py      # Read-only ArcGIS staging utility
docs/                       # Project documentation and guides
```

---

## III. SECURITY AND PREVIEW LIMITATIONS

The SOGGY-011 parser handles a 92-byte header laid out as 12/16/32/32 bytes.
It rejects inputs shorter than the header and headers whose first field is not
`usg-ai-node`. It decodes the remaining fixed-width fields as text and ignores
any trailing bytes. The field names `uuid`, `hash`, and `signature` describe
their positions only: the parser does not validate their formats, recompute a
hash, verify a signature, or establish sender identity or authenticity.

The TCP listener is a basic prototype, not a secure transport. It does not
provide TLS, client authentication, production-grade framing, or rate limiting.
Do not expose it to untrusted networks or use it to protect sensitive data.
The spatial-drift helper performs a local numeric comparison only; it does not
monitor external data or trigger agency notifications, funding decisions,
network isolation, or other automated actions.

No FIPS validation, ECDSA or other signature verification, HSM integration,
hardware zeroization, key revocation, agency registration, or physical-site
protection is implemented or demonstrated by this preview. References to such
controls or to government programs in generated sample files are illustrative,
not verified claims or operational integrations.

---

## IV. LOCAL EXECUTION
The following script generates illustrative portfolio files and can overwrite
files at its destination. It is not an installer; run it only in a disposable
working directory:
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

---

## MCP SERVER STATUS

This repository is progressing toward MCP compatibility, but it is not yet presented as a registry-ready production package.

The current server skeleton is designed to:
- expose reviewable tools for packet validation and spatial drift checks
- demonstrate a local-first tool pattern compatible with future MCP client integration
- allow the repo to be framed as a prototype environment for AI and civic workflow evaluation

For full registry readiness, the project still requires a more formal server implementation, tools manifest, packaging metadata, and validation against an MCP client runtime.

See: `docs/MCP_SERVER.md`

---

## Conclusion

SWAINJOHN serves as a prototype for structured public-sector modernization, spatial workflow design, and AI system evaluation. It remains intentionally bounded, transparent, and illustrative while still offering a clear technical foundation for future MCP integration and broader government-tech experimentation.

