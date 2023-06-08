from flask import Flask, jsonify, request, abort
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask_cors import CORS


# Hier initialiseren we de Flask applicatie
app = Flask(__name__)
# hier maken we een CORS object aan

CORS(app)
# Hier initialiseren we de database -- C:\Users\matth\Documents\Engrafi\EngrafiNew\Apps\API.App \\dit is de DB van ons oorspronkelijk project
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///C:/Users/matth/Documents/Engrafi/EngrafiNew/Apps/API.App/Allphi.db'
db = SQLAlchemy(app)

# we definieren ook eem classe voor de bezoekers, anders kunnen we geen data opvragen/veranderen


class Bezoekers(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    voornaam = db.Column(db.String(255), nullable=False)
    achternaam = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), nullable=False)


class Bedrijven(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    naam = db.Column(db.Text, nullable=False)
    btwNummer = db.Column(db.Text, nullable=False)
    adres = db.Column(db.BLOB, nullable=False)
    telefoonNr = db.Column(db.BLOB, nullable=False)
    email = db.Column(db.Text, nullable=False)
    status = db.Column(db.Integer, nullable=False)


class Bezoek(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    bedrijf_id = db.Column(db.Integer, nullable=False)
    bezoeker_id = db.Column(db.Integer, nullable=False)
    bezochtte_werknemer = db.Column(db.Text, nullable=False)
    start_tijd = db.Column(db.DateTime, nullable=False)
    eind_tijd = db.Column(db.DateTime)
    status = db.Column(db.Integer, nullable=False)


@app.route('/bezoeker', methods=['GET'])
def get_bezoekers():
    bezoekers = Bezoekers.query.all()
    result = []
    for bezoeker in bezoekers:
        result.append({
            'id': bezoeker.id,
            'voornaam': bezoeker.voornaam,
            'achternaam': bezoeker.achternaam,
            'email': bezoeker.email
        })
    return jsonify(result)


# Route to retrieve a specific Bezoek by ID
@app.route('/bezoeker/<int:bezoek_id>', methods=['GET'])
def get_bezoek(bezoek_id):
    bezoeker = Bezoekers.query.get(bezoek_id)
    if bezoeker is None:
        return jsonify({'error': 'Bezoek not found'}), 404
    result = {
        'id': bezoeker.id,
        'voornaam': bezoeker.voornaam,
        'achternaam': bezoeker.achternaam,
        'email': bezoeker.email
    }
    return jsonify(result)

# Bezoeker ophalen met email:


@app.route('/bezoeker/email/<string:email>', methods=['GET'])
def get_bezoeker_by_email(email):
    bezoeker = Bezoekers.query.filter_by(email=email).first()
    if bezoeker is None:
        abort(404, 'Bezoeker not found')
    result = {
        'id': bezoeker.id,
        'voornaam': bezoeker.voornaam,
        'achternaam': bezoeker.achternaam,
        'email': bezoeker.email
    }
    return jsonify(result)


# Route to create a new Bezoek

@app.route('/bezoeker', methods=['POST'])
def create_bezoek():
    data = request.get_json()
    bezoeker = Bezoekers(
        voornaam=data['voornaam'],
        achternaam=data['achternaam'],
        email=data['email']
    )
    db.session.add(bezoeker)
    db.session.commit()
    return jsonify({'message': 'Bezoeker created successfully'})

# Route om alle bedrijven op te halen


@app.route('/bedrijven', methods=['GET'])
def get_bedrijven():
    bedrijven = Bedrijven.query.all()
    result = []
    for bedrijf in bedrijven:
        result.append({
            'id': bedrijf.id,
            'naam': bedrijf.naam,
            'btwNummer': bedrijf.btwNummer,
            'adres': bedrijf.adres,
            'telefoonNr': bedrijf.telefoonNr,
            'email': bedrijf.email,
            'status': bedrijf.status
        })
    return jsonify(result)


if __name__ == '__main__':
    app.run()

    # myenv\Scripts\activate --> daarna python main.py
