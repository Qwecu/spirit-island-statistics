Create table measureunit (
id SERIAL PRIMARY KEY,
name TEXT
);

CREATE TABLE ingredients (
id SERIAL PRIMARY KEY,
ingredient TEXT,
price NUMERIC(6, 2),
amount NUMERIC(6, 4),
measureunit_id INT REFERENCES measureunit(id),
priceperunit NUMERIC GENERATED ALWAYS AS (price / amount) STORED
);

INSERT INTO ingredients (ingredient, price, amount)
VALUES
('pipari', 1.5, 0.3),
('punaiset linssit', 1.4, 0.4),
('punaviini', 14.2, 0.75)
;

CREATE TABLE recipes (
id SERIAL PRIMARY KEY,
name TEXT
);

CREATE TABLE recipes_ingredients (
recipe_id INT REFERENCES recipes(id),
ingredient_id INT REFERENCES ingredients(id),
count INT
);

CREATE TABLE filter (
id SERIAL PRIMARY KEY,
name TEXT
);

CREATE TABLE filter_ingredient (
filter_id INT REFERENCES recipes(id),
ingredient_id INT REFERENCES ingredients(id)
);

