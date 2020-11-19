from flask import Flask, g 
import sqlite3, os, atexit, time, schedule, random, uuid
from flask import Flask, render_template, redirect, url_for, jsonify, request, session, make_response, json, flash
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm 
from datetime import date, datetime
from wtforms import StringField, PasswordField, BooleanField
from wtforms.validators import InputRequired, Email, Length
from flask_sqlalchemy  import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from apscheduler.schedulers.background import BackgroundScheduler
from PIL import Image

def checkForAchievements():
    with app.app_context():
        db = get_db()
        sql = "SELECT * FROM achievements"       
        achievements = db.cursor().execute(sql).fetchall()
        result = ''
        for item in achievements:
            achievement_id = item[0]
            method_name = item[3]
            condition = item[4]
            #this way of calling a method by its name is from a stackoverflow page - add link
            possibles = globals().copy()
            possibles.update(locals())
            method = possibles.get(method_name)
            if not method:
                raise NotImplementedError("Method %s not implemented" % method_name)
            result = result + method(achievement_id, condition)
        return result

def createDailyChallenge():
    with app.app_context():
        db = get_db()
        sql = "DELETE FROM challenge_questions"
        db.cursor().execute(sql)
        db.commit()
        sql = "DELETE FROM challenge_progress"
        db.cursor().execute(sql)
        db.commit()
        sql = "SELECT count(*) FROM questions"    
        numberOfQuestions = db.cursor().execute(sql).fetchone()        
        questionIds = random.sample(range(1,numberOfQuestions[0]), 10)
        questionIDs = []
        for item in questionIds:
            questionId = []
            questionId.append(item)
            questionIDs.append(questionId)
        cursor = db.cursor()
        cursor.executemany("INSERT INTO challenge_questions (question_id) VALUES(?);", questionIDs)
        db.commit()
        return str(questionIDs)

#should only be checked at midnight in a real environment
scheduler = BackgroundScheduler()
scheduler.add_job(func=checkForAchievements, trigger="interval", seconds=10)
scheduler.add_job(func=createDailyChallenge, trigger="interval", seconds=10)
scheduler.start()
atexit.register(lambda: scheduler.shutdown())
app = Flask(__name__)

app.config['SECRET_KEY'] = 'b"\'\xb6\x0c\x06\xf3\xe8\x9do\xb4\xfb\xffx\x12\xafQ!\x8e\xd7ew)\x1a\x0b\x81"'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database/quizia.db'

#todo: better templating
#todo: improve editProfile validation
#todo: style 404 page
#todo: improve css and html
#todo: separate code to different files

UPLOAD_FOLDER = 'Quizia\static\questionImages'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

UPLOAD_FOLDER2 = 'Quizia\static\profilePictures'
app.config['UPLOAD_FOLDER2'] = UPLOAD_FOLDER2

bootstrap = Bootstrap(app)
db = SQLAlchemy(app)
db_location = 'Quizia\database\quizia.db'
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(15), unique=True)
    email = db.Column(db.String(50), unique=True)
    password = db.Column(db.String(80))
    played_quizzes = db.Column(db.Integer)
    profile_pic = db.Column(db.Text())
    introduction = db.Column(db.String(300))
    reg_date = db.Column(db.Date)
    challenge_score = db.Column(db.Integer)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[InputRequired(), Length(min=4, max=15)])
    password = PasswordField('Password', validators=[InputRequired(), Length(min=8, max=80)])
    remember = BooleanField('Stay logged in')

class RegisterForm(FlaskForm):
    email = StringField('E-mail', validators=[InputRequired(), Email(message='Invalid email'), Length(max=50)])
    username = StringField('Username', validators=[InputRequired(), Length(min=4, max=15)])
    password = PasswordField('Password', validators=[InputRequired(), Length(min=8, max=80)])

def init_db():
    with app.app_context():
        db = get_db()
        with app.open_resource('database/schema.sql', mode='r') as f:
            db.cursor().executescript(f.read())
        db.commit()

def get_db():
    db = getattr(g, 'db', None)
    if db is None:
        db = sqlite3.connect(db_location)
        g.db = db
    return db

@app.route('/')
@login_required
def index():   
    return redirect(url_for('home'))

@app.route('/listusers')
@login_required
def listusers():
    db = get_db()
    page = []
    page.append(' ')
    sql = "SELECT * FROM user"
    for row in db.cursor().execute(sql):
        page.append(str(row)) 
    return ''.join(page)

