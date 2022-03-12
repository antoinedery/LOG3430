import json
import math
from decimal import Decimal

from text_cleaner import TextCleaning


class EmailAnalyzer:
    """Classe pour classifier les e-mails comme spam ou non spam (ham)"""

    def __init__(self):
        self.vocab    = "vocabulary.json"
        self.cleaning = TextCleaning()
        self.voc_data = {}

    def is_spam(self, subject_orig, body_orig, log_calculate, log_combine, stemming_disable):
        '''
        Description: fonction pour verifier si e-mail est spam ou ham,
        en calculant les probabilites d'etre spam et ham, 
        en fonction du sujet et du texte d'email.
        Sortie: 'True' - si l'email est spam, 'False' - si email est ham.
        '''
        # Clean email's subject and body
        email_subject = self.clean_text(subject_orig, stemming_disable)
        email_body    = self.clean_text(body_orig, stemming_disable)
        # Get the spam/ham probabilities
        p_subject_spam, p_subject_ham = self.spam_ham_subject_prob(email_subject, log_calculate)
        p_body_spam,    p_body_ham    = self.spam_ham_body_prob(email_body, log_calculate)

        # Compute the merged probabilities
        if not log_combine:
            p_spam = Decimal(0.6) * p_subject_spam + Decimal(0.4) * p_body_spam
            p_ham = Decimal(0.6) * p_subject_ham + Decimal(0.4) * p_body_ham
        else:
            p_spam = Decimal(p_subject_spam).log10() * Decimal(0.6) + Decimal(p_body_spam).log10()*Decimal(0.4)
            p_spam = pow(p_spam, 10)
            p_ham =  Decimal(p_subject_ham).log10() * Decimal(0.6) + Decimal(p_body_ham).log10()*Decimal(0.4)
            p_ham = pow(p_spam, 10)  

        # Decide is the email is spam or ham
        if p_spam > p_ham:
            return True 
        else:
            return False

    def spam_ham_body_prob(self, body, log_calculate):
        '''
        Description: fonction pour calculer la probabilite
        que le 'body' d'email est spam ou ham.
        Sortie: probabilite que email body est spam, probabilite
        que email body est ham.
        '''

        if not log_calculate:
            # we initialize it to 1 because we are going to use it in multiplications
            p_spam = Decimal(1.0)
            p_ham  = Decimal(1.0)
        else:
            # we initialize it to 0 because we are going to use it in additions
            p_spam = Decimal(0.0)
            p_ham  = Decimal(0.0)
        
        voc_data = self.load_dict()
        
        # Parse the text to compute the probability
        for word in body:
            # Check the spam probability
            if word in voc_data["p_body_spam"]:
                if not log_calculate:
                    p_spam *= Decimal(voc_data["p_body_spam"][word])
                else:
                    p_spam += Decimal(voc_data["p_body_spam"][word]).log10()

            else:
                if not log_calculate:
                    p_spam *= Decimal(1.0 / (len(voc_data["p_body_spam"]) + 1.0))
                else:
                    p_spam += Decimal(1.0 / (len(voc_data["p_body_spam"]) + 1.0)).log10()
            
            # Check the ham probability
            if word in voc_data["p_body_ham"]:
                if not log_calculate:
                    p_ham *= Decimal(voc_data["p_body_ham"][word])
                else:
                    p_ham += Decimal(voc_data["p_body_ham"][word]).log10()
                    
            else:
                if not log_calculate:
                    p_ham *= Decimal(1.0 / (len(voc_data["p_body_ham"]) + 1.0))
                else:
                    p_ham += Decimal(1.0 / (len(voc_data["p_body_ham"]) + 1.0)).log10()


        if not log_calculate:
            p_spam *= Decimal(0.5925)
            p_ham *= Decimal(0.4075)
        else:
            # we raise it to the power of 10 because the formula gives us log(p_spam)
            # so, we want to remove the log (base 10) function
            p_spam += Decimal(0.5925).log10()
            p_spam = pow(p_spam, 10)
            p_ham += Decimal(0.4075).log10() 
            p_ham = pow(p_ham, 10)

        return (p_spam, p_ham)

    def spam_ham_subject_prob(self, subject, log_calculate):
        '''
        Description: fonction pour calculer la probabilite
        que le sujet d'email est spam ou ham.
        Sortie: probabilite que email subject est spam, probabilite
        que email subject est ham.
        '''
        if not log_calculate:
            # we initialize it to 1 because we are going to use it in multiplications
            p_spam = Decimal(1.0)
            p_ham  = Decimal(1.0)
        else:
            # we initialize it to 0 because we are going to use it in additions
            p_spam = Decimal(0.0)
            p_ham  = Decimal(0.0)

        voc_data = self.load_dict()

        # Walk the text to compute the probability
        for word in subject:
            # Check the spam probability
            if word in voc_data["p_sub_spam"]:
                if not log_calculate:
                    p_spam *= Decimal(voc_data["p_sub_spam"][word])
                else:
                    p_spam += Decimal(voc_data["p_sub_spam"][word]).log10()
            else:
                if not log_calculate:
                    p_spam *= Decimal(1.0 / (len(voc_data["p_sub_spam"]) + 1.0))
                else:
                    p_spam += Decimal(1.0 / (len(voc_data["p_sub_spam"]) + 1.0)).log10()
            
            # Check the ham probability
            if word in voc_data["p_sub_ham"]:
                if not log_calculate:
                    p_ham *= Decimal(voc_data["p_sub_ham"][word])
                else:
                    p_ham += Decimal(voc_data["p_sub_ham"][word]).log10()
            else:
                if not log_calculate:
                    p_ham *= Decimal(1.0 / (len(voc_data["p_sub_ham"]) + 1.0))
                else:
                    p_ham += Decimal(1.0 / (len(voc_data["p_sub_ham"]) + 1.0)).log10()

        if not log_calculate:
            p_spam *= Decimal(0.5925)
            p_ham *= Decimal(0.4075)
        else:
            # we raise it to the power of 10 because the formula gives us log(p_spam)
            # so, we want to remove the log (base 10) function
            p_spam += Decimal(0.5925).log10()
            p_spam = pow(p_spam, 10)
            p_ham += Decimal(0.4075).log10() 
            p_ham = pow(p_ham, 10)
        
        return (p_spam, p_ham)
    
    def clean_text(self, text, stemming_disable): #pragma: no cover
        return self.cleaning.clean_text(text, stemming_disable)

    def load_dict(self): #pragma: no cover
        # Open vocabulary 
        with open(self.vocab) as json_data:
            vocab = json.load(json_data)
        
        return vocab
