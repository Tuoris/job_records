
DROP TABLE IF EXISTS job_records;

CREATE TABLE job_records (
  id INTEGER PRIMARY KEY autoincrement,
  job_title TEXT NOT NULL,
  company TEXT NOT NULL,
  job_url TEXT NOT NULL,
  score INTEGER NOT NULL,
  salary REAL NOT NULL
);
