python-rest-handler
====================

![Continuous Integration Status](https://secure.travis-ci.org/paulocheque/python-rest-handler.png)

#### Latest version: 0.0.2 (2013/04/28)

A simple and abstract library to create Rest Handlers for different Web frameworks and ORMs.

This project was born from **Tornado Rest Handler** (https://github.com/paulocheque/tornado-rest-handler). It is an abstract layer of that project to allow the code be used by another Web frameworks.

* [Basic Example of Usage](#basic-example-of-usage)
  * [Routes](#routes)
  * [Data Managers](#data-managers)
  * [Handlers](#handlers)
  * [Templates](#templates)
* [Plugins](#plugins)
* [Installation](#installation)
* [Change Log](#change-log)
* [TODO](#todo)

Basic Example of Usage
------------------------

To use the rest handler logic, it is necessary to implement a **python_rest_handler.RestRequestHandler** class and at least one **DataManager**. Then it is possible to use the **rest_routes** fabric method or it is possible to inherit your request handler manually. Check the next sections for more details.

PS: The project **Tornado Rest Handler** (https://github.com/paulocheque/tornado-rest-handler) contains a real example.

Handlers
------------------------

To create a handler for your Web framework, you need to create a subclass of **RestRequestHandler**

```python
import python_rest_handler

class YourRequestRestHandler(YOUR_FRAMEWORK_BASE_HANDLER, python_rest_handler.RestRequestHandler):
    def raise403(self): pass
    def raise404(self): pass
    def get_request_uri(self): pass
    def get_request_data(self): return {}
    def render(self, template_name, **kwargs): pass
    def redirect(self, url, permanent=False, status=None, **kwargs): pass
```

All the get/post/put/delete methods are implemented for you, but you need to link them with your Framework's Request Handler:

```python
    def get(self, instance_id=None, edit=False): # or other method here
    	# next line is the required link
        return self.rest_handler.get(instance_id=instance_id, edit=edit)

    def post(self, instance_id=None, action=None): # or other method here
	    # next line is the required link
        return self.rest_handler.post(instance_id=instance_id, action=action)

    def put(self, instance_id): # or other method here
	    # next line is the required link
        return self.rest_handler.put(instance_id=instance_id)

    def delete(self, instance_id): # or other method here
	    # next line is the required link
        return self.rest_handler.delete(instance_id=instance_id)
```

Just be sure that a **RestRequestHandler** **requires** a **model** and **DataManager** to be instantiated.

Until this moment, this library include just a simple **DataManager** for the MongoEngine.


Data Managers
------------------------

To create a Data Manager for your ORM you must override the **DataManager** class and implement the following methods:

```python
from python_rest_handler import DataManager

class YourDataManager(DataManager):
    def instance_list(self): return []
    def find_instance_by_id(self, instance_id): pass
    def save_instance(self, data): pass
    def update_instance(self, instance, data): pass
    def delete_instance(self, instance): pass
```

After that, you may use the Data Manager in any RequestRestHandler you want to:

```python
class YourRequestRestHandler(python_rest_handler.RequestRestHandler):
    data_manager = YourDataManager
```

Tip: You can create a general data manager, and let the user subclass your DataManager when he/she wants to customize some behavior, for example:

```python
class AnimalDataManager(YourDataManager):
    def instance_list(self):
        return Animal.objects.filter(user=current_user)
```

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

```python
import python_rest_handler

class SomeImplementationOfRestHandler(BASE_CLASS_OF_YOUR_FRAMEWORK, python_rest_handler.RestRequestHandler): pass

ROUTES = python_rest_handler.rest_routes(Animal, YourDataManager, YourRequestRestHandler),
```

The **routes** is a useful function in case you want to include a call of the **rest_routes** function inside of a list. It just flat the list with depth 1.

```python
ROUTES = python_rest_handler.routes(ROUTES)
```

The library does not support auto-pluralization yet, so you may want to change the prefix:

```python
ROUTES = rest_routes(Animal, prefix='animals')
```

You can also define to where will be redirect after an action succeed:

```python
ROUTES = rest_routes(Animal, prefix='animals', redirect_pos_action='/animals')
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

```python
from python_rest_handler.plugins.bootstrap import *

extra_attributes = {'bs_input_text': bs_input_text,
                    'bs_input_password':bs_input_password,
                    'bs_select_field':bs_select_field,
                    'bs_button':bs_button}

rest_routes(Animal, extra_attributes=extra_attributes),
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
python-rest-handler==0.0.2
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

#### 0.0.2 (2013/04/28)

* [new] Bootstrap plugin has two more functions: <code>bs_text_area</code> and <code>bs_input_file</code>.
* [new] Now it is possible to select which routes and actions you want to create, using the <code>only</code> and <code>exclude</code> parameter. Options are: <code>new</code>, <code>show</code>, <code>list</code>, <code>edit</code> and <code>delete</code>
* [new] Now is possible to activate and deactivate plugins for all rest_routes using the <code>activate_plugin</code> and <code>deactivate_plugin</code> methods.
* [bugfix] The selected_value for <code>bs_select_field</code> in the Bootstrap plugin now convert the value to string.
* [bugfix] Fixed setup.py dependencies.
* [optimization] Regular expressions are now pre-compiled.

#### 0.0.1 (2013/03/30)

* [important] This project is an abstraction of tornado-rest-handler. Now tornado-rest-handler will use this project.
* [new] It has all features of tornado-rest-handler 0.0.5 (besides the Tornado Request Manager and MongoEngine Data Manager).
* [new] Plugin support.
* [new] Bootstrap plugin: bs_input_text, bs_input_password, bs_select_field, bs_button.


TODO
-------------

* Pagination
* i18n
* pluralize urls
* bootstrap plugin: delete button, edit button
