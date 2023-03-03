
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}




def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def convert_filename(filename, question_id):
    [name, ext] = filename.rsplit('.', 1)
    [name, ext] = [question_id, ext]
    new_name = str(name) + (".") + str(ext)
    return new_name