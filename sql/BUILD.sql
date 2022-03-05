CREATE TABLE IF NOT EXISTS tokens (user INTEGER PRIMARY KEY, permission TEXT, token TEXT);
CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT, permission TEXT, password TEXT);
CREATE TABLE IF NOT EXISTS squeezes (id INTEGER PRIMARY KEY AUTOINCREMENT, juice INTEGER, used_apples INTEGER);
CREATE TABLE IF NOT EXISTS investments (user INTEGER PRIMARY KEY, given_apples INTEGER);
CREATE TABLE IF NOT EXISTS totals (of TEXT PRIMARY KEY, value INTEGER);