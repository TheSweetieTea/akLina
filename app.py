from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime



app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///Desktop.db'
db = SQLAlchemy(app)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


class Contact(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    text = db.Column(db.Text(100), nullable=False)
    date = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return '<Contact %r>' % self.id


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/posts')
def posts():
    contacts = Contact.query.order_by(Contact.date.desc()).all()
    return render_template('posts.html', contacts=contacts)


@app.route('/posts/<int:id>')
def detail(id):
    contact = Contact.query.get(id)
    return render_template('detail.html', contact=contact)


@app.route('/posts/<int:id>/delete')
def detail_delete(id):

    contact = Contact.query.get_or_404(id)

    try:
        db.session.delete(contact)
        db.session.commit()
        return redirect('/posts')
    except:
        return 'Произошла ошибка'


@app.route('/posts/<int:id>/update', methods=['POST', 'GET'])
def update(id):
    contact = Contact.query.get(id)
    if request.method == 'POST':
        contact.title = request.form['title']
        contact.text = request.form['text']

        try:
            db.session.commit()
            return redirect('/posts')
        except:
            return 'Произошла ошибка при редактировании отзыва'
    else:
        return render_template('update.html', contact=contact)


@app.route('/contact', methods=['POST', 'GET'])
def contact():
    if request.method == 'POST':
        title = request.form['title']
        text = request.form['text']

        contact = Contact(title=title, text=text)

        try:
            db.session.add(contact)
            db.session.commit()
            return redirect('/')
        except:
            return 'Произошла ошибка при добавлении отзыва'
    else:
        return render_template('contact.html')


@app.route('/sign_up')
def sign_up():
    return render_template("signup.html")


@app.route('/learn')
def learn():
    return render_template('learn.html')




if __name__ == '__main__':
    app.run(debug=True)
