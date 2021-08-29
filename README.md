flask-request-arg
=================

Easy way to convert Flask request form and args to route parameters.

Introduction
------------

Handling `form` and `request` parameters in `Flask` is complex and error-prone. Common 
issues are:

 * Values need to be converted to the correct type.
 * intricate logic used to handle defaults and missing values.
 * Parameter and form fields are not clear from the method signature.
 * GET, PUT, POST all require different logic to get values.

`flask-request-arg` solves this issues by allowing you to use a simple decorator
to specify the argument name, type and default value.  Then any form data, json
data or request parameter is converted into a named method parameter.  POST using form 
data, GET using parameters or PUT with JSON body data all can use the same
code logic.

Installation
------------

pip install flask-request-arg

Usage
-----

To call an area of circle method with a parameter argument as in this example:

```
   /area_of_circle?radius=23.456
   
   # 1727.57755904
```

Structure your Flask route as follows:

```python
from request_arg import request_arg
from flask import Response

@request_arg('radius', float)
@app.route('/area_of_circle', methods=['GET'])
def area_of_circle(radius):
    result = radius * radius * 3.14
    return Response(f"{result}", 200)
```

Release history
---------------

1.0.0
