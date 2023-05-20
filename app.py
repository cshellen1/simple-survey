from flask import Flask, render_template, request, session, redirect, flash
from flask_debugtoolbar import DebugToolbarExtension
from surveys import satisfaction_survey

app = Flask(__name__)
app.debug = True
app.config['SECRET_KEY'] = '<ilikedogs1982!>'
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

toolbar = DebugToolbarExtension(app)

responses = []
QUESTIONS = satisfaction_survey.questions

@app.route('/')
def show_home_page():
    """get home page and button to start survey"""
    return render_template('home.html', survey=satisfaction_survey)

@app.route('/start')
def start_survey():
    """reset the responses and handle starting the survey"""
    
    responses = []
    return redirect('/question/0')

@app.route('/question/<int:qid>')
def get_question(qid):
    """get question form survey and return html for question"""
    if (qid is not len(responses)):
        flash('Invalid question ID')
        return redirect(f'/question/{len(responses)}')
    
        
    if (qid == len(QUESTIONS)):
        return redirect('/finish')
    
    else:
        question = QUESTIONS[qid].question 
        choices = QUESTIONS[qid].choices
        return render_template('question.html', question=question, choices=choices, )


@app.route('/answer', methods=['POST'])
def handle_question_answer():
    """handle submitted response and update stored responses"""
    response = request.form['answer']
    responses.append(response)
    
    if len(responses) == len(QUESTIONS):
        return redirect ('/finish')
    
    else:
        return redirect(f'/question/{len(responses)}')
    
@app.route('/finish')
def show_finish():
    """show survey finish html"""
    return render_template('finish.html')