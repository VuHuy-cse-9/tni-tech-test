CREATE EXTENSION IF NOT EXISTS pgcrypto;

CREATE TABLE detection_results (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    det_box_count INTEGER NOT NULL,
    vis_image_path TEXT NOT NULL
);