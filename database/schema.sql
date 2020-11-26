DROP TABLE IF EXISTS questions;
DROP TABLE IF EXISTS quizzes;
DROP TABLE IF EXISTS earned_achievements;
DROP TABLE IF EXISTS achievements;
DROP TABLE IF EXISTS categories;
DROP TABLE IF EXISTS user;
DROP TABLE IF EXISTS challenge_progress;
DROP TABLE IF EXISTS challenge_questions;

CREATE TABLE user (
    id              INTEGER   PRIMARY KEY,
    username        TEXT (15) UNIQUE,
    email           TEXT (50) UNIQUE,
    password        TEXT (80),
    played_quizzes  INTEGER,
    profile_pic     TEXT,
    introduction    TEXT,
    reg_date        DATE,
    challenge_score INTEGER
);

INSERT INTO user (id, username, email, password, played_quizzes, profile_pic, introduction, reg_date, challenge_score) VALUES (1, 'testUser', 'testUser@testUser.com', 'sha256$Nj90WrYv$7f4e8974ab3529be3ff46eee4fd822848e29afb334b92eaae68f9f7b7d188482', 123, '/static/profilePictures/defaultProfPic.png', 'No introduction', '2020-10-03', 32);

CREATE TABLE achievements (
    achievement_id   INTEGER   PRIMARY KEY,
    achievement_name TEXT (80),
    description      TEXT,
    methodname       TEXT,
    condition        TEXT,
    icon             TEXT
);

INSERT INTO achievements ( achievement_id, achievement_name, description, methodname, condition, icon ) VALUES (0,'5 days old account', 'Welcome, newbie', 'memberSince', '5', '/static/achievementIcons/5days.png');
INSERT INTO achievements ( achievement_id, achievement_name, description, methodname, condition, icon ) VALUES (1,'10 days old account','Found a new hobby?', 'memberSince', '10', '/static/achievementIcons/10days.png');
INSERT INTO achievements ( achievement_id, achievement_name, description, methodname, condition, icon ) VALUES (2,'100 days old account', 'You must really like it here', 'memberSince', '100', '/static/achievementIcons/100days.png');
INSERT INTO achievements ( achievement_id, achievement_name, description, methodname, condition, icon ) VALUES (3,'1000 days old account','Veteran', 'memberSince', '1000', '/static/achievementIcons/1000days.png');
INSERT INTO achievements ( achievement_id, achievement_name, description, methodname, condition, icon ) VALUES (4,'10 played quizzes','You can do better than this', 'playedQuizzes', '10', '/static/achievementIcons/10quizzes.png');
INSERT INTO achievements ( achievement_id, achievement_name, description, methodname, condition, icon ) VALUES (5,'100 played quizzes','Getting smarter...', 'playedQuizzes', '100', '/static/achievementIcons/100quizzes.png');
INSERT INTO achievements ( achievement_id, achievement_name, description, methodname, condition, icon ) VALUES (6,'1000 played quizzes','That is some dedication', 'playedQuizzes', '1000', '/static/achievementIcons/1000quizzes.png');
INSERT INTO achievements ( achievement_id, achievement_name, description, methodname, condition, icon ) VALUES (7,'5000 played quizzes','You really have this much freetime?', 'playedQuizzes', '5000', '/static/achievementIcons/5000quizzes.png');

CREATE TABLE earned_achievements (
    user_id        INTEGER REFERENCES user (id),
    achievement_id INTEGER REFERENCES achievements (achievement_id),
    UNIQUE (user_id, achievement_id)
);

CREATE TABLE categories (
    category_id   INTEGER   PRIMARY KEY,
    category_name TEXT (50) 
);

INSERT INTO categories ( category_id, category_name) VALUES (0,'Sports');
INSERT INTO categories ( category_id, category_name) VALUES (1,'Music');
INSERT INTO categories ( category_id, category_name) VALUES (2,'History');
INSERT INTO categories ( category_id, category_name) VALUES (3,'Geography');
INSERT INTO categories ( category_id, category_name) VALUES (4,'Science');
INSERT INTO categories ( category_id, category_name) VALUES (5,'Language');
INSERT INTO categories ( category_id, category_name) VALUES (6,'General knowledge');
INSERT INTO categories ( category_id, category_name) VALUES (7,'Films');

CREATE TABLE quizzes (
    quiz_id     INTEGER PRIMARY KEY,
    category_id INTEGER REFERENCES categories (category_id),
    user_id     INTEGER REFERENCES user (id),
    quiz_name   TEXT,
    plays       INTEGER
);

INSERT INTO quizzes ( quiz_id, category_id, user_id, quiz_name, plays) VALUES (1,6,1,'A general quiz',0);
INSERT INTO quizzes ( quiz_id, category_id, user_id, quiz_name, plays) VALUES (2,4,1,'A science quiz',0);
INSERT INTO quizzes ( quiz_id, category_id, user_id, quiz_name, plays) VALUES (3,1,1,'A music quiz',0);
INSERT INTO quizzes ( quiz_id, category_id, user_id, quiz_name, plays) VALUES (4,0,1,'A sports quiz',0);

