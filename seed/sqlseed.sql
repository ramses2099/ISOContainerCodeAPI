-- code	description	length	height	group
CREATE TABLE IF NOT EXISTS ISOContainerType(
    gkey INTEGER PRIMARY KEY AUTOINCREMENT,
    code VARCHAR,
    description	VARCHAR,
    length	INTEGER,
    height REAL,
    "group" VARCHAR
);


INSERT INTO ISOContainerType (code, description, "length", height, "group")
SELECT code, description, "length", height, "group" FROM iso_container_codes;


SELECT gkey, code, description, "length", height, "group"
FROM ISOContainerType;
