import unittest
from time import sleep
import os
unittest.TestLoader.sortTestMethodsUsing = None


class TestCaseBase(unittest.TestCase):
    def assert_capture_config_not_found(self):
        from dnres import DnRes
        try:
            res = DnRes('configs_for_testing/foo.ini')
        except Exception as error:
            if error.args[0] != "Config file does not exist.":
                raise AssertionError("Capturing config not found error failed.")
        else:
            raise AssertionError("Capturing config not found error failed.")

    def assert_capture_config_missing_structure_section(self):
        from dnres import DnRes
        try:
            res = DnRes('configs_for_testing/wrong_config_01.ini')
        except Exception as error:
            if error.args[0] != "STRUCTURE section is missing in configuration file.":
                raise AssertionError("Capturing STRUCTURE section missing in config error failed.")
        else:
            raise AssertionError("Capturing STRUCTURE section missing in config error failed.")

    def assert_capture_structure_section_in_config_is_empty(self):
        from dnres import DnRes
        try:
            res = DnRes('configs_for_testing/wrong_config_02.ini')
        except Exception as error:
            if error.args[0] != "STRUCTURE section in configuration file is empty.":
                raise AssertionError("Capturing STRUCTURE section empty error failed.")
        else:
            raise AssertionError("Capturing STRUCTURE section empty error failed.")

    def assert_capture_database_section_is_missing_in_config(self):
        from dnres import DnRes
        try:
            res = DnRes('configs_for_testing/wrong_config_03.ini')
        except Exception as error:
            if error.args[0] != "DATABASE section is missing in configuration file.":
                raise AssertionError("Capturing DATABASE section is missing error failed.")
        else:
            raise AssertionError("Capturing DATABASE section is missing error failed.")

    def assert_capture_filename_is_missing_in_database_section(self):
        from dnres import DnRes
        try:
            res = DnRes('configs_for_testing/wrong_config_04.ini')
        except Exception as error:
            if error.args[0] != 'The key "filename" is missing in DATABASE section.':
                raise AssertionError("Capturing filename key is missing in DATABASE section error failed.")
        else:
            raise AssertionError("Capturing filename key is missing in DATABASE section error failed.")

    def assert_capture_info_section_is_missing_in_config_file(self):
        from dnres import DnRes
        try:
            res = DnRes('configs_for_testing/wrong_config_05.ini')
        except Exception as error:
            if error.args[0] != "INFO section is missing in configuration file.":
                raise AssertionError("Capturing INFO section is missing in config file error failed.")
        else:
            raise AssertionError("Capturing INFO section is missing in config file error failed.")

    def assert_structure_has_been_created_successfully(self):
        from dnres import DnRes
        try:
            res = DnRes('configs_for_testing/correct_config.ini')
        except Exception:
            raise AssertionError("Config error was not expected in this test.")
        dirsToFind = ['foo', 'foo/bar', 'foo/foo', 'foo/foo/bar']
        for d in dirsToFind:
            if not os.path.exists(d):
                raise AssertionError("Structure directories were not created successfully.")

    def assert_database_has_been_created_successfully(self):
        from dnres import DnRes
        try:
            res = DnRes('configs_for_testing/correct_config.ini')
        except Exception:
            raise AssertionError("Config error is not expected in this test.")
        if not os.path.exists(res.db):
            raise AssertionError("Database was not initialized.")

    def assert_store_object(self):
        from dnres import DnRes
        try:
            res = DnRes('configs_for_testing/correct_config.ini')
        except Exception:
            raise AssertionError("Config error is not expected in this test.")
        x = [1,2,3]
        res.store(data=x,
                  directory='dir1',
                  filename='x_var.json',
                  description='List with three numbers',
                  source='foo.py',
                  serialization='json'
                 )
        if not os.path.exists(os.path.join(res.structure['dir1'], 'x_var.json')):
            raise AssertionError("File not stored in structure.")
        if not res._has_filename('dir1', 'x_var.json'):
            raise AssertionError("File not stored in database.")

    def assert_store_file(self):
        from dnres import DnRes
        try:
            res = DnRes('configs_for_testing/correct_config.ini')
        except Exception:
            raise AssertionError("Config error is not expected in this test.")
        res.store(data='data_for_testing/foo.csv',
                  directory='dir2',
                  filename='foo.csv',
                  description='External csv file.',
                  source='some url',
                  isfile=True
                 )
        if not os.path.exists(os.path.join(res.structure['dir2'], 'foo.csv')):
            raise AssertionError("File not stored in structure.")
        if not res._has_filename('dir2', 'foo.csv'):
            raise AssertionError("File not stored in database.")

    def assert_load_object(self):
        from dnres import DnRes
        try:
            res = DnRes('configs_for_testing/correct_config.ini')
        except Exception:
            raise AssertionError("Config error is not expected in this test.")
        x = res.load('dir1', 'x_var.json')
        if not isinstance(x, list):
            raise AssertionError("Object expected to be a list.")
        if x != [1,2,3]:
            raise AssertionError("Loaded data are incorrect.")

    def assert_delete_object(self):
        from dnres import DnRes
        try:
            res = DnRes('configs_for_testing/correct_config.ini')
        except Exception:
            raise AssertionError("Config error is not expected in this test.")
        res.delete('dir1', 'x_var.json')
        if res._has_filename('dir1', 'x_var.json'):
            raise AssertionError("Object not deleted from database.")
        if os.path.exists(os.path.join(res.structure['dir1'], 'x_var.json')):
            raise AssertionError("Object not seleted from structure.")
            
    def assert_move_stored_object(self):
        from dnres import DnRes
        try:
            res = DnRes('configs_for_testing/correct_config.ini')
        except Exception:
            raise AssertionError("Config error is not expected in this test.")
        res.move("foo.csv", "dir2", "dir1")
        if res._has_filename("dir2", "foo.csv"):
            raise AssertionError("Object not moved from source in database.")
        if not res._has_filename("dir1", "foo.csv"):
            raise AssertionError("Object not moved to destination in database.")
        if os.path.exists(os.path.join(res.structure['dir2'], 'foo.csv')):
            raise AssertionError("Object not moved from source structure.")
        if not os.path.exists(os.path.join(res.structure['dir1'], 'foo.csv')):
            raise AssertionError("Object not moved to destination structure.")
            
    def assert_rename_object(self):
        from dnres import DnRes
        try:
            res = DnRes('configs_for_testing/correct_config.ini')
        except Exception:
            raise AssertionError("Config error is not expected in this test.")
        res.rename('dir1', 'foo.csv', 'bar.txt')
        if res._has_filename('dir1', 'foo.csv') or not res._has_filename('dir1', 'bar.txt'):
            raise AssertionError("Object not renamed in database.")
        previousPath = os.path.join(res.structure['dir1'], 'foo.csv')
        newPath = os.path.join(res.structure['dir1'], 'bar.txt')
        if os.path.exists(previousPath) or not os.path.exists(newPath):
            raise AssertionError("Object not renamed in structure.")