@app.route('/querydatabase')
@login_required
def listcategories():
    db = get_db()
    page = []
    page.append(' ')
    sql = "SELECT u.username, u.played_quizzes, u.profile_pic, u.introduction, u.reg_date, (SELECT COUNT(*) FROM quizzes q WHERE q.user_id = 1) as created_quizzes, u.challenge_score, u.played_quizzes + (u.challenge_score * 10) + ((SELECT COUNT(*) FROM earned_achievements ea WHERE ea.user_id = 1) * 15) as score FROM user u WHERE u.id = 1"
    categoryIDs = db.cursor().execute(sql).fetchall()
    for item in categoryIDs:
        page.append(str(item))
    # for row in db.cursor().execute(sql):
    #     page.append(str(row)) 
    return ''.join('b"\'\xb6\x0c\x06\xf3\xe8\x9do\xb4\xfb\xffx\x12\xafQ!\x8e\xd7ew)\x1a\x0b\x81"')

#if id < 0 or id > table length return 404
@app.route('/play/<quiz_id>')
@login_required
def play(quiz_id):
    db = get_db() 
    cur = db.cursor()  
    sql = "SELECT COUNT(*) FROM quizzes WHERE quiz_id = " + quiz_id + ""
    result = cur.execute(sql)
    rowcount = result.fetchall()
    if rowcount[0][0] > 0:
        db = get_db() 
        cur = db.cursor()  
        sql = "UPDATE quizzes SET plays = plays + 1 WHERE quiz_id = {}"
        cur.execute(sql.format(quiz_id))
        db.commit()        
        sql = "SELECT qu.quiz_name, u.username, qs.question_id, qs.quiz_id, qs.question, qs.time_limit, qs.image, qs.answer1, qs.answer2, qs.answer3, qs.answer4, qs.correctAnswer, qs.attempts, qs.correct_attempts FROM questions qs JOIN quizzes qu ON qs.quiz_id = qu.quiz_id JOIN user u ON qu.user_id = u.id WHERE qs.quiz_id = {}"
        questions = []    
        cur.execute(sql.format(quiz_id))
        #idea from https://stackoverflow.com/questions/3286525/return-sql-table-as-json-in-python
        r = [dict((cur.description[i][0], value) for i, value in enumerate(row)) for row in cur.fetchall()]
        userid = current_user.id
        return render_template('playQuiz.html', questions=r, name=current_user.username, userid=userid)
    else:
        return render_template('404.html'), 404

@app.route('/categories')
@login_required
def categories():
    db = get_db()
    categories = []
    sql = "SELECT category_name FROM categories"
    for category in db.cursor().execute(sql):
        categories.append(category[0])
    return render_template('categories.html', categories=categories, name=current_user.username)

@app.route('/randomQuiz')
@login_required
def randomQuiz():
    db = get_db()    
    sql = "SELECT quiz_id FROM quizzes ORDER BY RANDOM() LIMIT 1"
    quiz_id = db.cursor().execute(sql).fetchone()[0]
    return redirect(url_for('play', quiz_id=quiz_id))  

@app.route('/createQuiz')
@login_required
def createQuiz():
    return render_template('createQuiz.html', name=current_user.username, categories=categories)

def paging(page, sql, template):
    db = get_db() 
    cur = db.cursor()  
    sql = sql
    startLimit = int(page) * 20 - 20
    result = cur.execute(sql.format(startLimit,21))    
    rowcount = result.fetchall()
    disableNext = 1
    data = []
    if len(rowcount) == 0 and int(page) == 1:
        return render_template(template, name=current_user.username, data=data, page=page, disableNext=disableNext)
    elif len(rowcount) == 0 and int(page) != 0:
        return render_template('404.html'), 404
    elif int(page) < 1:
        return render_template('404.html'), 404
    else:
        for item in cur.execute(sql.format(startLimit, 20)):
            data.append(item)
        if len(rowcount) > 20:
            disableNext = 0
        return render_template(template, name=current_user.username, data=data, page=page, disableNext=disableNext)

