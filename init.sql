CREATE TABLE IF NOT EXISTS stock_data (
    symbol TEXT NOT NULL,
    date   DATE NOT NULL,
    open   NUMERIC,
    close  NUMERIC,
    PRIMARY KEY (symbol, date)
);