class PerformTests(TestCaseBase):
    def test_01_capture_config_not_found(self):
        """Captures config file not found error."""
        self.assert_capture_config_not_found()

    def test_02_capture_config_missing_structure_section(self):
        """Captures STRUCTURE section is missing from the config file."""
        self.assert_capture_config_missing_structure_section()

    def test_03_capture_structure_section_in_config_is_empty(self):
        """Captures STRUCTURE section is emtpy in the config file."""
        self.assert_capture_structure_section_in_config_is_empty()

    def test_04_capture_database_section_is_missing_in_config(self):
        """Captures DATABASE section is missing in the config file."""
        self.assert_capture_database_section_is_missing_in_config()

    def test_05_capture_filename_is_missing_in_database_section(self):
        """Captures filename key is missing in DATABASE section of confi file"""
        self.assert_capture_filename_is_missing_in_database_section()

    def test_06_capture_info_section_is_missing_in_config_file(self):
        """Captures INFO section is missing in the config file."""
        self.assert_capture_info_section_is_missing_in_config_file()

    def test_07_structure_has_been_created_successfully(self):
        """Asserts structure has been created successfully."""
        self.assert_structure_has_been_created_successfully()

    def test_08_database_has_been_created_successfully(self):
        """Asserts database has been created successfully."""
        self.assert_database_has_been_created_successfully()

    def test_09_store_object(self):
        """Asserts object has been stored_successfully."""
        self.assert_store_object()

    def test_10_store_file(self):
        """Asserts file has been stored successfully."""
        self.assert_store_file()

    def test_11_load_object(self):
        """Asserts object has been loaded successfully."""
        self.assert_load_object()

    def test_12_delete_object(self):
        """Asserts object has been deleted successfully."""
        self.assert_delete_object()

    def test_13_move_stored_object(self):
        """Asserts object has been moved successfully."""
        self.assert_move_stored_object()

    def test_14_rename_object(self):
        """Asserts object has been renamed successfully."""
        self.assert_rename_object()

if __name__ == "__main__":
    unittest.main()