CREATE TABLE questions (
    question_id      INTEGER PRIMARY KEY,
    quiz_id          INTEGER REFERENCES quizzes (quiz_id),
    question         TEXT,
    time_limit       INTEGER,
    image            TEXT,
    answer1          TEXT,
    answer2          TEXT,
    answer3          TEXT,
    answer4          TEXT,
    correctAnswer    TEXT,
    attempts         INTEGER,
    correct_attempts INTEGER
);

INSERT INTO questions ( question_id, quiz_id, question, time_limit, image, answer1, answer2, answer3, answer4, correctAnswer, attempts, correct_attempts) VALUES(1, 1, 'Which country operationalized the worlds largest radio telescope?', 10, '/static/questionImages/telescope.jpg', 'USA', 'China', 'Russia', 'India', 'answer2', 0, 0);
INSERT INTO questions ( question_id, quiz_id, question, time_limit, image, answer1, answer2, answer3, answer4, correctAnswer, attempts, correct_attempts) VALUES(2, 1, 'Katerina Sakellaropoulou was elected the first woman President of...', 10, '/static/questionImages/katerina.jpg', 'Greece', 'Spain', 'Finland', 'Netherland', 'answer1', 0, 0);
INSERT INTO questions ( question_id, quiz_id, question, time_limit, image, answer1, answer2, answer3, answer4, correctAnswer, attempts, correct_attempts) VALUES(3, 1, 'Which is the largest coffee producing state of India?', 15, '/static/questionImages/coffee.jpg', 'Kerala', 'Tamil Nadu', 'Karnataka', 'Arunachal Pradesh', 'answer3', 0, 0);
INSERT INTO questions ( question_id, quiz_id, question, time_limit, image, answer1, answer2, answer3, answer4, correctAnswer, attempts, correct_attempts) VALUES(4, 1, 'Nobel prize is awarded for which of the following disciplines?', 10, '/static/questionImages/nobel.jpg', 'Peace and economics', 'Medicine or Physiology', 'Chemistry and Physics', 'All of these', 'answer4', 0, 0);
INSERT INTO questions ( question_id, quiz_id, question, time_limit, image, answer1, answer2, answer3, answer4, correctAnswer, attempts, correct_attempts) VALUES(5, 1, 'Entomology studies what?', 20, '/static/questionImages/noImage.PNG', 'Human beings', 'Insects', 'Rocks', 'Origin of languages', 'answer2', 0, 0);
INSERT INTO questions ( question_id, quiz_id, question, time_limit, image, answer1, answer2, answer3, answer4, correctAnswer, attempts, correct_attempts) VALUES(6, 1, 'Galileo was an astronomer who...', 15, '/static/questionImages/galileo.jpg', 'Developed the telescope', 'Discovered satellites of Jupiter', 'Discovered gravity', 'All of these', 'answer2', 0, 0);
INSERT INTO questions ( question_id, quiz_id, question, time_limit, image, answer1, answer2, answer3, answer4, correctAnswer, attempts, correct_attempts) VALUES(7, 1, 'Who is the father of geometry?', 10, '/static/questionImages/geometry.jpg', 'Aristotle', 'Euclid', 'Pythagoras', 'Kepler', 'answer2', 0, 0);
INSERT INTO questions ( question_id, quiz_id, question, time_limit, image, answer1, answer2, answer3, answer4, correctAnswer, attempts, correct_attempts) VALUES(8, 1, 'The worlds largest desert is?', 10, '/static/questionImages/desert.jpg', 'Thar', 'Kalahari', 'Sahara', 'Sonoran', 'answer3', 0, 0);
INSERT INTO questions ( question_id, quiz_id, question, time_limit, image, answer1, answer2, answer3, answer4, correctAnswer, attempts, correct_attempts) VALUES(9, 1, 'In which year was the Pulitzer Award Introduced?', 15, '/static/questionImages/pulitzer.jpg', '1829', '1918', '1822', '1917', 'answer4', 0, 0);
INSERT INTO questions ( question_id, quiz_id, question, time_limit, image, answer1, answer2, answer3, answer4, correctAnswer, attempts, correct_attempts) VALUES(10, 1, 'What is the worlds smallest bird?', 20, '/static/questionImages/bird.jpg', 'Bee hummingbird', 'Blue jay', 'Parrotlet', 'Colibri', 'answer1', 0, 0);
INSERT INTO questions ( question_id, quiz_id, question, time_limit, image, answer1, answer2, answer3, answer4, correctAnswer, attempts, correct_attempts) VALUES(11, 1, 'What is the lifespan of a dragonfly?', 20, '/static/questionImages/dragonfly.jpg', '1 week', '1 day', '12 hours', '1 month', 'answer2', 0, 0);
INSERT INTO questions ( question_id, quiz_id, question, time_limit, image, answer1, answer2, answer3, answer4, correctAnswer, attempts, correct_attempts) VALUES(12, 2, 'How much water is there on Earth per human being?', 15, '/static/questionImages/water.jpg', '210 billion litres per person', '12 billion litres per person', '250 million litres per person', '750 million litres per person', 'answer1', 0, 0);
INSERT INTO questions ( question_id, quiz_id, question, time_limit, image, answer1, answer2, answer3, answer4, correctAnswer, attempts, correct_attempts) VALUES(13, 2, 'Where were the first computer animations produced?', 20, '/static/questionImages/animation.jpg', 'Rutherford Appleton Laboratory', 'Cambridge University', 'Daresbury Laboratory', 'Harwell Science Campus', 'answer1', 0, 0);
INSERT INTO questions ( question_id, quiz_id, question, time_limit, image, answer1, answer2, answer3, answer4, correctAnswer, attempts, correct_attempts) VALUES(14, 2, 'How many hearts does an octopus have?', 10, '/static/questionImages/octopus.jpg', 'Five', 'Three', 'Six', 'One', 'answer2', 0, 0);
INSERT INTO questions ( question_id, quiz_id, question, time_limit, image, answer1, answer2, answer3, answer4, correctAnswer, attempts, correct_attempts) VALUES(15, 2, 'What is the furthest you can see with the naked eye?', 20, '/static/questionImages/eye.jpg', '2.5 million light years', '250 million light years', '2 million kilometers', '500 kilometers', 'answer1', 0, 0);
INSERT INTO questions ( question_id, quiz_id, question, time_limit, image, answer1, answer2, answer3, answer4, correctAnswer, attempts, correct_attempts) VALUES(16, 2, 'Who invented man-made fizzy drinks?', 15, '/static/questionImages/fizzy.jpg', 'Antoine Lavoisier', 'Carl Wilhelm Scheele', 'Henry Cavendish', 'Joseph Priestley', 'answer4', 0, 0);
INSERT INTO questions ( question_id, quiz_id, question, time_limit, image, answer1, answer2, answer3, answer4, correctAnswer, attempts, correct_attempts) VALUES(17, 3, 'What pop group created the surfin sound?', 10, '/static/questionImages/beachboys.jpg', 'Journey', 'The Cure', 'The Beach Boys', 'Kool and the Gang', 'answer3', 0, 0);
INSERT INTO questions ( question_id, quiz_id, question, time_limit, image, answer1, answer2, answer3, answer4, correctAnswer, attempts, correct_attempts) VALUES(18, 3, 'What was Adeles first record called?', 15, '/static/questionImages/adele.jpg', 'Hometown Glory', 'Rolling In The Deep', ' One and Only', 'Turning Tables', 'answer1', 0, 0);
INSERT INTO questions ( question_id, quiz_id, question, time_limit, image, answer1, answer2, answer3, answer4, correctAnswer, attempts, correct_attempts) VALUES(19, 3, 'Who was lead singer with the 1970s pop group Slade?', 20, '/static/questionImages/slade.jpg', 'Derek Leckenby', 'Peter Noone', 'Karl Green', 'Barry Whitwam', 'answer2', 0, 0);
INSERT INTO questions ( question_id, quiz_id, question, time_limit, image, answer1, answer2, answer3, answer4, correctAnswer, attempts, correct_attempts) VALUES(20, 3, 'Losing my religion was a hit for which rock band?', 20, '/static/questionImages/rem.jpg', 'R.E.M.', 'The Beatles', 'Green Day', 'Arcade Fire', 'answer1', 0, 0);
INSERT INTO questions ( question_id, quiz_id, question, time_limit, image, answer1, answer2, answer3, answer4, correctAnswer, attempts, correct_attempts) VALUES(21, 3, 'Who is the best musician of all time?', 10, '/static/questionImages/paul.jpg', 'Paul McCartney', 'Madonna', 'Elvis Presley', 'Bob Dylan', 'answer1', 0, 0);
INSERT INTO questions ( question_id, quiz_id, question, time_limit, image, answer1, answer2, answer3, answer4, correctAnswer, attempts, correct_attempts) VALUES(22, 3, 'In what year did the Beatles first go to the USA?', 20, '/static/questionImages/beatles.jpg', '1964', '1965', '1963', '1962', 'answer1', 0, 0);
INSERT INTO questions ( question_id, quiz_id, question, time_limit, image, answer1, answer2, answer3, answer4, correctAnswer, attempts, correct_attempts) VALUES(23, 4, 'Who was the BBCs Sports Personality of the Year in 2001?', 10, '/static/questionImages/beckham.jpg', 'Zinedine Zidane', 'David Beckham', 'Diego Maradona', 'Ronaldinho', 'answer1', 0, 0);

CREATE TABLE challenge_progress (
    user_id            INTEGER PRIMARY KEY,
    challenge_progress INTEGER
);

CREATE TABLE challenge_questions (
    question_id INTEGER REFERENCES questions (question_id) 
);



