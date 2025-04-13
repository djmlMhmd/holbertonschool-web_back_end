#!/usr/bin/env python3
""" Test for utils module
"""

from parameterized import parameterized
from typing import Dict
from utils import access_nested_map, get_json, memoize
import unittest
from unittest.mock import Mock, patch


class TestAccessNestedMap(unittest.TestCase):
    """Tests for access nested map method"""
    @parameterized.expand([
        ({"a": 1}, ("a",), 1),
        ({"a": {"b": 2}}, ("a",), {"b": 2}),
        ({"a": {"b": 2}}, ("a", "b"), 2),
    ])
    def test_access_nested_map(self, nested_map, path, expected) -> None:
        """Tests the same thing with expected values"""
        self.assertEqual(access_nested_map(nested_map, path), expected)

    @parameterized.expand([
        ({}, ("a",), KeyError),
        ({"a": 1}, ("a", "b"), KeyError),
    ])
    def test_access_nested_map_exception(self,
                                         nested_map, path, expected) -> None:
        """Tests exception values"""
        self.assertRaises(KeyError, access_nested_map, nested_map, path)


class TestGetJson(unittest.TestCase):
    """Tests for the get_json function"""
    @parameterized.expand([
        ("http://example.com", {"payload": True}),
        ("http://holberton.io", {"payload": False}),
    ])
    @patch('requests.get')
    def test_get_json(self, url, expected, mock_get) -> Dict:
        """Test expected payload"""
        mock_get.return_value.json.return_value = expected

        result = get_json(url)
        mock_get.assert_called_once_with(url)
        self.assertEqual(result, expected)


class TestMemoize(unittest.TestCase):
    """Test for memoize function"""

    def test_memoize(self):
        """The method to test memoize"""
        class TestClass:
            """The reqiered class"""

            def a_method(self):
                """A method to test"""
                return 42

            @memoize
            def a_property(self):
                """Testing testing testing"""
                return self.a_method()

        with patch.object(TestClass, 'a_method') as mock:
            test_class = TestClass()
            test_class.a_property()
            test_class.a_property()
            mock.assert_called_once()
