from flask import Flask
from flask_bootstrap import Bootstrap



app = Flask(__name__)
import os
SECRET_KEY = 'secret'
app.config['SECRET_KEY'] = SECRET_KEY


bootstrap = Bootstrap(app)


@app.route("/")
def hello():
    return " <html><head></head> <body> Hello World! </body></html>"
import threading
if __name__ == "__main__":
    app.run(host='127.0.0.1',port=5000)

from flask import render_template
#наша новая функция сайта
@app.route("/data_to")
def data_to():
    #создаем переменные с данными для передачи в шаблон
    some_pars = {'user':'Ivan','color':'red'}
    some_str = 'Hello my dear friends!'
    some_value = 10
    #передаем данные в шаблон и вызываем его
    return render_template('simple.html',some_str = some_str,some_value = some_value,some_pars=some_pars)



from flask_wtf import FlaskForm,RecaptchaField
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired
from flask_wtf.file import FileField, FileAllowed, FileRequired


app.config['RECAPTCHA_USE_SSL'] = False
app.config['RECAPTCHA_PUBLIC_KEY'] = '6LerYPEUAAAAAG4hhwu8djjem0KY2xd011Ki1gE5'
app.config['RECAPTCHA_PRIVATE_KEY'] = '6LerYPEUAAAAABcN5lLC9bhTmM_ByEt1iK3uSd47'
app.config['RECAPTCHA_OPTIONS'] = {'theme': 'white'}
#app.config['UPLOAD_FOLDER'] = './data'
#app.config['ALLOWED_EXTENSIONS'] = {'jpg','png','jpeg'}

#создаем форму для загрузки файла
class NetForm(FlaskForm):
    # валидатор проверяет введение данных после submit
    #и указывает пользователю ввести данные
    openid = StringField('openid', validators = [DataRequired()])
    #здесь валидатор укажет ввести правильные файлы
    upload = FileField('Load image', validators=[
        FileRequired(),
        FileAllowed(['jpg', 'png', 'jpeg'], 'Images only!')])
    recaptcha = RecaptchaField()
    #кнопка submit
    submit = SubmitField('send')



from werkzeug.utils import secure_filename
import os
import net as neuronet
@app.route("/net",methods=['GET', 'POST'])
def net():
    form = NetForm()
    filename=None
    neurodic = {}
    if form.validate_on_submit():
        filename = os.path.join('./static', secure_filename(form.upload.data.filename))
        fcount, fimage = neuronet.read_image_files(10,'./static')
        decode = neuronet.getresult(fimage)

        for elem in decode:
            print(elem)
            neurodic[elem[0][1]] = elem[0][2]
        form.upload.data.save(filename)

    return render_template('net.html',form=form,image_name=filename,neurodic=neurodic)

from flask import request
from flask import Response
import base64
from PIL import Image
from io import BytesIO
import json
@app.route("/apinet",methods=['GET', 'POST'])
def apinet():
    if request.mimetype == 'application/json':
        data = request.get_json()
        filebytes = data['imagebin'].encode('utf-8')
        cfile = base64.b64decode(filebytes)
        img = Image.open(BytesIO(cfile))
        decode = neuronet.getresult([img])
        neurodic = {}
        for elem in decode:
            neurodic[elem[0][1]] = str(elem[0][2])
            print(elem)

        #handle = open('./static/f.png','wb')
        #handle.write(cfile)
        #handle.close()
    ret = json.dumps(neurodic)
    resp = Response(response=ret,
                    status=200,
                    mimetype="application/json")

    return resp


import lxml.etree as ET

@app.route("/apixml",methods=['GET', 'POST'])
def apixml():
    #парсим xml файл в dom
    dom = ET.parse("./static/xml/file.xml")
    #парсим шаблон в dom
    xslt = ET.parse("./static/xml/file.xslt")
    #получаем трансформер
    transform = ET.XSLT(xslt)
    #преобразуем xml с помощью трансформера xslt
    newhtml = transform(dom)
    #преобразуем из памяти dom в строку, возможно, понадобится указать кодировку
    strfile = ET.tostring(newhtml)
    return strfile
