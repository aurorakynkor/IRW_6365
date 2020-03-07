DELIMITER &&

DROP PROCEDURE IF EXISTS insertJsons;

CREATE PROCEDURE insertJsons()
    BEGIN
        DECLARE @JSON VARCHAR(MAX)

		SELECT @JSON = BulkColumn
		FROM OPENROWSET 
		(BULK 'monster_spider.jl', SINGLE_CLOB) 
		AS j

		SELECT Keyword, Location, Count
		INTO monster_listings_week1
		  FROM OPENJSON (@JSON)
		  WITH (Keyword varchar(32)
			Location varchar(32),
			Count INT
    END &&

DELIMITER ;

call insertJsons();