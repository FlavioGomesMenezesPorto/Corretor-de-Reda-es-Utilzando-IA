CREATE TABLE IF NOT EXISTS essays (
    id INT AUTO_INCREMENT PRIMARY KEY,
    text TEXT NOT NULL,
    theme TEXT,
    source TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS evaluations (
    id INT AUTO_INCREMENT PRIMARY KEY,
    essay_id INT NOT NULL,
    score DECIMAL(5,2) NOT NULL CHECK (score >= 0),
    score_coerencia DECIMAL(5,2),
    score_coesao DECIMAL(5,2),
    score_capacidade_argumentativa DECIMAL(5,2),
    evaluator TEXT,
    notes TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (essay_id) REFERENCES essays(id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS model_runs (
    id INT AUTO_INCREMENT PRIMARY KEY,
    model_name TEXT NOT NULL,
    dataset_path TEXT,
    train_size INT,
    test_size INT,
    mse DECIMAL(10,4),
    rmse DECIMAL(10,4),
    mae DECIMAL(10,4),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS predictions (
    id INT AUTO_INCREMENT PRIMARY KEY,
    essay_id INT,
    model_run_id INT,
    predicted_score DECIMAL(5,2) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (essay_id) REFERENCES essays(id) ON DELETE SET NULL,
    FOREIGN KEY (model_run_id) REFERENCES model_runs(id) ON DELETE SET NULL
);
