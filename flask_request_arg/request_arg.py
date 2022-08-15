from functools import wraps
from http import HTTPStatus
from typing import Any, Callable

from flask import request, abort, Response


TRUTHY_VALUES = ("y", "Y", "yes", "Yes", "YES", True, "true", "True", "TRUE", 1, "1")


def is_truthy(value: Any) -> bool:
    """
    return True if value seems to be a true value.
    :param value:
    :return: True or False
    """
    return value in TRUTHY_VALUES


def request_arg(arg_name: str, arg_type: Any = None, arg_default=None) -> Callable:
    """
    decorator to auto convert argument, json body or form fields to
    named method parameters with the correct type
    conversion. Example:

        @route('/something/<greeting>/')
        @flask_request_arg('repeat', int, 1)
        def route_something(greeting='', repeat):
            return greeting * repeat

        # /something/yo/?repeat=10

        # yoyoyoyoyoyoyoyoyoyo


    :param arg_name: name of the form field or arg
    :param arg_type: (optional) the type to convert to
    :param arg_default: (optional) a default value.  Use '' or 0 when allowing optional fields
    :return: a decorator
    """

    def decorator(f):
        @wraps(f)
        def decorated(*args, **kwargs):
            arg_value = None
            if request.content_type == "application/json":
                # json body
                json_data = request.get_json()
                arg_value = json_data.get(arg_name, arg_default)

            # form or parameter arguments
            if arg_value is None:
                arg_value = (
                    request.form.get(arg_name)
                    or request.args.get(arg_name)
                    or arg_default
                )

            if arg_value is not None:
                if arg_type:
                    try:
                        if arg_type == bool:
                            arg_value = is_truthy(arg_value)
                        arg_value = arg_type(arg_value)
                    except Exception as e:
                        abort(
                            Response(
                                f"""Required argument failed type conversion: {arg_name}, {str(e)}""",
                                status=HTTPStatus.BAD_REQUEST,
                            )
                        )

                kwargs[arg_name] = arg_value
                return f(*args, **kwargs)
            abort(
                Response(
                    f"""Required argument missing: {arg_name}""",
                    status=HTTPStatus.BAD_REQUEST,
                )
            )

        return decorated

    return decorator
