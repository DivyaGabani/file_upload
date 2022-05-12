"""This checks database folder"""
import os


def test_database_directory():
    """this checks database"""
    root = os.path.dirname(os.path.abspath(__file__))
    dbdir = os.path.join(root, '../database')
    assert os.path.exists(dbdir) is True
