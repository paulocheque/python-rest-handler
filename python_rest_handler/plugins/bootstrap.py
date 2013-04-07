# coding: utf-8

def bootstrap_panel(field, widget, error=None, **kwargs):
    label = kwargs.get('label', '')
    has_error = 'error' if error else ''
    error = error if error else ''
    help_text = kwargs.get('help_text', '')
    return '''
<div class="control-group %(has_error)s">
  <label class="control-label">%(label)s</label>
  <div class="controls">
    %(widget)s
    <p class="help-inline">%(error)s</p>
    <p class="help-block">%(help_text)s</p>
  </div>
</div>
''' % {'has_error':has_error, 'label':label, 'widget':widget, 'error':error, 'help_text':help_text}


def input_field(field, value=None, error=None, **kwargs):
    input_type = kwargs.get('input_type', 'text')
    label = kwargs.get('label', field)
    autocomplete = kwargs.get('autocomplete', False)
    autocomplete = "on" if autocomplete else "off"
    required = kwargs.get('required', True)
    required = 'required=""' if required else ''
    value = value if value else ''

    widget = '<input id="%(field)s" name="%(field)s" type="%(input_type)s" placeholder="%(label)s" class="input-xlarge" %(required)s autocomplete="%(autocomplete)s" value="%(value)s">' % \
    {'field':field, 'input_type':input_type, 'label':label, 'required':required, 'autocomplete':autocomplete, 'value':value}

    return bootstrap_panel(field, widget, error=error, **kwargs)


def password_field(field, value=None, error=None, **kwargs):
    kwargs['input_type'] = 'password'
    return input_field(field, value=value, error=error, **kwargs)


def select_field(field, options, error=None, **kwargs):
    required = kwargs.get('required', True)
    required = 'required=""' if required else ''
    selected_value = kwargs.get('selected_value', '')
    option_widgets = []
    for option in options:
        option_value = option['value']
        option_label = option['label']
        selected = 'selected="selected"' if selected_value == option_value else ''
        option_widget = '<option value="%(option_value)s" %(selected)s>%(option_label)s</option>' % \
        {'option_value':option_value, 'selected':selected, 'option_label':option_label}
        option_widgets.append(option_widget)
    option_widgets = ''.join(option_widgets)

    widget = '''
    <select id="%(field)s" name="%(field)s" %(required)s>
      %(option_widgets)s
    </select>
''' % {'field':field, 'required':required, 'option_widgets':option_widgets}

    return bootstrap_panel(field, widget, error=error, **kwargs)


def button(**kwargs):
    button_id = kwargs.get('button_id', 'save')
    label = kwargs.get('label', 'Save')

    widget = '''
    <button id="%(button_id)s" name="%(button_id)s" class="btn btn-primary">%(label)s</button>
''' % {'button_id':button_id, 'label':label}

    return bootstrap_panel(None, widget, **kwargs)
