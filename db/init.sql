CREATE DATABASE knights;
use knights;

CREATE TABLE channels (
  id MEDIUMINT NOT NULL AUTO_INCREMENT,
  title VARCHAR(48),
  description VARCHAR(1024),
  PRIMARY KEY (id)
);


INSERT INTO channels
  (title, description)
VALUES
  ('Lancelot', 'blue'),
  ('Galahad', 'yellow');

CREATE TABLE channel_entries (
  id MEDIUMINT NOT NULL AUTO_INCREMENT,
  channel_id INT NOT NULL,
  title VARCHAR(128) NOT NULL,
  link VARCHAR(256) NOT NULL,
  description VARCHAR(1024) NOT NULL,
  PRIMARY KEY (id)
);

INSERT INTO channel_entries
  (channel_id, title, link, description)
VALUES
  (1, 'Galahsad', 'Lancqelot', 'yelloww'),
  (2, 'Galadhad', 'Lanceloqt', 'yelleow');

CREATE TABLE channel_entries_datetimes (
  id MEDIUMINT NOT NULL,
  datetime INT,
  PRIMARY KEY (id)
);