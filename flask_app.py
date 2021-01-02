

from flask import render_template, flash, redirect, Flask, request, url_for

from forms import LoginForm




import csv

app = Flask(__name__)
app.config.from_object('config')

@app.route('/')
@app.route('/index')
def index():
    user = { 'nickname': 'User' }
    return render_template("index.html", title = 'Home', user = user)



    #return redirect(url_for('profile'))

@app.route('/login', methods = ['GET', 'POST'])
def login():
    form = LoginForm()
    return render_template('login.html', title = 'Sign In', form = form)

#@app.route('/output', data = data)
#def output():
#    return render_template("output.html", title = 'Output', data = data)


UPLOAD_FOLDER = '/home/qwerty1000/mysite'
@app.route('/upload', methods=["POST", "GET"])
def upload():
    global UPLOAD_FOLDER
    if request.method == 'POST':
        file = request.files['file']
        try:
            fullpath = UPLOAD_FOLDER + '/' + file.filename
            file.save(fullpath)
            with open(fullpath, newline='') as csvfile:
                reader = csv.reader(csvfile, delimiter=',')
                #return str(reader)
                rowlist = [] # хранит строки файла
                keylist = [] # хранит ключи - Ранг
                headlist = [] # хранит заголовки таблицы - первая строка файла
                bodylist = [] # хранит остальные значения таблицы
                for row in reader:
                    rowlist.append(row) # считываем весь файл
                for i in range(len(rowlist)):
                    if i != 0:
                        keylist.append(int(rowlist[i][0])) # копируем ключи - Ранг

                keylist.sort() # сортируем

                for i in range(len(rowlist[0])):
                    headlist.append({'name': rowlist[0][i]}) # копируем заголовки - шапку таблицы

                for i in range(len(keylist)): # перебираем ключи из отсортированного списка
                    for j in range(len(rowlist)): # для каждого ключа перебираем строки
                        if j != 0: # кроме шапки
                            if int(rowlist[j][0]) == keylist[i]: # при совпадении
                                bodylist.append([])
                                for k in range(len(rowlist[j])): # копируем значения
                                    bodylist[i].append({'value':rowlist[j][k]})

                return render_template("output.html", title = 'Output', head = headlist, body = bodylist)

        except Exception as e:
            return "exception detect "+ str(e)
    else:
        return render_template('upload.html')



