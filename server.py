from flask import Flask, render_template, request, redirect, url_for,session
import data_manager



app = Flask(__name__)
app.secret_key="rekin"

@app.route("/")
def home():
    return render_template("home.html", questions=data_manager.get_last_questions())


@app.route('/list')
def list_questions():
    order_by = request.args.get('order_by', default='id')
    order_direction = request.args.get('order_direction', default='DESC')
    return render_template("list.html", questions = data_manager.get_all_questions(order_by,order_direction))
    # error


@app.route("/question/<question_id>")
def show_question(question_id):
    user_id = session['user_id']
    return render_template('question.html',
    question=data_manager.get_table_data_by_id(question_id,'question'),
    answers=data_manager.get_all_data_by_id_question(question_id,'answer'),
    comments=data_manager.get_comments(),
    tags=data_manager.get_all_tags_by_id_question(question_id),
    user_id = user_id)
    # join
    


@app.route("/random")
def random_question():
    return redirect(url_for('show_question', question_id=data_manager.random_question()['id']))

@app.route("/add-question", methods=['POST', 'GET'])
def add_new_question():
    
    if request.method == 'GET':
        return render_template("add-question.html")
    if request.method == 'POST':
        autor = session['user_id'] 
        data_manager.add_new_question(dict(request.form),autor)
        
        if request.files['file']:

            app.config['UPLOAD_FOLDER'] = 'static/images/questions'
            data_manager.upload_file(app.config['UPLOAD_FOLDER'])
            file_name = request.files['file'].filename
            data_manager.path_image_to_db(file_name,request.form,'question')
        
        return redirect(url_for('list_questions'))

@app.route("/question/<question_id>/edit", methods=['POST', 'GET'])
def edit_question(question_id):
    if request.method == 'GET':
        return render_template("edit-question.html", question=data_manager.get_table_data_by_id(question_id,'question'))
    if request.method == 'POST':
        updated_question = dict(request.form)
        data_manager.update_question(updated_question,question_id)
        return redirect(url_for('show_question', question_id=question_id))


@app.route("/question/<question_id>/delete")
def delete_question(question_id):
    data_manager.delete_question(question_id)
    
    return redirect(url_for('list_questions'))


@app.route("/question/<question_id>/new-answer", methods=['POST', 'GET'])
def add_answer(question_id):
    if request.method == 'GET':
        return render_template("add-answer.html", question=data_manager.get_table_data_by_id(question_id,'question') )
    if request.method == 'POST':
        autor = session['user_id']
        data_manager.add_answer(dict(request.form),autor)
        if request.files['file']:
            app.config['UPLOAD_FOLDER'] = 'static/images/answers'
            data_manager.upload_file(app.config['UPLOAD_FOLDER'])
            file_name = request.files['file'].filename
            data_manager.path_image_to_db(file_name,request.form,'answer')
        
        
        return redirect(url_for('show_question', question_id=question_id))

@app.route("/answer/<answer_id>/edit", methods=['POST', 'GET'])
def edit_answer(answer_id):
    answer=data_manager.get_table_data_by_id(answer_id,'answer')
    if request.method == 'GET':
        return render_template("edit-answer.html", answer=data_manager.get_table_data_by_id(answer_id,'answer'))
    if request.method == 'POST':
        data_manager.edit_answer(dict(request.form),answer_id)        
        return redirect(url_for('show_question', question_id=answer['question_id']))

@app.route("/answer/<answer_id>/delete")
def delete_answer(answer_id):
    answer = data_manager.get_table_data_by_id(answer_id,'answer')
    data_manager.delete_answer(answer)
    return redirect(url_for('show_question', question_id=answer['question_id']))

@app.route("/question/<question_id>/new-tag",methods=['POST', 'GET'])
def add_tag_to_question(question_id):
    if request.method == 'GET':
        return render_template('add-tag-to-question.html',tags=data_manager.get_all_tags(),question_id=question_id)
    if request.method == 'POST':
        print(dict(request.form))
        data_manager.add_tag_to_question(dict(request.form),question_id)
        return redirect(url_for('show_question',question_id=question_id ))

@app.route("/question/<question_id>/new-tag/create",methods=['POST', 'GET'])
def add_tag(question_id):
    if request.method == 'GET':
        return render_template('add-tag.html',question_id=question_id)
    if request.method == 'POST':
        data_manager.add_tag(request.form)
        return redirect(url_for('add_tag_to_question',question_id=question_id ))

@app.route("/question/<question_id>/tag/<tag_id>/delete")
def delete_tag_from_question(question_id,tag_id):
    data_manager.delete_tag_from_question(question_id,tag_id)
    return redirect(request.referrer)


 


@app.route("/question/<question_id>/vote-up")
def vote_up_question(question_id):
    data_manager.vote_up(question_id,'question')
    question = data_manager.get_table_data_by_id(question_id, 'question')
    data_manager.gain_rep(question['autor_id'], 'question')
    return redirect(request.referrer)



