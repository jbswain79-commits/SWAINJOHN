-- SWAINJOHN Overlay Nodes schema
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
