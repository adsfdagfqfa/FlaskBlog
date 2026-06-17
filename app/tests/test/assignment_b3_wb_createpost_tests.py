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


class CreatePostWhiteBoxTests(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory(ignore_cleanup_errors=True)
        self.posts_db = str(Path(self.temp_dir.name) / "posts.db")
        create_posts_db(self.posts_db)

        import settings

        settings.DB_POSTS_ROOT = self.posts_db

    def tearDown(self):
        self.temp_dir.cleanup()

    def client(self):
        import routes.createPost as createpost_mod

        createpost_mod.DB_POSTS_ROOT = self.posts_db
        createpost_mod.Log = SilentLog
        createpost_mod.flashMessage = lambda **kwargs: None
        createpost_mod.addPoints = lambda *args, **kwargs: None
        createpost_mod.render_template = lambda *args, **kwargs: "create page"

        app = Flask("createpost-whitebox-test")
        app.secret_key = "test"
        app.testing = True
        app.register_blueprint(createpost_mod.createPostBlueprint)
        return app.test_client()

    def test_wb_create_01_redirects_when_user_is_not_logged_in(self):
        client = self.client()
        with client.session_transaction() as session:
            session["language"] = "en"

        response = client.get("/createpost")

        self.assertEqual(response.status_code, 302)
        self.assertIn("/login/redirect=&createpost", response.location)

    def test_wb_create_02_logged_in_get_renders_page(self):
        client = self.client()
        with client.session_transaction() as session:
            session["language"] = "en"
            session["userName"] = "alice"

        response = client.get("/createpost")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.text, "create page")

    def test_wb_create_03_empty_content_does_not_insert_post(self):
        client = self.client()
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

    def test_wb_create_04_valid_input_inserts_post(self):
        client = self.client()
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