@app.route("/question/<question_id>/vote-down")
def vote_down_question(question_id):
    data_manager.vote_down(question_id,'question')
    question = data_manager.get_table_data_by_id(question_id, 'question')
    data_manager.lose_rep(question['autor_id'])
    return redirect(request.referrer)


@app.route("/answer/<answer_id>/vote-up")
def vote_up_answer(answer_id):
    data_manager.vote_up(answer_id,'answer')
    answer = data_manager.get_table_data_by_id(answer_id, 'answer')
    data_manager.gain_rep(answer['autor_id'], 'answer')
    return redirect(request.referrer)


@app.route("/answer/<answer_id>/vote-down")
def vote_down_answer(answer_id):
    data_manager.vote_down(answer_id,'answer')
    answer = data_manager.get_table_data_by_id(answer_id, 'answer')
    data_manager.lose_rep(answer['autor_id'])
    return redirect(request.referrer)

@app.route("/question/<question_id>/new-comment", methods=['POST', 'GET'])
def add_comment_to_question(question_id):    
    if request.method == 'GET':
        return render_template("add-question-comment.html", question=data_manager.get_table_data_by_id(question_id,'question') )
    if request.method == 'POST':
        autor = session['user_id']
        data_manager.add_question_comment(dict(request.form),autor)
        return redirect(url_for('show_question', question_id=question_id))

@app.route("/answer/<answer_id>/new-comment", methods=['POST', 'GET'])
def add_comment_to_answer(answer_id):
    if request.method == 'GET':
        return render_template("add-answer-comment.html", answer=data_manager.get_table_data_by_id(answer_id,'answer') )
    if request.method == 'POST':
        autor = session['user_id']
        data_manager.add_answer_comment(dict(request.form),autor)     
        answer = data_manager.get_table_data_by_id(answer_id,'answer')
        return redirect(url_for('show_question', question_id=answer['question_id']))

@app.route("/comment/<comment_id>/edit", methods=['POST', 'GET'])
def edit_comment(comment_id):
    if request.method == 'GET':
        return render_template("edit-comment.html", comment=data_manager.get_comment(comment_id))
    if request.method == 'POST':
        comment=data_manager.get_comment(comment_id)
        data_manager.edit_comment(dict(request.form),comment_id)        
        if comment['question_id'] in ["NULL", "", None]:
            answer = data_manager.get_table_data_by_id(comment['answer_id'],'answer')
            return redirect(url_for('show_question', question_id= answer['question_id']))
        else:
            return redirect(url_for('show_question', question_id=comment['question_id']))

@app.route("/comment/<comment_id>/delete")
def delete_comment(comment_id):
    comment = data_manager.get_comment(comment_id)
    data_manager.delete_comment(comment)
    return redirect(request.referrer)

@app.route("/search")
def search():
    search_phrase=request.args.get('q')
    return render_template("search.html", questions=data_manager.search(search_phrase))

@app.route("/users")
def list_users():
    return render_template("list-user.html", users= data_manager.get_all_users() )

@app.route("/user/<user_id>")
def user_data(user_id):
    return render_template("user.html", 
    user =data_manager.get_user_data(user_id),
    questions=data_manager.get_activity_of_user('question',user_id),
    answers=data_manager.get_activity_of_user('answer',user_id),
    comments=data_manager.get_activity_of_user('comment',user_id))

@app.route("/registration", methods=['POST', 'GET'])
def registration():
    if request.method == 'GET':
        return render_template("registration.html")
    if request.method == 'POST':
        data_manager.registration_process(dict(request.form))        
        return redirect(url_for('home'))
        
@app.route("/tags")
def tag_page():
    return render_template("tags.html", tags=data_manager.get_all_tags_counted())

@app.route("/login", methods=['POST', 'GET'])
def login():
    if request.method=='GET':
        return render_template("login.html")
    if request.method=='POST':
        login_form=dict(request.form)
        user_data=data_manager.get_login_data(dict(request.form))
        password_check=validate_password(user_data,login_form)
        if password_check:
            session['username']=user_data['username']
            session['user_id']=user_data['id']
            return redirect(url_for('home'))
        else:
            return render_template("login.html")

def validate_password(user_data,form_data):
    if user_data['password']==form_data['password']:
        return True
    else:
        return False

@app.route("/logout")
def logout():
    session.pop('username', None)
    session.pop('user_id', None)
    return redirect(url_for('home'))

@app.route("/answer/<answer_id>/accept")
def accept_answer(answer_id):
    data_manager.accept_answer(answer_id,'answer')
    answer = data_manager.get_table_data_by_id(answer_id, 'answer')
    data_manager.gain_rep(answer['autor_id'], 'accept')
    return redirect(request.referrer)

@app.route("/answer/<answer_id>/refuse")
def refuse_answer(answer_id):
    data_manager.refuse_answer(answer_id,'answer')
    return redirect(request.referrer)


if __name__ == "__main__":
    app.run(debug=True)