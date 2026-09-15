CREATE TABLE IF NOT EXISTS processing_runs(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    source TEXT NOT NULL CHECK(source in ('cli', 'api')),
    upc_filename TEXT NOT NULL,
    products_filename TEXT NOT NULL,
    status TEXT NOT NULL DEFAULT 'running' CHECK(status in ('running','success','failed')),
    upc_rows INTEGER,
    products_rows INTEGER,
    output_rows INTEGER,
    validation_issue_count INTEGER DEFAULT 0,
    started_at TEXT NOT NULL,
    finished_at TEXT,
    error_message TEXT
);

CREATE TABLE IF NOT EXISTS validation_issues(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    run_id INTEGER NOT NULL,
    source TEXT NOT NULL,
    row_number INTEGER,
    field TEXT,
    value TEXT,
    error_type TEXT NOT NULL,
    message TEXT NOT NULL,
    FOREIGN KEY (run_id)
    REFERENCES processing_runs(id)
);
