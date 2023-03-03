import database_common
import random
import util
from flask import request,redirect,flash
import datetime
import os
import server


@database_common.connection_handler
def get_all_questions(cursor,order,sort):

    query = f"""
    SELECT * 
    FROM question
    ORDER BY {order} {sort}
    """
    cursor.execute(query)
    return cursor.fetchall()

@database_common.connection_handler
def get_table_data_by_id(cursor, id_question,table_sql):
    query=f"""
    SELECT *
    FROM {table_sql} 
    WHERE id='{id_question}'
    """
    cursor.execute(query)
    return cursor.fetchone()

@database_common.connection_handler
def get_all_data_by_id_question(cursor,id_question,data):
    query=f"""
    SELECT *
    FROM {data} 
    WHERE question_id='{id_question}'
    ORDER BY id
    """
    cursor.execute(query)
    return cursor.fetchall()

@database_common.connection_handler
def get_all_tags_by_id_question(cursor,id_question):
    query=f"""
    SELECT question_tag.question_id,tag.name,question_tag.tag_id
    FROM question_tag
    INNER JOIN tag ON question_tag.tag_id=tag.id
    WHERE question_tag.question_id='{id_question}';
    """
    cursor.execute(query)
    return cursor.fetchall()

@database_common.connection_handler
def get_comments(cursor):

    query=f"""
    SELECT *
    FROM comment
    ORDER BY id;
    """
    cursor.execute(query)
    return cursor.fetchall()

@database_common.connection_handler
def get_comment(cursor,id_comment):

    query=f"""
    SELECT *
    FROM comment
    WHERE id={id_comment};
    """
    cursor.execute(query)
    return cursor.fetchone()

@database_common.connection_handler
def random_question(cursor):
    query="""
    SELECT * 
    FROM question  
    ORDER BY Random()  
    LIMIT 1
    """
    cursor.execute(query)
    return cursor.fetchone()

@database_common.connection_handler
def add_new_question(cursor,question_data,autor):
    query="""
    INSERT INTO question 
    (id,submission_time,view_number,vote_number,title,message,image,autor_id)
    VALUES (%(id)s,%(time)s,%(view)s,%(vote)s,%(title)s,%(message)s,%(image)s,%(autor_id)s)
    """
    cursor.execute(query,
    {'id':int(generate_max_id('question')),
    'time':datetime.datetime.now().strftime("%Y-%m-%d %H:%M"),
    'view':question_data['view_number'],
    'vote':question_data['vote_number'],
    'title':question_data['title'],
    'message':question_data['message'],
    'image':'[null]',
    'autor_id':autor})
    # none 

@database_common.connection_handler
def update_question(cursor, question_data,id):
    query = f"""
    UPDATE question
    SET
    submission_time ='{datetime.datetime.now().strftime("%Y-%m-%d %H:%M")}',
    title='{question_data['title']}',
    message='{question_data['message']}'
    WHERE id='{id}';
    """
    cursor.execute(query)

@database_common.connection_handler
def delete_question(cursor,question_id):

    query4 = f"""
    DELETE from comment
    WHERE question_id='{question_id}';
    """
    cursor.execute(query4)

    query3=f"""
    DELETE from question_tag
    WHERE question_id ='{question_id}';
    """
    cursor.execute(query3)
    query2=f"""
    DELETE from answer
    WHERE question_id ='{question_id}';
    """
    cursor.execute(query2)

    query = f"""
    DELETE from question
    WHERE id='{question_id}';
    """
    cursor.execute(query)

    # delete cascade

@database_common.connection_handler
def add_answer(cursor,answer_data,autor):
    query="""
    INSERT INTO answer 
    (id,submission_time,question_id,vote_number,message,image,autor_id)
    VALUES (%(id)s,%(time)s,%(question_id)s,%(vote)s,%(message)s,%(image)s,%(autor_id)s)
    """
    cursor.execute(query,
    {'id':int(generate_max_id('answer')),
    'time':datetime.datetime.now().strftime("%Y-%m-%d %H:%M"),
    'question_id':answer_data['question_id'],
    'vote':answer_data['vote_number'],
    'message':answer_data['message'],
    'image':'[null]',
    'autor_id':autor})
    
@database_common.connection_handler
def edit_answer(cursor,answer_data,id):
    query=f"""
    UPDATE answer
    SET 
    message='{answer_data['message']}'
    WHERE id ='{id}'
    """
    cursor.execute(query)

@database_common.connection_handler
def delete_answer(cursor,answer_data):

    query2 = f"""
    DELETE from comment
    WHERE answer_id='{answer_data['id']}';
    """
    cursor.execute(query2)

    query = f"""
    DELETE from answer
    WHERE id='{answer_data['id']}';
    """
    cursor.execute(query)

