USE api_db;
DROP TABLE IF EXISTS api_tab;
DROP USER IF EXISTS 'user_api'@'%';


CREATE TABLE api_tab (
	id INT AUTO_INCREMENT  PRIMARY KEY,
    g_api_k_one VARCHAR(100) NOT NULL,
    g_api_k_two VARCHAR(100) NOT NULL,
    se_ID_one VARCHAR(100) NOT NULL,
    se_ID_two VARCHAR(100) NOT NULL,
    hostio VARCHAR(100) NOT NULL
);
