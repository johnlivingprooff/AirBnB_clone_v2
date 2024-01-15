#!/usr/bin/python3
"""Unittest for BaseModel"""
import unittest
from unittest.mock import patch
from datetime import datetime
from models import storage
from models.base_model import BaseModel


class test_basemodel(unittest.TestCase):
    """Test cases for the BaseModel Class"""

    # BASIC TESTS

    def test_instance(self):
        """test instantisation"""
        obj = BaseModel()
        self.assertIsInstance(obj, BaseModel)

    def test_instance_hasattr(self):
        """Tests if an instance has attributes"""
        obj = BaseModel()

        self.assertTrue(hasattr(obj, 'id'))
        self.assertTrue(hasattr(obj, 'created_at'))
        self.assertTrue(hasattr(obj, 'updated_at'))

    def test_instance_with_value(self):
        """
        Test whether the instance attributes are correctly assigned
        """
        _id = "7q795"
        _created_at = "2023-12-07T09:49:07.936066"
        _updated_at = "2023-12-07T09:49:07.936176"
        d_format = "%Y-%m-%dT%H:%M:%S.%f"

        obj_c_at = datetime.strptime(_created_at, d_format)
        obj_u_at = datetime.strptime(_updated_at, d_format)
        obj = BaseModel(id=_id, created_at=_created_at, updated_at=_updated_at)

        self.assertEqual(obj.id, _id)
        self.assertEqual(obj.created_at, obj_c_at)
        self.assertEqual(obj.updated_at, obj_u_at)

    def test_str_method(self):
        """testing the __str__ method"""
        obj = BaseModel()
        expected_str = f"[BaseModel] ({obj.id}) {obj.__dict__}"
        self.assertEqual(str(obj), expected_str)

    def test_save_method(self):
        """test case for save method"""
        obj = BaseModel()
        first_update = obj.updated_at
        obj.user = "Testin"
        obj.save()
        self.assertNotEqual(first_update, obj.updated_at)

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
        obj = BaseModel()
        obj_dict = obj.to_dict()

        new_obj = BaseModel(**obj_dict)
        self.assertIsInstance(new_obj, BaseModel)
        self.assertEqual(new_obj.id, obj.id)
        self.assertEqual(new_obj.created_at, obj.created_at)
        self.assertEqual(new_obj.updated_at, obj.updated_at)

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

    # ATTRIBUTES TESTS
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
        obj1 = BaseModel(id='State1')
        obj2 = BaseModel(id='State2')
        self.assertNotEqual(obj1, obj2)

    # FILE STORAGE INTEGRATION
    @patch('models.storage.save')  # helpst to mock save method
    def test_save_method_updates_storage(self, mock_save):
        """Test whether models.storage.save
        is called and updates the storage
        """
        obj = BaseModel()
        original_updated_at = obj.updated_at

        # Modify some attributes to trigger the need to save
        obj.some_attribute = 'new_value'

        obj.save()
        mock_save.assert_called_once()

        # Verify that updated_at has changed after saving
        self.assertNotEqual(original_updated_at, obj.updated_at)

    @patch('models.storage.all')
    def test_all_method_returns_dict(self, mock_all):
        """Test whether models.storage.all returns a dictionary"""
        mock_all.return_value = {'some_key': 'some_value'}
        result = storage.all()
        self.assertIsInstance(result, dict)

    # OTHER EDGE CASES
    def test_empty_name(self):
        """Test if the class handles empty name"""
        obj = BaseModel(name='')
        self.assertEqual(obj.name, '')

    def test_custom_attribute_assignment(self):
        """Test if the class handles custom attribute assignment"""
        obj = BaseModel()
        obj.custom_attribute = 'custom_value'
        self.assertEqual(obj.custom_attribute, 'custom_value')
