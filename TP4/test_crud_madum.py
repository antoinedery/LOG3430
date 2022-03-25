from crud import CRUD

import unittest
from unittest.mock import patch

class TestCRUD_MADUM(unittest.TestCase):
    def setUp(self):
        self.group_data_1 = {
            "name": "name_1", 
            "Trust": 0, 
            "List_of_members": []
        }

############################# add_new_group #############################

    @patch("crud.CRUD.modify_groups_file")
    def test_d1(self, mock_modify_groups_file):
        crud = CRUD()
        crud.add_new_group("", 0, [])
        crud.remove_group(1)
        crud.remove_group_member(1, "")
        crud.update_groups(1, "", "")
        self.assertEqual(crud.get_groups_data(1, ""), False)

    @patch("crud.CRUD.modify_groups_file")
    def test_d2(self, mock_modify_groups_file):
        crud = CRUD()
        crud.add_new_group("", 0, [])
        crud.remove_group(1)
        crud.update_groups(1, "", "")
        crud.remove_group_member(1, "")
        self.assertEqual(crud.get_groups_data(1, ""), False)

    @patch("crud.CRUD.modify_groups_file")
    def test_d3(self, mock_modify_groups_file):
        crud = CRUD()
        crud.add_new_group("", 0, [])
        crud.remove_group_member(1, "")
        crud.remove_group(1)
        crud.update_groups(1, "", "")
        self.assertEqual(crud.get_groups_data(1, ""), False)

    @patch("crud.CRUD.modify_groups_file")
    def test_d4(self, mock_modify_groups_file):
        crud = CRUD()
        crud.add_new_group("", 0, [])
        crud.remove_group_member(1, "")
        crud.update_groups(1, "", "")
        crud.remove_group(1)
        self.assertEqual(crud.get_groups_data(1, ""), False)

    @patch("crud.CRUD.modify_groups_file")
    def test_d5(self, mock_modify_groups_file):
        crud = CRUD()
        crud.add_new_group("", 0, [])
        crud.update_groups(1, "", "")
        crud.remove_group(1)
        crud.remove_group_member(1, "")
        self.assertEqual(crud.get_groups_data(1, ""), False)

    @patch("crud.CRUD.modify_groups_file")
    def test_d6(self, mock_modify_groups_file):
        crud = CRUD()
        crud.add_new_group("", 0, [])
        crud.update_groups(1, "", "")
        crud.remove_group_member(1, "")
        crud.remove_group(1)
        self.assertEqual(crud.get_groups_data(1, ""), False)

    @patch("crud.CRUD.modify_groups_file")
    @patch("crud.CRUD.modify_users_file")
    def test_d7(self, mock_modify_users_file, mock_modify_groups_file):
        crud = CRUD()

        crud.remove_group(1)
        crud.add_new_group("", 0, ["user@email.ca"])
        crud.remove_group_member(1, "user@email.ca")
        crud.update_groups(1, "name", "name_1")

        self.assertEqual(crud.get_groups_data(1, "name"), "name_1")
        self.assertEqual(crud.get_groups_data(1, "List_of_members"), [])

    @patch("crud.CRUD.modify_groups_file")
    @patch("crud.CRUD.modify_users_file")
    def test_d8(self, mock_modify_users_file, mock_modify_groups_file):
        crud = CRUD()

        crud.remove_group(1)
        crud.add_new_group("", 0, ["user@email.ca"])
        crud.update_groups(1, "name", "name_1")
        crud.remove_group_member(1, "user@email.ca")
        
        self.assertEqual(crud.get_groups_data(1, "name"), "name_1")
        self.assertEqual(crud.get_groups_data(1, "List_of_members"), [])

    @patch("crud.CRUD.modify_groups_file")
    @patch("crud.CRUD.modify_users_file")
    def test_d9(self, mock_modify_users_file, mock_modify_groups_file):
        crud = CRUD()

        crud.remove_group(1)
        crud.remove_group_member(1, "user@email.ca")
        crud.add_new_group("", 0, ["user@email.ca"])
        crud.update_groups(1, "name", "name_1")
        
        self.assertEqual(crud.get_groups_data(1, "name"), "name_1")
        self.assertEqual(crud.get_groups_data(1, "List_of_members"), ["user@email.ca"])

    @patch("crud.CRUD.modify_groups_file")
    @patch("crud.CRUD.modify_users_file")
    def test_d10(self, mock_modify_users_file, mock_modify_groups_file):
        crud = CRUD()

        crud.remove_group(1)
        crud.remove_group_member(1, "user@email.ca")
        crud.update_groups(1, "name", "name_1")
        crud.add_new_group("", 0, ["user@email.ca"])
        
        self.assertEqual(crud.get_groups_data(1, "name"), "")
        self.assertEqual(crud.get_groups_data(1, "List_of_members"), ["user@email.ca"])

    @patch("crud.CRUD.modify_groups_file")
    @patch("crud.CRUD.modify_users_file")
    def test_d11(self, mock_modify_users_file, mock_modify_groups_file):
        crud = CRUD()

        crud.remove_group(1)
        crud.update_groups(1, "name", "name_1")
        crud.add_new_group("", 0, ["user@email.ca"])
        crud.remove_group_member(1, "user@email.ca")
        
        self.assertEqual(crud.get_groups_data(1, "name"), "")
        self.assertEqual(crud.get_groups_data(1, "List_of_members"), [])

    @patch("crud.CRUD.modify_groups_file")
    @patch("crud.CRUD.modify_users_file")
    def test_d12(self, mock_modify_users_file, mock_modify_groups_file):
        crud = CRUD()

        crud.remove_group(1)
        crud.update_groups(1, "name", "name_1")
        crud.remove_group_member(1, "user@email.ca")
        crud.add_new_group("", 0, ["user@email.ca"])
        
        self.assertEqual(crud.get_groups_data(1, "name"), "")
        self.assertEqual(crud.get_groups_data(1, "List_of_members"), ["user@email.ca"])

    @patch("crud.CRUD.modify_groups_file")
    @patch("crud.CRUD.modify_users_file")
    def test_d13(self, mock_modify_users_file, mock_modify_groups_file):
        crud = CRUD()

        crud.remove_group_member(1, "user@email.ca")
        crud.add_new_group("", 0, ["user@email.ca"])
        crud.remove_group(1)
        crud.update_groups(1, "name", "name_1")
        
        self.assertEqual(crud.get_groups_data(1, ""), False)

    @patch("crud.CRUD.modify_groups_file")
    @patch("crud.CRUD.modify_users_file")
    def test_d14(self, mock_modify_users_file, mock_modify_groups_file):
        crud = CRUD()

        crud.remove_group_member(1, "user@email.ca")
        crud.add_new_group("", 0, ["user@email.ca"])
        crud.update_groups(1, "name", "name_1")
        crud.remove_group(1)
        
        self.assertEqual(crud.get_groups_data(1, ""), False)


    @patch("crud.CRUD.modify_groups_file")
    @patch("crud.CRUD.modify_users_file")
    def test_d15(self, mock_modify_users_file, mock_modify_groups_file):
        crud = CRUD()

        crud.remove_group_member(1, "user@email.ca")
        crud.remove_group(1)
        crud.add_new_group("", 0, ["user@email.ca"])
        crud.update_groups(1, "name", "name_1")
        
        self.assertEqual(crud.get_groups_data(1, "name"), "name_1")
        self.assertEqual(crud.get_groups_data(1, "List_of_members"), ["user@email.ca"])

    @patch("crud.CRUD.modify_groups_file")
    @patch("crud.CRUD.modify_users_file")
    def test_d16(self, mock_modify_users_file, mock_modify_groups_file):
        crud = CRUD()

        crud.remove_group_member(1, "user@email.ca")
        crud.remove_group(1)
        crud.update_groups(1, "name", "name_1")
        crud.add_new_group("", 0, ["user@email.ca"])
        
        self.assertEqual(crud.get_groups_data(1, "name"), "")
        self.assertEqual(crud.get_groups_data(1, "List_of_members"), ["user@email.ca"])

    @patch("crud.CRUD.modify_groups_file")
    @patch("crud.CRUD.modify_users_file")
    def test_d17(self, mock_modify_users_file, mock_modify_groups_file):
        crud = CRUD()

        crud.remove_group_member(1, "user@email.ca")
        crud.update_groups(1, "name", "name_1")
        crud.add_new_group("", 0, ["user@email.ca"])
        crud.remove_group(1)
        
        self.assertEqual(crud.get_groups_data(1, ""), False)

    @patch("crud.CRUD.modify_groups_file")
    @patch("crud.CRUD.modify_users_file")
    def test_d18(self, mock_modify_users_file, mock_modify_groups_file):
        crud = CRUD()

        crud.remove_group_member(1, "user@email.ca")
        crud.update_groups(1, "name", "name_1")
        crud.remove_group(1)
        crud.add_new_group("", 0, ["user@email.ca"])
        
        self.assertEqual(crud.get_groups_data(1, ""), False)

    @patch("crud.CRUD.modify_groups_file")
    @patch("crud.CRUD.modify_users_file")
    def test_d19(self, mock_modify_users_file, mock_modify_groups_file):
        crud = CRUD()

        crud.update_groups(1, "name", "name_1")
        crud.add_new_group("", 0, ["user@email.ca"])
        crud.remove_group(1)
        crud.remove_group_member(1, "user@email.ca")
        
        self.assertEqual(crud.get_groups_data(1, ""), False)

    @patch("crud.CRUD.modify_groups_file")
    @patch("crud.CRUD.modify_users_file")
    def test_d20(self, mock_modify_users_file, mock_modify_groups_file):
        crud = CRUD()

        crud.update_groups(1, "name", "name_1")
        crud.add_new_group("", 0, ["user@email.ca"])
        crud.remove_group_member(1, "user@email.ca")
        crud.remove_group(1)
        
        self.assertEqual(crud.get_groups_data(1, ""), False)

    @patch("crud.CRUD.modify_groups_file")
    @patch("crud.CRUD.modify_users_file")
    def test_d21(self, mock_modify_users_file, mock_modify_groups_file):
        crud = CRUD()

        crud.update_groups(1, "name", "name_1")
        crud.remove_group(1)
        crud.add_new_group("", 0, ["user@email.ca"])
        crud.remove_group_member(1, "user@email.ca")
        
        self.assertEqual(crud.get_groups_data(1, "name"), "")
        self.assertEqual(crud.get_groups_data(1, "List_of_members"), [])

    @patch("crud.CRUD.modify_groups_file")
    @patch("crud.CRUD.modify_users_file")
    def test_d22(self, mock_modify_users_file, mock_modify_groups_file):
        crud = CRUD()

        crud.update_groups(1, "name", "name_1")
        crud.remove_group(1)
        crud.remove_group_member(1, "user@email.ca")
        crud.add_new_group("", 0, ["user@email.ca"])
        
        self.assertEqual(crud.get_groups_data(1, "name"), "")
        self.assertEqual(crud.get_groups_data(1, "List_of_members"), ["user@email.ca"])

    @patch("crud.CRUD.modify_groups_file")
    @patch("crud.CRUD.modify_users_file")
    def test_d23(self, mock_modify_users_file, mock_modify_groups_file):
        crud = CRUD()

        crud.update_groups(1, "name", "name_1")
        crud.remove_group_member(1, "user@email.ca")
        crud.add_new_group("", 0, ["user@email.ca"])
        crud.remove_group(1)
        
        self.assertEqual(crud.get_groups_data(1, "name"), False)
        self.assertEqual(crud.get_groups_data(1, "List_of_members"), False)


    @patch("crud.CRUD.modify_groups_file")
    @patch("crud.CRUD.modify_users_file")
    def test_d24(self, mock_modify_users_file, mock_modify_groups_file):
        crud = CRUD()

        crud.update_groups(1, "name", "name_1")
        crud.remove_group_member(1, "user@email.ca")
        crud.remove_group(1)
        crud.add_new_group("", 0, ["user@email.ca"])
    
        self.assertEqual(crud.get_groups_data(1, "name"), "")
        self.assertEqual(crud.get_groups_data(1, "List_of_members"), ["user@email.ca"])