@app.route('/categories/<category>/<page>')
@login_required
def categoriesCategory(category, page):
    db = get_db() 
    cur = db.cursor()  
    sql = "SELECT COUNT(*) FROM categories WHERE category_name = '" + category + "'"
    result = cur.execute(sql)
    rowcount = result.fetchall()
    if rowcount[0][0] > 0:
        sql = "SELECT quiz_id, c.category_name, u.username, quiz_name, plays FROM quizzes q JOIN user u ON q.user_id = u.id JOIN categories c ON q.category_id = c.category_id WHERE c.category_name = '" + category + "' LIMIT {}, {}"
        template = 'category.html'
        return paging(page, sql, template) 
    else:
        return render_template('404.html'), 404

@app.route('/popular/<page>')
@login_required
def popular(page):  
    sql = "SELECT q.quiz_id, c.category_name, u.username, q.quiz_name, q.plays FROM quizzes q JOIN user u ON q.user_id = u.id JOIN categories c ON q.category_id = c.category_id ORDER BY q.plays DESC LIMIT {}, {}"
    template = 'popularQuizzes.html'
    return paging(page, sql, template)

@app.route('/myQuizzes/<page>')
@login_required
def myQuizzes(page):    
    sql = "SELECT q.quiz_id, c.category_name, u.username, q.quiz_name, q.plays FROM quizzes q JOIN user u ON q.user_id = u.id JOIN categories c ON q.category_id = c.category_id WHERE q.user_id = " + str(current_user.id) + " LIMIT {}, {}"
    template = 'myQuizzes.html'
    return paging(page, sql, template)

@app.route('/leaderboard/<page>')
@login_required
def leaderboard(page):
    sql = "SELECT u.id, u.username, u.played_quizzes + (u.challenge_score * 10) + ((SELECT COUNT(*) FROM earned_achievements ea WHERE ea.user_id = u.id) * 15) as score, (SELECT COUNT(*) FROM earned_achievements ea WHERE ea.user_id = u.id) as numberOfAchievements, u.played_quizzes, u.challenge_score FROM user u ORDER BY score DESC LIMIT {}, {}"
    template = 'leaderboard.html'
    return paging(page, sql, template)

@app.route('/achievements')
@login_required
def achievements():
    db = get_db()
    sql = "SELECT * FROM achievements"
    achievements = []        
    for achievement in db.cursor().execute(sql):
        achievements.append(achievement)
    return render_template('achievements.html', achievements=achievements, name=current_user.username)   

@app.route('/_checkForAchievements')
@login_required
def _checkForAchievements():
    result = checkForAchievements()
    return result

def memberSince(achievement_id, condition):
    db = get_db()
    today = date.today()
    stringDate = today.strftime("%m/%d/%Y")
    result = ''
    sql = "SELECT id, reg_date FROM user"
    users = db.cursor().execute(sql).fetchall()
    for item in users:
        difference = datetime.now() - datetime.strptime(item[1], '%Y-%m-%d')
        if difference.days >= int(condition):
            result = achievement_id
            sql = "INSERT OR IGNORE INTO earned_achievements(user_id, achievement_id) VALUES(?,?)"
            db.cursor().execute(sql, (item[0], achievement_id))
            db.commit()
        else:
            result = "didn't meet condition|"
    return str(result)

def playedQuizzes(achievement_id, condition):
    db = get_db()
    sql = "SELECT id, played_quizzes FROM user"
    result = ''
    users = db.cursor().execute(sql).fetchall()
    for item in users:
        if item[1] >= int(condition):
            result = achievement_id
            sql = "INSERT OR IGNORE INTO earned_achievements(user_id, achievement_id) VALUES(?,?)"
            db.cursor().execute(sql, (item[0], achievement_id))
            db.commit()
        else:
            result = "didn't meet condition"
    return str(result)

