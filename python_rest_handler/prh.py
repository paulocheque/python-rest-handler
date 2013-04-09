# coding: utf-8
import re

from python_rest_handler.utils import ObjectDict


class DataManager(object):
    model = None

    def __init__(self, request_handler):
        self.handler = request_handler

    def instance_list(self): return []
    def find_instance_by_id(self, instance_id): pass
    def save_instance(self, data): pass
    def update_instance(self, instance, data): pass
    def delete_instance(self, instance): pass


class CrudHandler(object):
    def __init__(self, request_handler):
        self.handler = request_handler

    def render(self, template_name, **kwargs):
        template_name = self.handler.template_path + template_name
        if self.handler.extra_attributes:
            kwargs.update(self.handler.extra_attributes)
        return self.handler.render(template_name, **kwargs)

    def redirect(self, url=None, permanent=False, status=None, **kwargs):
        if self.handler.redirect_pos_action:
            url = self.handler.redirect_pos_action
        else:
            url = '/'
        message = kwargs.get('message', None)
        return self.handler.redirect(url, permanent=permanent, status=status, **kwargs)

    def page_list(self, alert=None):
        return self.render(self.handler.list_template, objs=self.handler.data_manager.instance_list(), alert=alert)

    def page_new(self):
        return self.page_edit(None)

    def page_show(self, instance):
        value_for = lambda field: getattr(instance, field, '') if getattr(instance, field, '') else ''
        has_error = lambda field: False
        error_for = lambda field: ''
        return self.render(self.handler.show_template, obj=instance,
                    value_for=value_for, has_error=has_error, error_for=error_for)

    def page_edit(self, instance, exception=None, alert=None):
        errors = None
        if exception:
            alert = 'Data sent contains some issues.'
            errors = ObjectDict()
            if hasattr(exception, 'to_dict'):
                errors.update(**exception.to_dict())
        value_for = lambda field: getattr(instance, field, '') if getattr(instance, field, '') else ''
        has_error = lambda field: errors and field in list(errors.keys())
        error_for = lambda field: errors[field] if errors and field in errors else ''
        return self.render(self.handler.edit_template, obj=instance, errors=errors, alert=alert,
                    value_for=value_for, has_error=has_error, error_for=error_for)

    def action_create(self):
        data = self.handler.get_request_data()
        try:
            self.handler.data_manager.save_instance(data)
            return self.redirect(message='Object added successfully.')
        except AssertionError as e:
            instance = ObjectDict()
            instance.update(**data)
            return self.page_edit(instance, exception=e)

    def action_read(self, instance_id, fail_silently=False):
        try:
            return self.handler.data_manager.find_instance_by_id(instance_id)
        except AssertionError as e:
            if fail_silently:
                return None
            self.handler.raise404()

    def action_update(self, instance_id):
        data = self.handler.get_request_data()
        instance = self.action_read(instance_id)
        try:
            self.handler.data_manager.update_instance(instance, data)
            return self.redirect(message='Object updated successfully.')
        except AssertionError as e:
            return self.page_edit(instance, exception=e)

    def action_delete(self, instance_id):
        instance = self.action_read(instance_id)
        try:
            self.handler.data_manager.delete_instance(instance)
            return self.redirect(message='Object deleted successfully.')
        except AssertionError as e:
            return self.page_list('Object could not be deleted.')


