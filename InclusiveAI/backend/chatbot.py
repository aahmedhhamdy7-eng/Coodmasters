
# chatbot.py
# chatbot.py

faq = {
    "inscription": "Pour vous inscrire, connectez-vous sur le portail étudiant et remplissez le formulaire en ligne.",
    "bourse": "Pour les bourses, remplissez le formulaire disponible sur le site officiel.",
    "certificat": "Pour obtenir une attestation, envoyez un mail au secrétariat.",
    "stage": "Pour un stage, envoyez votre CV et lettre de motivation à la coordination des stages.",
    "absences": "Les absences doivent être signalées via le portail étudiant.",
    "rattrapage": "Les demandes de rattrapage se font auprès de votre département.",
    "paiement": "Le paiement des frais universitaires se fait en ligne sur le portail.",
    "calendrier": "Le calendrier universitaire est disponible sur le site officiel.",
    "reglement": "Le règlement intérieur est consultable dans la section documents du site.",
    "mot de passe": "tu reccupere ton mot de passe par l'appui au bouton mot de passe oublie"
}


def chatbot_response_admin(question):
    question = question.lower()
    for key, answer in faq.items():
        if key in question:
            return answer
    return "Désolé, je n'ai pas trouvé la réponse exacte. Veuillez contacter le secrétariat."
# chatbot.py


def generate_email_request(type_request, student_name):
    if type_request == "attestation":
        return f"Bonjour,\n\nJe soussigné(e) {student_name},  souhaite obtenir une attestation. Merci.\n\n"
    elif type_request == "reclamation":
        return f"Bonjour,\n\nJe soussigné(e) {student_name}, souhaite déposer une réclamation concernant ...\n\n"
    elif type_request == "stage":
        return f"Bonjour,\n\nJe soussigné(e) {student_name}, souhaite postuler pour un stage. \n\n"
    else:
        return "Type de demande non reconnu."