@app.route('/_saveQuizToDB', methods=['GET', 'POST'])
@login_required
def _saveQuizToDB():
    f = request.form  
    try:
        db = get_db()
        cursor = db.cursor()
        sql = "SELECT category_id FROM categories"
        categoryIDs = cursor.execute(sql).fetchall()
        #quizname cannot be empty        
        if not f['quizName']:
            raise Exception("Quiz name was empty")
        #selectcategory cannot be empty, has to be in category table id
        categoryExists = False
        if not f['selectCategory']:
            raise Exception("No category selected")
        for item in categoryIDs:
            if int(f['selectCategory']) == item[0]:
                categoryExists = True
                break
        if not categoryExists:
            raise Exception("Category does not exist")
        
        #number of questions cannot be empty, has to be a number, and be bigger than 1
        if not f['numberOfQuestions']:
            raise Exception("Number of questions was zero")
        elif not f['numberOfQuestions'].isdigit():
            raise Exception("Number of questions was not a number")
        elif int(f['numberOfQuestions']) < 1:
            raise Exception("There were no questions")

        sql = "INSERT INTO quizzes (category_id, user_id, quiz_name, plays) VALUES ({}, '{}', '{}', 0)"
        cursor.execute(sql.format(f['selectCategory'], current_user.id, f['quizName']))        
        quiz_id = cursor.lastrowid 

        questionsToSave = []        
        for i in range(int(f['numberOfQuestions'])):            
            questionQ = []
            questionQ.append(quiz_id)
            if not f['questionQ' + str(i + 1)]:
                raise Exception("Question was empty")
            else:
                questionQ.append(f['questionQ' + str(i + 1)])

            if not f['answer1' + str(i + 1)] or not f['answer2' + str(i + 1)] or not f['answer3' + str(i + 1)] or not f['answer4' + str(i + 1)]:
                raise Exception("Answer was empty")
            else:
                questionQ.append(f['answer1' + str(i + 1)])
                questionQ.append(f['answer2' + str(i + 1)])
                questionQ.append(f['answer3' + str(i + 1)])
                questionQ.append(f['answer4' + str(i + 1)])

            file = request.files['image' + str(i + 1)]
            if not file.filename:
                questionQ.append('/static/questionImages/noImage.PNG')
            else:
                filename = secure_filename(file.filename)
                if allowed_file(filename):
                    image = Image.open(request.files['image' + str(i + 1)])                   
                    size = (640, 360)
                    image = image.resize(size)
                    uniqueFilename = uuid.uuid4().hex + filename
                    image.save(os.path.join(app.config['UPLOAD_FOLDER'], uniqueFilename))
                    questionQ.append('/static/questionImages/' + uniqueFilename)
                else:
                    raise Exception("Wrong file format")

            if f['correctAnswer' + str(i + 1)] == "answer1" or f['correctAnswer' + str(i + 1)] == "answer2" or f['correctAnswer' + str(i + 1)] == "answer3" or f['correctAnswer' + str(i + 1)] == "answer4":
                questionQ.append(f['correctAnswer' + str(i + 1)])                 
            else:                
                raise Exception("No correct answer selected")

            if not f['timeLimit' + str(i + 1)]:
                raise Exception("Time limit was empty")
            elif not f['timeLimit' + str(i + 1)].isdigit():
                raise Exception("Time limit was not a number")
            elif int(f['timeLimit' + str(i + 1)]) < 1 or int(f['timeLimit' + str(i + 1)]) > 999:
                raise Exception("Time limit was not in accepted range")
            else:
                questionQ.append(f['timeLimit' + str(i + 1)])

            questionQ.append('0')
            questionQ.append('0')
            questionsToSave.append(questionQ)      
        cursor.executemany("INSERT INTO questions (quiz_id, question, answer1, answer2, answer3, answer4, image, correctAnswer, time_limit, attempts, correct_attempts) VALUES(?,?,?,?,?,?,?,?,?,?,?);", questionsToSave)
        db.commit()
        return jsonify("Quiz successfully saved")
    except Exception as inst:        
        return jsonify(str(inst))

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/_updatedb')
@login_required
def _updatedb():
    db = get_db()
    whatToUpdate = request.args    
    page = []
    for item in whatToUpdate:
        page.append(item + " " + whatToUpdate[item] + "<br>")
    for i in range(int(whatToUpdate['numberOfQuestions'])):
        sql = "UPDATE questions SET attempts = attempts + 1, correct_attempts = correct_attempts + " + whatToUpdate['questions[' + str(i) + '][correct_attempts]'] + " WHERE question_id = " + whatToUpdate['questions[' + str(i) + '][question_id]'] + ""
        db.cursor().execute(sql)    
    sql = "UPDATE user SET played_quizzes = played_quizzes + 1 WHERE username = '" + current_user.username + "'"
    db.cursor().execute(sql)
    db.commit()
    return jsonify(result=page)

