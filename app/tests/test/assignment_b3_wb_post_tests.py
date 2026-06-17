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
    connection.execute(
        """
        insert into posts(title,tags,content,banner,author,views,timeStamp,lastEditTimeStamp,category,urlID)
        values(?,?,?,?,?,?,?,?,?,?)
        """,
        (
            "Valid Blog Title",
            "flask,test",
            "This article body is long enough for read-time calculation.",
            b"banner",
            "alice",
            0,
            1,
            1,
            "Code",
            "abc123",
        ),
    )
    connection.commit()
    connection.close()


def create_comments_db(path):
    connection = sqlite3.connect(path)
    connection.execute(
        """
        create table comments(
            id integer primary key autoincrement,
            post integer,
            comment text,
            user text,
            timeStamp integer
        )
        """
    )
    connection.execute(
        """
        insert into comments(post,comment,user,timeStamp)
        values(?,?,?,?)
        """,
        (1, "Existing comment", "bob", 1),
    )
    connection.commit()
    connection.close()


def create_analytics_db(path):
    connection = sqlite3.connect(path)
    connection.execute(
        """
        create table postsAnalytics(
            id integer primary key autoincrement,
            postID integer,
            visitorUserName text,
            country text,
            os text,
            continent text,
            timeSpendDuration integer default 0,
            timeStamp integer
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


class PostWhiteBoxTests(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory(ignore_cleanup_errors=True)
        self.posts_db = str(Path(self.temp_dir.name) / "posts.db")
        self.comments_db = str(Path(self.temp_dir.name) / "comments.db")
        self.analytics_db = str(Path(self.temp_dir.name) / "analytics.db")
        create_posts_db(self.posts_db)
        create_comments_db(self.comments_db)
        create_analytics_db(self.analytics_db)

        self.analytics_enabled = False
        self.deleted_posts = []
        self.deleted_comments = []
        self.user_ip_data = {
            "status": 0,
            "payload": {
                "country": "Testland",
                "os": "TestOS",
                "continent": "Testinent",
            },
        }

        import settings

        settings.DB_POSTS_ROOT = self.posts_db
        settings.DB_COMMENTS_ROOT = self.comments_db
        settings.DB_ANALYTICS_ROOT = self.analytics_db
        settings.ANALYTICS = False

    def tearDown(self):
        self.temp_dir.cleanup()

    def client(self):
        import routes.post as post_mod

        test_case = self

        class FakeDelete:
            @staticmethod
            def post(post_id):
                test_case.deleted_posts.append(post_id)

            @staticmethod
            def comment(comment_id):
                test_case.deleted_comments.append(comment_id)

        post_mod.DB_POSTS_ROOT = self.posts_db
        post_mod.DB_COMMENTS_ROOT = self.comments_db
        post_mod.DB_ANALYTICS_ROOT = self.analytics_db
        post_mod.ANALYTICS = self.analytics_enabled
        post_mod.Delete = FakeDelete
        post_mod.Log = SilentLog
        post_mod.flashMessage = lambda **kwargs: None
        post_mod.addPoints = lambda *args, **kwargs: None
        post_mod.getDataFromUserIP = lambda *args, **kwargs: self.user_ip_data
        post_mod.render_template = lambda template, **kwargs: f"{template}:{kwargs.get('views', '')}"

        app = Flask("post-whitebox-test")
        app.secret_key = "test"
        app.testing = True
        app.register_blueprint(post_mod.postBlueprint)
        return app.test_client()

    def test_wb_post_01_missing_post_renders_not_found_page(self):
        client = self.client()
        with client.session_transaction() as session:
            session["language"] = "en"

        response = client.get("/post/missing")

        self.assertEqual(response.status_code, 200)
        self.assertIn("notFound.html", response.text)

    def test_wb_post_02_slugless_existing_post_redirects_to_slug_url(self):
        client = self.client()
        with client.session_transaction() as session:
            session["language"] = "en"

        response = client.get("/post/abc123")

        self.assertEqual(response.status_code, 302)
        self.assertIn("/post/valid-blog-title-abc123", response.location)

    def test_wb_post_03_existing_post_renders_and_increments_views(self):
        client = self.client()
        with client.session_transaction() as session:
            session["language"] = "en"

        response = client.get("/post/valid-blog-title-abc123")

        self.assertEqual(response.status_code, 200)
        self.assertIn("post.html", response.text)
        self.assertEqual(
            scalar(self.posts_db, "select views from posts where urlID = ?", ("abc123",)),
            1,
        )

    def test_wb_post_04_post_delete_button_redirects_home(self):
        client = self.client()
        with client.session_transaction() as session:
            session["language"] = "en"
            session["userName"] = "alice"

        response = client.post(
            "/post/valid-blog-title-abc123",
            data={"postDeleteButton": "1"},
        )

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.location, "/")
        self.assertEqual(self.deleted_posts, [1])

    def test_wb_post_05_comment_delete_button_redirects_to_post(self):
        client = self.client()
        with client.session_transaction() as session:
            session["language"] = "en"
            session["userName"] = "alice"

        response = client.post(
            "/post/valid-blog-title-abc123",
            data={"commentDeleteButton": "1", "commentID": "1"},
        )

        self.assertEqual(response.status_code, 301)
        self.assertIn("/post/abc123", response.location)
        self.assertEqual(self.deleted_comments, ["1"])

    def test_wb_post_06_logged_in_comment_is_inserted(self):
        client = self.client()
        with client.session_transaction() as session:
            session["language"] = "en"
            session["userName"] = "alice"

        response = client.post(
            "/post/valid-blog-title-abc123",
            data={"comment": "This is a useful comment for the test case."},
        )

        self.assertEqual(response.status_code, 301)
        self.assertEqual(
            scalar(
                self.comments_db,
                "select count(*) from comments where user = ?",
                ("alice",),
            ),
            1,
        )

    def test_wb_post_07_comment_without_login_is_handled_safely(self):
        client = self.client()
        with client.session_transaction() as session:
            session["language"] = "en"

        response = client.post(
            "/post/valid-blog-title-abc123",
            data={"comment": "Anonymous comment should not crash the route."},
        )

        self.assertIn(response.status_code, (200, 301, 302, 401, 403))
        self.assertEqual(
            scalar(
                self.comments_db,
                "select count(*) from comments where comment = ?",
                ("Anonymous comment should not crash the route.",),
            ),
            0,
        )

    def test_wb_post_08_analytics_logged_in_success_inserts_row(self):
        self.analytics_enabled = True
        client = self.client()
        with client.session_transaction() as session:
            session["language"] = "en"
            session["userName"] = "alice"

        response = client.get("/post/valid-blog-title-abc123")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            scalar(
                self.analytics_db,
                "select count(*) from postsAnalytics where visitorUserName = ?",
                ("alice",),
            ),
            1,
        )

    def test_wb_post_09_analytics_anonymous_success_inserts_unsigned_user(self):
        self.analytics_enabled = True
        client = self.client()
        with client.session_transaction() as session:
            session["language"] = "en"

        response = client.get("/post/valid-blog-title-abc123")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            scalar(
                self.analytics_db,
                "select count(*) from postsAnalytics where visitorUserName = ?",
                ("unsignedUser",),
            ),
            1,
        )

    def test_wb_post_10_analytics_failure_still_renders_page(self):
        self.analytics_enabled = True
        self.user_ip_data = {"status": 1, "message": "lookup failed"}
        client = self.client()
        with client.session_transaction() as session:
            session["language"] = "en"

        response = client.get("/post/valid-blog-title-abc123")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            scalar(self.analytics_db, "select count(*) from postsAnalytics"),
            0,
        )


if __name__ == "__main__":
    unittest.main(verbosity=2)
