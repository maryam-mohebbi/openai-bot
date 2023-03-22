-- Create the botdb database
CREATE DATABASE IF NOT EXISTS botdb;

-- Create the botuser
CREATE USER IF NOT EXISTS 'botuser'@'%' IDENTIFIED BY 'botpassword';

-- Grant necessary privileges to the botuser
GRANT ALL PRIVILEGES ON botdb.* TO 'botuser'@'%';
FLUSH PRIVILEGES;
