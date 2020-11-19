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

CREATE TABLE quizzes (
    quiz_id     INTEGER PRIMARY KEY,
    category_id INTEGER REFERENCES categories (category_id),
    user_id     INTEGER REFERENCES user (id),
    quiz_name   TEXT,
    plays       INTEGER
);

INSERT INTO quizzes ( quiz_id, category_id, user_id, quiz_name, plays) VALUES (1,0,1,'The sports quiz', 10);

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

INSERT INTO questions ( question_id, quiz_id, question, time_limit, image, answer1, answer2, answer3, answer4, correctAnswer, attempts, correct_attempts) VALUES (1,1,'How much is 1+1?',20, '/static/questionImages/noImage.PNG', 'dunno', '2?', '4', 'help', 'answer1', 5, 3);
INSERT INTO questions ( question_id, quiz_id, question, time_limit, image, answer1, answer2, answer3, answer4, correctAnswer, attempts, correct_attempts) VALUES (2,1,'How much is 1+1?',20, '/static/questionImages/noImage.PNG', 'dunno', '2?', '4', 'help', 'answer1', 5, 3);
INSERT INTO questions ( question_id, quiz_id, question, time_limit, image, answer1, answer2, answer3, answer4, correctAnswer, attempts, correct_attempts) VALUES (3,1,'How much is 1+1?',20, '/static/questionImages/noImage.PNG', 'dunno', '2?', '4', 'help', 'answer1', 5, 3);
INSERT INTO questions ( question_id, quiz_id, question, time_limit, image, answer1, answer2, answer3, answer4, correctAnswer, attempts, correct_attempts) VALUES (4,1,'How much is 1+1?',20, '/static/questionImages/noImage.PNG', 'dunno', '2?', '4', 'help', 'answer1', 5, 3);
INSERT INTO questions ( question_id, quiz_id, question, time_limit, image, answer1, answer2, answer3, answer4, correctAnswer, attempts, correct_attempts) VALUES (5,1,'How much is 1+1?',20, '/static/questionImages/noImage.PNG', 'dunno', '2?', '4', 'help', 'answer1', 5, 3);
INSERT INTO questions ( question_id, quiz_id, question, time_limit, image, answer1, answer2, answer3, answer4, correctAnswer, attempts, correct_attempts) VALUES (6,1,'How much is 1+1?',20, '/static/questionImages/noImage.PNG', 'dunno', '2?', '4', 'help', 'answer1', 5, 3);
INSERT INTO questions ( question_id, quiz_id, question, time_limit, image, answer1, answer2, answer3, answer4, correctAnswer, attempts, correct_attempts) VALUES (7,1,'How much is 1+1?',20, '/static/questionImages/noImage.PNG', 'dunno', '2?', '4', 'help', 'answer1', 5, 3);
INSERT INTO questions ( question_id, quiz_id, question, time_limit, image, answer1, answer2, answer3, answer4, correctAnswer, attempts, correct_attempts) VALUES (8,1,'How much is 1+1?',20, '/static/questionImages/noImage.PNG', 'dunno', '2?', '4', 'help', 'answer1', 5, 3);
INSERT INTO questions ( question_id, quiz_id, question, time_limit, image, answer1, answer2, answer3, answer4, correctAnswer, attempts, correct_attempts) VALUES (9,1,'How much is 1+1?',20, '/static/questionImages/noImage.PNG', 'dunno', '2?', '4', 'help', 'answer1', 5, 3);
INSERT INTO questions ( question_id, quiz_id, question, time_limit, image, answer1, answer2, answer3, answer4, correctAnswer, attempts, correct_attempts) VALUES (10,1,'How much is 1+1?',20, '/static/questionImages/noImage.PNG', 'dunno', '2?', '4', 'help', 'answer1', 5, 3);
INSERT INTO questions ( question_id, quiz_id, question, time_limit, image, answer1, answer2, answer3, answer4, correctAnswer, attempts, correct_attempts) VALUES (11,1,'How much is 1+1?',20, '/static/questionImages/noImage.PNG', 'dunno', '2?', '4', 'help', 'answer1', 5, 3);
INSERT INTO questions ( question_id, quiz_id, question, time_limit, image, answer1, answer2, answer3, answer4, correctAnswer, attempts, correct_attempts) VALUES (12,1,'How much is 1+1?',20, '/static/questionImages/noImage.PNG', 'dunno', '2?', '4', 'help', 'answer1', 5, 3);

CREATE TABLE challenge_progress (
    user_id            INTEGER PRIMARY KEY,
    challenge_progress INTEGER
);

CREATE TABLE challenge_questions (
    question_id INTEGER REFERENCES questions (question_id) 
);



