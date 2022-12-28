CREATE SCHEMA if_gp_ocr;


CREATE TABLE IF NOT EXISTS if_gp_ocr.template_info(
    template_id VARCHAR(19) PRIMARY KEY,
    user_id VARCHAR(5) NOT NULL,
    template_name VARCHAR,
    bbox JSON[],
    updated_at TIMESTAMP WITH TIME ZONE,
    is_public BOOLEAN NOT NULL
);

/*紀錄驗證碼辨識結果的表*/
CREATE TABLE IF NOT EXISTS if_gp_ocr.ocr_results(
    image_cv_id character varying,
    tag character varying,
    det_model character varying,
    rec_model character varying,
    text character varying,
    det_prob float,
    rec_prob float,
    x_1 int,
    y_1 int,
    x_2 int,
    y_2 int,
    x_3 int,
    y_3 int,
    x_4 int,
    y_4 int,
    etl_dt timestamp without time zone not null default current_timestamp
);

CREATE INDEX IF NOT EXISTS ocr_results_etl_dt ON if_gp_ocr.ocr_results (etl_dt);
