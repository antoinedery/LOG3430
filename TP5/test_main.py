import unittest
from main import evaluate
import json
import random
import copy
from text_cleaner import TextCleaning
from vocabulary_creator import VocabularyCreator
from renege import RENEGE

class TestMain(unittest.TestCase):
    def cleaner(self, fileName):
        with open("./JsonFiles/"+ fileName + "_set.json") as email_file:
            emails = json.load(email_file)

        textCleaner = TextCleaning()

        for index, e_mail in enumerate(emails["dataset"]):
            emails["dataset"][index]["mail"]["Body"] = ' '.join(textCleaner.clean_text(e_mail["mail"]["Body"]))

        with open("./JsonFiles/"+ fileName + "_clean.json", "w") as outfile:
            json.dump(emails, outfile, indent=2)

    def shuffle(self, fileName):
        with open("./JsonFiles/"+ fileName + "_set.json") as email_file:
            emails = json.load(email_file)

        for index, e_mail in enumerate(emails["dataset"]):
            bodyArray = e_mail["mail"]["Body"].split(' ')
            for i in range(9) :
                var1 = random.randint(0, len(bodyArray) - 1)
                var2 = random.randint(0, len(bodyArray) - 1)
                tmp = bodyArray[var1] 
                bodyArray[var1] = bodyArray[var2]
                bodyArray[var2] = tmp
            emails["dataset"][index]["mail"]["Body"] = ' '.join(bodyArray)

        with open("./JsonFiles/"+ fileName + "_shuffle.json", "w") as outfile:
            json.dump(emails, outfile, indent=2)

    def triplage(self, fileName):
        with open("./JsonFiles/"+ fileName + "_set.json") as email_file:
            emails = json.load(email_file)

        tmp = copy.deepcopy(emails)
        emails["dataset"] += emails["dataset"]
        emails["dataset"] += tmp["dataset"]

        with open("./JsonFiles/"+ fileName + "_triplicate.json", "w") as outfile:
            json.dump(emails, outfile, indent=2)

    def duplicate(self, fileName) :
        with open("./JsonFiles/"+ fileName + "_set.json") as email_file:
            emails = json.load(email_file)

        for index, e_mail in enumerate(emails["dataset"]):
            body = e_mail["mail"]["Body"]
            bodyArray = body + body
            emails["dataset"][index]["mail"]["Body"] = bodyArray
        
        with open("./JsonFiles/"+ fileName + "_words.json", "w") as outfile:
            json.dump(emails, outfile, indent=2)

    def setUp(self):
        fileName = ["test", "train"]
        for file in fileName:
            self.cleaner(file)
            self.shuffle(file)
            self.triplage(file)
            self.duplicate(file)

    def test_test_clean(self):
        print("")
        print("Test_test_clean")
        vocab = VocabularyCreator("train_set")
        vocab.create_vocab()
        renege = RENEGE("train_set")
        renege.classify_emails()

        f1_initial=evaluate("test_set")
        f1_final=evaluate("test_clean")
        print("F1 initial : " + str(f1_initial))
        print("F1 final : " + str(f1_final))
        self.assertTrue(((f1_initial / f1_final) < 1.03) and ((f1_initial / f1_final) > 0.97))
    
    def test_test_shuffle(self):
        print("")
        print("Test_test_shuffle")
        vocab = VocabularyCreator("train_set")
        vocab.create_vocab()
        renege = RENEGE("train_set")
        renege.classify_emails()

        f1_initial=evaluate("test_set")
        f1_final=evaluate("test_shuffle")
        print("F1 initial : " + str(f1_initial))
        print("F1 final : " + str(f1_final))
        self.assertTrue(((f1_initial / f1_final) < 1.03) and ((f1_initial / f1_final) > 0.97))
    
    def test_test_triplicate(self):
        print("")
        print("Test_test_triplicate")
        vocab = VocabularyCreator("train_set")
        vocab.create_vocab()
        renege = RENEGE("train_set")
        renege.classify_emails()

        f1_initial=evaluate("test_set")
        f1_final=evaluate("test_triplicate")
        print("F1 initial : " + str(f1_initial))
        print("F1 final : " + str(f1_final))
        self.assertTrue(((f1_initial / f1_final) < 1.03) and ((f1_initial / f1_final) > 0.97))

    def test_test_words(self):
        print("")
        print("Test_test_words")
        vocab = VocabularyCreator("train_set")
        vocab.create_vocab()
        renege = RENEGE("train_set")
        renege.classify_emails()

        f1_initial=evaluate("test_set")
        f1_final=evaluate("test_words")
        print("F1 initial : " + str(f1_initial))
        print("F1 final : " + str(f1_final))
        self.assertTrue(((f1_initial / f1_final) < 1.03) and ((f1_initial / f1_final) > 0.97))

    def test_train_clean(self):
        print("")
        print("Test_train_clean")

        vocab = VocabularyCreator("train_set")
        vocab.create_vocab()
        renege = RENEGE("train_set")
        renege.classify_emails()
        f1_initial=evaluate("test_set")

        vocab = VocabularyCreator("train_clean")
        vocab.create_vocab()
        renege = RENEGE("train_clean")
        renege.classify_emails()
        f1_final=evaluate("test_set")

        print("Test_train_clean")
        print("F1 initial : " + str(f1_initial))
        print("F1 final : " + str(f1_final))
        self.assertTrue(((f1_initial / f1_final) < 1.03) and ((f1_initial / f1_final) > 0.97))

    def test_train_shuffle(self):
        print("")
        print("Test_train_shuffle")
        
        vocab = VocabularyCreator("train_set")
        vocab.create_vocab()
        renege = RENEGE("train_set")
        renege.classify_emails()
        f1_initial=evaluate("test_set")

        vocab = VocabularyCreator("train_shuffle")
        vocab.create_vocab()
        renege = RENEGE("train_shuffle")
        renege.classify_emails()
        f1_final=evaluate("test_set")

        print("F1 initial : " + str(f1_initial))
        print("F1 final : " + str(f1_final))
        self.assertTrue(((f1_initial / f1_final) < 1.03) and ((f1_initial / f1_final) > 0.97))

    def test_train_triplicate(self):
        print("")
        print("Test_train_triplicate")

        vocab = VocabularyCreator("train_set")
        vocab.create_vocab()
        renege = RENEGE("train_set")
        renege.classify_emails()
        f1_initial=evaluate("test_set")

        vocab = VocabularyCreator("train_triplicate")
        vocab.create_vocab()
        renege = RENEGE("train_triplicate")
        renege.classify_emails()
        f1_final=evaluate("test_set")

        print("F1 initial : " + str(f1_initial))
        print("F1 final : " + str(f1_final))
        self.assertTrue(((f1_initial / f1_final) < 1.03) and ((f1_initial / f1_final) > 0.97))

    def test_train_words(self):
        print("")
        print("Test_train_words")

        vocab = VocabularyCreator("train_set")
        vocab.create_vocab()
        renege = RENEGE("train_set")
        renege.classify_emails()
        f1_initial=evaluate("test_set")

        vocab = VocabularyCreator("train_words")
        vocab.create_vocab()
        renege = RENEGE("train_words")
        renege.classify_emails()
        f1_final=evaluate("test_set")

        print("F1 initial : " + str(f1_initial))
        print("F1 final : " + str(f1_final))
        self.assertTrue(((f1_initial / f1_final) < 1.03) and ((f1_initial / f1_final) > 0.97))