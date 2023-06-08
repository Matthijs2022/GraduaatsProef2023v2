from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

# Hier initialiseren we de Flask applicatie
app = Flask(__name__)
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