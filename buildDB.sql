DROP DATABASE IF EXISTS IRW;
CREATE DATABASE IRW;
USE IRW;

CREATE TABLE Monster_Listings_Week1
   	 (
      	Keyword varchar(32) NOT NULL, 
        Location varchar(32) NOT NULL,
        Count int NOT NULL,
     	 
      	PRIMARY KEY (Keyword, Location)
        
);

CREATE TABLE Careerbuilder_Listings_Week1
   	 (
      	Keyword varchar(32) NOT NULL, 
        Location varchar(32) NOT NULL,
        Count int NOT NULL,
     	 
      	PRIMARY KEY (Keyword, Location)
        
);

CREATE TABLE Simplyhired_Listings_Week1
   	 (
      	Keyword varchar(32) NOT NULL, 
        Location varchar(32) NOT NULL,
        Count int NOT NULL,
     	 
      	PRIMARY KEY (Keyword, Location)
        
);