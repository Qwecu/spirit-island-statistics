CREATE TABLE player (
id SERIAL PRIMARY KEY,
name TEXT NOT NULL UNIQUE CHECK (name <> ''),
password_hash TEXT,
permanentAccount BIT
);

CREATE TABLE complexity (
    id SERIAL PRIMARY KEY,
    name TEXT NOT NULL CHECK (name <> '')
);

INSERT INTO complexity(name)
VALUES ('Low'), ('Moderate'),('High'),('Very high');

CREATE TABLE gameset (
        id SERIAL PRIMARY KEY,
    name TEXT NOT NULL CHECK (name <> '')
);

INSERT INTO gameset(name)
VALUES ('Base Game'), ('Branch & Claw'),
('Promo Pack 1'),('Jagged Earth'), ('Promo Pack 2');

CREATE TABLE spirit (
    id SERIAL PRIMARY KEY,
    name TEXT NOT NULL UNIQUE CHECK (name <> ''),
    complexityId  INT REFERENCES complexity(id),
    gamesetId  INT REFERENCES gameset(id)
);


INSERT INTO spirit(name, complexityId, gamesetId)
VALUES 
('Lightning' || CHR(39) || 's Swift Strike', 1, 1), --1
('River Surges in Sunlight', 1, 1), --2
('Vital Strength of the Earth', 1, 1), --3
('Shadows Flicker Like Flame', 1, 1), --4
('Thunderspeaker', 2, 1), --5
('A Spread of Rampant Green', 2, 1), --6
('Ocean' || CHR(39) || 's Hungry Grasp', 3, 1), --7
('Bringer of Dreams and Nightmares', 3, 1), --8
('Sharp Fangs Behind the Leaves', 2, 2), --9
('Keeper of the Forbidden Wilds', 2, 2), --10
('Heart of the Wildfire', 3, 3), --11
('Serpent Slumbering Beneath the Island', 3, 3), --12
('Stone' || CHR(39) || 's Unyielding Defiance', 2, 4), --13
('Shifting Memory of Ages', 2, 4), --14
('Grinning Trickster Stirs Up Trouble', 2, 4), --15
('Lure of the Deep Wilderness', 2, 4), --16
('Many Minds Move as One', 2, 4), --17
('Volcano Looming High', 2, 4), --18
('Shroud of Silent Mist', 3, 4), --19
('Vengeance as a Burning Plague', 3, 4), --20
('Starlight Seeks Its Form', 4, 4), --21
('Fractured Days Split the Sky', 4, 4), --22
('Downpour Drenches the World', 3, 5), --23
('Finder of Paths Unseen', 4, 5) --24
;

CREATE TABLE spiritNickname (
    id SERIAL PRIMARY KEY,
    spiritId INT REFERENCES spirit(id),
    name TEXT NOT NULL UNIQUE CHECK (name <> '')
);

INSERT INTO spiritNickname(spiritid, name)
values 
    (1, 'Salama'),
    (2, 'Joki'),
    (3, 'Kivi'),
    (4, 'Varjo'),
    (5, 'Ukkonen'),
    (6, 'Puska'),
    (7, 'Meri'),
    (8, 'Painajainen'),
    (9, 'Tassu'),
    (10, 'Keeper'),
    (11, 'Maastopalo'),
    (12, 'Käärme'),
    (12, 'Saarikäärme'),
    (13, 'Peruskallio'),
    (14, 'Muisto'),
    (15, 'Metkuttaja'),
    (16, 'Sisämaa'),
    (16, 'Sisämaila'),
    (17, 'Pariviäly'),
    (18, 'Tulivuori'),
    (18, 'Vuori'),
    (19, 'Sumu'),
    (19, 'Haittaava sumu'),
    (20, 'Rutto'),
    (21, 'Tähti'),
    (22, 'Ajankääntäjä'),
    (23, 'Mutaveijari'),
    (24, 'Kolibri')
;

CREATE TABLE game(
    id SERIAL PRIMARY KEY,
    guid TEXT,
    time TIMESTAMP,
    scoreCustom INT,
    win BIT,
    lose BIT,
    difficultyCustomChange INT NOT NULL,
    invaderCardsInDeck INT,
    dahan INT,
    blight INT,
    comment TEXT,
    thematicMap BIT,
    extraBoards INT,
    unranked BIT NOT NULL DEFAULT('0')
);


ALTER TABLE game ALTER COLUMN difficultyCustomChange set default 0;

CREATE TABLE adversary(
    id SERIAL PRIMARY KEY,
    name TEXT NOT NULL UNIQUE CHECK (name <> '')
);

INSERT INTO adversary(name)
VALUES
    ('Sweden'),
    ('England'),
    ('Brandenburg-Prussia'),
    ('France'),
    ('Habsburg Monarchy'),
    ('Russia'),
    ('Scotland')
;

CREATE TABLE adversaryLevel(
    id SERIAL PRIMARY KEY,
    adversaryId INT REFERENCES adversary(id),
    level INT NOT NULL,
    difficulty INT NOT NULL,
    adversaryCards INT
);

INSERT INTO adversaryLevel(adversaryId, level, difficulty, adversaryCards)
VALUES
    (1,0,1,12), --Sweden
    (1,1,2,12),
    (1,2,3,12),
    (1,3,5,12),
    (1,4,6,12),
    (1,5,7,12),
    (1,6,8,12),
    (2,0,1,12), --England
    (2,1,3,12),
    (2,2,4,12),
    (2,3,6,12),
    (2,4,7,12),
    (2,5,9,12),
    (2,6,10,12),
    (3,0,1,12), --'Brandenburg-Prussia'
    (3,1,2,12),
    (3,2,4,12),
    (3,3,6,11),
    (3,4,7,10),
    (3,5,9,9),
    (3,6,10,8),
    (4,0,2,12), --'France'
    (4,1,3,12),
    (4,2,5,12),
    (4,3,7,12),
    (4,4,8,12),
    (4,5,9,12),
    (4,6,10,12),
    (5,0,2,12), --'Habsburg Monarchy'
    (5,1,3,12),
    (5,2,6,12),
    (5,3,7,11),
    (5,4,8,11),
    (5,5,9,11),
    (5,6,10,11),
    (6,0,1,12), --'Russia'
    (6,1,3,12),
    (6,2,4,12),
    (6,3,6,12),
    (6,4,7,12),
    (6,5,9,12),
    (6,6,11,12),
    (7,0,1,12), --Scotland
    (7,1,3,12),
    (7,2,4,11),
    (7,3,6,11),
    (7,4,7,11),
    (7,5,8,11),
    (7,6,10,11)
;

CREATE TABLE game_adversaryLevel (
    id SERIAL PRIMARY KEY,
    gameId INT REFERENCES game(id),
    adversaryLevelId INT REFERENCES adversaryLevel(id)
);

CREATE TABLE game_player_spirit(
    id SERIAL PRIMARY KEY,
    gameId INT NOT NULL REFERENCES game(id),
    playerId INT REFERENCES player(id),
    spiritId INT REFERENCES spirit(id)
);