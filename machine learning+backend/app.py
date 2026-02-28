from flask_mysqldb import MySQL

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'        # ton utilisateur MySQL
app.config['MYSQL_PASSWORD'] = ''        # ton mot de passe
app.config['MYSQL_DB'] = 'assistant_ai'

mysql = MySQL(app)
from flask import Flask, request, jsonify, render_template
import joblib
import sqlite3

# 📌 Charger le modèle et vectorizer
model = joblib.load("question_model.pkl")
vectorizer = joblib.load("tfidf_vectorizer.pkl")

# 📌 Templates de réponses
templates = {
    "Inscription": "Bonjour {name},\nPour l'inscription, veuillez compléter le formulaire en ligne.",
    "Documents": "Bonjour {name},\nVous pouvez obtenir vos documents via le secrétariat.",
    "Examens": "Bonjour {name},\nLe calendrier des examens est disponible sur votre espace étudiant.",
    # Ajoute toutes tes catégories ici...
}

# 📌 Initialiser Flask
app = Flask(__name__)

# 📌 Créer la DB si elle n’existe pas
conn = sqlite3.connect('chatbot.db', check_same_thread=False)
cursor = conn.cursor()
cursor.execute('''
CREATE TABLE IF NOT EXISTS conversations (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    question TEXT,
    category TEXT,
    response TEXT
)
''')
conn.commit()

# 📌 Route pour interface web
@app.route("/")
def index():
    return render_template("index.html")

# 📌 Route pour poser une question via AJAX
@app.route("/ask", methods=["POST"])
def ask():
    data = request.json
    question = data.get("question", "")
    user_name = data.get("name", "Ali")

    # Transformer la question et prédire catégorie
    vec = vectorizer.transform([question])
    category = model.predict(vec)[0]

    # Générer réponse
    response = templates.get(category, "Désolé, je n'ai pas de réponse.").format(name=user_name)

    # Sauvegarder dans DB
    cursor.execute('INSERT INTO conversations (question, category, response) VALUES (?, ?, ?)',
                   (question, category, response))
    conn.commit()

    return jsonify({"category": category, "response": response})

# 📌 Lancer Flask
if __name__ == "__main__":
    app.run(debug=True)
@app.route("/predict", methods=["POST"])
def predict():
    cur = mysql.connection.cursor()
cur.execute(
    "INSERT INTO questions (question, reponse) VALUES (%s, %s)",
    (data, prediction)
)
mysql.connection.commit()
    data = request.json["question"]
    # envoie au modèle ML
    prediction = model.predict([data])[0]
    # enregistre dans MySQL
    cur.execute("INSERT INTO questions (question, reponse) VALUES (%s,%s)", (data, prediction))
    mysql.connection.commit()
    return jsonify({"response": prediction})
from flask import Flask, request, jsonify
import joblib

app = Flask(__name__)

# Charger le modèle ML
model, vectorizer = joblib.load("model.pkl")  # ton fichier ML

@app.route("/predict", methods=["POST"])
def predict():
    # 1️⃣ Récupérer la question du frontend
    user_input = request.json["question"]

    # 2️⃣ Transformer la question pour le modèle ML
    X = vectorizer.transform([user_input])
    prediction = model.predict(X)[0]  # le modèle renvoie la réponse

    # 3️⃣ Renvoyer la réponse au frontend
    return jsonify({"response": prediction})

if __name__ == "__main__":
    app.run(debug=True)

