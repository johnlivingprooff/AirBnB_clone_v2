#!/usr/bin/python3
"""Unittest for BaseModel"""
import unittest
from models.base_model import BaseModel, Base
import models
import pep8
from datetime import datetime
import inspect
from unittest.mock import patch
import os
from sqlalchemy import create_engine, inspect
from sqlalchemy.orm import sessionmaker
FileStorage = models.FileStorage

models.storage = FileStorage()


class test_BaseModel_pep8_docs(unittest.TestCase):
    """Unittest for BaseModel class docs and style"""

    def test_docstring(self):
        """checks for docstrings"""
        self.assertIsNotNone(BaseModel.__doc__)
        self.assertIsNotNone(BaseModel.__init__.__doc__)
        self.assertIsNotNone(BaseModel.__str__.__doc__)
        self.assertIsNotNone(BaseModel.save.__doc__)
        self.assertIsNotNone(BaseModel.to_dict.__doc__)
        self.assertIsNotNone(BaseModel.delete.__doc__)

    def test_pep8(self):
        """Checks PEP8 compliance"""
        msg = "PEP8 incompliant, errors found"
        style = pep8.StyleGuide()
        res = style.check_files(["models/base_model.py"])
        self.assertEqual(res.total_errors, 0, msg)


class TestBaseModel(unittest.TestCase):
    """Unittest for the BaseModel Class"""

    @classmethod
    def setUp(cls):
        """set up for unittests"""

        try:
            # rename existing file.json to preserve data
            os.rename("file.json", "org_file")
        except IOError:
            pass

        FileStorage._FileStorage__objects = {}
        cls.storage = FileStorage()
        cls.base_i = BaseModel()

        # if os.getenv("HBNB_TYPE_STORAGE") == 'db':
        #     # Connect to the database
        #     uri = "mysql+mysqldb://{}:{}@localhost:3306/{}"\
        #         .format("hbnb_test", "hbnb_test_pwd", "hbnb_test_db")
        #     cls.engine = create_engine(uri, pool_pre_ping=True)
        #     Base.metadata.create_all(cls.engine)
        #     cls.Session = sessionmaker(bind=cls.engine)

    @classmethod
    def tearDown(cls):
        try:
            os.remove("file.json")
        except IOError:
            pass

        try:
            # restore the original file.json
            os.rename("org_file", "file.json")
        except IOError:
            pass

        del cls.storage
        del cls.base_i

    # Attributes tests
    # @unittest.skipIf(
    #         os.getenv("HBNB_TYPE_STORAGE") != 'db',
    #         "testing db_storage")
    # def test_attributes_in_table(self):
    #     """docstring here -_-"""
    #     session = self.Session()
    #     b_model = BaseModel()
    #     session.add(b_model)
    #     session.commit()

    #     # Inspect the table
    #     inspector = inspect(self.engine)
    #     columns = inspector.get_columns('b_model')

    #     # Check if the 'id', 'created_at', and 'updated_at' columns exist
    #     column_names = [column['name'] for column in columns]
    #     self.assertIn('id', column_names)
    #     self.assertIn('created_at', column_names)
    #     self.assertIn('updated_at', column_names)

    #     # Clean up
    #     session.close()

    def test_init(self):
        """Test instantisation"""
        self.assertIsInstance(self.base_i, BaseModel)

    def test_instance_hasattr(self):
        """Tests if an instance has attributes"""

        self.assertTrue(hasattr(self.base_i, 'id'))
        self.assertTrue(hasattr(self.base_i, 'created_at'))
        self.assertTrue(hasattr(self.base_i, 'updated_at'))

    def test_unique_models(self):
        """Test checks that two models are unique"""
        model_two = BaseModel()
        self.assertNotEqual(model_two.id, self.base_i.id)
        self.assertLess(self.base_i.created_at, model_two.created_at)
        self.assertNotEqual(model_two.updated_at, self.base_i.updated_at)

    def test_id_attribute(self):
        """When assigning an id to instance"""
        obj = BaseModel(id="7e156w")
        self.assertEqual("7e156w", obj.id)

    def test_created_at(self):
        """Assigning created at time"""
        d_format = "%Y-%m-%dT%H:%M:%S.%f"
        same_date = "2023-12-07T16:16:21.285406"
        obj = BaseModel(created_at=same_date)
        obj_c_at = datetime.strptime(same_date, d_format)
        self.assertEqual(obj_c_at, obj.created_at)

    def test_updated_at(self):
        """Assigning updated at"""
        d_format = "%Y-%m-%dT%H:%M:%S.%f"
        same_date = "2023-12-07T16:16:21.285406"
        obj = BaseModel(updated_at=same_date)
        obj_u_at = datetime.strptime(same_date, d_format)
        self.assertEqual(obj_u_at, obj.updated_at)

    def test_changeTo_updated_at(self):
        """Checking if updated at changes"""
        obj = BaseModel()
        update_one = obj.updated_at
        obj.save()
        self.assertNotEqual(update_one, obj.updated_at)

    def test_new_args(self):
        """when passed new arg"""
        _id = "7q795"
        _created_at = "2023-12-07T09:49:07.936066"
        _updated_at = "2023-12-07T09:49:07.936176"
        obj = BaseModel(
            name="object name", id=_id,
            created_at=_created_at, updated_at=_updated_at)
        obj_dict = obj.to_dict()
        dictionary = {
            'id': '7q795', 'created_at': "2023-12-07T09:49:07.936066",
            'updated_at': "2023-12-07T09:49:07.936176",
            '__class__': "BaseModel", 'name': "object name"
            }
        self.assertDictEqual(obj_dict, dictionary)

    def test_equality(self):
        """Test if two instances with the same attributes are equal"""
        obj1 = BaseModel(name='Object1')
        obj2 = BaseModel(name='Object1')
        self.assertEqual(obj1.name, obj2.name)

    def test_inequality(self):
        """Test if two instances with different attributes are not equal"""
        obj1 = BaseModel(name='Object1')
        obj2 = BaseModel(name='Object2')
        self.assertNotEqual(obj1, obj2)

    def test_multiple_instances(self):
        """Test the behavior of multiple instances"""
        obj2 = BaseModel(id='State2')
        self.assertNotEqual(self.base_i, obj2)

    # Method tests
    def test_str_method(self):
        """testing the __str__ method"""
        expected_str = f"[BaseModel] ({self.base_i.id}) {self.base_i.__dict__}"
        self.assertEqual(str(self.base_i), expected_str)

    def test_save_method(self):
        """test case for save method"""
        og_updated_at = self.base_i.updated_at
        self.base_i.user = "Testin"
        self.base_i.save()
        self.assertLess(og_updated_at, self.base_i.updated_at)

    def test_to_dict_method(self):
        """Test Case for to_dict method"""
        _id = "7q795"
        _created_at = "2023-12-07T09:49:07.936066"
        _updated_at = "2023-12-07T09:49:07.936176"

        obj = BaseModel(id=_id, created_at=_created_at, updated_at=_updated_at)
        obj_dict = obj.to_dict()
        dictionary = {
            'id': '7q795', 'created_at': "2023-12-07T09:49:07.936066",
            'updated_at': "2023-12-07T09:49:07.936176",
            '__class__': "BaseModel",
            }
        self.assertEqual(dictionary, obj_dict)

    def test_inst_from_dict(self):
        """Test the creation of an instance from a dictionary"""
        obj_dict = self.base_i.to_dict()
        new_obj = BaseModel(**obj_dict)

        self.assertIsInstance(new_obj, BaseModel)
        self.assertEqual(new_obj.id, self.base_i.id)
        self.assertEqual(new_obj.created_at, self.base_i.created_at)
        self.assertEqual(new_obj.updated_at, self.base_i.updated_at)

    def test_custom_datetime_format(self):
        """Test the creation of an instance
        from a dictionary with custom date format"""

        _created_at = "2023-12-07T09:49:07.936066"
        _updated_at = "2023-12-07T09:49:07.936176"
        d_format = "%Y-%m-%dT%H:%M:%S.%f"
        obj = BaseModel()
        obj_dict = obj.to_dict()
        obj_dict['created_at'] = _created_at
        obj_dict['updated_at'] = _updated_at
        obj_c_at = datetime.strptime(_created_at, d_format)
        obj_u_at = datetime.strptime(_updated_at, d_format)
        self.assertIsInstance(obj, BaseModel)
        self.assertNotEqual(obj.created_at, obj_c_at)
        self.assertNotEqual(obj.updated_at, obj_u_at)

    # Storage Integrations Test
    @patch('models.storage.save')
    def test_save_method_updates_storage(self, mock_save):
        """Test that save() updates the file storage"""
        original_updated_at = self.base_i.updated_at
        self.base_i.name = "Test"

        self.base_i.save()
        mock_save.assert_called_once()

        self.assertLess(original_updated_at, self.base_i.updated_at)

    @patch('models.storage.all')
    def test_all_method_returns_dict(self, mock_all):
        """Test whether models.storage.all returns a dictionary"""
        mock_all.return_value = {'user': 'some_value'}
        result = models.storage.all()
        self.assertIsInstance(result, dict)

    @unittest.skipIf(
            os.getenv("HBNB_TYPE_STORAGE") == 'db',
            "testing file_storage")
    def test_saved_to_file(self):
        """Test if changes are in file"""
        original_updated_at = self.base_i.updated_at
        self.base_i.save()
        self.assertLess(original_updated_at, self.base_i.updated_at)
        with open("file.json", "r") as f:
            self.assertIn(f"BaseModel.{self.base_i.id}", f.read())

    @unittest.skipIf(
            os.getenv("HBNB_ENV") is not None,
            "testing file_storage")
    def test_saved_to_file(self):
        """Test if changes are in file"""
        original_updated_at = self.base_i.updated_at
        self.base_i.save()
        self.assertLess(original_updated_at, self.base_i.updated_at)
        with open("file.json", "r") as f:
            self.assertIn(f"BaseModel.{self.base_i.id}", f.read())
