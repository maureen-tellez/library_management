-- Create editorial table
CREATE TABLE IF NOT EXISTS editorial (
    id_editorial INT NOT NULL,
    name VARCHAR(50) NOT NULL,
    country_of_origin VARCHAR(25) NOT NULL,
    year_established INT NOT NULL,
    PRIMARY KEY (id_editorial),
    CONSTRAINT editorial_check_1 CHECK(year_established > 0)
);

-- Create genre table
CREATE TABLE IF NOT EXISTS genre (
    id_genre INT NOT NULL,
    name VARCHAR(20) NOT NULL,
    PRIMARY KEY (id_genre)
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

-- Create members table
CREATE TABLE IF NOT EXISTS members (
    id_member INT NOT NULL,
    name VARCHAR(50) NOT NULL,
    mobile VARCHAR(20) NOT NULL,
    email VARCHAR(50) NOT NULL,
    PRIMARY KEY (id_member)
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

-- Create reviews table
CREATE TABLE IF NOT EXISTS reviews (
    review_number INT NOT NULL,
    review TEXT NOT NULL,
    book_id_book INT NOT NULL,
    PRIMARY KEY (review_number),
    CONSTRAINT book_id_fk FOREIGN KEY (book_id_book) REFERENCES books (id_book) ON DELETE NO ACTION ON UPDATE NO ACTION
);

-- Create loans table
CREATE TABLE IF NOT EXISTS loans (
    book_id_book INT NOT NULL, 
    member_id_member INT NOT NULL,
    loan_date TIMESTAMP NOT NULL,
    return_date DATE DEFAULT NULL,
    PRIMARY KEY (book_id_book, member_id_member),
    CONSTRAINT book_id_fk FOREIGN KEY (book_id_book) REFERENCES books (id_book) ON DELETE NO ACTION ON UPDATE NO ACTION, 
    CONSTRAINT member_id_fk FOREIGN KEY (member_id_member) REFERENCES members (id_member) ON DELETE NO ACTION ON UPDATE NO ACTION,
    CONSTRAINT loan_return_check CHECK (return_date > loan_date)
);

-- Create book_genres table
CREATE TABLE IF NOT EXISTS book_genres (
    book_id_book INT NOT NULL,
    genre_id_genre INT NOT NULL,
    PRIMARY KEY (book_id_book, genre_id_genre),
    FOREIGN KEY (book_id_book) REFERENCES books(id_book) ON DELETE NO ACTION ON UPDA
