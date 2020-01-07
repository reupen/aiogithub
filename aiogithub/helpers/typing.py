from typing import _GenericAlias


def is_generic_type_hint(T):
    return isinstance(T, _GenericAlias)


def is_list_type_hint(T):
    return is_generic_type_hint(T) and T.__origin__ is list


def get_list_element_hint(T):
    return T.__args__[0]
