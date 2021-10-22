-- DROP TABLE filter_ingredient;
-- DROP TABLE filter;
-- DROP TABLE recipes_ingredients;
-- DROP TABLE recipes;
-- DROP TABLE ingredients;
-- DROP TABLE measureunit;
-- DROP TABLE users;
DROP TABLE CASTLES;

-- CREATE TABLE users (
-- id SERIAL PRIMARY KEY,
-- username TEXT NOT NULL UNIQUE CHECK (username <> ''),
-- password_hash TEXT
-- );

CREATE TABLE castles (
id SERIAL PRIMARY KEY,
userId INT REFERENCES users(id),
name TEXT NOT NULL CHECK (name <> ''),
lat FLOAT8 NOT NULL,
lng FLOAT8 NOT NULL,
diameter INT NOT NULL
);


-- CREATE table measureunit (
-- id SERIAL PRIMARY KEY,
-- name TEXT NOT NULL UNIQUE CHECK (name <> '')
-- );

-- INSERT INTO measureunit (name)
-- VALUES
-- ('kg'), ('l')
-- ;

-- CREATE TABLE ingredients (
-- id SERIAL PRIMARY KEY,
-- ingredient TEXT NOT NULL UNIQUE CHECK (ingredient <> ''),
-- price NUMERIC(6, 2) CHECK (price > 0.01),
-- amount NUMERIC(6, 4) CHECK (amount > 0.001),
-- measureunit_id INT NOT NULL REFERENCES measureunit(id),
-- priceperunit NUMERIC GENERATED ALWAYS AS (price / amount) STORED
-- );

-- INSERT INTO ingredients (ingredient, price, amount, measureunit_id)
-- VALUES
-- ('pipari', 1.5, 0.3, 1),
-- ('punaiset linssit', 1.4, 0.4, 1),
-- ('punaviini', 14.2, 0.75, 2),
-- ('pecorino', 3.8, 0.180, 1),
-- ('greippimehu', 2.2, 1, 2)
-- ;

-- CREATE TABLE recipes (
-- id SERIAL PRIMARY KEY,
-- name TEXT NOT NULL UNIQUE CHECK (name <> ''),
-- creator_id INT REFERENCES users(id)
-- );

-- CREATE TABLE recipes_ingredients (
-- recipe_id INT NOT NULL REFERENCES recipes(id),
-- ingredient_id INT NOT NULL REFERENCES ingredients(id),
-- count INT
-- );

-- CREATE TABLE filter (
-- id SERIAL PRIMARY KEY,
-- name TEXT NOT NULL UNIQUE CHECK (name <> '')
-- );

-- insert into filter (name) values ('vegaaninen');
-- insert into filter (name) values ('K-18');
-- insert into filter (name) values ('ei lisättyä sokeria');

-- CREATE TABLE filter_ingredient (
-- filter_id INT NOT NULL REFERENCES filter(id),
-- ingredient_id INT NOT NULL REFERENCES ingredients(id)
-- );

-- insert into filter_ingredient (filter_id, ingredient_id) VALUES (1, 2);
-- insert into filter_ingredient (filter_id, ingredient_id) VALUES (1, 5);
-- insert into filter_ingredient (filter_id, ingredient_id) VALUES (2, 3);
-- insert into filter_ingredient (filter_id, ingredient_id) VALUES (3, 2);
-- insert into filter_ingredient (filter_id, ingredient_id) VALUES (3, 3);
-- insert into filter_ingredient (filter_id, ingredient_id) VALUES (3, 4);
-- insert into filter_ingredient (filter_id, ingredient_id) VALUES (3, 5);