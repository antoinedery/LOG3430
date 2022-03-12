import json
import os
from text_cleaner import TextCleaning


class VocabularyCreator:
    """Class for creating vocabulary of spam and non-spam messages"""

    def __init__(self):
        self.train_set = "train_set.json"
        self.cleaning = TextCleaning()
        self.vocabulary = "vocabulary.json"
        self.voc_data = {}

    def compute_proba(self, data, total):
        '''
        Description: calcule la probabilité de chaque mot du dictionnaire basé sur
        sa fréquence d'occurrence
        Sortie: le dictionnaire des probabilités pour chaque mot
        '''
        proba_dict = {}
        for wd in data:
            proba_dict[wd] = data[wd] / total

        return proba_dict

    def create_vocab(self, frequency, stemming_disable):
        '''
        Description: fonction pour creer le vocabulaire des mots presents
        dans les e-mails spam et ham et le sauvegarder dans le fichier
        vocabulary.json selon le format specifie dans la description de lab
        Sortie: bool, 'True' pour success, 'False' dans le cas de failure.
        '''

        dataset = self.load_dict()

        #These dictionaries contains every words with their frequencies
        occ_spam_sub_temp = {}
        occ_spam_bod_temp = {}
        occ_ham_sub_temp = {}
        occ_ham_bod_temp = {}

        #These dictionaries only contains words with the desired frequency
        occ_spam_sub = {}
        occ_spam_bod = {}
        occ_ham_sub = {}
        occ_ham_bod = {}

        total_occ_spam_sub = 0
        total_occ_ham_sub = 0
        total_occ_spam_bod = 0
        total_occ_ham_bod = 0

        i = 0

        # Analyze each email
        for email in dataset["dataset"]:
            i += 1

            # Get data
            data = email["mail"]
            subject = data["Subject"]
            body = data["Body"]
            is_spam = False

            # Update the number of spams / hams
            if data["Spam"] == "true":
                is_spam = True

            # Analyze the subject
            subject = self.clean_text(subject, stemming_disable)

            if is_spam:
                for wd in subject:
                    total_occ_spam_sub += 1                      
                    # Add the word to the dictionary or update its occurence count
                    if wd not in occ_spam_sub_temp:
                        occ_spam_sub_temp[wd] = 1
                    else:
                        occ_spam_sub_temp[wd] += 1
            else:
                for wd in subject:
                    total_occ_ham_sub += 1
                    # Add the word to the dictionary or update its occurence count
                    if wd not in occ_ham_sub_temp:
                        occ_ham_sub_temp[wd] = 1
                    else:
                        occ_ham_sub_temp[wd] += 1

            # Analyze the body
            body = self.clean_text(body, stemming_disable)
            if is_spam:
                for wd in body:
                    total_occ_spam_bod += 1
                    # Add the word to the dictionary or update its occurence count
                    if wd not in occ_spam_bod_temp :
                        occ_spam_bod_temp [wd] = 1
                    else:
                        occ_spam_bod_temp [wd] += 1
            else:
                for wd in body:
                    total_occ_ham_bod += 1
                    # Add the word to the dictionary or update its occurence count
                    if wd not in occ_ham_bod_temp:
                        occ_ham_bod_temp[wd] = 1
                    else:
                        occ_ham_bod_temp[wd] += 1

        #Add words that have the desired frequency in the dictionary
        for key in occ_spam_sub_temp:
            if(occ_spam_sub_temp[key] >= frequency):
                occ_spam_sub[key] = occ_spam_sub_temp[key]
        
        for key in occ_ham_sub_temp:
            if(occ_ham_sub_temp[key] >= frequency):
                occ_ham_sub[key] = occ_ham_sub_temp[key]

        for key in occ_spam_bod_temp:
            if(occ_spam_bod_temp[key] >= frequency):
                occ_spam_bod[key] = occ_spam_bod_temp[key]
        
        for key in occ_ham_bod_temp:
            if(occ_ham_bod_temp[key] >= frequency):
                occ_ham_bod[key] = occ_ham_bod_temp[key]

        # Create the data dictionary
        p_sub_spam = self.compute_proba(occ_spam_sub, total_occ_spam_sub)
        p_sub_ham = self.compute_proba(occ_ham_sub, total_occ_ham_sub)
        p_body_spam = self.compute_proba(occ_spam_bod, total_occ_spam_bod)
        p_body_ham = self.compute_proba(occ_ham_bod, total_occ_ham_bod)

        self.voc_data = {
            "p_sub_spam": p_sub_spam,
            "p_sub_ham": p_sub_ham,
            "p_body_spam": p_body_spam,
            "p_body_ham": p_body_ham
        }

        # Save data
        self.write_data_to_vocab_file(self.voc_data)

        #print("\n")
        return self.voc_data

    def load_dict(self): #pragma: no cover
        with open(self.train_set) as json_data:
            data_dict = json.load(json_data)
        return data_dict

    def write_data_to_vocab_file(self, vocab): #pragma: no cover
        try:
            with open(self.vocabulary, "w") as outfile:
                json.dump(vocab, outfile, indent=4)
                # print("Vocab created")
                return True
        except:
            return False

    def clean_text(self, text, stemming_disable): #pragma: no cover
        return self.cleaning.clean_text(text, stemming_disable)
