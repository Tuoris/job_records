CREATE TABLE IF NOT EXISTS job_records (
  id SERIAL PRIMARY KEY,
  job_title TEXT NOT NULL,
  company TEXT NOT NULL,
  job_url TEXT NOT NULL,
  score INTEGER NOT NULL,
  salary REAL NOT NULL
);

CREATE TABLE IF NOT EXISTS users (
  id SERIAL PRIMARY KEY,
  username TEXT NOT NULL,
  password TEXT NOT NULL
);
