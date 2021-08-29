import unittest

from flask import Flask

from request_arg import request_arg
from http import HTTPStatus


def create_app():
    app = Flask("test")
    app.config["TESTING"] = True

    @request_arg("int_value", int)
    @request_arg("float_value", float)
    def route_int_float(int_value, float_value):
        return f"""
        <p>int_value:{int_value}</p>
        <p>float_value:{float_value}</p>
        """

    @request_arg("string_value")
    def route_string(string_value):
        return f"""
        <p>string_value:{string_value}</p>
        """

    app.add_url_rule("/post", view_func=route_int_float, methods=["POST"])
    app.add_url_rule("/get", view_func=route_int_float, methods=["GET"])

    app.add_url_rule("/post_string", view_func=route_string, methods=["POST"])
    app.add_url_rule("/get_string", view_func=route_string, methods=["GET"])
    return app


class TestRequestArg(unittest.TestCase):
    def assertInHTML(self, value, response):
        HTML_text = response.data.decode("utf-8")
        self.assertIn(value, HTML_text)

    def setUp(self) -> None:
        _app = create_app()
        self.app = _app.test_client()

    def test_post(self):
        float_value = 123.456
        int_value = 43987439
        r = self.app.post(
            "/post", data=dict(int_value=int_value, float_value=float_value)
        )
        self.assertEqual(HTTPStatus.OK, r.status_code)
        self.assertInHTML(f"int_value:{int_value}", r)
        self.assertInHTML(f"float_value:{float_value}", r)

    def test_get(self):
        float_value = 123.456
        int_value = 43987439
        string_value = "o4iuuo34u390jsfdsf"
        r = self.app.get(
            "/get", data=dict(int_value=int_value, float_value=float_value)
        )
        self.assertEqual(HTTPStatus.OK, r.status_code)
        self.assertInHTML(f"int_value:{int_value}", r)
        self.assertInHTML(f"float_value:{float_value}", r)

        # string

        r = self.app.get("/get_string", data=dict(string_value=string_value))
        self.assertEqual(HTTPStatus.OK, r.status_code)
        self.assertInHTML(f"string_value:{string_value}", r)

        r = self.app.post("/post_string", data=dict(string_value=string_value))
        self.assertEqual(HTTPStatus.OK, r.status_code)
        self.assertInHTML(f"string_value:{string_value}", r)

    def test_argument_missing(self):
        float_value = 123.456
        int_value = 43987439

        # GET

        r = self.app.get("/get", data=dict(int_value=int_value))
        self.assertEqual(HTTPStatus.BAD_REQUEST, r.status_code)
        self.assertEqual(b"Required argument missing: float_value", r.data)
        r = self.app.get("/get", data=dict(float_value=float_value))
        self.assertEqual(HTTPStatus.BAD_REQUEST, r.status_code)
        self.assertEqual(b"Required argument missing: int_value", r.data)

        # POST

        r = self.app.post("/post", data=dict(int_value=int_value))
        self.assertEqual(HTTPStatus.BAD_REQUEST, r.status_code)
        self.assertEqual(b"Required argument missing: float_value", r.data)
        r = self.app.post("/post", data=dict(float_value=float_value))
        self.assertEqual(HTTPStatus.BAD_REQUEST, r.status_code)
        self.assertEqual(b"Required argument missing: int_value", r.data)

    def test_invalid_cast(self):
        float_value = 123.456
        int_value = 43987439

        # GET

        r = self.app.get(
            "/get", data=dict(int_value=float_value, float_value=float_value)
        )
        self.assertEqual(HTTPStatus.BAD_REQUEST, r.status_code)
        self.assertIn(b"Required argument failed type conversion: int_value", r.data)
        r = self.app.get("/get", data=dict(float_value="hello", int_value=int_value))
        self.assertEqual(HTTPStatus.BAD_REQUEST, r.status_code)
        self.assertIn(b"Required argument failed type conversion: float_value", r.data)

        # POST

        r = self.app.post(
            "/post", data=dict(int_value=float_value, float_value=float_value)
        )
        self.assertEqual(HTTPStatus.BAD_REQUEST, r.status_code)
        self.assertIn(b"Required argument failed type conversion: int_value", r.data)
        r = self.app.post("/post", data=dict(float_value="hello", int_value=int_value))
        self.assertEqual(HTTPStatus.BAD_REQUEST, r.status_code)
        self.assertIn(b"Required argument failed type conversion: float_value", r.data)
