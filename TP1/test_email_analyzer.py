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
        self.vocab = (
            {
                "p_sub_spam": {"subspam"},
                "p_sub_ham": {"subham"},
                "p_body_spam": {"bodyspam"},
                "p_body_ham": {"bodyham"}
            }
        )  # vocabulaire avec les valeurs de la probabilité pour mocker "return_value" du "load_dict"
        self.spam_ham_body_prob_expected = 0.03703125, 0.02546875  # valeurs des probabilités attendues pour body = "body"
        self.spam_ham_subject_prob_expected = 0.0740625, 0.0509375  # valeurs des probabilités attendues pour subject = "sub"

    @patch("email_analyzer.EmailAnalyzer.clean_text")
    @patch("email_analyzer.EmailAnalyzer.spam_ham_body_prob")
    @patch("email_analyzer.EmailAnalyzer.spam_ham_subject_prob")
    def test_is_spam_Returns_True_if_spam_prob_is_higher(
        self, mock_spam_ham_subject_prob, mock_spam_ham_body_prob, mock_clean_text
    ):
        mock_spam_ham_subject_prob.return_value = self.spam_ham_subject_prob_true
        mock_spam_ham_body_prob.return_value = self.spam_ham_subject_prob_true

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
    def test_spam_ham_body_prob_Returns_expected_probability(self, mock_load_dict):
        mock_load_dict.return_value = self.vocab
        emailAnalyser = EmailAnalyzer()

        self.assertEqual(emailAnalyser.spam_ham_body_prob("body"), (self.spam_ham_body_prob_expected))


    @patch("email_analyzer.EmailAnalyzer.load_dict")
    def test_subject_spam_ham_prob_Returns_expected_probability(self, mock_load_dict):
        mock_load_dict.return_value = self.vocab
        emailAnalyser = EmailAnalyzer()
        emailAnalyser.spam_ham_subject_prob("")

        self.assertEqual(emailAnalyser.spam_ham_subject_prob("sub"), (self.spam_ham_subject_prob_expected))

    ###########################################
    #               CUSTOM TEST               #
    ###########################################
