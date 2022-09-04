from flask import Flask, render_template, request ,send_file
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail
import os
from flask_marshmallow import Marshmallow
from werkzeug.utils import secure_filename
from flask_cors import CORS, cross_origin
import json
from PyPDF2 import PdfReader
import re
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
with open('config.json','r') as c:
    params = json.load(c)["params"]
local_server = True

app = Flask(__name__)
CORS(app)
# app.config['UPLOAD_FOLDER'] = params['upload_location']
# app.config.update(
#     MAIL_SERVER = 'smtp.gmail.com',
#     MAIL_PORT = '465',
#     MAIL_USE_SSL = True,
#     MAIL_USERNAME = params['gmail-user'],
#     MAIL_PASSWORD = params['gmail-password']
# )
# mail = Mail(app)

if local_server:
    app.config['SQLALCHEMY_DATABASE_URI'] = params['local_uri']
else:
    app.config['SQLALCHEMY_MODIFICATIONS'] = params['prod_uri']

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
ma=Marshmallow(app)


class Colleges(db.Model):
    nameOfState = db.Column(db.String(100),primary_key=True)
    nameOfInstituteType = db.Column(db.String(100),nullable=False)
    nameOfInstitute = db.Column(db.String(100),nullable=False)
    nameOfField = db.Column(db.String(100),nullable=False)
    nameOfBranch = db.Column(db.String(100),nullable=False)
    nameOfSemesterId = db.Column(db.String(100),nullable = False)

    def __init__(self, nameOfState, nameOfInstituteType, nameOfInstitute, nameOfField, nameOfBranch,nameOfSemesterId):
        self.nameOfState = nameOfState
        self.nameOfInstituteType = nameOfInstituteType
        self.nameOfInstitute = nameOfInstitute
        self.nameOfField = nameOfField
        self.nameOfBranch = nameOfBranch
        self.nameOfSemesterId = nameOfSemesterId

class CollegeSchema(ma.Schema):
    class Meta:
        fields = ('id','file','body','date')

colleges_schema = CollegeSchema()


# class Contacts(db.Model):
#     # id,email,age,textarea
#     __tablename__ = 'users'
#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String(100))
#     email = db.Column(db.String(80), nullable=False)
#     age = db.Column(db.Integer, nullable=False)
#     phone = db.Column(db.Integer, nullable=False)
#     textarea = db.Column(db.String(120), nullable=False)
#     filename = db.Column(db.String(50))
#     data = db.Column(db.LargeBinary)

# @app.route("/", methods=['GET', 'POST'])
# def home():
#     if (request.method == 'POST'):
#         '''add entry to the database'''
#         # id = request.form.get('id')
#         # name = request.form.get('name')
#         # email = request.form.get('email')
#         # age = request.form.get('age')
#         # phone = request.form.get('phone')
#         # textarea = request.form.get('textarea')

#         file = request.files['file']
#         file.save(os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(file.filename)))
#         entry = Contacts(filename=file.filename, data=file.read())
#         db.session.add(entry)
#         db.session.commit()
#         # mail.send_message('New message from ' + name,
#         #                       sender=email,
#         #                       recipients=[params['gmail-user']],
#         #                       body=id + "\n" + phone
#         #                       )
#         return f'Uploaded: {file.filename}'
#     return render_template('index.html', params = params)

# @app.route("/download/upload_id")
# def download(upload_id):
#     upload = Contacts.query.filter_by(id=upload_id).first()
#     return send_file(BytesIO(Contacts.data), attachment_filename=Contacts.filename, as_attachment=True)




# @app.route('/uploader', methods=['GET', 'POST'])
# @cross_origin()
# def login(self):
#     if request.method == 'POST':
#         email = request.form.get("email")
#         password = request.form.get("password")
#             # mail.send_message('New message from ' + name,
#             #                   sender=email,
#             #                   recipients=[params['gmail-user']],
#             #                   body=id + "\n" + phone
#             #                                                 )
#         return 'login successfully'

