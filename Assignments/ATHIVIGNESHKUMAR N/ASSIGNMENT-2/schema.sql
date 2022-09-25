DROP TABLE IF EXISTS client_details;
CREATE TABLE client_details (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  username TEXT NOT NULL,
  email TEXT NOT NULL,
  password TEXT NOT NULL
);