@app.route('/_updateChallengedb')
@login_required
def _updateChallengedb():    
    db = get_db()
    whatToUpdate = request.args    
    page = []
    for item in whatToUpdate:
        page.append(item + " " + whatToUpdate[item] + "<br>")
    for i in range(int(whatToUpdate['numberOfQuestions'])):
        sql = "UPDATE questions SET attempts = attempts + 1, correct_attempts = correct_attempts + " + whatToUpdate['questions[' + str(i) + '][correct_attempts]'] + " WHERE question_id = " + whatToUpdate['questions[' + str(i) + '][question_id]'] + ""
        db.cursor().execute(sql)    
    sql = "UPDATE user SET challenge_score = challenge_score + {} WHERE username = '" + current_user.username + "'"
    db.cursor().execute(sql.format(whatToUpdate['correctNumber']))
    db.commit()
    return jsonify(result=page)

@app.route('/profile/<id>')
@login_required
def profile(id):
    #check if user exists
    db = get_db()
    if id == 'me' or int(id) == current_user.id:
        userid = current_user.id
        remove = 0
    else:
        userid = id
        remove = 1    
    cur = db.cursor()  
    sql = "SELECT COUNT(*) FROM user WHERE id = " + str(userid) + ""
    result = cur.execute(sql)
    rowcount = result.fetchall()
    print(rowcount)
    if rowcount[0][0] > 0:
        sql = "SELECT u.username, u.played_quizzes, u.profile_pic, u.introduction, u.reg_date, (SELECT COUNT(*) FROM quizzes q WHERE q.user_id = {}) as created_quizzes, u.challenge_score, u.played_quizzes + (u.challenge_score * 10) + ((SELECT COUNT(*) FROM earned_achievements ea WHERE ea.user_id = {}) * 15) as score FROM user u WHERE u.id = {}"
        userdata = db.cursor().execute(sql.format(userid, userid, userid)).fetchall()       
        sql = "SELECT a.achievement_name, a.description, a.icon FROM achievements a JOIN earned_achievements e ON a.achievement_id = e.achievement_id WHERE e.user_id = {}"
        userachievements = db.cursor().execute(sql.format(userid)).fetchall()
        return render_template('profile.html', name=current_user.username, userdata=userdata, userachievements=userachievements, remove=remove)
    else:
        return render_template('404.html'), 404

@app.route('/editProfile')
@login_required
def editProfile():
    db = get_db()
    sql = "SELECT u.username, u.profile_pic, u.introduction FROM user u WHERE u.id = {}"
    userdata = db.cursor().execute(sql.format(current_user.id)).fetchall()
    return render_template('editProfile.html', name=current_user.username, userdata=userdata)

@app.route('/_saveUserdataToDB', methods=['GET', 'POST'])
@login_required
def _saveUserdataToDB(): 
    f = request.form
    try:                 
        db = get_db()
        cursor = db.cursor()
        file = request.files['image']
        if not f['introduction'] and not file.filename:
            raise Exception("Nothing to be saved")
        if not f['introduction'] and file.filename:
            filename = secure_filename(file.filename)
            if allowed_file(filename):
                image = Image.open(request.files['image'])                   
                size = (400, 400)
                image = image.resize(size)
                uniqueFilename = uuid.uuid4().hex + filename
                image.save(os.path.join(app.config['UPLOAD_FOLDER2'], uniqueFilename))
                filePath = '/static/profilePictures/' + uniqueFilename
                sql = "UPDATE user SET profile_pic = '{}' WHERE id = {}"
                cursor.execute(sql.format(filePath, current_user.id))    
                db.commit()
            else:
                raise Exception("Wrong file format")
        elif f['introduction'] and not file.filename:
            introduction = f['introduction']
            sql = "UPDATE user SET introduction = '{}' WHERE id = {}"
            cursor.execute(sql.format(introduction, current_user.id))    
            db.commit()
        else:
            introduction = f['introduction']
            filename = secure_filename(file.filename)
            if allowed_file(filename):
                image = Image.open(request.files['image'])                   
                size = (400, 400)
                image = image.resize(size)
                uniqueFilename = uuid.uuid4().hex + filename
                image.save(os.path.join(app.config['UPLOAD_FOLDER2'], uniqueFilename))
                filePath = '/static/profilePictures/' + uniqueFilename
                sql = "UPDATE user SET profile_pic = '{}', introduction = '{}' WHERE id = {}"
                cursor.execute(sql.format(filePath, introduction, current_user.id))    
                db.commit()
            else:
                raise Exception("Wrong file format")
        return jsonify("Profile successfully saved")
    except Exception as inst:        
        return jsonify(str(inst))

