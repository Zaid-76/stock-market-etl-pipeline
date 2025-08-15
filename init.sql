CREATE TABLE IF NOT EXISTS stock_data (
    stock_symbol VARCHAR(10),
    date DATE,
    open NUMERIC,
    close NUMERIC,
    PRIMARY KEY (date)
);