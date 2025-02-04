# Importation de la fonction chat depuis la librairie ollama
from ollama import chat
from colorama import Fore, Back, Style

# Fonction pour envoyer un message simple au modèle
def send_message(model_name: str, message: str) -> str:
    """
    Envoie un message simple au modèle et retourne sa réponse
    Args:
        model_name: Nom du modèle à utiliser (ex: 'llama3.2:1b')
        message: Message à envoyer
    Returns:
        La réponse du modèle
    """

    # Création du message au format attendu par l'API
    messages = [{'role': 'user', 'content': message}]
    
    # Envoi de la requête au modèle
    response = chat(model=model_name, messages=messages)
    
    # Retour du contenu de la réponse
    return response.message.content

def initialize_context(role_description: str) -> None:
    """
    Initialise le contexte du chatbot avec un rôle spécifique
    Args:
        role_description: Description du rôle que doit jouer le modèle
    """
    # On efface l'historique existant
    messages_history.clear()
    
    # On ajoute le message de contexte qui définit le rôle
    context_message = {
        'role': 'system',
        'content': f"Tu es un assistant spécialisé qui agit en tant que {role_description}. " \
                  f"Réponds toujours en respectant ce rôle."
    }
    messages_history.append(context_message)

def send_message_with_history(model_name: str, message: str) -> str:
    """
    Envoie un message en tenant compte de l'historique et du contexte
    Args:
        model_name: Nom du modèle à utiliser
        message: Message à envoyer
    Returns:
        La réponse du modèle
    """
    # Ajout du nouveau message à l'historique

    messages_history.append({
        'role': 'system',
        'content': message
    })

    # Envoi de tout l'historique au modèle
    response = chat(model=model_name, messages=messages_history)
    
    # Ajout de la réponse à l'historique
    messages_history.append(response.message)
    
    return response.message.content


# Liste pour stocker l'historique des messages
messages_history = []

def lance_conversation():
    """
    Lance une conversation avec le chatbot
    """
    print(Fore.CYAN + "Bonjour, en quoi puis-je vous aider?")
    
    choix = 0
    while choix == 0:
        print(Fore.CYAN +"Préciser à qui vous vous adressez: \n")
        print(Fore.CYAN +"1. Expert en Python")
        print(Fore.CYAN +"2. Spécialiste cybersécurité")
        print(Fore.CYAN +"3. Coach agile")
        print(Fore.CYAN +"4 Quitter")
        try:
            choix = int(input(Fore.RED +"votre choix: "))
        except ValueError:
            print(Fore.CYAN +"Veuillez entrer un nombre.")
        else:
            match(choix):
                case 1:
                    # Initialisation du contexte avec le rôle 'expert en Python'
                    initialize_context('expert en Python')
                case 2:
                # Initialisation du contexte avec le rôle 'spécialiste cybersécurité'
                    initialize_context('spécialiste cybersécurité')
                case 3:
                # Initialisation du contexte avec le rôle 'coach agile'
                    initialize_context('coach agile')
                case 4:
                    break
                case _:
                    choix = 0

    # Boucle infinie pour la conversation
    while True:

        user_input = input(Fore.RED + "Vous: ")
        
        # Si l'utilisateur tape 'bye', on arrête la conversation
        if user_input.lower() == 'bye':
            print(Fore.CYAN + "Au revoir!")
            break
        
        # Envoi du message au modèle et récupération de la réponse
        response = send_message('deepseek-r1', user_input)
        
        # Affichage de la réponse à l'IA
        if( choix == 1):
            print(Fore.CYAN + f"Expert en Python: {response}")
            send_message_with_history('deepseek-r1', user_input)
        elif(choix == 2):
            print(Fore.CYAN + f"Spécialiste cybersécurité: {response}")
            send_message_with_history('deepseek-r1', user_input)
        else:
            print(Fore.CYAN + f"Coach agile: {response}")
            send_message_with_history('deepseek-r1', user_input)

        # Ajout du message à l'historique
        send_message_with_history('deepseek-r1', user_input)
        send_message_with_history('deepseek-r1', response)

lance_conversation()


