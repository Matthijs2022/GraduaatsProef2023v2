from flask import Flask, jsonify, request, abort
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask_cors import CORS
import os

# Dit is Python funcionaliteit om het pad te bepalen waar de applicatie draait
base_dir = os.path.abspath(os.path.dirname(__file__))

# Hier bepalen we vervolgens het (relatieve) pad naar de database
db_path = os.path.join(base_dir, 'Database/Allphi.db')

# Hier initialiseren we de Flask applicatie
app = Flask(__name__)

# hier maken we een CORS object aan, anders krijgen we problemen met de cross origin requests
CORS(app)

# Hier initialiseren we de database
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{db_path}'
db = SQLAlchemy(app)

# vervolgens definieren we hier de klassen, zoals ze in de database staan


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
    bedrijfId = db.Column(db.Integer, nullable=False)
    bezoekerId = db.Column(db.Integer, nullable=False)
    bezochtteWerknemer = db.Column(db.Text, nullable=False)
    startTijd = db.Column(db.DateTime, nullable=False)
    eindTijd = db.Column(db.DateTime)
    status = db.Column(db.Integer, nullable=False)

# Nu kunnen we routes omschrijven om de data op te halen en te bewerken
# We beginnen met een route om alle bezoekers op te halen


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


# Bezoeker ophalen met email:
@app.route('/bezoeker/email/<string:email>', methods=['GET'])
def get_bezoeker_by_email(email):
    bezoeker = Bezoekers.query.filter_by(email=email).first()
    if bezoeker is None:
        return jsonify({'exists': False})
    result = {
        'exists': True,
        'id': bezoeker.id,
        'voornaam': bezoeker.voornaam,
        'achternaam': bezoeker.achternaam,
        'email': bezoeker.email
    }
    return jsonify(result)


# Route om een bezoeker te creeren
@app.route('/bezoeker', methods=['POST'])
def create_bezoeker():
    data = request.get_json()
    bezoeker = Bezoekers(
        voornaam=data['voornaam'],
        achternaam=data['achternaam'],
        email=data['email']
    )
    db.session.add(bezoeker)
    db.session.commit()

    # We geven hier de id mee terug zodat we deze direct kunnen gebruiken bij het aanmaken van een bezoek
    return jsonify({'message': 'Bezoeker created successfully', 'id': bezoeker.id})


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


# Route voor het creeren van een bezoek
@app.route('/bezoek', methods=['POST'])
def create_bezoek():
    data = request.get_json()
    start_tijd_str = data['startTijd']
    eind_tijd_str = data['eindTijd']

    startTijd = None
    if start_tijd_str:
        startTijd = datetime.fromisoformat(
            start_tijd_str.replace('Z', '+00:00'))

    eindTijd = None
    if eind_tijd_str:
        eindTijd = datetime.fromisoformat(eind_tijd_str.replace('Z', '+00:00'))

    bezoek = Bezoek(
        bedrijfId=data['bedrijfId'],
        bezoekerId=data['bezoekerId'],
        bezochtteWerknemer=data['bezochtteWerknemer'],
        startTijd=startTijd,
        eindTijd=eindTijd,
        status=data['status']
    )
    db.session.add(bezoek)
    db.session.commit()
    return jsonify({'message': 'Bezoek created successfully'})

# # route voor het deleten van een bezoek
# @app.route('/bezoek/<int:bezoek_id>', methods=['DELETE'])
# def delete_bezoek(bezoek_id):
#     bezoek = Bezoek.query.get(bezoek_id)

#     if not bezoek:
#         return jsonify({'message': 'Bezoek not found'})

#     db.session.delete(bezoek)
#     db.session.commit()

#     return jsonify({'message': 'Bezoek deleted successfully'})

# Beter een andere methode dan delete...

# Deze methode laat nog het best zien hoe Python en SQLAlchemy hier eigenlijk een
# volwaardige backend kunnen neerzetten met relatief weinig code


@app.route('/bezoek/end', methods=['POST'])
def end_bezoek():
    data = request.get_json()
    email = data['email']
    # print(email)

    # hier zie je hoe je een query kan uitvoeren met SQLAlchemy
    bezoeker = Bezoekers.query.filter_by(email=email).first()
    if not bezoeker:
        return jsonify({'message': 'Bezoeker not found'})

    # Python springt uit de functie als je een return statement tegenkomt
    # dus je hoeft niet overal een else statement te gebruiken
    # als hij een bezoeker vindt, dan gaat hij verder met de volgende regel
    # als hij geen bezoeker vindt, dan stopt hij met de functie en geeft hij een response terug
    # hieronder zoekt hij het bezoek dat bij de bezoeker hoort en nog actief is
    bezoek = Bezoek.query.filter_by(bezoekerId=bezoeker.id, status=1).first()
    if not bezoek:
        return jsonify({'message': 'Active bezoek not found for the given Bezoeker'})

    # vervolgens zetten we de status op 0 en de eindtijd op het huidige moment
    bezoek.status = 0
    bezoek.eindTijd = datetime.now()
    db.session.commit()

    return jsonify({'message': 'Bezoek ended successfully'})


if __name__ == '__main__':
    app.run()

    # myenv\Scripts\activate --> daarna python main.py
