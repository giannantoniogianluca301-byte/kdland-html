# Import
from flask import Flask, render_template,request, redirect, session
# Collegare la libreria del database
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
# Impostare la chiave segreta per la sessione
app.secret_key = 'il_mio_super_segreto_1234'
# Connettere SQLite
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///diary.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# Creare il DB
db = SQLAlchemy(app)
# Creare la tabella

class Card(db.Model):
    # Creazione delle colonne
    # id
    id = db.Column(db.Integer, primary_key=True)
    # Titolo
    title = db.Column(db.String(100), nullable=False)
    # Sottotitolo
    subtitle = db.Column(db.String(200), nullable=False)
    # Testo
    text = db.Column(db.Text(400), nullable=False)
    # La mail del proprietario della scheda
    user_email = db.Column(db.String(100), nullable=False)

    # Visualizzazione dell'oggetto e dell'id
    def __repr__(self):
        return f'<Card {self.id}>'
    

#Consegna #1. Creare la tabella User
class User(db.Model):
    # Creazione delle colonne
    #
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String(100), nullable=False)
    password = db.Column(db.String(20), nullable=False)
    
    def __repr__(self):
        return f'<User {self.id}>'

# Esecuzione della pagina dei contenuti
@app.route('/', methods=['GET','POST'])
def login():
        error = ''
        if request.method == 'POST':
            form_login = request.form['email']
            form_password = request.form['password']
            
            #Consegna #4. Implementare l'autorizzazione
            users = User.query.all()
            for user in users:
                if form_login == user.email and form_password == user.password:
                    session['user_email'] = user.email
                    return redirect('/index')
            
            error = "credenziali errate"
            return render_template("login.html", error=error)
         
        else:
            return render_template('login.html')



@app.route('/reg', methods=['GET','POST'])
def reg():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        
        # Consegna #3. Implementare la registrazione dell'utente.
        user = User(email=email, password=password)
        db.session.add(user)
        db.session.commit()

        
        return redirect('/')
    
    else:    
        return render_template('registration.html')


# Esecuzione della pagina dei contenuti
@app.route('/index')
def index():
    # Consegna #4. Assicurarsi gli utenti vedano solo le proprie schede
    cards = Card.query.order_by(Card.id).all()
    return render_template('index.html', cards=cards)

# Esecuzione della pagina con la scheda
@app.route('/card/<int:id>')
def card(id):
    card = Card.query.get(id)

    return render_template('card.html', card=card)

# Esecuzione della pagina di creazione della voce
@app.route('/create')
def create():
    return render_template('create_card.html')

# Il modulo di creazione della scheda
@app.route('/form_create', methods=['GET','POST'])
def form_create():
    if request.method == 'POST':
        title =  request.form['title']
        subtitle =  request.form['subtitle']
        text =  request.form['text']
        mail = session['user_email']

        # Consegna #4. Fare in modo che la creazione avvenga per contro dell'utente corretto
        card = Card(title=title, subtitle=subtitle, text=text, user_email=mail)

        db.session.add(card)
        db.session.commit()
        return redirect('/index')
    else:
        return render_template('create_card.html')

if __name__ == "__main__":
    app.run(debug=True)
