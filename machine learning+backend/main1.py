# 📌 Imports
import pandas as pd
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import accuracy_score, classification_report
import joblib

# 📌 Templates pour chaque catégorie
templates = {
    "Inscription": "Bonjour {name},\nPour l'inscription, veuillez compléter le formulaire en ligne disponible sur le site universitaire.",
    "Examens": "Bonjour {name},\nLe calendrier des examens est disponible sur votre espace étudiant.",
    "Documents": "Bonjour {name},\nVous pouvez obtenir vos documents officiels via le secrétariat ou votre espace étudiant.",
    "Stage": "Bonjour {name},\nPour faire un stage, veuillez consulter les offres et envoyer votre candidature via la plateforme universitaire.",
    "Bourse": "Bonjour {name},\nPour les bourses, veuillez consulter la section Bourses sur le site universitaire et soumettre votre demande.",
    "Certificat": "Bonjour {name},\nVous pouvez demander vos certificats officiels via le secrétariat ou votre espace étudiant.",
    "Absences": "Bonjour {name},\nPour justifier une absence, veuillez envoyer votre justificatif au secrétariat.",
    "Rattrapages": "Bonjour {name},\nLe planning des rattrapages est disponible sur votre espace étudiant.",
    "Paiement": "Bonjour {name},\nPour le paiement des frais universitaires, consultez la section Paiement sur le site officiel.",
    "Calendrier": "Bonjour {name},\nLe calendrier académique est disponible sur votre espace étudiant.",
    "Reglement": "Bonjour {name},\nLe règlement intérieur peut être consulté sur le site officiel de l'université."
}

# 📌 Dataset (160 questions)
data = {
    "Question": [
        # Inscription (20)
        "Comment faire l'inscription", "Je veux m'inscrire", "Procédure pour inscription",
        "Comment s'inscrire en ligne", "Je veux enregistrer mon inscription", "Quand est le début des inscriptions",
        "Quels documents pour s'inscrire", "Comment compléter le formulaire d'inscription", "Comment finaliser l'inscription",
        "Inscription universitaire", "Comment changer de matière", "Est-ce que je peux m'inscrire tardivement",
        "Comment renouveler mon inscription", "Comment modifier mon inscription", "Où s'inscrire pour les cours",
        "Formulaire d'inscription en ligne", "Instructions pour inscription", "Comment m'inscrire au semestre prochain",
        "Procédure rapide pour inscription", "Comment valider mon inscription",
        # Examens (20)
        "Quand est le rattrapage", "Date des examens", "Comment se préparer aux examens", "Calendrier des examens",
        "Résultats des examens", "Quand a lieu l'examen final", "Planning des examens", "Comment contester un examen",
        "Heures des examens", "Informations sur les examens", "Où consulter les résultats", "Comment récupérer une copie d'examen",
        "Procédure pour rattrapage", "Examens partiels", "Notes finales", "Quand sont les examens du semestre",
        "Examens en ligne", "Date limite inscription examen", "Comment se réinscrire pour un examen", "Organisation des examens",
        # Documents (20)
        "Comment demander une attestation", "Comment obtenir un relevé de notes", "Demande de certificat",
        "Où récupérer mes documents", "Relevé de notes en ligne", "Certificat d'inscription", "Attestation de présence",
        "Comment télécharger mes documents", "Demande officielle de document", "Comment obtenir une copie certifiée",
        "Certificat de stage", "Documents administratifs", "Comment obtenir un document officiel", "Demande d'attestation en ligne",
        "Relevé de notes officiel", "Certificat académique", "Attestation pour bourse", "Procédure pour document universitaire",
        "Télécharger certificat", "Comment faire une demande officielle",
        # Stage (20)
        "Je veux faire un stage", "Comment postuler pour un stage", "Stage universitaire", "Comment trouver un stage",
        "Stage obligatoire pour la formation", "Comment envoyer ma candidature pour stage", "Où faire un stage", "Durée d'un stage",
        "Documents pour le stage", "Comment valider le stage", "Stage pratique", "Stage d'été", "Inscription stage",
        "Recommandations pour stage", "Comment réussir son stage", "Stage rémunéré", "Procédure pour stage", "Stage entreprise",
        "Planification d'un stage", "Stage académique",
        # Bourse (10)
        "Comment demander une bourse", "Qui peut bénéficier d'une bourse", "Quels documents pour la bourse", "Date limite pour la bourse",
        "Bourse pour étudiants internationaux", "Comment renouveler ma bourse", "Montant des bourses", "Procédure demande bourse",
        "Bourse semestre prochain", "Comment vérifier l'état de ma bourse",
        # Certificat (10)
        "Comment obtenir un certificat officiel", "Demande de certificat académique", "Certificat d'inscription", "Certificat de stage",
        "Certificat de réussite", "Où récupérer un certificat officiel", "Comment demander un certificat rapidement",
        "Certificat pour bourse", "Certificat pour emploi", "Demande en ligne de certificat",
        # Absences (10)
        "Comment justifier une absence", "Procédure pour absence", "Quelle pièce pour absence", "Comment envoyer un justificatif",
        "Absence pour maladie", "Absence pour raisons personnelles", "Comment signaler une absence", "Absence sans prévenir",
        "Comment récupérer les cours manqués", "Absence prolongée",
        # Rattrapages (10)
        "Quand est le rattrapage", "Comment s'inscrire au rattrapage", "Planning des rattrapages", "Résultats de rattrapage",
        "Date limite rattrapage", "Examens de rattrapage", "Comment annuler un rattrapage", "Rattrapage en ligne",
        "Conditions pour rattrapage", "Procédure pour rattrapage",
        # Paiement (10)
        "Quand est la date limite de paiement", "Comment payer les frais", "Modes de paiement acceptés", "Paiement en ligne",
        "Paiement tardif", "Réception du reçu", "Frais de scolarité", "Comment vérifier le paiement", "Paiement semestre prochain",
        "Procédure paiement",
        # Calendrier (10)
        "Quand commence le semestre", "Planning des cours", "Calendrier académique", "Dates importantes", "Jours fériés",
        "Examens et rattrapages", "Vacances universitaires", "Début et fin semestre", "Calendrier officiel", "Modification du calendrier",
        # Règlement (10)
        "Où trouver le règlement intérieur", "Quelles sont les règles universitaires", "Règles de conduite", "Sanctions en cas de non-respect",
        "Procédure disciplinaire", "Règlement académique", "Consultation du règlement", "Obligations des étudiants",
        "Charte de l'étudiant", "Règlement officiel"
    ],
    "Category": [
        *["Inscription"]*20, *["Examens"]*20, *["Documents"]*20, *["Stage"]*20,
        *["Bourse"]*10, *["Certificat"]*10, *["Absences"]*10, *["Rattrapages"]*10,
        *["Paiement"]*10, *["Calendrier"]*10, *["Reglement"]*10
    ]
}

