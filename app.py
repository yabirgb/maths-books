from flask import Flask, render_template, request, send_from_directory
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__, static_url_path="/static")
app.config['SQLALCHEMY_DATABASE_URI'] = 'YOURDATABASE'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Create database model

book_node = db.Table('shelfs',
    db.Column('book_id', db.String, db.ForeignKey('book.asin')),
    db.Column('node_pk', db.String, db.ForeignKey('node.pk'))
)

class Node(db.Model):
    __tablename__ = "node"
    pk = db.Column(db.String(30), primary_key=True)
    name = db.Column(db.String(300), nullable=True)
    def __repr__(self):
        return '' % self.name

    def __init__(self, name, pk):
        self.pk = pk
        self.name = name

class Book(db.Model):
    __tablename__ = "book"
    asin = db.Column(db.String, primary_key=True, nullable=True)
    title = db.Column(db.String(300), nullable=True)
    author = db.Column(db.String(300), nullable=True)
    ean = db.Column(db.String(300), nullable=True)
    isbn = db.Column(db.String(300), nullable=True)
    url = db.Column(db.String(300), nullable=True)
    image = db.Column(db.String(300), nullable=True)
    publisher = db.Column(db.String(300), nullable=True)
    published = db.Column(db.String(300), nullable=True)

    nodes = db.relationship('Node', secondary=book_node,
        backref=db.backref('books'))

    def __init__(self, asin, title, author, ean, isbn, url, image, publisher, published):
        self.asin = asin
        self.title = title
        self.author = author
        self.ean = ean
        self.isbn = isbn
        self.url = url
        self.image = image
        self.publisher = publisher
        self.published = published

    def __repr__(self):
        return '' % self.title

# Set "homepage"
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/book/<asin>')
def show_book(asin):
    book = Book.query.filter_by(asin=asin).first_or_404()
    return render_template('book.html', book=book)

@app.route('/css/<path:path>')
def send_css(path):
    return send_from_directory('static/css', path)

# Save e-mail to database and send to success page
@app.route('/prereg', methods=['POST'])
def prereg():
    email = None
    if request.method == 'POST':
        email = request.form['email']
        # Check that email does not already exist (not a great query, but works)
        if not db.session.query(User).filter(User.email == email).count():
            reg = User(email)
            db.session.add(reg)
            db.session.commit()
            return render_template('success.html')
    return render_template('index.html')

if __name__ == '__main__':
    app.debug = True
    app.run()
