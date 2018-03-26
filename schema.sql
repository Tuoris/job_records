CREATE TABLE job_records (
  id SERIAL PRIMARY KEY,
  job_title TEXT NOT NULL,
  company TEXT NOT NULL,
  job_url TEXT NOT NULL,
  score INTEGER NOT NULL,
  salary REAL NOT NULL
);
