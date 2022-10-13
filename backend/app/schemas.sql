--  template_info
CREATE TABLE IF NOT EXISTS if_gp_ocr.template_info(
    template_id VARCHAR(17) PRIMARY KEY,
    user_id VARCHAR(5) NOT NULL,
    template_name VARCHAR,
    bbox JSON[],
    updated_at TIMESTAMP WITH TIME ZONE
);

-- GRANT TO if_gp_ocr
GRANT SELECT, INSERT, UPDATE, DELETE ON ALL TABLES IN SCHEMA if_gp_ocr TO if_gp_ocr;
