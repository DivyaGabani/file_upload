"""csv file test"""
import csv
from app.db.models import User, Song


def test_csv_dile(client, add_user, application):
    """This test csv file is created or not """
    with application.app_context():
        user = User('dummy1@test.com', 'abcd1234')
        filepath = 'tests/music1.csv'
        with open(filepath) as file:
            csv_read = csv.DictReader(file)
            for row in csv_read:
                test_csv = row
            assert test_csv == {'Title': 'song1', 'Artist': 'artist1', 'Genre': 'genre1'}
