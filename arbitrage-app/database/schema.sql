CREATE TABLE arbitrage_opportunities (
  opportunity_id INT AUTO_INCREMENT PRIMARY KEY,
  timestamp DATETIME,
  exchange_from VARCHAR(50),
  exchange_to VARCHAR(50),
  coin_pair VARCHAR(20),
  price_diff DECIMAL(10,4),
  fees DECIMAL(10,4),
  net_profit DECIMAL(10,4),
  status ENUM('pending', 'executed', 'expired')
);
CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL
);

CREATE TABLE user_exchanges (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    exchange_name VARCHAR(50) NOT NULL,
    api_key VARCHAR(255) NOT NULL,
    api_secret VARCHAR(255) NOT NULL,
    FOREIGN KEY (user_id) REFERENCES users(id)
);

CREATE TABLE user_coins (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    coin_pair VARCHAR(20) NOT NULL,
    FOREIGN KEY (user_id) REFERENCES users(id)
);