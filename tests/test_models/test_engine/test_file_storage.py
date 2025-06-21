#!/usr/bin/python3
"""Unittest for FileStorage class"""
import unittest
import os
from models.engine.file_storage import FileStorage
from models.base_model import BaseModel


class TestFileStorage(unittest.TestCase):
    """Tests for the FileStorage class"""

    def setUp(self):
        """Set up test environment"""
        self.storage = FileStorage()
        self.model = BaseModel()
        self.model.name = "TestModel"
        self.storage.new(self.model)
        self.storage.save()

    def tearDown(self):
        """Clean up test environment"""
        try:
            os.remove("file.json")
        except FileNotFoundError:
            pass

    def test_all_returns_dict(self):
        self.assertIsInstance(self.storage.all(), dict)

    def test_new_adds_object(self):
        key = f"{self.model.__class__.__name__}.{self.model.id}"
        self.assertIn(key, self.storage.all())

    def test_save_creates_file(self):
        self.assertTrue(os.path.exists("file.json"))

    def test_reload_loads_objects(self):
        key = f"{self.model.__class__.__name__}.{self.model.id}"
        self.storage.reload()
        self.assertIn(key, self.storage.all())

    def test_delete_removes_object(self):
        key = f"{self.model.__class__.__name__}.{self.model.id}"
        self.storage.delete(self.model)
        self.assertNotIn(key, self.storage.all())


if __name__ == '__main__':
    unittest.main()
