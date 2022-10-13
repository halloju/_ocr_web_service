CREATE SCHEMA if_gp_ocr;

CREATE TABLE IF NOT EXISTS if_gp_ocr.template_info(
    template_id VARCHAR(19) PRIMARY KEY,
    user_id VARCHAR(5) NOT NULL,
    template_name VARCHAR,
    bbox JSON[],
    created_at TIMESTAMP WITH TIME ZONE DEFAULT current_timestamp,
    updated_at TIMESTAMP WITH TIME ZONE
);
