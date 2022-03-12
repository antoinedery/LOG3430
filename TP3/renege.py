
import json
import sys
from crud import CRUD
from email_analyzer import EmailAnalyzer


class RENEGE:

    """Classe pour realiser le filtrage du spam en utilisant le fichier vocabulary.json et
    les classes CRUD et EmailAnalyzer"""

    def __init__(self):
        self.email_file = "train_set.json"
        self.crud = CRUD()
        self.e_mail = EmailAnalyzer()

    def classify_emails(self):
        '''
        Description: fonction pour commencer l'analyse des e-mails.
        Sortie: bool, 'True' pour success, 'False' dans le cas de failure.
        '''
        try:
            self.process_email(self.get_email())
            return True
        except Exception as e:
            print("Error!", e.__class__, "occurred.")
            raise e
            return False

    def process_email(self, new_emails):
        '''
        Description: fonction pour analyser chaque nouvel e-mail dans le 
        dictionnaire. Elle gere l'ajout des nouveaux utilisateurs et/ou modification
        de l'information existante sur les utilisateurs et groupes. 
        Sortie: bool, 'True' pour success, 'False' dans le cas de failure.
        '''
        emails = self.get_email()
        print("Processing emails")
        i = 0
        email_count = len(emails["dataset"])
        # Load emails
        for email in emails["dataset"]:
            i += 1
            print("\rEmail " + str(i) + "/" + str(email_count), end="")

            data = email["mail"]
            subject = data["Subject"]
            name = data["From"]
            date = data["Date"]
            body = data["Body"]
            is_spam = data["Spam"]

            # Get registered data
            user_id = -1
            try:
                user_id = self.crud.get_user_id(name)
            except RuntimeError:
                # Create the user
                if not self.crud.add_new_user(name, date):
                    return False

                user_id = self.crud.get_user_id(name)

            # Update user's emails info
            if is_spam == "true":
                if not self.update_user_info(user_id, date, 1, 0):
                    return False
            else:
                if not self.update_user_info(user_id, date, 0, 1):
                    return False

            # Update groups data
            groups = self.crud.get_user_data(user_id, "Groups")
            for group_name in groups:
                try:
                    group_id = self.crud.get_group_id(group_name)
                    if not self.update_group_info(group_id, user_id):
                        return False

                except RuntimeError:
                    return False

        print("\n")

        return True

    def update_user_info(self, user_id, new_user_date, new_email_spam, new_email_ham):
        '''
        Description: fonction pour modifier l'information de utilisateur (date de dernier message arrive,
        numero de spam/ham, trust level, etc).
        Sortie: bool, 'True' pour success, 'False' dans le cas de failure.
        '''

        # Update last / first seen date
        new_date = self.crud.convert_to_unix(new_user_date)
        if new_date > self.crud.get_user_data(user_id, "Date_of_last_seen_message"):
            if not self.crud.update_users(user_id, "Date_of_last_seen_message", new_user_date):
                return False
        elif new_date < self.crud.get_user_data(user_id, "Date_of_first_seen_message"):
            if not self.crud.update_users(user_id, "Date_of_first_seen_message", new_user_date):
                return False

        # Update trust score
        spam_n = self.crud.get_user_data(user_id, "SpamN") + new_email_spam
        ham_n = self.crud.get_user_data(user_id, "HamN") + new_email_ham

        trust_lvl = 50
        if (spam_n + ham_n) != 0:
            trust_lvl = ham_n / (spam_n + ham_n) * 100
            if trust_lvl > 100:
                trust_lvl = 100

        if not self.crud.update_users(user_id, "SpamN", spam_n):
            return False

        if not self.crud.update_users(user_id, "HamN", ham_n):
            return False

        return self.crud.update_users(user_id, "Trust", trust_lvl)

    def update_group_info(self, group_id, user_id):
        '''
        Description: fonction pour modifier l'information de groupe dans lequel 
        l'utilisateur est present (trust level, etc).
        Sortie: bool, 'True' pour success, 'False' dans le cas de failure.
        '''
        try:
            # Get list of users and update it
            users_list = self.crud.get_groups_data(group_id, "List_of_members")
            user_name = self.crud.get_user_data(user_id, "name")
            if user_name not in users_list:
                users_list.append(user_name)

            # Get data for trust update
            user_count = len(users_list)
            trust_lvl = 0

            # Compute group's trust
            for user in users_list:
                curr_user_id = self.crud.get_user_id(user)
                trust_lvl += self.crud.get_user_data(curr_user_id, "Trust")

            if(trust_lvl > 100):
                trust_lvl = 100

            # Update the group with the new trust level and the new member list
            if self.crud.update_groups(group_id, "Trust", trust_lvl):
                return self.crud.update_groups(group_id, 'List_of_members', users_list)

            return False
        except RuntimeError:
            return False

    def get_user_email_list(self):
        '''
        Description: fonction pour creer la liste des e-mails (noms)
        des utilisateurs.
        Sortie: liste des e-mails des utilisateurs
        '''
        emails = []
        for user in self.crud.users_data:
            emails.append(user["name"])
        return emails

    def get_email(self):
        '''
        Description: fonction pour lire le ficher json avec les mails et extraire les 
        donnees necessaires.
        Sortie: dictionnaire des e-mails formates selon le JSON.
        '''
        with open(self.email_file) as email_file:
            return json.load(email_file)

    ###########################################
    #             CUSTOM FUNCTION             #
    ###########################################

    # fonction imprime les emails des utilisateurs avec leur confiance
    # permet de tester notre implémentation en affichant dans la console
    def print_trust_of_users(self):
        
        # parcourt chaque utilisateur
        for user_id in self.crud.users_data.keys():
            # imprime les emails des utilisateurs avec leur confiance
            print(
                self.crud.get_user_data(str(user_id), "name") + " : " +
                str(self.compute_trust(user_id))
            )


    # calcule la trust totale d'un utilisateur
    def compute_trust(self, user_id):

        # calcule la trust 1
        trust_one = self.compute_trust_one(user_id)
        # calcule la trust 2
        trust_two = self.compute_trust_two(user_id)

        # calcule la trust totale
        trust = (0.6 * trust_one + 0.4 * trust_two) / 2

        if trust_two < 60:
            trust = trust_two
        elif trust_one > 100:
            trust = 100

        if 0 <= trust <= 100:
            # retourne la trust si elle répond aux critères
            return trust

        # retourne faux si la trust calculée ne répond pas aux critères
        return False


    # fonction qui calcule et retourne la trust 1 d'un utilisateur
    def compute_trust_one(self, user_id):

        # recupere la date du dernier message vu
        date_of_last_seen_message = self.crud.get_user_data(
            user_id, "Date_of_last_seen_message")
        # convertit la date en unix
        date_of_last_seen_message_unix = self.crud.convert_to_unix(
            date_of_last_seen_message)

        # recupere la date du premier message vu
        date_of_first_seen_message = self.crud.get_user_data(
            user_id, "Date_of_first_seen_message")
        # convertit la date en unix
        date_of_first_seen_message_unix = self.crud.convert_to_unix(
            date_of_first_seen_message)

        # retourne le nombre de mails non-spam
        ham_n = self.crud.get_user_data(user_id, "HamN")
        # retourne le nombre de mails spam
        spam_n = self.crud.get_user_data(user_id, "SpamN")

        # calcule et retourne la trust 1 selon la formule donnée dans l'énoncé
        print((date_of_last_seen_message_unix * ham_n) / (date_of_first_seen_message_unix * (ham_n + spam_n)))
        return (date_of_last_seen_message_unix * ham_n) / (date_of_first_seen_message_unix * (ham_n + spam_n))


    # fonction qui calcule et retourne la trust 2 pour un utilisateur
    def compute_trust_two(self, user_id):
        # retourne la liste des noms des groupes auxquels appartient l'utilisateur
        user_groups_names = self.crud.get_user_data(user_id, "Groups")

        # somme des trusts des groupes de l'utilisateur
        trust_sum = 0
        # nombre de groupes auxquels appartient l'utilisateur
        number_of_groups = 0
        # parcourt chaque groupe de l'utilisateur
        for group_name in user_groups_names:

            # recupere l'id du groupe à partir de son nom
            group_id = self.crud.get_group_id(group_name)
            # recupere la trust du groupe
            group_trust = self.crud.get_groups_data(group_id, "Trust")

            trust_sum += group_trust
            number_of_groups = number_of_groups + 1

        # calcule et retourne la trust 2
        return trust_sum / number_of_groups