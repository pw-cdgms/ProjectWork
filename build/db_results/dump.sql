USE results_db;
DROP TABLE IF EXISTS search_app_results;
DROP USER IF EXISTS 'search_app_user'@'%';


CREATE TABLE search_app_results (
	id INT AUTO_INCREMENT  PRIMARY KEY,
    query VARCHAR(100) NOT NULL,
    website VARCHAR(100) NOT NULL,
    ip VARCHAR(20) NOT NULL,
    dns VARCHAR(70) NOT NULL,
    email VARCHAR(100),
    ig_link VARCHAR(100),
    ig_username VARCHAR(50),
    ig_followers VARCHAR(10),
    ig_posts VARCHAR(20)
);