# @app.route("/contact")
# def bootstrap():
#     return render_template('contact.html')
# def matcher(name):
#     reader = PdfReader(name)
#     aicte_syllabus = []
#     pdf_syllabus = []
#     f = open('syllabus.txt', 'w')
#     for i in range(len(reader.pages)):
#         try:
#             page = reader.pages[i]
#             f.write(page.extract_text())
#         except:
#             continue
#     f.close()
#     # end of conversion of pdf to text
#     # start extracting syllabus from text file
#     f = open('syllabus.txt', 'r')
#     file = open('topics.txt', 'w')
#     count = 0
#     write = False
#     search = True
#     while True:
#         count += 1
#         text = f.readline().lower()
#         if not text:
#             break
#         if search and re.findall('syllabus', text):
#             write = True
#             search = False
#             print("syllabus found on line ", count)
#         if not search and (
#                 re.findall('outline', text) or re.findall('outcome', text) or re.findall('pedagogy',
#                                                                                          text) or re.findall(
#             'reference  books', text) or re.findall('objective', text)):
#             write = False
#             print("other found on line ", count)
#             search = True
#         if write:
#             file.write(text)
#     f.close()
#     file.close()
#     # completion of topics extraction
#     file = open('model.txt', 'r').readlines()
#
#     for line in file:
#         line = line.replace('module ', '')
#         lne = line.lstrip('0123456789.- ')
#         aicte_syllabus.append(line)
#
#     # creating list of given pdf
#
#     with open("topics.txt", 'r') as file:
#         for line in file:
#             grade_data = line.strip().split(',')
#             for i in range(len(grade_data)):
#                 pdf_syllabus.append(grade_data[i])
#
#     found = []
#     not_found = []
#
#     # def create_dataframe(matrix, tokens):
#     #     doc_names = [f'doc_{i + 1}' for i, _ in enumerate(matrix)]
#     #     df = pd.DataFrame(data=matrix, index=doc_names, columns=tokens)
#     #     return (df)
#
#     pdf_syllabus = [x for x in pdf_syllabus if x != '']
#
#     for str in pdf_syllabus:
#         str.replace('\n', ' ')
#     for str in aicte_syllabus:
#         str.replace('\n', ' ')
#
#     for i in range(len(aicte_syllabus)):
#         for j in range(len(pdf_syllabus)):
#             try:
#                 data = [aicte_syllabus[i], pdf_syllabus[j]]
#                 print(data)
#                 count_vectorizer = CountVectorizer()
#                 vector_matrix = count_vectorizer.fit_transform(data)
#
#                 tokens = count_vectorizer.get_feature_names()
#                 vector_matrix.toarray()
#
#                 cosine_similarity_matrix = cosine_similarity(vector_matrix)
#                 # frame = create_dataframe(cosine_similarity_matrix, ['doc_1', 'doc_2'])
#                 if cosine_similarity_matrix[0][1] > 0.5:
#                     found.append(aicte_syllabus[i])
#             except:
#                 continue
#     not_found = [x for x in aicte_syllabus if x not in found]
#     found = list(set(found))
#     not_found = list(set(not_found))
#     print(found)
#     print(not_found)
@app.route('/uploader', methods=['GET', 'POST'])
@cross_origin()
def upload_file():

  if request.method == 'POST':
    print(1)
    print(request.form.get("testKey"))
    print(request.form.get("nameOfState"))
    nameOfState = request.form.get("nameOfState")
    nameOfInstituteType = request.form.get("nameOfInstituteType")
    nameOfInstitute = request.form.get("nameOfInstitute")
    nameOfField = request.form.get("nameOfField")
    nameOfBranch = request.form.get("nameOfBranch")
    nameOfSemesterId = request.form.get("nameOfSemesterId")
    print(2)
    f = request.files['file']
    # mail.send_message('New message from ' + name,
    #                   sender=email,
    #                   recipients=[params['gmail-user']],
    #                   body=id + "\n" + phone
    #                                                 )
    f.save(secure_filename("collage.pdf"))
    return 'file uploaded successfully'
    # matcher(f.filename)


app.run('0.0.0.0', port=8080, debug=True)
# local_server = True
#
# app = Flask(__name__)
# CORS(app)
# app.config['UPLOAD_FOLDER'] = params['upload_location']
# app.config.update(
#     MAIL_SERVER = 'smtp.gmail.com',
#     MAIL_PORT = '465',
#     MAIL_USE_SSL = True,
#     MAIL_USERNAME = params['gmail-user'],
#     MAIL_PASSWORD = params['gmail-password']
# )
# mail = Mail(app)
#
# if local_server:
#     app.config['SQLALCHEMY_DATABASE_URI'] = params['local_uri']
# else:
#     app.config['SQLALCHEMY_MODIFICATIONS'] = params['prod_uri']
# db = SQLAlchemy(app)
#
# class Contacts(db.Model):
#     # id,email,age,textarea
#     __tablename__ = 'users'
#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String(100))
#     email = db.Column(db.String(80), nullable=False)
#     age = db.Column(db.Integer, nullable=False)
#     phone = db.Column(db.Integer, nullable=False)
#     textarea = db.Column(db.String(120), nullable=False)
#     filename = db.Column(db.String(50))
#     data = db.Column(db.LargeBinary)
#
# @app.route("/", methods=['GET', 'POST'])
# def home():
#     if (request.method == 'POST'):
#         '''add entry to the database'''
#         id = request.form.get('id')
#         name = request.form.get('name')
#         email = request.form.get('email')
#         age = request.form.get('age')
#         phone = request.form.get('phone')
#         textarea = request.form.get('textarea')
#
#         file = request.files['file']
#         file.save(os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(file.filename)))
#         entry = Contacts(id=id,name = name , email=email, age=age, phone=phone, textarea=textarea,filename=file.filename, data=file.read())
#         db.session.add(entry)
#         db.session.commit()
#         mail.send_message('New message from ' + name,
#                               sender=email,
#                               recipients=[params['gmail-user']],
#                               body=id + "\n" + phone
#                               )
#         return f'Uploaded: {file.filename}'
#     return render_template('index.html', params = params)
#
# @app.route("/download/upload_id")
# def download(upload_id):
#     upload = Contacts.query.filter_by(id=upload_id).first()
#     return send_file(BytesIO(Contacts.data), attachment_filename=Contacts.filename, as_attachment=True)
#
# @app.route("/about")
# def about():
#     return {"members" : ["member1","member2","member3","member4"]}
#
#
# @app.route("/contact")
# def bootstrap():
#     return render_template('contact.html')
#
#
# app.run(debug=True)
