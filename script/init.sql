USE mydatabase;

CREATE TABLE IF NOT EXISTS player_appearances (
    appearance_id VARCHAR(255) PRIMARY KEY,
    game_id INT,
    player_id INT,
    player_club_id INT,
    player_current_club_id INT,
    date DATE,
    player_name VARCHAR(255),
    competition_id VARCHAR(50),
    yellow_cards INT,
    red_cards INT,
    goals INT,
    assists INT,
    minutes_played INT
);

LOAD DATA INFILE '/var/lib/mysql-files/sampled_data_part_6.csv'
INTO TABLE player_appearances
FIELDS TERMINATED BY ',' 
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 ROWS;

LOAD DATA INFILE '/var/lib/mysql-files/sampled_data_part_7.csv'
INTO TABLE player_appearances
FIELDS TERMINATED BY ',' 
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 ROWS;
