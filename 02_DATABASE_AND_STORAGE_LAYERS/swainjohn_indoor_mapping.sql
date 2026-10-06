-- Indoor mapping schema for courthouse facilities, levels, spaces, routing nodes, and edges.
-- Geometry retains its source spatial reference; see spatial_reference on each record.

CREATE EXTENSION IF NOT EXISTS postgis;

CREATE TABLE IF NOT EXISTS indoor_facilities (
    facility_id UUID PRIMARY KEY,
    facility_code TEXT NOT NULL UNIQUE,
    facility_name TEXT NOT NULL,
    source_uri TEXT,
    source_layer_url TEXT,
    source_object_id TEXT,
    spatial_reference TEXT NOT NULL,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE TABLE IF NOT EXISTS indoor_levels (
    level_id UUID PRIMARY KEY,
    facility_id UUID NOT NULL REFERENCES indoor_facilities(facility_id),
    level_code TEXT NOT NULL,
    level_name TEXT NOT NULL,
    vertical_order INTEGER NOT NULL,
    elevation NUMERIC,
    elevation_unit TEXT,
    spatial_reference TEXT NOT NULL,
    source_uri TEXT,
    source_layer_url TEXT,
    source_object_id TEXT,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    UNIQUE (facility_id, level_code),
    UNIQUE (facility_id, vertical_order)
);

CREATE TABLE IF NOT EXISTS indoor_spaces (
    space_id UUID PRIMARY KEY,
    level_id UUID NOT NULL REFERENCES indoor_levels(level_id),
    space_code TEXT NOT NULL,
    space_name TEXT NOT NULL,
    space_type TEXT NOT NULL CHECK (
        space_type IN (
            'courtroom',
            'courtroom_well',
            'corridor',
            'lobby',
            'stair',
            'elevator',
            'other'
        )
    ),
    geometry geometry,
    spatial_reference JSONB NOT NULL,
    geometry_srid INTEGER,
    source_uri TEXT,
    source_layer_url TEXT,
    source_object_id TEXT,
    retrieved_at TIMESTAMPTZ,
    source_hash TEXT,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    UNIQUE (level_id, space_code),
    CHECK (
        geometry IS NULL
        OR ST_GeometryType(geometry) IN ('ST_Polygon', 'ST_MultiPolygon')
    ),
    CHECK (
        geometry IS NULL
        OR (
            geometry_srid IS NOT NULL
            AND ST_SRID(geometry) = geometry_srid
            AND (
                spatial_reference ->> 'latestWkid' = geometry_srid::TEXT
                OR spatial_reference ->> 'wkid' = geometry_srid::TEXT
                OR (spatial_reference ? 'wkt' AND geometry_srid = 0)
            )
        )
    )
);

CREATE TABLE IF NOT EXISTS indoor_nodes (
    node_id UUID PRIMARY KEY,
    level_id UUID NOT NULL REFERENCES indoor_levels(level_id),
    space_id UUID REFERENCES indoor_spaces(space_id),
    node_code TEXT NOT NULL,
    node_name TEXT NOT NULL,
    node_type TEXT NOT NULL CHECK (
        node_type IN (
            'courtroom_well',
            'entrance',
            'junction',
            'poi',
            'stair',
            'elevator',
            'other'
        )
    ),
    geometry geometry,
    spatial_reference JSONB NOT NULL,
    geometry_srid INTEGER,
    source_uri TEXT,
    source_layer_url TEXT,
    source_object_id TEXT,
    retrieved_at TIMESTAMPTZ,
    source_hash TEXT,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    UNIQUE (level_id, node_code),
    CHECK (geometry IS NULL OR ST_GeometryType(geometry) = 'ST_Point'),
    CHECK (
        geometry IS NULL
        OR (
            geometry_srid IS NOT NULL
            AND ST_SRID(geometry) = geometry_srid
            AND (
                spatial_reference ->> 'latestWkid' = geometry_srid::TEXT
                OR spatial_reference ->> 'wkid' = geometry_srid::TEXT
                OR (spatial_reference ? 'wkt' AND geometry_srid = 0)
            )
        )
    )
);

CREATE TABLE IF NOT EXISTS indoor_edges (
    edge_id UUID PRIMARY KEY,
    from_node_id UUID NOT NULL REFERENCES indoor_nodes(node_id),
    to_node_id UUID NOT NULL REFERENCES indoor_nodes(node_id),
    edge_type TEXT NOT NULL CHECK (
        edge_type IN ('path', 'door', 'stair', 'elevator', 'transition', 'other')
    ),
    geometry geometry,
    spatial_reference JSONB NOT NULL,
    geometry_srid INTEGER,
    is_accessible BOOLEAN,
    source_uri TEXT,
    source_layer_url TEXT,
    source_object_id TEXT,
    retrieved_at TIMESTAMPTZ,
    source_hash TEXT,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    CHECK (from_node_id <> to_node_id),
    CHECK (
        geometry IS NULL
        OR ST_GeometryType(geometry) IN ('ST_LineString', 'ST_MultiLineString')
    ),
    CHECK (
        geometry IS NULL
        OR (
            geometry_srid IS NOT NULL
            AND ST_SRID(geometry) = geometry_srid
            AND (
                spatial_reference ->> 'latestWkid' = geometry_srid::TEXT
                OR spatial_reference ->> 'wkid' = geometry_srid::TEXT
                OR (spatial_reference ? 'wkt' AND geometry_srid = 0)
            )
        )
    )
);

CREATE INDEX IF NOT EXISTS idx_indoor_spaces_geom
    ON indoor_spaces USING GIST (geometry);

CREATE INDEX IF NOT EXISTS idx_indoor_spaces_level_type
    ON indoor_spaces (level_id, space_type);

CREATE INDEX IF NOT EXISTS idx_indoor_nodes_geom
    ON indoor_nodes USING GIST (geometry);

CREATE INDEX IF NOT EXISTS idx_indoor_nodes_level_space
    ON indoor_nodes (level_id, space_id);

CREATE INDEX IF NOT EXISTS idx_indoor_edges_geom
    ON indoor_edges USING GIST (geometry);

CREATE INDEX IF NOT EXISTS idx_indoor_edges_endpoints
    ON indoor_edges (from_node_id, to_node_id);
