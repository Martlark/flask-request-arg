from flask import Flask, Response

from request_arg import request_arg


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
    @request_arg("optional_string_value", arg_default="")
    def route_string(string_value, optional_string_value):
        return f"""
        <p>string_value:{string_value}</p>
        <p>optional_string_value:{optional_string_value}</p>
        """

    @request_arg("radius", float)
    def area_of_circle(radius):
        result = radius * radius * 3.14
        return Response(f"{result}", 200)

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

    app.add_url_rule("/post", view_func=route_int_float, methods=["POST"])
    app.add_url_rule("/get", view_func=route_int_float, methods=["GET"])
    app.add_url_rule("/put_json", view_func=route_int_float, methods=["PUT"])
    # string with optional string

    app.add_url_rule("/post_string", view_func=route_string, methods=["POST"])
    app.add_url_rule("/get_string", view_func=route_string, methods=["GET"])
    return app
