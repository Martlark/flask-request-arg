flask-request-arg
=================

Easy way to convert Flask request form and args to route parameters.

Introduction
------------

Handling `form` and `request` and `header` parameters in `Flask` is complex and error-prone. Common 
issues are:

 * Values need to be converted to the correct type.
 * Intricate logic used to handle defaults and missing values.
 * Request arguments and form fields are not clear from the method signature.
 * GET, PUT, POST all require different logic to get values.
 * Documentation for request and form values are not easy to generate.

`flask-request-arg` solves this issues by allowing you to use a simple decorator
to specify the argument name, type and default value.  Then any form data, JSOM
data, header or request argument is converted into a named method parameter.  POST using form 
data, GET using arguments or PUT with JSON body data all can use the same
code logic.

Installation
------------

pip install flask-request-arg

Usage
-----

```python

@request_arg(arg_name: str, arg_type: Any = None, arg_default=None) -> Callable:
```

* `arg_name` - the name of the argument to add as a method parameter.
* `arg_type` - the type of the argument.  All form and request args are usually strings.
* `arg_default`  - default value of the argument when not in form or request.

### Notes

 * to make an argument required do not provide an `arg_default`.
 * a `<form>` `<input>` `name` must match the `request_arg` argument name.
 * a JSON body key must match the `request_arg` argument name.
 * any request argument name must be a valid `Python` variable name.

Example
-------

To call an area of circle method with a parameter argument as in this example:

```
   /area_of_circle?radius=23.456
   
   # 1727.57755904
```

Structure your Flask route as follows:

```python
from flask_request_arg import request_arg
from flask import Response


@request_arg('radius', float)
@app.route('/area_of_circle', methods=['GET'])
def area_of_circle(radius):
    result = radius * radius * 3.14
    return Response(f"{result}", 200)
```

Forms
-----

A method that handles POST can be structured the same as a GET. Example:

```python
from flask_request_arg import request_arg
from flask import Response


@request_arg('radius', float)
@app.route('/area_of_circle', methods=['POST'])
def area_of_circle(radius):
    result = radius * radius * 3.14
    return Response(f"{result}", 200)
```

HTML example:

```html
<form action="/area_of_circle" method="post">
    <label>Radius:<input name="radius" type="number"/></label>
    <button type="submit">Get area</button>
</form>
```
NOTE: the form input name must match the `request_arg` argument name.

NOTE: request arguments and form data can be used together on the same request.

JSON Data
---------

JSON body data is treated the same as a POST or GET. Example:

```python
from flask_request_arg import request_arg
from flask import Response


@request_arg('radius', float)
@app.route('/area_of_circle', methods=['PUT'])
def area_of_circle(radius):
    result = radius * radius * 3.14
    return Response(f"{result}", 200)
```

Called like:

```javascript
fetch('/area_of_circle', {
  headers: { 'Content-Type': 'application/json' }, // tells the server we have json
  method:'PUT', 
  body: JSON.stringify({radius:45.67}), // json is sent to the server as text
})
```

NOTE: request arguments and JSON body data can be used together on the same request.

As you can see the `Flask` method code is the same for GET, PUT and POST.  So you can
do all three at once. Example:

```python
from flask_request_arg import request_arg
from flask import Response


@request_arg('radius', float)
@app.route('/area_of_circle', methods=['GET', 'PUT', 'POST'])
def area_of_circle(radius):
    result = radius * radius * 3.14
    return Response(f"{result}", 200)
```

Request arguments
-----------------

Request arguments of the type 

   `/route?argument1=value1&argument2=value2` 
   
are treated the same as `form` or `JSON` data. Example:

```python
from flask_request_arg import request_arg
from flask import Response


# /area_of_circle?radius=124.56

@request_arg('radius', float)
@app.route('/area_of_circle')
def area_of_circle(radius):
    result = radius * radius * 3.14
    return Response(f"{result}", 200)
```

Request headers
---------------

Request headers of the format:

   `header-name: values here and here` 
   
are treated the same as `form`, `parameters` or `JSON` data.



Converting values
-----------------

Use the `arg_type` parameter to specify a type conversion for the string value.

The arg_type can be any Python type.  The default is`str`.  Example:

```python
from flask_request_arg import request_arg
from flask import Response


@request_arg('radius', float)
@request_arg('number_of_circles', int)
@request_arg('name', str)
@app.route('/area_of_circle', methods=['GET'])
def area_of_circle(radius, number_of_circles, name):
    result = number_of_circles * radius * radius * 3.14
    return Response(f"{number_of_circles} of {name} is {result}", 200)
```

Custom type converters can be supplied using a `lambda`.  Example: 

```python
    @request_arg("arg_type", lambda x: x == "True")
    @app.route('/custom')
    def custom_arg_type(arg_type):
        result = "yes" if arg_type else "no"
        return Response(f"{result}", 200)
```
 
When using `bool` as an `arg_type`, a _truthy_ test will be done and 
return `True` if the value is in:

```python

    ("y", "Y", "yes", "Yes", "YES", True, "true", "True", "TRUE", 1, "1")

```

Mixing parameters
-----------------

If required, you can mix Flask request parameters with request arguments.  Example:

```python
from flask_request_arg import request_arg
from flask import Response


@request_arg('radius', float)
@app.route('/area_of_circle/<float:pi>/', methods=['GET'])
def area_of_circle(pi, radius):
    result = radius * radius * pi
    return Response(f"{result}", 200)
```


Release history
---------------

* 1.0.2 - Add header support
* 1.0.2 - Fix publish
* 1.0.1 - Use truthy values for `bool` types
* 1.0.0 - Tidy up documentation.  Proper release.
* 0.0.2 - Initial release
