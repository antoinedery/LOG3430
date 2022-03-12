import json

from email_analyzer import EmailAnalyzer

import unittest
from unittest.mock import patch


class TestEmailAnalyzer(unittest.TestCase):
    def setUp(self):
        self.subject = "TEST-SUBJECT"
        self.body = "TEST-BODY"
        self.clean_subject = []  # données pour mocker "return_value" du "clean_text"
        self.clean_body = []  # données pour mocker "return_value" du "clean_text"
        self.spam_ham_body_prob_true = (
            2,
            1,
        )  # données pour mocker "return_value" du "spam_ham_body_prob"
        self.spam_ham_subject_prob_true = (
            2,
            1,
        )  # données pour mocker "return_value" du "subject_spam_ham_prob"
        self.spam_ham_body_prob_false = (
            1,
            2,
        )  # données pour mocker "return_value" du "spam_ham_body_prob"
        self.spam_ham_subject_prob_false = (
            1,
            2,
        )  # données pour mocker "return_value" du "subject_spam_ham_prob"
        self.vocab = {
            "p_sub_spam": {
                "abc": 0.0740625,
                "abcd": 0.03703125,
            },
            "p_sub_ham": {
                "abc": 0.0509375,
                "abcd": 0.03703125,
            },
            "p_body_spam": {
                "abc": 0.0740625,
                "abcd": 0.03703125,
            },
            "p_body_ham": {
                "abc": 0.0509375,
                "abcd": 0.02546875,
            }
        }
        # vocabulaire avec les valeurs de la probabilité pour mocker "return_value" du "load_dict"
        # valeurs des probabilités attendues pour body = "body"
        self.spam_ham_body_prob_expected_word_not_in_vocab = 0.1975, 0.1358333333333333
        self.spam_ham_body_prob_expected_word_in_vocab = 0.021941015625, 0.010378515625
        # valeurs des probabilités attendues pour subject = "sub"
        self.spam_ham_sub_prob_expected_word_not_in_vocab = 0.1975, 0.1358333333333333
        self.spam_ham_sub_prob_expected_word_in_vocab = 0.04388203125, 0.02075703125

    @patch("email_analyzer.EmailAnalyzer.clean_text")
    @patch("email_analyzer.EmailAnalyzer.spam_ham_body_prob")
    @patch("email_analyzer.EmailAnalyzer.spam_ham_subject_prob")
    def test_is_spam_Returns_True_if_spam_prob_is_higher(
        self, mock_spam_ham_subject_prob, mock_spam_ham_body_prob, mock_clean_text
    ):
        mock_spam_ham_subject_prob.return_value = self.spam_ham_subject_prob_true
        mock_spam_ham_body_prob.return_value = self.spam_ham_body_prob_true

        emailAnalyser = EmailAnalyzer()

        self.assertTrue(emailAnalyser.is_spam(self.subject, self.body))

    @patch("email_analyzer.EmailAnalyzer.clean_text")
    @patch("email_analyzer.EmailAnalyzer.spam_ham_body_prob")
    @patch("email_analyzer.EmailAnalyzer.spam_ham_subject_prob")
    def test_is_spam_Returns_False_if_spam_prob_is_lower(
        self, mock_spam_ham_subject_prob, mock_spam_ham_body_prob, mock_clean_text
    ):
        mock_spam_ham_subject_prob.return_value = self.spam_ham_subject_prob_false
        mock_spam_ham_body_prob.return_value = self.spam_ham_subject_prob_false

        emailAnalyser = EmailAnalyzer()

        self.assertFalse(emailAnalyser.is_spam(self.subject, self.body))

    @patch("email_analyzer.EmailAnalyzer.load_dict")
    def test_spam_ham_body_prob_Returns_expected_probability_when_word_is_in_voc_data(self, mock_load_dict):
        mock_load_dict.return_value = self.vocab
        emailAnalyser = EmailAnalyzer()

        self.assertEqual(emailAnalyser.spam_ham_body_prob(["abcd"]), (self.spam_ham_body_prob_expected_word_in_vocab))

    @patch("email_analyzer.EmailAnalyzer.load_dict")
    def test_subject_spam_ham_prob_Returns_expected_probability_when_word_is_in_voc_data(self, mock_load_dict):
        mock_load_dict.return_value = self.vocab
        emailAnalyser = EmailAnalyzer()
        self.assertEqual(emailAnalyser.spam_ham_subject_prob(["abc"]), (self.spam_ham_sub_prob_expected_word_in_vocab))

    ###########################################
    #               CUSTOM TEST               #
    ###########################################

    # Test pout vérifier que la fonction spam_ham_body_prob retourne la bonne valeur quand les mots du corps ne sont pas dans la liste de vocabulaire
    @patch("email_analyzer.EmailAnalyzer.load_dict")
    def test_spam_ham_body_prob_Returns_expected_probability_when_word_is_not_in_voc_data(self, mock_load_dict):
        mock_load_dict.return_value = self.vocab
        emailAnalyser = EmailAnalyzer()

        self.assertEqual(emailAnalyser.spam_ham_body_prob(["body"]), (self.spam_ham_body_prob_expected_word_not_in_vocab))

    # Test pout vérifier que la fonction spam_ham_subject_prob retourne la bonne valeur quand les mots du titre ne sont pas dans la liste de vocabulaire
    @patch("email_analyzer.EmailAnalyzer.load_dict")
    def test_spam_ham_subject_prob_Returns_expected_probability_when_word_is_not_in_voc_data(self, mock_load_dict):
        mock_load_dict.return_value = self.vocab
        emailAnalyser = EmailAnalyzer()

        self.assertEqual(emailAnalyser.spam_ham_subject_prob(["sub"]), (self.spam_ham_sub_prob_expected_word_not_in_vocab))