df = pd.DataFrame(data)

# 📌 Split train/test
X_train, X_test, y_train, y_test = train_test_split(
    df["Question"], df["Category"], test_size=0.2, random_state=42
)

# 📌 TF-IDF vectorisation
vectorizer = TfidfVectorizer()
X_train_tfidf = vectorizer.fit_transform(X_train)
X_test_tfidf = vectorizer.transform(X_test)

# 📌 Modèle MultinomialNB avec GridSearchCV pour hyperparam
param_grid = {'alpha': [0.1, 0.5, 1.0, 2.0]}
nb_model = MultinomialNB()
grid = GridSearchCV(nb_model, param_grid, cv=5)
grid.fit(X_train_tfidf, y_train)

# 📌 Meilleur modèle
best_model = grid.best_estimator_

# 📌 Prédiction test set
y_pred = best_model.predict(X_test_tfidf)

# 📌 Évaluation
accuracy = accuracy_score(y_test, y_pred)
print("✅ Accuracy:", accuracy)
print("\n📊 Classification Report:\n")
print(classification_report(y_test, y_pred, zero_division=0))

# 📌 Nouvelles questions à tester
nouvelles_questions = [
    "Je veux m'inscrire rapidement", "Comment obtenir une attestation officielle", "Quand est le rattrapage",
    "Je cherche un stage universitaire", "Comment demander une bourse", "Comment obtenir un certificat officiel",
    "Comment justifier une absence", "Quand commence le semestre", "Où trouver le règlement intérieur",
    "Comment payer les frais universitaires"
]

new_vec = vectorizer.transform(nouvelles_questions)
predictions = best_model.predict(new_vec)

# 📌 Génération automatique des réponses
name_etudiant = "Ali"  # Nom par défaut pour les tests

print("\n" + "="*50)
print("📝 TEST DES 10 NOUVELLES QUESTIONS")
print("="*50)

for q, p in zip(nouvelles_questions, predictions):
    response = templates.get(p, "Désolé, je n'ai pas de réponse pour cette question.").format(name=name_etudiant)
    print(f"\n❓ Question: {q}")
    print(f"🏷️ Catégorie prédite: {p}")
    print(f"💬 Réponse automatique:\n{response}")

# 📌 Sauvegarder modèle et vectorizer
joblib.dump(best_model, "question_model.pkl")
joblib.dump(vectorizer, "tfidf_vectorizer.pkl")
print("\n" + "="*50)
print("✅ Modèle et vectorizer sauvegardés avec succès !")
print("="*50)

# 📌 --- CHATBOT INTERACTIF CORRIGÉ (UN SEUL while True) ---
print("\n" + "="*50)
print("🤖 BIENVENUE DANS LE CHATBOT UNIVERSITAIRE")
print("="*50)

# Demander le nom une seule fois au début
nom_utilisateur = input("\n👤 Veuillez entrer votre nom : ")

while True:
    # Poser la question
    user_input = input("\n❓ Posez votre question (ou tapez 'exit' pour quitter) : ")
    
    # Vérifier si l'utilisateur veut quitter
    if user_input.lower() in ["exit", "quit", "bye", "au revoir"]:
        print(f"👋 Merci {nom_utilisateur}! À bientôt.")
        break
    
    # Vérifier si la question n'est pas vide
    if not user_input.strip():
        print("⚠️ Veuillez entrer une question valide.")
        continue
    
    # Prédire la catégorie
    user_vec = vectorizer.transform([user_input])
    pred_category = best_model.predict(user_vec)[0]
    
    # Générer la réponse
    response = templates.get(
        pred_category, 
        "Désolé, je n'ai pas de réponse pour cette question."
    ).format(name=nom_utilisateur)
    
    # Afficher la réponse
    print(f"\n🏷️ Catégorie prédite: {pred_category}")
    print(f"💬 Réponse automatique:\n{response}")

print("\n📦 Programme terminé.")