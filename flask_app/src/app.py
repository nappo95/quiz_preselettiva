from flask import Flask, render_template, request, redirect, url_for, session
from question_manager import QuestionManager
from typing import List
from models.questions import Question

app = Flask(__name__)
app.secret_key = 'replace_this_with_a_secret_key'  # Needed for session

qm = QuestionManager()

session = {}

questions: List[Question] = []

@app.route('/')
def home():
    """
    Start page: reset session and redirect to question 0
    """
    session['current_question'] = 0
    global questions
    questions = qm.get_questions()
    # user_answers will hold the indexes of selected answers for each question
    # None means not answered yet
    session['user_answers'] = [None] * len(questions)
    return redirect(url_for('show_question', q_index=0))


@app.route('/question/<int:q_index>', methods=['GET', 'POST'])
def show_question(q_index):
    """
    Display the question at index q_index.
    Handle user answer if method=POST.
    """
    # Safety check: if user tries to go out of range
    if q_index < 0 or q_index >= len(questions):
        return redirect(url_for('result'))  # or handle differently

    # If POST, store the user's selected answer in the session
    if request.method == 'POST':
        selected_option = request.form.get('option')
        if selected_option is not None:
            # Convert selected_option to integer
            selected_option_index = int(selected_option)
            session['user_answers'][q_index] = selected_option_index

    # Prepare data for the template
    question_data = questions[q_index]
    user_answer = session['user_answers'][q_index]

    return render_template(
        'quiz.html',
        question_data=question_data,
        q_index=q_index,
        total_questions=len(questions),
        user_answer=user_answer
    )


@app.route('/next/<int:q_index>')
def next_question(q_index):
    """
    Go to the next question (if available).
    """
    if q_index + 1 < len(questions):
        return redirect(url_for('show_question', q_index=q_index + 1))
    else:
        # If no more questions, show the result or handle differently
        return redirect(url_for('result'))


@app.route('/back/<int:q_index>')
def back_question(q_index):
    """
    Go to the previous question (if available).
    """
    if q_index - 1 >= 0:
        return redirect(url_for('show_question', q_index=q_index - 1))
    else:
        # If we're at the first question, just reload it
        return redirect(url_for('show_question', q_index=0))


@app.route('/result')
def result():
    """
    Show final results. For example, count how many correct answers the user had.
    """
    user_answers = session.get('user_answers', [])
    score = 0
    right_question = []

    for i, answer_index in enumerate(user_answers):
        if answer_index is not None and answer_index == questions[i].answer_index:
            right_question.append(questions[i])
            score += 1
    
    qm.mark_completed_questions(right_question)
    return render_template('result.html', score=score, total=len(questions))


if __name__ == '__main__':
    app.run(debug=True)
