from flask import Flask, render_template, request ,send_file
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail
import os
from flask_marshmallow import Marshmallow
from werkzeug.utils import secure_filename
from flask_cors import CORS
import json

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

    def __init__(self, nameOfState, nameOfInstituteType, nameOfInstitute, nameOfField, nameOfBranch):
        self.nameOfState = nameOfState
        self.nameOfInstituteType = nameOfInstituteType
        self.nameOfInstitute = nameOfInstitute
        self.nameOfField = nameOfField
        self.nameOfBranch = nameOfBranch

class CollegeSchema(ma.Schema):
    class Meta:
        fields = ('nameOfState','nameOfInstituteType','nameOfInstitute','nameOfField','nameOfBranch')

college_schema = CollegeSchema()
colleges_schema = CollegeSchema(many=True)


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

# @app.route("/about")
# def about():
#     return {"members" : ["member1","member2","member3","member4"]}


# @app.route("/contact")
# def bootstrap():
#     return render_template('contact.html')

@app.route('/uploader', methods=['GET', 'POST'])
def upload_file():

  if request.method == "GET":
      db.create_all()
  if request.method == 'POST':
    print(1)
    print(request.form.get("testKey"))
    print(request.form.get("nameOfState"))
    nameOfState = request.form.get("nameOfState")
    nameOfInstituteType = request.form.get("nameOfInstituteType")
    nameOfInstitute = request.form.get("nameOfInstitute")
    nameOfField = request.form.get("nameOfField")
    nameOfBranch = request.form.get("nameOfBranch")
    print(2)
    f = request.files['file']

    f.save(secure_filename(f.filename))

    colleges = Colleges(nameOfState, nameOfInstituteType, nameOfInstitute, nameOfField, nameOfBranch)
    db.session.add(colleges)
    db.session.commit()

    return college_schema.jsonify(colleges)





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
