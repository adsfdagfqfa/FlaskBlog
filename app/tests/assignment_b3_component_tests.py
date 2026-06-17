import io
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


def create_posts_db(path):
    connection = sqlite3.connect(path)
    connection.execute(
        """
        create table posts(
            id integer primary key autoincrement,
            title text not null,
            tags text not null,
            content text not null,
            banner blob not null,
            author text not null,
            views integer,
            timeStamp integer,
            lastEditTimeStamp integer,
            category text not null,
            urlID text not null
        )
        """
    )
    connection.commit()
    connection.close()


def scalar(db_path, sql):
    connection = sqlite3.connect(db_path)
    try:
        return connection.execute(sql).fetchone()[0]
    finally:
        connection.close()


class AssignmentB3ComponentTests(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory(ignore_cleanup_errors=True)
        self.users_db = str(Path(self.temp_dir.name) / "users.db")
        self.posts_db = str(Path(self.temp_dir.name) / "posts.db")
        create_users_db(self.users_db)
        create_posts_db(self.posts_db)

        import settings

        settings.DB_USERS_ROOT = self.users_db
        settings.DB_POSTS_ROOT = self.posts_db
        settings.RECAPTCHA = False
        settings.REGISTRATION = True

    def tearDown(self):
        self.temp_dir.cleanup()

    def signup_client(self):
        import routes.signup as signup_mod

        signup_mod.DB_USERS_ROOT = self.users_db
        signup_mod.RECAPTCHA = False
        signup_mod.REGISTRATION = True
        signup_mod.Log = SilentLog
        signup_mod.flashMessage = lambda **kwargs: None
        signup_mod.addPoints = lambda *args, **kwargs: None
        signup_mod.render_template = lambda *args, **kwargs: "signup page"

        app = Flask("signup-test")
        app.secret_key = "test"
        app.testing = True
        app.register_blueprint(signup_mod.signUpBlueprint)
        return app.test_client()

    def createpost_client(self):
        import routes.createPost as createpost_mod

        createpost_mod.DB_POSTS_ROOT = self.posts_db
        createpost_mod.Log = SilentLog
        createpost_mod.flashMessage = lambda **kwargs: None
        createpost_mod.addPoints = lambda *args, **kwargs: None
        createpost_mod.render_template = lambda *args, **kwargs: "create page"

        app = Flask("createpost-test")
        app.secret_key = "test"
        app.testing = True
        app.register_blueprint(createpost_mod.createPostBlueprint)
        return app.test_client()

    def test_bb_valid_signup_is_accepted(self):
        client = self.signup_client()
        with client.session_transaction() as session:
            session["language"] = "en"

        response = client.post(
            "/signup",
            data={
                "userName": "validuser",
                "email": "valid@example.com",
                "password": "abcdefgh",
                "passwordConfirm": "abcdefgh",
            },
        )

        self.assertEqual(response.status_code, 302)
        self.assertEqual(
            scalar(
                self.users_db,
                "select count(*) from users where userName = 'validuser'",
            ),
            1,
        )

    def test_bb_invalid_signup_input_is_rejected(self):
        client = self.signup_client()
        with client.session_transaction() as session:
            session["language"] = "en"

        client.post(
            "/signup",
            data={
                "userName": "ab",
                "email": "bad-email",
                "password": "short",
                "passwordConfirm": "short",
            },
        )

        self.assertEqual(
            scalar(self.users_db, "select count(*) from users where userName = 'ab'"),
            0,
            "Invalid signup input should not be inserted into users table.",
        )

    def test_bb_duplicate_username_is_rejected(self):
        client = self.signup_client()
        with client.session_transaction() as session:
            session["language"] = "en"

        payload = {
            "userName": "validuser",
            "email": "valid@example.com",
            "password": "abcdefgh",
            "passwordConfirm": "abcdefgh",
        }
        client.post("/signup", data=payload)

        with client.session_transaction() as session:
            session.clear()
            session["language"] = "en"
        payload["email"] = "new@example.com"
        client.post("/signup", data=payload)

        self.assertEqual(
            scalar(
                self.users_db,
                "select count(*) from users where userName = 'validuser'",
            ),
            1,
        )

    def test_wb_createpost_redirects_when_user_is_not_logged_in(self):
        client = self.createpost_client()
        with client.session_transaction() as session:
            session["language"] = "en"

        response = client.get("/createpost")

        self.assertEqual(response.status_code, 302)
        self.assertIn("/login/", response.location)

    def test_wb_createpost_empty_content_does_not_insert_post(self):
        client = self.createpost_client()
        with client.session_transaction() as session:
            session["language"] = "en"
            session["userName"] = "alice"

        response = client.post(
            "/createpost",
            data={
                "postTitle": "Valid Blog Title",
                "postTags": "flask,test",
                "postContent": "",
                "postCategory": "Code",
                "postBanner": (io.BytesIO(b"banner"), "banner.png"),
            },
            content_type="multipart/form-data",
        )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(scalar(self.posts_db, "select count(*) from posts"), 0)

    def test_wb_createpost_valid_input_inserts_post(self):
        client = self.createpost_client()
        with client.session_transaction() as session:
            session["language"] = "en"
            session["userName"] = "alice"

        response = client.post(
            "/createpost",
            data={
                "postTitle": "Valid Blog Title",
                "postTags": "flask,test",
                "postContent": (
                    "This is a long enough content body for the article creation "
                    "positive path."
                ),
                "postCategory": "Code",
                "postBanner": (io.BytesIO(b"banner"), "banner.png"),
            },
            content_type="multipart/form-data",
        )

        self.assertEqual(response.status_code, 302)
        self.assertEqual(scalar(self.posts_db, "select count(*) from posts"), 1)


if __name__ == "__main__":
    unittest.main(verbosity=2)