class RestHandler(CrudHandler):
    '''
    GET    /animals            Index display a list of all animals
    GET    /animals/new        New return an HTML form for creating a new animal
    POST   /animals            Create create a new animal
    GET    /animals/:id        Show show an animal
    GET    /animals/:id/edit   Return an HTML form for editing a photo
    PUT    /animals/:id        Update an animal data
    DELETE /animals/:id        Delete an animal

    POST   /animals/:id/delete Same as DELETE /animals/:id
    POST   /animals/:id        Same as PUT /animals/:id

    Since HTML5-forms does not support PUT/DELETE. It is possible to use those two methods above.
    '''

    def get(self, instance_id=None, edit=False):
        if re.match('^/.+/new', self.handler.get_request_uri()):
            return self.page_new()
        if instance_id:
            instance = self.action_read(instance_id, fail_silently=True)
            if instance:
                if edit:
                    return self.page_edit(instance)
                else:
                    return self.page_show(instance)
            else:
                return self.page_list('Object not found.')
        else:
            return self.page_list()

    def post(self, instance_id=None, action=None):
        if instance_id and re.match('^/.+/delete', self.handler.get_request_uri()):
            return self.action_delete(instance_id)
        if instance_id:
            return self.action_update(instance_id)
        return self.action_create()

    def put(self, instance_id):
        return self.action_update(instance_id)

    def delete(self, instance_id):
        return self.action_delete(instance_id)


class RestRequestHandler(object):
    model = None
    data_manager = None
    template_path = None
    def raise403(self): pass
    def raise404(self): pass
    def get_request_uri(self): pass
    def get_request_data(self): return {}
    def render(self, template_name, **kwargs): pass
    def redirect(self, url, permanent=False, status=None, **kwargs): pass


class RestRequestHandlerMetaclass(type):
    def __init__(cls, name, bases, attrs):
        if cls.model and not cls.template_path:
            cls.template_path = cls.model.__name__.lower() + '/'
        if cls.data_manager:
            cls.data_manager.model = cls.model
        return super(RestRequestHandlerMetaclass, cls).__init__(name, bases, attrs)

    def __call__(cls, *args):
        result = super(RestRequestHandlerMetaclass, cls).__call__(*args)
        msg = 'RestRequestHandler classes (%s) requires the attribute "%s"'
        if not result.model:
            raise NotImplementedError(msg % (cls.__name__, 'model'))
        if not result.data_manager:
            raise NotImplementedError(msg % (cls.__name__, 'data_manager'))
        result.rest_handler = RestHandler(result)
        result.data_manager = result.data_manager(result)
        return result


RestRequestHandler = RestRequestHandlerMetaclass(RestRequestHandler.__name__, RestRequestHandler.__bases__, dict(RestRequestHandler.__dict__))


def routes(route_list):
    routes = []
    for route in route_list:
        if isinstance(route, list):
            routes.extend(route)
        else:
            routes.append(route)
    return routes


dynamic_classes_cache = {}

def rest_handler(model, data_manager, base_handler, **kwargs):
    model_name = model.__name__
    attrs = {}
    attrs['model'] = model
    attrs['data_manager'] = data_manager
    attrs['template_path'] = kwargs.get('template_path', model_name.lower() + '/')
    attrs['list_template'] = kwargs.get('list_template', 'list.html')
    attrs['edit_template'] = kwargs.get('edit_template', 'edit.html')
    attrs['show_template'] = kwargs.get('show_template', 'show.html')
    attrs['redirect_pos_action'] = kwargs.get('redirect_pos_action', '/')
    attrs['extra_attributes'] = kwargs.get('extra_attributes', None)
    handler = kwargs.get('handler', None)
    base_name = base_handler.__name__

    class_name = model_name + base_name
    index = dynamic_classes_cache.setdefault(class_name, 1)
    unique_class_name = class_name + str(index)
    index += 1
    dynamic_classes_cache[class_name] = index

    if handler:
        rest_handler = type(unique_class_name, (handler, base_handler), attrs)
    else:
        rest_handler = type(unique_class_name, (base_handler,), attrs)
    return rest_handler


def rest_routes(model, data_manager, base_handler, **kwargs):
    prefix = kwargs.get('prefix', model.__name__.lower())
    handler = rest_handler(model, data_manager, base_handler, **kwargs)
    return [
        (r'/%s/?' % prefix, handler),
        (r'/%s/new/?' % prefix, handler),
        (r'/%s/([0-9a-fA-F]{24,})/?' % prefix, handler),
        (r'/%s/([0-9a-fA-F]{24,})/(edit|delete|)/?' % prefix, handler),
    ]
