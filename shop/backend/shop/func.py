import random


ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def isForm(request):

    if 'file' not in request.files:
        return False 

    file = request.files['file']
    if file.filename == "":
        return False

    if file and allowed_file(file.filename):
        return True
    else:
        return False


def isFormEdit(request):

    return True
    

def randomId(el):
    filenameid = ""
    for i in range(8):
        filenameid += str(random.randint(1, 9))
    el = filenameid + el

    return el
        

