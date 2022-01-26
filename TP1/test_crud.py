from crud import CRUD
import unittest
from unittest.mock import patch
import copy

import datetime


class TestCRUD(unittest.TestCase):
    def setUp(self):
        # c'est un exemple de données "mock" à utiliser comme "return value" de read_users_file
        self.users_data = {
            "1": {
                "name": "alex@gmail.com",
                "Trust": 100,
                "SpamN": 0,
                "HamN": 20,
                "Date_of_first_seen_message": 1596844800.0,
                "Date_of_last_seen_message": 1596844800.0,
                "Groups": ["default"],
            },
            "2": {
                "name": "mark@mail.com",
                "Trust": 65.45454,
                "SpamN": 171,
                "HamN": 324,
                "Date_of_first_seen_message": 1596844800.0,
                "Date_of_last_seen_message": 1596844800.0,
                "Groups": ["default"],
            }
        }
        # c'est un exemple de données "mock" à utiliser comme "return value" de read_groups_file
        self.groups_data = {
            "1": {
                "name": "default",
                "Trust": 50,
                "List_of_members": ["alex@gmail.com", "mark@mail.com"],
            },
            "2": {
                "name": "friends",
                "Trust": 90,
                "List_of_members": ["alex@gmail.com"],
            },
        }

    def tearDown(self):
        pass

    @patch("crud.CRUD.read_users_file")
    @patch("crud.CRUD.modify_groups_file")
    @patch("crud.CRUD.modify_users_file")
    def test_add_new_user_Passes_correct_data_to_modify_users_file(
            self, mock_modify_users_file, mock_modify_groups_file, mock_read_users_file
    ):
        # Ici on mock pour que read_users_file retourne la liste d'utilisateurs
        mock_read_users_file.return_value = self.users_data

        # Les informations du nouvel utilisateur
        new_user_data = {
            "name": "james@gmail.com",
            "Trust": 50,
            "SpamN": 0,
            "HamN": 0,
            "Date_of_first_seen_message": 1596844800.0,
            "Date_of_last_seen_message": 1596844800.0,
            "Groups": ["default"],
        }

        # On effectue une copie de la liste d'utilisateurs
        users_data_final = {}
        users_data_final["1"] = self.users_data["1"]
        users_data_final["2"] = self.users_data["2"]
        # On ajoute les infos du nouvel utilisateur
        users_data_final["0"] = new_user_data

        crud = CRUD()
        crud.add_new_user("james@gmail.com", "2020-08-08")
        # On vérifie que quand on ajoute un nouvel utilisateur, modify_users_file est appelée avec la nouvelle liste mise à jour
        mock_modify_users_file.assert_called_once_with(users_data_final)

    @patch("crud.CRUD.read_users_file")
    @patch("crud.CRUD.read_groups_file")
    @patch("crud.CRUD.modify_groups_file")
    def test_add_new_group_Passes_correct_data_to_modify_groups_file(
            self, mock_modify_groups_file, mock_read_groups_file, mock_read_users_file
    ):
        # Ici on mock pour que read_group_file retourne la liste d'utilisateurs du groupe
        name = "test"
        self.users_data["1"]["Groups"].append(name)

        mock_read_groups_file.return_value = self.groups_data
        mock_read_users_file.return_value = self.users_data

        member_list = ["alex@gmail.com", "mark@mail.com"]
        new_group_data = {
            "name": name,
            "Trust": 50,
            "List_of_members": member_list,
        }

        groups_data_final = {}
        groups_data_final["1"] = self.groups_data["1"]
        groups_data_final["2"] = self.groups_data["2"]
        groups_data_final["0"] = new_group_data

        crud = CRUD()
        crud.add_new_group(name, 50, member_list)

        mock_modify_groups_file.assert_called_once_with(groups_data_final)

    @patch("crud.CRUD.modify_groups_file")
    @patch("crud.CRUD.read_users_file")
    def test_get_user_data_Returns_false_for_invalid_id(self, mock_read_users_file, mock_modify_groups_file):
        mock_read_users_file.return_value = self.users_data

        crud = CRUD()
        self.assertFalse(crud.get_user_data("0", ""))

    @patch("crud.CRUD.modify_groups_file")
    @patch("crud.CRUD.read_users_file")
    def test_get_user_data_Returns_false_for_invalid_field(self, mock_read_users_file, mock_modify_groups_file):
        mock_read_users_file.return_value = self.users_data

        crud = CRUD()
        self.assertFalse(crud.get_user_data("1", ""))

    @patch("crud.CRUD.modify_groups_file")
    @patch("crud.CRUD.read_users_file")
    def test_get_user_data_Returns_correct_value_if_field_and_id_are_valid(
            self, mock_read_users_file, mock_modify_groups_file
    ):
        mock_read_users_file.return_value = self.users_data

        crud = CRUD()
        self.assertEqual(crud.get_user_data("1", "name"), "alex@gmail.com")

    @patch("crud.CRUD.modify_groups_file")
    @patch("crud.CRUD.read_groups_file")
    def test_get_group_data_Returns_false_for_invalid_id(self, mock_read_groups_file, mock_modify_groups_file):
        mock_read_groups_file.return_value = self.groups_data

        crud = CRUD()
        self.assertFalse(crud.get_groups_data("0", ""))

    @patch("crud.CRUD.modify_groups_file")
    @patch("crud.CRUD.read_groups_file")
    def test_get_group_data_Returns_false_for_invalid_field(
            self, mock_read_groups_file, mock_modify_groups_file
    ):
        mock_read_groups_file.return_value = self.groups_data

        crud = CRUD()
        self.assertFalse(crud.get_groups_data("1", ""))

    @patch("crud.CRUD.modify_groups_file")
    @patch("crud.CRUD.read_groups_file")
    def test_get_group_data_Returns_correct_value_if_field_and_id_are_valid(
            self, mock_read_groups_file, mock_modify_groups_file
    ):
        mock_read_groups_file.return_value = self.groups_data

        crud = CRUD()
        self.assertEqual(crud.get_groups_data("1", "name"), "default")

    @patch("crud.CRUD.modify_groups_file")
    @patch("crud.CRUD.read_users_file")
    def test_get_user_id_Returns_false_for_invalid_user_name(
            self, mock_read_users_file, mock_modify_groups_file
    ):
        mock_read_users_file.return_value = self.users_data

        crud = CRUD()
        self.assertFalse(crud.get_user_id(""))

    @patch("crud.CRUD.modify_groups_file")
    @patch("crud.CRUD.read_users_file")
    def test_get_user_id_Returns_id_for_valid_user_name(self, mock_read_users_file, mock_modify_groups_file):
        mock_read_users_file.return_value = self.users_data

        crud = CRUD()
        self.assertEqual(crud.get_user_id("alex@gmail.com"), "1")

    @patch("crud.CRUD.modify_groups_file")
    @patch("crud.CRUD.read_groups_file")
    def test_get_group_id_Returns_false_for_invalid_group_name(
            self, mock_read_groups_file, mock_modify_groups_file
    ):
        mock_read_groups_file.return_value = self.groups_data

        crud = CRUD()
        self.assertFalse(crud.get_group_id(""))

    @patch("crud.CRUD.modify_groups_file")
    @patch("crud.CRUD.read_groups_file")
    def test_get_group_id_Returns_id_for_valid_group_name(self, mock_read_groups_file, mock_modify_groups_file):
        mock_read_groups_file.return_value = self.groups_data

        crud = CRUD()
        self.assertEqual(crud.get_group_id("default"), "1")

    @patch("crud.CRUD.modify_groups_file")
    @patch("crud.CRUD.read_users_file")
    def test_update_users_Returns_false_for_invalid_id(
            self, mock_read_users_file, mock_modify_groups_file
    ):
        mock_read_users_file.return_value = self.users_data

        crud = CRUD()
        self.assertFalse(crud.update_users("", "", {}))

    @patch("crud.CRUD.modify_groups_file")
    @patch("crud.CRUD.read_users_file")
    def test_update_users_Returns_false_for_invalid_field(
            self, mock_read_users_file, mock_modify_groups_file
    ):
        mock_read_users_file.return_value = self.users_data

        crud = CRUD()
        self.assertFalse(crud.update_users("1", "", {}))

    @patch("crud.CRUD.modify_groups_file")
    @patch("crud.CRUD.modify_users_file")
    @patch("crud.CRUD.read_users_file")
    def test_update_users_Passes_correct_data_to_modify_users_file(
            self, mock_read_users_file, mock_modify_users_file, mock_modify_groups_file
    ):
        mock_read_users_file.return_value = self.users_data

        name = "test@gmail.com"

        users_data_final = {}
        users_data_final["1"] = self.users_data["1"]
        users_data_final["2"] = self.users_data["2"]
        users_data_final["1"]["name"] = name

        crud = CRUD()
        crud.update_users("1", "name", name)
        mock_modify_users_file.assert_called_once_with(users_data_final)

    @patch("crud.CRUD.modify_groups_file")
    @patch("crud.CRUD.read_groups_file")
    def test_update_groups_Returns_false_for_invalid_id(
            self, mock_read_groups_file, mock_modify_groups_file
    ):
        mock_read_groups_file.return_value = self.groups_data

        crud = CRUD()
        self.assertFalse(crud.update_groups("", "", {}))

    @patch("crud.CRUD.modify_groups_file")
    @patch("crud.CRUD.read_groups_file")
    def test_update_groups_Returns_false_for_invalid_field(
            self, mock_read_groups_file, mock_modify_groups_file
    ):
        mock_read_groups_file.return_value = self.groups_data

        crud = CRUD()
        self.assertFalse(crud.update_groups("1", "", {}))

    @patch("crud.CRUD.modify_groups_file")
    @patch("crud.CRUD.read_groups_file")
    def test_update_groups_Passes_correct_data_to_modify_groups_file(
            self, mock_read_groups_file, mock_modify_groups_file
    ):
        mock_read_groups_file.return_value = self.groups_data

        name = "test"
        groups_data_final = {}
        groups_data_final["1"] = self.groups_data["1"]
        groups_data_final["2"] = self.groups_data["2"]
        groups_data_final["2"]["name"] = name

        crud = CRUD()
        crud.update_groups("2", "name", name)
        mock_modify_groups_file.assert_called_with(groups_data_final)

    @patch("crud.CRUD.modify_groups_file")
    @patch("crud.CRUD.read_users_file")
    def test_remove_user_Returns_false_for_invalid_id(
            self, mock_read_users_file, mock_modify_groups_file
    ):
        mock_read_users_file.return_value = self.users_data

        crud = CRUD()
        self.assertFalse(crud.remove_user(""))

    @patch("crud.CRUD.modify_groups_file")
    @patch("crud.CRUD.modify_users_file")
    @patch("crud.CRUD.read_users_file")
    def test_remove_user_Passes_correct_value_to_modify_users_file(
            self, mock_read_users_file, mock_modify_users_file, mock_modify_groups_file
    ):
        mock_read_users_file.return_value = self.users_data

        users_data_final = {}
        users_data_final["1"] = self.users_data["1"]

        crud = CRUD()
        crud.remove_user("2")
        mock_modify_users_file.assert_called_with(users_data_final)

    @patch("crud.CRUD.modify_groups_file")
    @patch("crud.CRUD.read_users_file")
    def test_remove_user_group_Returns_false_for_invalid_id(
            self, mock_read_users_file, mock_modify_groups_file
    ):
        mock_read_users_file.return_value = self.users_data

        crud = CRUD()
        self.assertFalse(crud.remove_user_group("", "default"))

    @patch("crud.CRUD.modify_groups_file")
    @patch("crud.CRUD.read_users_file")
    def test_remove_user_group_Returns_false_for_invalid_group(
            self, mock_read_users_file, mock_modify_groups_file
    ):
        mock_read_users_file.return_value = self.users_data

        crud = CRUD()
        self.assertFalse(crud.remove_user_group("1", ""))

    @patch("crud.CRUD.modify_groups_file")
    @patch("crud.CRUD.modify_users_file")
    @patch("crud.CRUD.read_users_file")
    def test_remove_user_group_Passes_correct_value_to_modify_users_file(
            self, mock_read_users_file, mock_modify_users_file, mock_modify_groups_file
    ):
        mock_read_users_file.return_value = self.users_data

        users_data_final = {}
        users_data_final = copy.deepcopy(self.users_data)
        users_data_final["1"]["Groups"] = []

        crud = CRUD()
        crud.remove_user_group("1", "default")
        mock_modify_users_file.assert_called_with(users_data_final)

    @patch("crud.CRUD.modify_groups_file")
    @patch("crud.CRUD.read_groups_file")
    def test_remove_group_Returns_false_for_invalid_id(
            self, mock_read_groups_file, mock_modify_groups_file
    ):
        mock_read_groups_file.return_value = self.groups_data

        crud = CRUD()
        self.assertFalse(crud.remove_group(""))

    @patch("crud.CRUD.modify_groups_file")
    @patch("crud.CRUD.read_groups_file")
    def test_remove_group_Passes_correct_value_to_modify_groups_file(
            self, mock_read_groups_file, mock_modify_groups_file
    ):
        mock_read_groups_file.return_value = self.groups_data

        groups_data_final = {}
        groups_data_final["1"] = self.groups_data["1"]

        crud = CRUD()
        crud.remove_group("2")
        mock_modify_groups_file.assert_called_with(groups_data_final)

    @patch("crud.CRUD.modify_groups_file")
    @patch("crud.CRUD.read_groups_file")
    def test_remove_group_member_Returns_false_for_invalid_id(
            self, mock_read_groups_file, mock_modify_groups_file
    ):
        mock_read_groups_file.return_value = self.groups_data

        crud = CRUD()
        self.assertFalse(crud.remove_group_member("", "alex@gmail.com"))

    @patch("crud.CRUD.modify_groups_file")
    @patch("crud.CRUD.read_groups_file")
    def test_remove_group_member_Returns_false_for_invalid_group_member(
            self, mock_read_groups_file, mock_modify_groups_file
    ):
        mock_read_groups_file.return_value = self.groups_data

        crud = CRUD()
        self.assertFalse(crud.remove_group_member("1", "test@gmail.com"))

    @patch("crud.CRUD.modify_groups_file")
    @patch("crud.CRUD.read_groups_file")
    def test_remove_group_member_Passes_correct_value_to_modify_groups_file(
            self, mock_read_groups_file, mock_modify_groups_file
    ):
        mock_read_groups_file.return_value = self.groups_data

        groups_data_final = {}
        groups_data_final = copy.deepcopy(self.groups_data)
        groups_data_final["2"]["List_of_members"] = []

        crud = CRUD()
        crud.remove_group_member("2", "alex@gmail.com")
        mock_modify_groups_file.assert_called_with(groups_data_final)

    ###########################################
    #               CUSTOM TEST               #
    ###########################################
    @patch("crud.CRUD.modify_groups_file")
    @patch("crud.CRUD.read_users_file")
    def test_update_users_Returns_false_for_invalid_name(
            self, mock_read_users_file, mock_modify_groups_file
    ):
        mock_read_users_file.return_value = self.users_data

        crud = CRUD()
        self.assertFalse(crud.update_users("1", "name", "abcdef"))

    @patch("crud.CRUD.modify_groups_file")
    @patch("crud.CRUD.read_users_file")
    def test_update_users_Returns_false_for_invalid_Date_of_last_seen_message(
            self, mock_read_users_file, mock_modify_groups_file
    ):
        mock_read_users_file.return_value = self.users_data

        crud = CRUD()
        self.assertFalse(crud.update_users(
            "1", "Date_of_last_seen_message", "1900-01-01"))

    @patch("crud.CRUD.modify_groups_file")
    @patch("crud.CRUD.read_users_file")
    def test_update_users_Returns_false_for_invalid_Date_of_first_seen_message(
            self, mock_read_users_file, mock_modify_groups_file
    ):
        mock_read_users_file.return_value = self.users_data

        crud = CRUD()
        self.assertFalse(crud.update_users(
            "1", "Date_of_first_seen_message", "2022-12-31"))

    @patch("crud.CRUD.modify_groups_file")
    @patch("crud.CRUD.read_users_file")
    def test_update_users_Returns_false_for_invalid_Trust(
            self, mock_read_users_file, mock_modify_groups_file
    ):
        mock_read_users_file.return_value = self.users_data

        crud = CRUD()
        self.assertFalse(crud.update_users("1", "Trust", 101))

    @patch("crud.CRUD.modify_groups_file")
    @patch("crud.CRUD.read_users_file")
    def test_update_users_Returns_false_for_invalid_SpamN(
            self, mock_read_users_file, mock_modify_groups_file
    ):
        mock_read_users_file.return_value = self.users_data

        crud = CRUD()
        self.assertFalse(crud.update_users("1", "SpamN", -1))

    @patch("crud.CRUD.modify_groups_file")
    @patch("crud.CRUD.read_users_file")
    def test_update_users_Returns_false_for_invalid_GroupList(
            self, mock_read_users_file, mock_modify_groups_file
    ):
        mock_read_users_file.return_value = self.users_data

        crud = CRUD()
        self.assertFalse(crud.update_users("1", "Groups", "default"))
