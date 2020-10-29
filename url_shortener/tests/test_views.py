import os

from unittest import TestCase
from unittest.mock import patch

import tempfile

from app import app

from models import create_tables, Url, database

from config import TEST_DB_NAME, DB_NAME

from peewee import SqliteDatabase

from decoders import Base62

app.config["TEST"] = True


class BaseViewTestCase(TestCase):
    def setUp(self) -> None:
        database.init(TEST_DB_NAME)
        # create tables for test
        create_tables()

    def tearDown(self) -> None:
        # Close connection after test
        database.close()
        # Back to old database
        database.init(DB_NAME)
        # Remove test db file
        os.remove(TEST_DB_NAME)


class IndexViewTests(BaseViewTestCase):
    _test_url = "http://test.com"

    def test_response_index(self):
        with app.test_client() as c:
            resp = c.get("/")
            self.assertEqual(resp.status_code, 200)

    def test_create_url(self):
        with app.test_client() as c:
            resp = c.post("/", data={"url": self._test_url})
            self.assertEqual(resp.status_code, 200)
        # Test url created in db
        self.assertEqual(Url.select().where(Url.url == self._test_url).count(), 1)

    def test_url_exists(self):
        Url.create(url=self._test_url)
        with app.test_client() as c:
            resp = c.post("/", data={"url": self._test_url})
        self.assertEqual(resp.status_code, 200)
        # Test url created in db
        self.assertEqual(Url.select().where(Url.url == self._test_url).count(), 1)


class RedirectViewTests(BaseViewTestCase):
    _test_url = "http://test.com"

    def test_redirect(self):
        url = Url.create(url=self._test_url)
        with app.test_client() as c:
            resp = c.get(f"/{Base62.encode(url.id)}")
            self.assertEqual(resp.status_code, 302)
        url = Url.select().where(Url.url == self._test_url).first()
        self.assertEqual(url.views, 1)

    def test_url_not_found(self):
        with app.test_client() as c:
            resp = c.get(f"/{Base62.encode(1000)}")
            self.assertEqual(resp.status_code, 404)