@database_common.connection_handler
def vote_up(cursor,question_id,table_name):
    query = f"""
    UPDATE {table_name}
    SET vote_number=vote_number+1
    WHERE id='{question_id}';
    """
    cursor.execute(query)

@database_common.connection_handler
def vote_down(cursor,question_id,table_name):
    query = f"""
    UPDATE {table_name}
    SET vote_number=vote_number-1
    WHERE id='{question_id}';
    """
    cursor.execute(query)

@database_common.connection_handler
def path_image_to_db(cursor,file_name,data,table_name):
    query =f"""
    UPDATE {table_name}
    SET image='{file_name}'
    WHERE message='{data['message']}';
    """
    cursor.execute(query)


@database_common.connection_handler
def generate_max_id(cursor,sql_table):
    try:
        query=f'''
        SELECT MAX(id)
        FROM {sql_table}
        '''
        cursor.execute(query)
        new_id = cursor.fetchall()[0]['max'] + 1
    except:
        new_id = 0
    return new_id
    # serial

@database_common.connection_handler
def add_question_comment(cursor,comment_data,autor):
    query="""
    INSERT INTO comment
    (id,question_id,answer_id,message,submission_time,edited_count,autor_id)
    VALUES (%(id)s,%(question_id)s,%(answer_id)s,%(message)s,%(submission_time)s,%(edited_count)s,%(autor_id)s)
    """
    if comment_data['question_id'] in ["NULL", ""]:
        comment_data['question_id'] = None
    elif comment_data['answer_id'] in ["NULL", ""]:
        comment_data['answer_id'] = None
    cursor.execute(query,
    {'id':int(generate_max_id('comment')),
    'question_id':comment_data['question_id'],
    'answer_id':comment_data['answer_id'],
    'message':comment_data['message'],
    'submission_time':datetime.datetime.now().strftime("%Y-%m-%d %H:%M"),
    'edited_count': 0,
    'autor_id':autor})

@database_common.connection_handler
def add_answer_comment(cursor,comment_data,autor):
    query="""
    INSERT INTO comment
    (id,question_id,answer_id,message,submission_time,edited_count,autor_id)
    VALUES (%(id)s,%(question_id)s,%(answer_id)s,%(message)s,%(submission_time)s,%(edited_count)s,%(autor_id)s)
    """
    if comment_data['question_id'] in ["NULL", ""]:
        comment_data['question_id'] = None
    elif comment_data['answer_id'] in ["NULL", ""]:
        comment_data['answer_id'] = None
    cursor.execute(query,
    {'id':int(generate_max_id('comment')),
    'question_id':comment_data['question_id'],
    'answer_id':comment_data['answer_id'],
    'message':comment_data['message'],
    'submission_time':datetime.datetime.now().strftime("%Y-%m-%d %H:%M"),
    'edited_count': 0,
    'autor_id':autor})

@database_common.connection_handler
def edit_comment(cursor,comment_data,id):
    query=f"""
    UPDATE comment
    SET 
    message='{comment_data['message']}',
    submission_time ='{datetime.datetime.now().strftime("%Y-%m-%d %H:%M")}',
    edited_count=edited_count+1
    WHERE id ='{id}'
    """
    cursor.execute(query)

@database_common.connection_handler
def delete_comment(cursor,comment_data):
    query = f"""
    DELETE from comment
    WHERE id='{comment_data['id']}';
    """
    cursor.execute(query)

@database_common.connection_handler
def delete_comments(cursor,answer_id):
    query = f"""
    DELETE from comment
    WHERE id='{answer_id}';
    """
    cursor.execute(query)

@database_common.connection_handler
def add_tag(cursor,data):
    tags = get_all_tags()
    for tag in tags:    
        if data['tag'] == tag['name']:
            return None
    query="""
    INSERT INTO tag
    (id,name)
    VALUES (%(id)s,%(name)s)
    """
    cursor.execute(query,
    {'id':int(generate_max_id('tag')),
    'name':data['tag']})

@database_common.connection_handler
def get_tag_id(cursor,tag_name):
    query=f"""
    SELECT id
    FROM tag
    WHERE name='{tag_name}';
    """
    cursor.execute(query)
    return cursor.fetchone()

@database_common.connection_handler
def add_tag_to_question(cursor,data,question_id):
    query="""
    INSERT INTO question_tag
    (question_id,tag_id)
    VALUES (%(questionid)s,%(tagid)s)
    """
    cursor.execute(query,
    {'questionid':question_id,
    'tagid':get_tag_id(data['tag'])['id']})
       


