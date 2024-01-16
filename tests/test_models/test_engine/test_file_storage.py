#!/usr/bin/python3
"""Test Module for file storage"""
import unittest
import os
import pep8
from models.base_model import BaseModel
from models.user import User
from models.place import Place
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.review import Review
from models.engine.file_storage import FileStorage


class TestAmenity_pep8(unittest.TestCase):
    """Unittest for Amenity class docs and style"""

    def test_docstring(self):
        """checks for docstrings"""
        self.assertTrue(hasattr(FileStorage, "__init__"))
        self.assertTrue(hasattr(FileStorage, "all"))
        self.assertTrue(hasattr(FileStorage, "new"))
        self.assertTrue(hasattr(FileStorage, "save"))
        self.assertTrue(hasattr(FileStorage, "delete"))
        self.assertTrue(hasattr(FileStorage, "reload"))

    def test_pep8(self):
        """Checks PEP8 compliance"""
        msg = "PEP8 incompliant, errors found"
        style = pep8.StyleGuide()
        res = style.check_files(["models/engine/file_storage.py"])
        self.assertEqual(res.total_errors, 0, msg)


class TestFileStorage(unittest.TestCase):

    def setUp(self):
        self.file_storage = FileStorage()
        self.base_model = BaseModel()
        self.user = User()
        self.place = Place()
        self.state = State()
        self.city = City()
        self.amenity = Amenity()
        self.review = Review()

    def tearDown(self):
        # Clean up: Delete the file.json if it exists after each test
        if os.path.exists(FileStorage._FileStorage__file_path):
            os.remove(FileStorage._FileStorage__file_path)

    def test_new_object_added_to_objects(self):
        # Check if the new method adds the object to __objects
        self.file_storage.new(self.base_model)
        self.assertIn("BaseModel.{}".format(self.base_model.id),
                      self.file_storage.all())

    def test_save_method_creates_file(self):
        # Check if the save method creates a file and it is not empty
        self.file_storage.new(self.base_model)
        self.file_storage.save()
        self.assertTrue(os.path.exists(FileStorage._FileStorage__file_path))
        with open(FileStorage._FileStorage__file_path, 'r') as f:
            data = f.read()
            self.assertTrue(data.strip())

    def test_all_method_returns_dict(self):
        # Check if all method returns a dictionary
        result = self.file_storage.all()
        self.assertIsInstance(result, dict)

    def test_all_method_returns_filtered_dict(self):
        self.file_storage.new(self.base_model)
        self.file_storage.new(self.user)
        self.file_storage.new(self.place)
        result = self.file_storage.all(User)
        self.assertIn("User.{}".format(self.user.id), result)
        self.assertNotIn("BaseModel.{}".format(self.base_model.id), result)

    def test_delete_method_removes_object(self):
        # Check if the delete method removes the specified object
        self.file_storage.new(self.base_model)
        self.file_storage.new(self.user)
        self.file_storage.delete(self.base_model)
        self.assertNotIn("BaseModel.{}".format(self.base_model.id),
                         self.file_storage.all())

    def test_reload_method_loads_data(self):
        # Check if the reload method loads data from the file
        self.file_storage.new(self.base_model)
        self.file_storage.save()

        new_file_storage = FileStorage()
        new_file_storage.reload()

        result = new_file_storage.all()
        self.assertIn("BaseModel.{}".format(self.base_model.id), result)

    def test_reload_method_handles_nonexistent_file(self):
        self.file_storage.reload()  # No exception should be raised


if __name__ == '__main__':
    unittest.main()
