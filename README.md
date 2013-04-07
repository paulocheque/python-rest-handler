python-rest-handler
====================

![Continuous Integration Status](https://secure.travis-ci.org/paulocheque/python-rest-handler.png)

A simple and abstract library to create Rest Handlers for different Web frameworks and ORMs.

This project was born from **Tornado Rest Handler** (https://github.com/paulocheque/tornado-rest-handler). It is an abstract layer of that project to allow the code be used by another Web frameworks.

* [Basic Example of Usage](#basic-example-of-usage)
  * [Routes](#routes)
  * [Handlers](#handlers)
  * [Request Managers](#request-managers)
  * [Data Managers](#data-managers)
  * [Templates](#templates)
* [Plugins](#plugins)
* [Installation](#installation)
* [Change Log](#change-log)
* [TODO](#todo)

Basic Example of Usage
------------------------

Check the project **Tornado Rest Handler** (https://github.com/paulocheque/tornado-rest-handler) for a real example.

With +-10 lines of code you can create a handler for your ORM.

Routes
------------------------

One handler manage every Rest routes:

| Method       | Route               | Comment |
|------------- |---------------------|---------|
| GET          | /animal index       | display a list of all animals |
| GET          | /animal/new         | new return an HTML form for creating a new animal |
| POST         | /animal             | create a new animal |
| GET          | /animal/:id         | show an animal |
| GET          | /animal/:id/edit    | return an HTML form for editing a photo |
| PUT          | /animal/:id         | update an animal data |
| DELETE       | /animal/:id         | delete an animal |
| POST*        | /animals/:id/delete | same as DELETE /animals/:id |
| POST*        | /animals/:id        | same as PUT /animals/:id |

*Since HTML5-forms does not support PUT/DELETE, these additional POSTs were added.

To specify the Rest routes in your Web framework you can use the method **rest_routes**:

In the sections *Handlers*, *Request Managers* and *Data Managers* you get information of how to create a **SomeImplementationOfRestHandler** class.

```python
import python_rest_handler
python_rest_handler.RestHandler

class SomeImplementationOfRestHandler(…): pass

ROUTES = [
    # another handlers here

    python_rest_handler.rest_routes(Animal, handler=SomeImplementationOfRestHandler),

    # another handlers here
]
ROUTES = python_rest_handler.routes(ROUTES)
```

The library does not support auto-pluralization yet, so you may want to change the prefix:

```python
rest_routes(Animal, prefix='animals'),
```

You can also define to where will be redirect after an action succeed:

```python
rest_routes(Animal, prefix='animals', redirect_pos_action='/animals'),
```

Handlers
------------------------

All the get/post/put/delete methods are implemented for you, but if you want to customize some behavior, you write your own handler:

```python
class AnimalHandler(RestHandler):
    pass # your custom methods here
```

And then, registered it:

```python
rest_routes(Animal, handler=AnimalHandler),
```

Just be sure that a RestHandler **requires** a RequestManager and a DataManager, but this library does not offer any one of those. 

But sections *Request Managers* and *Data Managers* will give details of how you can implement them.

But you want a real example, you can check the library **Tornado Rest Handler** (https://github.com/paulocheque/tornado-rest-handler).

Request Managers
------------------------

To create a Request Manager for your Web Framework, you must override the **RequestManager** class and implement the following methods:

```python
from python_rest_handler import RestHandler, DataManager, RequestManager

class MyWebFrameworkRequestManager(RequestManager):
    def raise403(self): pass
    def raise404(self): pass
    def get_request_data(self): return {}
    def render(self, template_name, **kwargs): pass
    def redirect(self, url, permanent=False, status=None, **kwargs): pass
```

After that, you may use thie Request Manager in any RestHandler you want to:

```python
class MyRestHandler(RestHandler):
    request_manager = MyWebFrameworkRequestManager
```

Data Managers
------------------------

To create a Data Manager for your ORM you must override the **DataManager** class and implement the following methods:

```python
from python_rest_handler import RestHandler, DataManager, RequestManager

class MyDataManager(DataManager):
    def instance_list(self): return []
    def find_instance_by_id(self, instance_id): pass
    def save_instance(self, data): pass
    def update_instance(self, instance, data): pass
    def delete_instance(self, instance): pass
```

After that, you may use thie Request Manager in any RestHandler you want to:

```python
class MyRestHandler(RestHandler):
    data_manager = MyWebFrameworkRequestManager
```

Tip: You can create a general data manager, and let the user subclass your DataManager when he/shw wants to customize some behavior, for example:

```python
class AnimalDataManager(MyDataManager):
    def instance_list(self):
        return Animal.objects.filter(...)
```


Templates
------------------------

You must create your own template. Templates will receive the variables **obj** or **objs** and **alert** in case there is some message. The edit template will also receive the variable **errors** and functions **value_for**, **error_for** and **has_error**.

It must have the names list.html, show.html and edit.html. But you can customize if you want to:

```python
rest_routes(Animal, list_template='another_name.html', edit_template='...', show_template='...'),
```

By default, the directory is the model name in lower case (animal in this example).

* animal/list.html
* animal/show.html
* animal/edit.html

But you may change the directory though:

```python
rest_routes(Animal, template_path='your_template_path'),
```


Plugins
------------
You can pass additional functions to your templates. This library include functions that generate widgets according to a Twitter-Bootstrap template.

TODO: complete documentation here

```python
from python_rest_handler.plugins.bootstrap import *
```


Installation
------------

```
pip install python-rest-handler
```

#### or

```
1. Download zip file
2. Extract it
3. Execute in the extracted directory: python setup.py install
```

#### Development version

```
pip install -e git+git@github.com:paulocheque/python-rest-handler.git#egg=python-rest-handler
```

#### requirements.txt

```
python-rest-handler==0.0.1
# or use the development version
git+git://github.com/paulocheque/python-rest-handler.git#egg=python-rest-handler
```

#### Upgrade:

```
pip install python-rest-handler --upgrade --no-deps
```

#### Requirements

* Python 2.6 / 2.7 / 3.2 / 3.3


Change Log
-------------

#### 0.0.1 (2013/03/30)

* [important] This project is an abstraction of tornado-rest-handler. Now tornado-rest-handler will use this project.
* [new] It has all features of tornado-rest-handler 0.0.5 (besides the Tornado Request Manager and MongoEngine Data Manager)
* [new] Plugin support
* [new] Bootstrap plugin: input_field, password_field, select_field, button


TODO
-------------

* Pagination
* i18n
* pluralize urls