@database_common.connection_handler
def get_all_tags(cursor):
    query="""
    SELECT *
    FROM tag
    """
    cursor.execute(query)
    return cursor.fetchall()

@database_common.connection_handler    
def delete_tag_from_question(cursor,id_question,id_tag):
    query=f"""
    DELETE from question_tag
    WHERE question_id='{id_question}'  AND tag_id='{id_tag}';
    """
    cursor.execute(query)

@database_common.connection_handler
def search(cursor,search):
    query = f"""
    SELECT * 
    FROM question
  	WHERE title LIKE '%{search}%' OR message LIKE '%{search}%'
    """
    cursor.execute(query)
    return cursor.fetchall()

@database_common.connection_handler
def get_last_questions(cursor):
    query = f"""
    SELECT * 
    FROM question
	ORDER BY id DESC
    LIMIT 5
    """
    cursor.execute(query)
    return cursor.fetchall()

@database_common.connection_handler
def registration_process(cursor,user_data):
    query1="""
    INSERT INTO users 
    (id,username,password,registration_date,salt)
    VALUES (%(id)s,%(username)s,%(password)s,%(registration_date)s,%(salt)s)
    """

    cursor.execute(query1,
    {'id':int(generate_max_id('users')),
    'username':user_data['username'],
    'password':user_data['password'],
    'registration_date':datetime.date.today().strftime("%d/%m/%Y"),
    'salt':user_data['salt']})

    query2="""
    INSERT INTO users_stats 
    (id,username)
    VALUES (%(id)s,%(username)s)
    """

    cursor.execute(query2,
    {'id':int(generate_max_id('users_stats')),
    'username':user_data['username']})


@database_common.connection_handler
def get_login_data(cursor,form_login):
    query=f"""
    SELECT * FROM users
    WHERE username = '{form_login['username']}'
    """
    cursor.execute(query)
    return cursor.fetchone()

@database_common.connection_handler
def get_all_users(cursor):
    query="""
    SELECT *
    FROM users
    """
    cursor.execute(query)
    return cursor.fetchall()

@database_common.connection_handler
def get_user_data(cursor,user_id):
    query=f"""
    SELECT *
    FROM users
    WHERE id='{user_id}';
    """
    cursor.execute(query)
    return cursor.fetchone()

@database_common.connection_handler
def get_activity_of_user(cursor, table,user_id):
    query=f"""
    SELECT *
    FROM {table}
    WHERE autor_id='{user_id}';
    """
    cursor.execute(query)
    return cursor.fetchall()

@database_common.connection_handler
def get_all_tags_counted(cursor):
    query="""
    select t.name, count(qt.question_id) as total
    from question_tag qt
    inner join tag t on t.id=qt.tag_id
    group by t.name
    """
    cursor.execute(query)
    return cursor.fetchall()

@database_common.connection_handler
def hashing(user_data):
    salt = os.urandom(32)
    key = hashlib.pbkdf2_hmac('sha256', user_data['password'].encode('utf-8'), salt, 100000)
    user_data['salt'] = salt
    user_data['password'] = key
    return(user_data)

@database_common.connection_handler
def accept_answer(cursor,answer_id,table_name):
    query = f"""
    UPDATE {table_name}
    SET is_accepted=TRUE
    WHERE id='{answer_id}';
    """
    cursor.execute(query)

@database_common.connection_handler
def refuse_answer(cursor,answer_id,table_name):
    query = f"""
    UPDATE {table_name}
    SET is_accepted=FALSE
    WHERE id='{answer_id}';
    """
    cursor.execute(query)

@database_common.connection_handler
def gain_rep(cursor,autor_id,table_name):
    if table_name == 'question':
        gain = 5
    elif table_name == 'answer':
        gain = 10
    elif table_name == 'accept':
        gain = 15
    query = f"""
    UPDATE users_stats
    SET reputation=reputation+{gain}
    WHERE username='{autor_id}';
    """
    cursor.execute(query)

@database_common.connection_handler
def lose_rep(cursor,autor_id):
    loss = 2
    query = f"""
    UPDATE users_stats
    SET reputation=reputation-{loss}
    WHERE username='{autor_id}';
    """
    cursor.execute(query)

def upload_file(path_folder):
    server.app.config['UPLOAD_FOLDER'] = path_folder
    if 'file' not in request.files:
        flash('No file part')
        return redirect(request.url)
    file = request.files['file']
   
    if file.filename == '':
        flash('No selected file')
        return redirect(request.url)
    if file and util.allowed_file(file.filename):
        # filename = util.convert_filename(file.filename, question_id)
        filename = file.filename
        file.save(os.path.join(server.app.config['UPLOAD_FOLDER'], filename))
    
        return redirect(request.url, filename)