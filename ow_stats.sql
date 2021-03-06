DROP DATABASE IF EXISTS ow_stats;
CREATE DATABASE ow_stats;
USE ow_stats;

SHOW ENGINE INNODB STATUS;

CREATE TABLE comp_match (
match_id	INT		NOT NULL,
map_name		VARCHAR(25)		NOT NULL,
victory	BOOLEAN		NOT NULL,
is_personal BOOLEAN DEFAULT FALSE,
date_time DATETIME DEFAULT CURRENT_TIMESTAMP,
PRIMARY KEY(match_id)
)ENGINE=InnoDB;

CREATE TABLE player (
match_id	INT		NOT NULL,
player_name		VARCHAR(25)		NOT NULL,
hero		VARCHAR(25)		NOT NULL,
FOREIGN KEY (match_id) REFERENCES comp_match(match_id) ON DELETE CASCADE
)ENGINE=InnoDB;

-- CREATE TABLE personal_game (
-- player_name		VARCHAR(25)		NOT NULL,
-- hero		VARCHAR(25)		NOT NULL,
-- map_name		VARCHAR(25)		NOT NULL,
-- victory	BOOLEAN		NOT NULL,
-- is_personal BOOLEAN DEFAULT TRUE,
-- date_time DATETIME DEFAULT CURRENT_TIMESTAMP
-- )ENGINE=InnoDB;




