# test_chatbot.py

from chatbot import chatbot_response_admin, generate_email_request

print("=== Chatbot Administratif Test ===")

while True:
    question = input("Élève: ")
    if question.startswith("email:"):
        # Exemple: "email:attestation,John Doe"
        parts = question.replace("email:", "").split(",")
        type_req = parts[0].strip()
        name = parts[1].strip()
        print("Chatbot:", generate_email_request(type_req, name))
    else:
        print("Chatbot:", chatbot_response_admin(question))
