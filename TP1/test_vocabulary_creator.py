from vocabulary_creator import VocabularyCreator
import unittest
from unittest.mock import patch

class TestVocabularyCreator(unittest.TestCase):
    def setUp(self):
        self.mails = {
            "dataset": [
                {
                "mail": {
                    "Subject": "LOG3430 - TP1",
                    "From": "charges-log3430@polymtl.ca",
                    "Date": "2022-01-27",
                    "Body": "Le TP1 est disponible sur Moodle.",
                    "Spam": "false",
                    "File": "enronds//enron4/spam/4536.2005-03-04.GP.spam.txt"
                }
                },
                {
                "mail": {
                    "Subject": "[poly-communaute]  LOG3430 PAVILLON J.-A. BOMBARDIER_Avis d'interruption_Ventilation",
                    "From": "sdi@polymtl.ca",
                    "Date": "2022-01-27",
                    "Body": "Aucun étudiant étudiant ne va lire ce courriel.",
                    "Spam": "true",
                    "File": "enronds//enron4/spam/0559.2004-03-09.GP.spam.txt"
                }
            }]
        } # données pour mocker "return_value" du "load_dict"
        self.clean_subject_spam = ['log','log']  # données pour mocker "return_value" du "clean_text"
        self.vocab_expected = {'p_sub_spam': {'log': 1.0}, 'p_sub_ham': {'log': 1.0}, 'p_body_spam': {'log': 1.0}, 'p_body_ham': {'log': 1.0}}  # vocabulaire avec les valeurs de la probabilité calculées correctement

    def tearDown(self):
        pass

    @patch("vocabulary_creator.VocabularyCreator.load_dict")
    @patch("vocabulary_creator.VocabularyCreator.clean_text")
    @patch("vocabulary_creator.VocabularyCreator.write_data_to_vocab_file")
    def test_create_vocab_spam_Returns_vocabulary_with_correct_values(
        self, mock_write_data_to_vocab_file, mock_clean_text, mock_load_dict
    ):
        """Description: Tester qu'un vocabulaire avec les probabilités calculées
        correctement va être retourné. Il faut mocker les fonctions "load dict"
         (utiliser self.mails comme une simulation de valeur de retour),"clean text"
         (cette fonction va être appelée quelques fois, pour chaque appel on
         va simuler une valeur de retour differente, pour cela il faut utiliser
         side_effect (voir l'exemple dans l'énonce)) et
         "write_data_to_vocab_file" qui va simuler "return True" au lieu
         d'écrire au fichier "vocabulary.json".
         if faut utiliser self.assertEqual(appel_a_create_vocab(), self.vocab_expected)
        """
        mock_load_dict.return_value = self.mails
        # def side_effect(self):
        #     return self.clean_subject_spam.pop()
        # mock_clean_text.side_effect = side_effect
        mock_clean_text.return_value = self.clean_subject_spam
        mock_write_data_to_vocab_file.return_value = True
        vocabCreator = VocabularyCreator()
        self.assertEqual(vocabCreator.create_vocab(), self.vocab_expected)
    
    ###########################################
    #               CUSTOM TEST               #
    ###########################################