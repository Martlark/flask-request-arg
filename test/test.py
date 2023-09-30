import unittest
from http import HTTPStatus

from test.flask_test_app import create_app


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
        header_value = "9xx9839"
        r = self.app.post(
            "/post",
            data=dict(int_value=int_value, float_value=float_value),
            headers={"header_value": header_value},
        )
        self.assertEqual(HTTPStatus.OK, r.status_code)
        self.assertInHTML(f"int_value:{int_value}", r)
        self.assertInHTML(f"float_value:{float_value}", r)
        self.assertInHTML(f"header_value:{header_value}", r)

    def test_put_json(self):
        float_value = 123.456
        int_value = 43987439
        r = self.app.put(
            "/put_json",
            json=dict(int_value=int_value, float_value=float_value),
            content_type="application/json",
        )
        self.assertEqual(HTTPStatus.OK, r.status_code, r.data)
        self.assertInHTML(f"int_value:{int_value}", r)
        self.assertInHTML(f"float_value:{float_value}", r)

    def test_default(self):

        # string
        string_value = "12345"
        r = self.app.get("/get_string_default")
        self.assertEqual(HTTPStatus.OK, r.status_code)
        self.assertInHTML(f"string_value:{string_value}", r)

        r = self.app.put("/put_string_default")
        self.assertEqual(HTTPStatus.OK, r.status_code)
        self.assertInHTML(f"string_value:{string_value}", r)

        r = self.app.post("/post_string_default")
        self.assertEqual(HTTPStatus.OK, r.status_code)
        self.assertInHTML(f"string_value:{string_value}", r)

    def test_get(self):
        float_value = 123.456
        int_value = 43987439
        string_value = "o4iuuo34u390jsfdsf"
        optional_string_value = "ooiiu43hssh"
        r = self.app.get(
            "/get",
            data=dict(
                int_value=int_value, float_value=float_value, header_value=string_value
            ),
        )
        self.assertEqual(HTTPStatus.OK, r.status_code)
        self.assertInHTML(f"int_value:{int_value}", r)
        self.assertInHTML(f"float_value:{float_value}", r)
        self.assertInHTML(f"header_value:{string_value}", r)

        # string

        r = self.app.get("/get_string", data=dict(string_value=string_value))
        self.assertEqual(HTTPStatus.OK, r.status_code)
        self.assertInHTML(f"string_value:{string_value}", r)
        self.assertInHTML(f"<p>optional_string_value:</p>", r)
        # optional value
        r = self.app.get(
            "/get_string",
            data=dict(
                string_value=string_value, optional_string_value=optional_string_value
            ),
        )
        self.assertEqual(HTTPStatus.OK, r.status_code)
        self.assertInHTML(f"string_value:{string_value}", r)
        self.assertInHTML(f"<p>optional_string_value:{optional_string_value}</p>", r)

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

        # PUT json

        r = self.app.put(
            "/put_json",
            json=dict(float_value=float_value),
            content_type="application/json",
        )
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

    def test_readme_example(self):
        r = self.app.get("/area_of_a_circle", data=dict(radius=1))
        self.assertEqual(b"3.14", r.data)
        r = self.app.put("/area_of_a_circle", json=dict(radius=1))
        self.assertEqual(b"3.14", r.data)
        r = self.app.post("/area_of_a_circle", data=dict(radius=1))
        self.assertEqual(b"3.14", r.data)
        r = self.app.put("/area_of_a_circle", data=dict(radius=1))
        self.assertEqual(b"3.14", r.data)

    def test_custom_arg_type(self):
        r = self.app.get("/custom_arg_type", data=dict(arg_type=True))
        self.assertEqual(b"yes", r.data)
        r = self.app.put(
            "/custom_arg_type",
            json=dict(arg_type=False),
            content_type="application/json",
        )
        self.assertEqual(b"no", r.data)
        r = self.app.put("/custom_arg_type", json=dict(arg_type="False"))
        self.assertEqual(b"no", r.data)
        r = self.app.put("/custom_arg_type", json=dict(arg_type="True"))
        self.assertEqual(b"yes", r.data)
        r = self.app.put("/custom_arg_type", json=dict(arg_type="true"))
        self.assertEqual(b"no", r.data)

    def test_get_json_arg_form(self):
        float_value = 123.456
        int_value = 43987439
        r = self.app.get(
            f"/get?int_value={int_value}", json=dict(float_value=float_value)
        )
        self.assertEqual(HTTPStatus.OK, r.status_code, r.data)
        self.assertInHTML(f"int_value:{int_value}", r)
        self.assertInHTML(f"float_value:{float_value}", r)

    def test_bool(self):

        for test_value in [True, "Yes", "Y", 1, "True", "true", "TRUE"]:
            r = self.app.get("/is_it_true", data=dict(the_truth=test_value))
            self.assertEqual(b"True", r.data)

        for test_value in [False, "No", "N", 0, "Frlong"]:
            r = self.app.get("/is_it_true", data=dict(the_truth=test_value))
            self.assertEqual(b"False", r.data)