@app.route('/dailyChallenge')
@login_required
def dailyChallenge():
    db = get_db() 
    cur = db.cursor()  
    sql = "SELECT COUNT(user_id) FROM challenge_progress WHERE user_id={}"
    result = cur.execute(sql.format(current_user.id))    
    rowcount = result.fetchone()[0]
    if rowcount > 0:
        return render_template('dailyChallenge.html', questions="empty", alreadyAttempted=rowcount, name=current_user.username)
    else:  
        sql = "SELECT qs.question_id, qs.question, qs.time_limit, qs.image, qs.answer1, qs.answer2, qs.answer3, qs.answer4, qs.correctAnswer, qs.attempts, qs.correct_attempts FROM questions qs WHERE qs.question_id IN (SELECT * FROM challenge_questions)"
        questions = []    
        cur.execute(sql)
        r = [dict((cur.description[i][0], value) for i, value in enumerate(row)) for row in cur.fetchall()]   
        return render_template('dailyChallenge.html', questions=r, alreadyAttempted="empty", name=current_user.username) 

@app.route('/_addUserToChallengeProgress', methods=['GET', 'POST'])
@login_required
def _addUserToChallengeProgress():
    db = get_db() 
    sql = "INSERT INTO challenge_progress (user_id, challenge_progress) VALUES ({},{})"
    db.cursor().execute(sql.format(current_user.id, 1))
    db.commit() 
    return jsonify("added")

@app.route('/_createDailyChallenge')
def _createDailyChallenge():
    results = createDailyChallenge()
    return results

@app.route('/_getcategories')
@login_required
def _getcategories():
    db = get_db()
    categories = []
    sql = "SELECT * FROM categories"
    for category in db.cursor().execute(sql):
        categories.append(category)
    return jsonify(result=categories)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user:
            if check_password_hash(user.password, form.password.data):
                login_user(user, remember=form.remember.data)
                return redirect(url_for('home'))
        return '<h1>Invalid username or password: ' + form.username.data + ' ' + form.password.data + '</h1>'
    return render_template('login.html', form=form)

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    form = RegisterForm()
    if form.validate_on_submit():
        hashed_password = generate_password_hash(form.password.data, method='sha256')
        today = date.today()
        new_user = User(username=form.username.data, email=form.email.data, password=hashed_password, played_quizzes=0, profile_pic="/static/profilePictures/defaultProfPic.png", introduction="No introduction", reg_date=today, challenge_score=0)
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('login'))
    return render_template('signup.html', form=form)

@app.route('/home')
@login_required
def home():
    db = get_db()
    popularQuizzes = []
    sql = "SELECT q.quiz_id, c.category_name, u.username, q.quiz_name, q.plays FROM quizzes q JOIN user u ON q.user_id = u.id JOIN categories c ON q.category_id = c.category_id ORDER BY q.plays DESC LIMIT 3"       
    for quiz in db.cursor().execute(sql):
        popularQuizzes.append(quiz)

    top3players = []
    sql = "SELECT u.id, u.username, u.played_quizzes + (u.challenge_score * 10) + ((SELECT COUNT(*) FROM earned_achievements ea WHERE ea.user_id = u.id) * 15) as score, (SELECT COUNT(*) FROM earned_achievements ea WHERE ea.user_id = u.id) as numberOfAchievements, u.played_quizzes, u.challenge_score FROM user u ORDER BY score DESC LIMIT 3"   
    for player in db.cursor().execute(sql):
        top3players.append(player)
    newestQuizzes = []
    sql = "SELECT q.quiz_id, c.category_name, u.username, q.quiz_name, q.plays FROM quizzes q JOIN user u ON q.user_id = u.id JOIN categories c ON q.category_id = c.category_id ORDER BY q.quiz_id DESC LIMIT 3"      
    for quiz in db.cursor().execute(sql):
        newestQuizzes.append(quiz)
    return render_template('home.html', name=current_user.username, popularQuizzes=popularQuizzes, top3players=top3players, newestQuizzes=newestQuizzes)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.errorhandler(404)
def page_not_found(e):
    # note that we set the 404 status explicitly
    return render_template('404.html'), 404

if __name__ == '__main__':
    app.run(host='192.168.1.72', port=3232, debug=True)