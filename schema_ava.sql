PRAGMA foreign_keys = ON;

CREATE TABLE IF NOT EXISTS essays (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    text TEXT NOT NULL,
    theme TEXT,
    source TEXT,
    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS evaluations (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    essay_id INTEGER NOT NULL,
    score REAL NOT NULL CHECK (score >= 0),
    evaluator TEXT,
    notes TEXT,
    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (essay_id) REFERENCES essays(id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS model_runs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    model_name TEXT NOT NULL,
    dataset_path TEXT,
    train_size INTEGER,
    test_size INTEGER,
    mse REAL,
    rmse REAL,
    mae REAL,
    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS predictions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    essay_id INTEGER,
    model_run_id INTEGER,
    predicted_score REAL NOT NULL,
    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (essay_id) REFERENCES essays(id) ON DELETE SET NULL,
    FOREIGN KEY (model_run_id) REFERENCES model_runs(id) ON DELETE SET NULL
);
