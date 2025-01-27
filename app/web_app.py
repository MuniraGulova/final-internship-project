from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)  # директива name указывает на web_app.py
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///new_flask.db'
db = SQLAlchemy(app)

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80), nullable=False)
    text = db.Column(db.Text, nullable=False)

@app.route("/index") # декоратор - обработчик для отображения сайта
@app.route("/")  # декоратор - обработчик для отображения сайта
def index():
    return render_template('index.html') #тут можно не указывать папку потому, что он по умолчанию уже указан во фласке

@app.route("/create", methods=['GET', 'POST'])
# отправляем в бд
def create():
    if request.method == 'POST':
        title=request.form["title"]
        text=request.form["text"]

        post=Post(title=title, text=text)

        try:
            db.session.add(post)
            db.session.commit()
            return redirect("/") # если все хорошо идем на главную станичку
        except:
            return 'При добавлении статьи произошла ошибка!'
    else:
        return render_template("create.html")
    return render_template("create.html")


# вывод из бд
@app.route("/posts")
def posts():
    posts=Post.query.all()
    return render_template('posts.html', posts=posts)



if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)
