--  Account
CREATE TABLE IF NOT EXISTS if_cdp.account(
    account VARCHAR(8) PRIMARY KEY,
    name VARCHAR NOT NULL,
    birthday VARCHAR NOT NULL,
    hashed_password VARCHAR NOT NULL,
    is_active BOOLEAN NOT NULL,
    is_superuser BOOLEAN NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT current_timestamp,
    updated_at TIMESTAMP WITH TIME ZONE
);
--  Login Hist
CREATE TABLE IF NOT EXISTS if_cdp.login_hist(
    id SERIAL PRIMARY KEY,
    account VARCHAR(8) NOT NULL,
    status VARCHAR NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT current_timestamp
);
-- Campaign
CREATE TABLE IF NOT EXISTS if_cdp.campaign(
    id SERIAL PRIMARY KEY,
    "campaignID" VARCHAR(20),
    name VARCHAR,
    expected_date DATE, 
    created_at TIMESTAMP WITH TIME ZONE DEFAULT current_timestamp,
    updated_at TIMESTAMP WITH TIME ZONE
);
-- Tag
CREATE TABLE IF NOT EXISTS if_cdp.tag(
    id SERIAL PRIMARY KEY,
    tag_name VARCHAR,
    column_name VARCHAR,
    name VARCHAR,
    description VARCHAR,
    table_name VARCHAR,
    categoriess VARCHAR,
    counts INTEGER,
    sql VARCHAR,
    type VARCHAR,
    minima INTERGER,
    maximum BIGINT,
    minima_date TIMESTAMP WITHOUT TIME ZONE,
    maximum_date TIMESTAMP WITHOUT TIME ZONE
    created_at TIMESTAMP WITH TIME ZONE DEFAULT current_timestamp,
    updated_at TIMESTAMP WITH TIME ZONE
);
-- List
CREATE TABLE IF NOT EXISTS if_cdp.list(
    id SERIAL PRIMARY KEY,
    campaign_id INTEGER REFERENCES if_cdp.campaign (id),
    lead_ids INTEGER [],
    department VARCHAR,
    created_by VARCHAR(8),
    creator_dep VARCHAR,
    tag_id INTEGER REFERENCES if_cdp.tag (id),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT current_timestamp,
    updated_at TIMESTAMP WITH TIME ZONE,
    approval_id INTEGER,
    approval_manager JSON,
    approval_employee JSON,
    aprroval_ok_time TIMESTAMP WITH TIME ZONE,
    status VARCHAR,
    metric_status VARCHAR DEFAULT "pending",
    airflow_status VARCHAR DEFAULT "pending",
    check_ab_test BOOLEAN DEFAULT false,
    filename VARCHAR,
    start_query_time TIMESTAMP WITH TIME ZONE,
    query_time TIME,
    adjust_time TIME,
    mail BOOLEAN
);
-- Approval
CREATE TABLE IF NOT EXISTS if_cdp.approval(
    id SERIAL PRIMARY KEY,
    list_id INTEGER REFERENCES if_cdp.list (id),
    account VARCHAR REFERENCES if_cdp.account (account),
    is_manager BOOLEAN NOT NULL,
    approve BOOLEAN,
    comment VARCHAR,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT current_timestamp,
    FOREIGN KEY (list_id) REFERENCES if_cdp.list (id) ON DELETE CASCADE
);
-- Cust List Detail
CREATE TABLE IF NOT EXISTS if_cdp.cust_list_detail(
    id SERIAL PRIMARY KEY,
    campaign_id INTEGER,
    list_id INTEGER,
    lead_id INTEGER,
    creator VARCHAR(8),
    total_count INTEGER,
    final_count INTEGER,
    query_time TIME,
    status VARCHAR,
    error_msg VARCHAR,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT current_timestamp,
    ended_at TIMESTAMP
);
-- Cust List Detail Log
CREATE TABLE IF NOT EXISTS if_cdp.cust_list_detail_log(
    id SERIAL PRIMARY KEY,
    campaign_id INTEGER,
    list_id INTEGER,
    lead_id INTEGER,
    creator VARCHAR(8),
    ended_at TIMESTAMP,
    total_count INTEGER,
    query_time TIME,
    status VARCHAR,
    error_msg VARCHAR,
    use_type VARCHAR,
    sqlstring VARCHAR,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT current_timestamp
);
-- Cust List
CREATE TABLE IF NOT EXISTS if_cdp.cust_list(
    ref_cust_list_detail_id INTEGER REFERENCES if_cdp.cust_list_detail (id),
    ref_cust_list_detail_lead_id INTEGER,
    cust_no VARCHAR,
    check_ab_test BOOLEAN,
    selected BOOLEAN,
    sas_cust_no VARCHAR,
    is_valid BOOLEAN,
    PRIMARY KEY(ref_cust_list_detail_id, ref_cust_list_detail_lead_id, cust_no)
);
-- Cust List Intent
CREATE TABLE IF NOT EXISTS if_cdp.cust_list_intent(
    ref_cust_list_detail_id INTEGER REFERENCES if_cdp.cust_list_detail (id),
    intent VARCHAR,
    PRIMARY KEY(ref_cust_list_detail_id, intent)
);
-- Lead
CREATE TABLE IF NOT EXISTS if_cdp.lead(
    id SERIAL PRIMARY KEY,
    "leadID" VARCHAR(10),
    intent VARCHAR [],
    target_clv VARCHAR [],
    channel VARCHAR,
    version INTEGER,
    counts INTEGER,
    clv INTEGER,
    status VARCHAR,
    download_link VARCHAR,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT current_timestamp,
    updated_at TIMESTAMP WITH TIME ZONE,
    start_query_time TIMESTAMP WITH TIME ZONE,
    query_time TIME,
    adjust_time TIME
);
-- LeadSql
CREATE TABLE IF NOT EXISTS if_cdp.lead_sql(
    lead_id INTEGER REFERENCES if_cdp.lead (id),
    indep_var VARCHAR,
    operator VARCHAR,
    ctrl_var VARCHAR,
    sql_string VARCHAR,
    PRIMARY KEY(lead_id)
);
-- LeadTags
CREATE TABLE IF NOT EXISTS if_cdp.lead_tags(
    id SERIAL PRIMARY KEY,
    lead_id INTEGER REFERENCES if_cdp.lead (id),
    tag_id INTEGER REFERENCES if_cdp.tag (id),
    condition VARCHAR
);
-- Manager
CREATE TABLE IF NOT EXISTS if_cdp.manager(
    account VARCHAR PRIMARY KEY,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT current_timestamp
);
-- TagItems
CREATE TABLE IF NOT EXISTS if_cdp.tag_items(
    id SERIAL PRIMARY KEY,
    ref_cust_list_detail_id INTEGER REFERENCES if_cdp.cust_list_detail (id),
    ref_tags_id INTEGER REFERENCES if_cdp.tag (id),
    FOREIGN KEY (ref_cust_list_detail_id) REFERENCES if_cdp.cust_list_detail (id) ON DELETE CASCADE
);
-- Metrics
CREATE TABLE IF NOT EXISTS if_cdp.metrics(
    id SERIAL PRIMARY KEY,
    lead_id INTEGER REFERENCES if_cdp.lead (id),
    name VARCHAR,
    value INTEGER,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT current_timestamp,
    updated_at TIMESTAMP WITH TIME ZONE
);
-- Metrics SQL
CREATE TABLE IF NOT EXISTS if_cdp.metrics_sql(
    id UUID PRIMARY KEY,
    name VARCHAR,
    sqlfile VARCHAR,
    type VARCHAR,
    params VARCHAR
);
-- Test Stat
CREATE TABLE IF NOT EXISTS if_cdp.test_stat(
    list_id INTEGER,
    ref_cust_list_detail_id INTEGER,
    ref_metrics_sql_id UUID,
    stat FLOAT,
    pval FLOAT,
    is_significant BOOLEAN,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT current_timestamp,
    PRIMARY KEY (list_id, ref_cust_list_detail_id, ref_metrics_sql_id)
);
-- CM CUST CAMP RESP METRICS
CREATE TABLE IF NOT EXISTS if_cdp.cm_cust_camp_resp_metrics(
    ref_cust_list_detail_id INTEGER,
    ref_metrics_sql_id UUID,
    metric_value_7 FLOAT,
    metric_value_14 FLOAT,
    metric_value_30 FLOAT,
    updated_at TIMESTAMP WITH TIME ZONE,
    PRIMARY KEY (ref_cust_list_detail_id, ref_metrics_sql_id)
);
-- GRANT TO if_cdp
GRANT SELECT, INSERT, UPDATE, DELETE ON ALL TABLES IN SCHEMA if_cdp TO if_cdp;
