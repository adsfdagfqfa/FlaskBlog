import sqlite3
import sys
import tempfile
import unittest
from pathlib import Path

from flask import Flask


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
    connection.commit()
    connection.close()


def scalar(db_path, sql, params=()):
    connection = sqlite3.connect(db_path)
    try:
        return connection.execute(sql, params).fetchone()[0]
    finally:
        connection.close()


def email_with_length(length):
    return "a" * (length - len("@b.co")) + "@b.co"


class SignupBlackBoxTests(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory(ignore_cleanup_errors=True)
        self.users_db = str(Path(self.temp_dir.name) / "users.db")
        create_users_db(self.users_db)

        import settings

        settings.DB_USERS_ROOT = self.users_db
        settings.RECAPTCHA = False
        settings.REGISTRATION = True

    def tearDown(self):
        self.temp_dir.cleanup()

    def client(self):
        import routes.signup as signup_mod

        signup_mod.DB_USERS_ROOT = self.users_db
        signup_mod.RECAPTCHA = False
        signup_mod.REGISTRATION = True
        signup_mod.Log = SilentLog
        signup_mod.flashMessage = lambda **kwargs: None
        signup_mod.addPoints = lambda *args, **kwargs: None
        signup_mod.render_template = lambda *args, **kwargs: "signup page"

        app = Flask("signup-blackbox-test")
        app.secret_key = "test"
        app.testing = True
        app.register_blueprint(signup_mod.signUpBlueprint)
        return app.test_client()

    def post_signup(self, payload):
        client = self.client()
        with client.session_transaction() as session:
            session["language"] = "en"
        return client.post("/signup", data=payload)

    def assert_user_count(self, username, expected):
        self.assertEqual(
            scalar(
                self.users_db,
                "select count(*) from users where userName = ?",
                (username,),
            ),
            expected,
        )

    def assert_signup_accepted(self, payload):
        response = self.post_signup(payload)

        self.assertEqual(response.status_code, 302)
        self.assert_user_count(payload["userName"], 1)

    def test_bb01_valid_signup_is_accepted(self):
        response = self.post_signup(
            {
                "userName": "validuser",
                "email": "valid@example.com",
                "password": "abcdefghij",
                "passwordConfirm": "abcdefghij",
            }
        )

        self.assertEqual(response.status_code, 302)
        self.assert_user_count("validuser", 1)

    def test_bb02_empty_username_is_rejected(self):
        self.post_signup(
            {
                "userName": "",
                "email": "valid@example.com",
                "password": "abcdefghij",
                "passwordConfirm": "abcdefghij",
            }
        )

        self.assert_user_count("", 0)

    def test_bb03_short_username_is_rejected(self):
        self.post_signup(
            {
                "userName": "abc",
                "email": "valid@example.com",
                "password": "abcdefghij",
                "passwordConfirm": "abcdefghij",
            }
        )

        self.assert_user_count("abc", 0)

    def test_bb04_long_username_is_rejected(self):
        username = "abcdefghijklmnopqrstuvwxyz"
        self.post_signup(
            {
                "userName": username,
                "email": "valid@example.com",
                "password": "abcdefghij",
                "passwordConfirm": "abcdefghij",
            }
        )

        self.assert_user_count(username, 0)

    def test_bb05_non_ascii_username_is_rejected(self):
        username = "测试用户"
        self.post_signup(
            {
                "userName": username,
                "email": "cn@example.com",
                "password": "abcdefghij",
                "passwordConfirm": "abcdefghij",
            }
        )

        self.assert_user_count(username, 0)

    def test_bb06_duplicate_username_is_rejected(self):
        client = self.client()
        with client.session_transaction() as session:
            session["language"] = "en"

        client.post(
            "/signup",
            data={
                "userName": "validuser",
                "email": "valid@example.com",
                "password": "abcdefghij",
                "passwordConfirm": "abcdefghij",
            },
        )
        with client.session_transaction() as session:
            session.clear()
            session["language"] = "en"
        client.post(
            "/signup",
            data={
                "userName": "validuser",
                "email": "new@example.com",
                "password": "abcdefghij",
                "passwordConfirm": "abcdefghij",
            },
        )

        self.assert_user_count("validuser", 1)

    def test_bb07_empty_email_is_rejected(self):
        self.post_signup(
            {
                "userName": "validuser",
                "email": "",
                "password": "abcdefghij",
                "passwordConfirm": "abcdefghij",
            }
        )

        self.assert_user_count("validuser", 0)

    def test_bb08_invalid_email_format_is_rejected(self):
        self.post_signup(
            {
                "userName": "validuser",
                "email": "bad-email",
                "password": "abcdefghij",
                "passwordConfirm": "abcdefghij",
            }
        )

        self.assert_user_count("validuser", 0)

    def test_bb09_short_email_is_rejected(self):
        self.post_signup(
            {
                "userName": "validuser",
                "email": "a@b.c",
                "password": "abcdefghij",
                "passwordConfirm": "abcdefghij",
            }
        )

        self.assert_user_count("validuser", 0)

    def test_bb10_long_email_is_rejected(self):
        long_email = email_with_length(51)
        self.post_signup(
            {
                "userName": "validuser",
                "email": long_email,
                "password": "abcdefghij",
                "passwordConfirm": "abcdefghij",
            }
        )

        self.assert_user_count("validuser", 0)

    def test_bb11_duplicate_email_is_rejected(self):
        client = self.client()
        with client.session_transaction() as session:
            session["language"] = "en"

        client.post(
            "/signup",
            data={
                "userName": "validuser",
                "email": "valid@example.com",
                "password": "abcdefghij",
                "passwordConfirm": "abcdefghij",
            },
        )
        with client.session_transaction() as session:
            session.clear()
            session["language"] = "en"
        client.post(
            "/signup",
            data={
                "userName": "otheruser",
                "email": "valid@example.com",
                "password": "abcdefghij",
                "passwordConfirm": "abcdefghij",
            },
        )

        self.assert_user_count("otheruser", 0)

    def test_bb12_empty_password_is_rejected(self):
        self.post_signup(
            {
                "userName": "validuser",
                "email": "valid@example.com",
                "password": "",
                "passwordConfirm": "",
            }
        )

        self.assert_user_count("validuser", 0)

    def test_bb13_short_password_is_rejected(self):
        self.post_signup(
            {
                "userName": "validuser",
                "email": "valid@example.com",
                "password": "abcdefg",
                "passwordConfirm": "abcdefg",
            }
        )

        self.assert_user_count("validuser", 0)

    def test_bb14_mismatched_password_confirmation_is_rejected(self):
        self.post_signup(
            {
                "userName": "validuser",
                "email": "valid@example.com",
                "password": "abcdefghij",
                "passwordConfirm": "abcdefghik",
            }
        )

        self.assert_user_count("validuser", 0)

    def test_bb15_username_length_4_is_accepted(self):
        self.assert_signup_accepted(
            {
                "userName": "user",
                "email": "u4@example.com",
                "password": "abcdefghij",
                "passwordConfirm": "abcdefghij",
            }
        )

    def test_bb16_username_length_5_is_accepted(self):
        self.assert_signup_accepted(
            {
                "userName": "usera",
                "email": "u5@example.com",
                "password": "abcdefghij",
                "passwordConfirm": "abcdefghij",
            }
        )

    def test_bb17_username_length_24_is_accepted(self):
        username = "u" * 24
        self.assert_signup_accepted(
            {
                "userName": username,
                "email": "u24@example.com",
                "password": "abcdefghij",
                "passwordConfirm": "abcdefghij",
            }
        )

    def test_bb18_username_length_25_is_accepted(self):
        username = "u" * 25
        self.assert_signup_accepted(
            {
                "userName": username,
                "email": "u25@example.com",
                "password": "abcdefghij",
                "passwordConfirm": "abcdefghij",
            }
        )

    def test_bb19_email_length_6_is_accepted(self):
        self.assert_signup_accepted(
            {
                "userName": "email06",
                "email": email_with_length(6),
                "password": "abcdefghij",
                "passwordConfirm": "abcdefghij",
            }
        )

    def test_bb20_email_length_7_is_accepted(self):
        self.assert_signup_accepted(
            {
                "userName": "email07",
                "email": email_with_length(7),
                "password": "abcdefghij",
                "passwordConfirm": "abcdefghij",
            }
        )

    def test_bb21_email_length_49_is_accepted(self):
        self.assert_signup_accepted(
            {
                "userName": "email49",
                "email": email_with_length(49),
                "password": "abcdefghij",
                "passwordConfirm": "abcdefghij",
            }
        )

    def test_bb22_email_length_50_is_accepted(self):
        self.assert_signup_accepted(
            {
                "userName": "email50",
                "email": email_with_length(50),
                "password": "abcdefghij",
                "passwordConfirm": "abcdefghij",
            }
        )

    def test_bb23_password_length_8_is_accepted(self):
        self.assert_signup_accepted(
            {
                "userName": "passlen8",
                "email": "p8@example.com",
                "password": "abcdefgh",
                "passwordConfirm": "abcdefgh",
            }
        )

    def test_bb24_password_length_9_is_accepted(self):
        self.assert_signup_accepted(
            {
                "userName": "passlen9",
                "email": "p9@example.com",
                "password": "abcdefghi",
                "passwordConfirm": "abcdefghi",
            }
        )


if __name__ == "__main__":
    unittest.main(verbosity=2)
