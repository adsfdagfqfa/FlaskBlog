import sqlite3
import sys
import tempfile
import unittest
from pathlib import Path

from flask import Flask
from passlib.hash import sha512_crypt as encryption


APP_DIR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(APP_DIR))


class SilentLog:
    @staticmethod
    def info(*args, **kwargs):
        pass

    @staticmethod
    def error(*args, **kwargs):
        pass

    @staticmethod
    def success(*args, **kwargs):
        pass

    @staticmethod
    def database(*args, **kwargs):
        pass

    @staticmethod
    def warning(*args, **kwargs):
        pass


def create_users_db(path):
    connection = sqlite3.connect(path)
    connection.execute(
        """
        create table users(
            userID integer primary key autoincrement,
            userName text unique,
            email text unique,
            password text,
            profilePicture text,
            role text,
            points integer,
            timeStamp integer,
            isVerified text
        )
        """
    )
    users = [
        ("u" * 20, "u20@example.com", "abcdefghij"),
        ("user", "u4@example.com", "abcdefghij"),
        ("usera", "u5@example.com", "abcdefghij"),
        ("u" * 24, "u24@example.com", "abcdefghij"),
        ("u" * 25, "u25@example.com", "abcdefghij"),
        ("pass5user", "p5@example.com", "abcde"),
        ("pass6user", "p6@example.com", "abcdef"),
    ]
    for user_name, email, password in users:
        connection.execute(
            """
            insert into users(userName,email,password,profilePicture,role,points,timeStamp,isVerified)
            values(?,?,?,?,?,?,?,?)
            """,
            (
                user_name,
                email,
                encryption.hash(password),
                "avatar",
                "user",
                0,
                1,
                "True",
            ),
        )
    connection.commit()
    connection.close()


class LoginBlackBoxTests(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory(ignore_cleanup_errors=True)
        self.users_db = str(Path(self.temp_dir.name) / "users.db")
        create_users_db(self.users_db)

        import settings

        settings.DB_USERS_ROOT = self.users_db
        settings.LOG_IN = True
        settings.RECAPTCHA = False

    def tearDown(self):
        self.temp_dir.cleanup()

    def client(self):
        import routes.login as login_mod

        login_mod.DB_USERS_ROOT = self.users_db
        login_mod.LOG_IN = True
        login_mod.RECAPTCHA = False
        login_mod.Log = SilentLog
        login_mod.flashMessage = lambda **kwargs: None
        login_mod.addPoints = lambda *args, **kwargs: None
        login_mod.render_template = lambda *args, **kwargs: "login page"

        app = Flask("login-blackbox-test")
        app.secret_key = "test"
        app.testing = True
        app.register_blueprint(login_mod.loginBlueprint)
        return app.test_client()

    def post_login(self, payload):
        client = self.client()
        with client.session_transaction() as session:
            session["language"] = "en"
        response = client.post("/login/redirect=&dashboard", data=payload)
        return client, response

    def assert_no_login_session(self, client):
        with client.session_transaction() as session:
            self.assertNotIn("userName", session)
            self.assertNotIn("userRole", session)

    def assert_login_success(self, client, expected_username):
        with client.session_transaction() as session:
            self.assertEqual(session["userName"], expected_username)
            self.assertEqual(session["userRole"], "user")

    def test_bb_login_01_valid_credentials_log_user_in(self):
        username = "u" * 20
        client, response = self.post_login(
            {"userName": username, "password": "abcdefghij"}
        )

        self.assertEqual(response.status_code, 301)
        self.assert_login_success(client, username)

    def test_bb_login_02_empty_username_is_rejected(self):
        client, response = self.post_login(
            {"userName": "", "password": "abcdefghij"}
        )

        self.assertEqual(response.status_code, 200)
        self.assert_no_login_session(client)

    def test_bb_login_03_short_username_is_rejected(self):
        client, response = self.post_login(
            {"userName": "abc", "password": "abcdefghij"}
        )

        self.assertEqual(response.status_code, 200)
        self.assert_no_login_session(client)

    def test_bb_login_04_username_length_4_is_accepted(self):
        client, response = self.post_login(
            {"userName": "user", "password": "abcdefghij"}
        )

        self.assertEqual(response.status_code, 301)
        self.assert_login_success(client, "user")

    def test_bb_login_05_username_length_5_is_accepted(self):
        client, response = self.post_login(
            {"userName": "usera", "password": "abcdefghij"}
        )

        self.assertEqual(response.status_code, 301)
        self.assert_login_success(client, "usera")

    def test_bb_login_06_username_length_24_is_accepted(self):
        username = "u" * 24
        client, response = self.post_login(
            {"userName": username, "password": "abcdefghij"}
        )

        self.assertEqual(response.status_code, 301)
        self.assert_login_success(client, username)

    def test_bb_login_07_username_length_25_is_accepted(self):
        username = "u" * 25
        client, response = self.post_login(
            {"userName": username, "password": "abcdefghij"}
        )

        self.assertEqual(response.status_code, 301)
        self.assert_login_success(client, username)

    def test_bb_login_08_long_username_is_rejected(self):
        long_username = "a" * 26
        client, response = self.post_login(
            {"userName": long_username, "password": "abcdefghij"}
        )

        self.assertEqual(response.status_code, 200)
        self.assert_no_login_session(client)

    def test_bb_login_09_unknown_user_is_rejected(self):
        client, response = self.post_login(
            {"userName": "nobody", "password": "abcdefghij"}
        )

        self.assertEqual(response.status_code, 200)
        self.assert_no_login_session(client)

    def test_bb_login_10_empty_password_is_rejected(self):
        username = "u" * 20
        client, response = self.post_login({"userName": username, "password": ""})

        self.assertEqual(response.status_code, 200)
        self.assert_no_login_session(client)

    def test_bb_login_11_password_length_4_is_rejected(self):
        username = "u" * 20
        client, response = self.post_login({"userName": username, "password": "abcd"})

        self.assertEqual(response.status_code, 200)
        self.assert_no_login_session(client)

    def test_bb_login_12_password_length_5_is_accepted(self):
        client, response = self.post_login(
            {"userName": "pass5user", "password": "abcde"}
        )

        self.assertEqual(response.status_code, 301)
        self.assert_login_success(client, "pass5user")

    def test_bb_login_13_password_length_6_is_accepted(self):
        client, response = self.post_login(
            {"userName": "pass6user", "password": "abcdef"}
        )

        self.assertEqual(response.status_code, 301)
        self.assert_login_success(client, "pass6user")

    def test_bb_login_14_wrong_password_is_rejected(self):
        username = "u" * 20
        client, response = self.post_login(
            {"userName": username, "password": "wrongpassx"}
        )

        self.assertEqual(response.status_code, 200)
        self.assert_no_login_session(client)


if __name__ == "__main__":
    unittest.main(verbosity=2)
