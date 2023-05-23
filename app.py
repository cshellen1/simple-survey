from flask import Flask, render_template, request, session, redirect, flash
from flask_debugtoolbar import DebugToolbarExtension
from surveys import satisfaction_survey

app = Flask(__name__)
app.debug = True
app.config['SECRET_KEY'] = '<ilikedogs1982!>'
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

toolbar = DebugToolbarExtension(app)

RESPONSES_KEY = 'responses'
QUESTIONS = satisfaction_survey.questions

@app.route('/')
def show_home_page():
    """get home page and button to start survey"""
    return render_template('home.html', survey=satisfaction_survey)

@app.route('/start', methods=['POST'])
def start_survey():
    """reset the responses and handle starting the survey"""
    
    session[RESPONSES_KEY] = []
    
    return redirect('/question/0')

@app.route('/question/<int:qid>')
def get_question(qid):
    """get question form survey and return html for question"""
    
    responses = session.get(RESPONSES_KEY)
    
    if ( responses is None):
        return redirect('/')
        
        
    if (qid == len(QUESTIONS)):
        return redirect('/finish')
    
    if (qid != len(responses)):
        flash('Invalid question ID')
        return redirect(f'/question/{len(responses)}')
    
    question = QUESTIONS[qid].question 
    choices = QUESTIONS[qid].choices
    return render_template('question.html', question=question, choices=choices, )


@app.route('/answer', methods=['POST'])
def handle_question_answer():
    """handle submitted response and update stored responses"""
    response = request.form['answer']
    responses = session[RESPONSES_KEY]
    responses.append(response)
    session[RESPONSES_KEY] = responses
    
    if len(responses) == len(QUESTIONS):
        return redirect ('/finish')
    
    else:
        return redirect(f'/question/{len(responses)}')
    
@app.route('/finish')
def show_finish():
    """show survey finish html"""
    return render_template('finish.html')