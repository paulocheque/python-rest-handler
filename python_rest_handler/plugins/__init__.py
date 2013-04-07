# coding: utf-8

def value_for(instance, field):
    return getattr(instance, field, '') if getattr(instance, field, '') else ''


def has_error(field):
    return errors and field in list(errors.keys())


def error_for(field):
    return errors[field] if errors and field in errors else ''