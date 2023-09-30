from flask import Flask, Response

from flask_request_arg import request_arg


def create_app():
    app = Flask("test")
    app.config["TESTING"] = True

    @request_arg("int_value", int)
    @request_arg("float_value", float)
    @request_arg("Header-Value", str, arg_default="")
    def route_int_float_str(int_value, float_value, header_value):
        return f"""
        <p>int_value:{int_value}</p>
        <p>float_value:{float_value}</p>
        <p>header_value:{header_value}</p>
        """

    @request_arg("string_value")
    @request_arg("optional_string_value", arg_default="")
    def route_string(string_value, optional_string_value):
        return f"""
        <p>string_value:{string_value}</p>
        <p>optional_string_value:{optional_string_value}</p>
        """

    @request_arg("string_value", arg_default="12345")
    def route_default(string_value):
        return f"""
        <p>string_value:{string_value}</p>
        """

    @request_arg("radius", float)
    def area_of_circle(radius):
        result = radius * radius * 3.14
        return Response(f"{result}", 200)

    @request_arg("the_truth", bool)
    def is_it_true(the_truth):
        return Response(f"{the_truth}", 200)

    app.add_url_rule(
        "/area_of_a_circle", view_func=area_of_circle, methods=["GET", "POST", "PUT"]
    )

    @request_arg("arg_type", lambda x: x == "True")
    def custom_arg_type(arg_type):
        result = "yes" if arg_type else "no"
        return Response(f"{result}", 200)

    app.add_url_rule(
        "/custom_arg_type", view_func=custom_arg_type, methods=["GET", "POST", "PUT"]
    )

    # int and float

    app.add_url_rule("/post", view_func=route_int_float_str, methods=["POST"])
    app.add_url_rule("/get", view_func=route_int_float_str, methods=["GET"])
    app.add_url_rule("/put_json", view_func=route_int_float_str, methods=["PUT"])
    # string with optional string

    app.add_url_rule("/post_string", view_func=route_string, methods=["POST"])
    app.add_url_rule("/get_string", view_func=route_string, methods=["GET"])

    app.add_url_rule("/post_string_default", view_func=route_default, methods=["POST"])
    app.add_url_rule("/get_string_default", view_func=route_default, methods=["GET"])
    app.add_url_rule("/put_string_default", view_func=route_default, methods=["PUT"])

    app.add_url_rule("/is_it_true", view_func=is_it_true, methods=["GET"])
    return app
