-- Create editorial table
CREATE TABLE IF NOT EXISTS editorial (
    id_editorial INT NOT NULL,
    name VARCHAR(50) NOT NULL,
    country_of_origin VARCHAR(25) NOT NULL,
    year_established INT NOT NULL,
    PRIMARY KEY (id_editorial),
    CONSTRAINT editorial_check_1 CHECK(year_established > 0)
);

-- Create authors table
CREATE TABLE IF NOT EXISTS authors (
    id_author INT NOT NULL,
    name VARCHAR(50) NOT NULL,
    nationality VARCHAR(50) NOT NULL,
    year_of_birth INT NOT NULL,
    year_of_death INT DEFAULT NULL,
    PRIMARY KEY (id_author)
);


-- Create books table
CREATE TABLE IF NOT EXISTS books (
    id_book INT NOT NULL,
    title VARCHAR(60) NOT NULL,
    isbn VARCHAR(20) NOT NULL,
    year_of_publication INT NOT NULL,
    language VARCHAR(20) NOT NULL,
    editorial_id_editorial INT NOT NULL,
    author_id_author INT NOT NULL,
    PRIMARY KEY (id_book),
    CONSTRAINT editorial_id_fk FOREIGN KEY (editorial_id_editorial) REFERENCES editorial (id_editorial) ON DELETE NO ACTION ON UPDATE NO ACTION,
    CONSTRAINT author_id_fk FOREIGN KEY (author_id_author) REFERENCES authors (id_author) ON DELETE NO ACTION ON UPDATE NO ACTION
);

