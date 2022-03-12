import csv
import json

from email_analyzer import EmailAnalyzer
from renege import RENEGE
from vocabulary_creator import VocabularyCreator


def evaluate(log_calculate, log_combine, stemming_disable): #pragma: no cover
    tp = 0
    tn = 0
    fp = 0
    fn = 0
    total = 0
    analyzer = EmailAnalyzer()
    with open("test_set.json") as email_file:
        new_emails = json.load(email_file)

    i = 0
    email_count = len(new_emails["dataset"])

    #print("Evaluating emails...")
    for e_mail in new_emails["dataset"]:
        i += 1
        print("\rEmail " + str(i) + "/" + str(email_count), end="")

        new_email = e_mail["mail"]
        subject = new_email["Subject"]
        body = new_email["Body"]
        spam = new_email["Spam"]

        if ((analyzer.is_spam(subject, body, log_calculate, log_combine, stemming_disable))) and (spam == "true"):
            tp += 1
        if (not (analyzer.is_spam(subject, body, log_calculate, log_combine, stemming_disable))) and (spam == "false"):
            tn += 1
        if ((analyzer.is_spam(subject, body, log_calculate, log_combine, stemming_disable))) and (spam == "false"):
            fp += 1
        if (not (analyzer.is_spam(subject, body, log_calculate, log_combine, stemming_disable))) and (spam == "true"):
            fn += 1
        total += 1

    print("")
    #Added to prevent division by 0 if all parameters are 0
    if(((tp + tn + fp + fn) > 0) and ((tp + fp) > 0) and ((tp+fn) > 0)):
        print("\nAccuracy: ", round((tp + tn) / (tp + tn + fp + fn), 2))
        print("Precision: ", round(tp / (tp + fp), 2))
        print("Recall: ", round(tp / (tp + fn), 2))
    else:
        print("\nAccuracy: ", 0.0)
        print("Precision: ", 0.0)
        print("Recall: ",  0.0)
    
    print("")

    return True

def read_csv_file():
    with open('TP3-output.csv') as csv_file:
        csv_reader = list(csv.reader(csv_file, delimiter=','))
      
        coveringArray = []
        for row in csv_reader:
            if(row[0].startswith('true') or row[0].startswith('false')):
                coveringArray.append(row)
    return coveringArray

def string_to_boolean(string):
    if string.upper() == 'TRUE':
        return True
    elif string.upper() == 'FALSE':
        return False
    else:
        raise ValueError


if __name__ == "__main__":

    coveringArray = read_csv_file()
    for row in coveringArray:

        log_calculate = string_to_boolean(row[0])
        log_combine = string_to_boolean(row[1])
        frequency = int(row[2])
        stemming_disable = string_to_boolean(row[3])

        print(log_calculate, log_combine, frequency, stemming_disable)

        # 1. Creation de vocabulaire.
        vocab = VocabularyCreator()
        vocab.create_vocab(frequency, stemming_disable)

        # 2. Classification des emails et initialisation des utilisateurs et des groupes.
        renege = RENEGE()
        renege.classify_emails(log_calculate, log_combine, stemming_disable)

        #3. Evaluation de performance du modele avec la fonction evaluate()
        evaluate(log_calculate, log_combine, stemming_disable)

        #4. Question 2 du laboratoire1
        renege.print_trust_of_users()
