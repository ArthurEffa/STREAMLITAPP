import os
import streamlit as st
from openai import OpenAI

# Récupérer la clé API depuis les variables d'environnement
api_key = os.getenv('OPENAI_API_KEY')

if not api_key:
    st.error("La clé API OpenAI n'est pas configurée. Veuillez définir la clé API en tant que secret sur GitHub.")
else:
    # Initialise le client OpenAI avec la clé API
    client = OpenAI(api_key=api_key)

    def get_response(prompt):
        try:
            # Utilise le client pour créer une complétion de chat
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "user", "content": prompt}
                ]
            )
            # Accède au contenu du message de la réponse du bot
            completion_message = response.choices[0].message
            # Assurez-vous de vérifier la structure exacte de la réponse
            if hasattr(completion_message, 'content'):
                return completion_message.content.strip()
            else:
                return str(completion_message).strip()
        except Exception as e:
            # Capture toutes les exceptions et renvoie un message d'erreur générique
            return f"Erreur inattendue : {e}"

    def main():
        st.title("CONNEXION A OPEN AI")

        # Initialiser la session state pour conserver les messages
        if 'messages' not in st.session_state:
            st.session_state.messages = []

        # Zone de saisie pour l'utilisateur
        user_input = st.text_input("ARTHUR : ", "")

        # Ajouter un bouton pour envoyer le message
        if st.button("Envoyer"):
            if user_input.strip():  # Vérifie si l'entrée n'est pas vide
                # Ajouter le message de l'utilisateur à la liste
                st.session_state.messages.append({"role": "user", "content": user_input})

                # Obtenir la réponse du modèle
                bot_response = get_response(user_input)

                # Ajouter la réponse du bot à la liste
                st.session_state.messages.append({"role": "bot", "content": bot_response})
            else:
                st.error("Le message ne peut pas être vide.")  # Affiche un message d'erreur si l'entrée est vide

        # Afficher les messages
        for message in st.session_state.messages:
            if message["role"] == "user":
                st.write(f"**ARTHUR :** {message['content']}")
            else:
                st.write(f"**Bot :** {message['content']}")

    if __name__ == "__main__":
        main()
