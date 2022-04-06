import json
import random
import copy
from vocabulary_creator import VocabularyCreator
from renege import RENEGE
from email_analyzer import EmailAnalyzer
from text_cleaner import TextCleaning


def cleaner(fileName):
    with open("./JsonFiles/"+ fileName + "_set.json") as email_file:
        emails = json.load(email_file)

    textCleaner = TextCleaning()

    for index, e_mail in enumerate(emails["dataset"]):
        emails["dataset"][index]["mail"]["Body"] = ' '.join(textCleaner.clean_text(e_mail["mail"]["Body"]))

    with open("./JsonFiles/"+ fileName + "_clean.json", "w") as outfile:
        json.dump(emails, outfile, indent=2)

def shuffle(fileName):
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

def triplage(fileName):
    with open("./JsonFiles/"+ fileName + "_set.json") as email_file:
        emails = json.load(email_file)

    tmp = copy.deepcopy(emails)
    emails["dataset"] += emails["dataset"]
    emails["dataset"] += tmp["dataset"]

    with open("./JsonFiles/"+ fileName + "_triplicate.json", "w") as outfile:
        json.dump(emails, outfile, indent=2)

def duplicate(fileName) :
    with open("./JsonFiles/"+ fileName + "_set.json") as email_file:
        emails = json.load(email_file)

    for index, e_mail in enumerate(emails["dataset"]):
        body = e_mail["mail"]["Body"]
        bodyArray = body + body
        emails["dataset"][index]["mail"]["Body"] = bodyArray
    
    with open("./JsonFiles/"+ fileName + "_words.json", "w") as outfile:
        json.dump(emails, outfile, indent=2)


def evaluate(fileName):
    tp = 0
    tn = 0
    fp = 0
    fn = 0
    total = 0
    analyzer = EmailAnalyzer()
    with open("./JsonFiles/" + fileName + ".json") as email_file:
        new_emails = json.load(email_file)

    i = 0
    email_count = len(new_emails["dataset"])

    # print("Evaluating emails ")
    for e_mail in new_emails["dataset"]:
        i += 1
        # print("\rEmail " + str(i) + "/" + str(email_count), end="")

        new_email = e_mail["mail"]
        subject = new_email["Subject"]
        body = new_email["Body"]
        spam = new_email["Spam"]

        if ((analyzer.is_spam(subject, body))) and (spam == "true"):
            tp += 1
        if (not (analyzer.is_spam(subject, body))) and (spam == "false"):
            tn += 1
        if ((analyzer.is_spam(subject, body))) and (spam == "false"):
            fp += 1
        if (not (analyzer.is_spam(subject, body))) and (spam == "true"):
            fn += 1
        total += 1
    
    print("")
    # print("\nAccuracy: ", round((tp + tn) / (tp + tn + fp + fn), 2))
    precision = round(tp / (tp + fp), 2)
    recall = round(tp / (tp + fn), 2)
    print("Precision: ", precision)
    print("Recall: ", recall)
    print("F1 score: ", f1(precision, recall))
    return True

def runApp(file1, file2):
    vocab = VocabularyCreator(file1)
    vocab.create_vocab()
    renege = RENEGE(file1)
    renege.classify_emails()
    evaluate(file2)

def f1(precision, recall):
    return 2 * (precision * recall) / (precision + recall)

if __name__ == "__main__":

    # # 1. Creation de vocabulaire.
    # vocab = VocabularyCreator()
    # vocab.create_vocab()

    # # 2. Classification des emails et initialisation des utilisateurs et des groupes.
    # renege = RENEGE()
    # renege.classify_emails()

    # #3. Evaluation de performance du modele avec la fonction evaluate()
    # evaluate("test_set")

    fileName = ["test", "train"]
    for file in fileName :
        cleaner(file)
        shuffle(file)
        triplage(file)
        duplicate(file)
    
    fileType = ["clean", "shuffle", "words", "triplicate"]
    for file in fileName :
        for type in fileType :
            fileName = file + '_' + type
            default = file + "_set"

            # print(default)

            vocab = VocabularyCreator(default)
            vocab.create_vocab()
            renege = RENEGE(default)
            renege.classify_emails()

            # runApp(default, default)

            print(fileName)

            if file == "train":
                runApp(fileName, "test_set")
            else:
                runApp("train_set", fileName)

            print("\n")
