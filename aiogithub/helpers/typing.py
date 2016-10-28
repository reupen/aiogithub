from typing import GenericMeta, List


def is_generic_type_hint(T):
    return isinstance(T, GenericMeta)


def is_list_type_hint(T):
    return is_generic_type_hint(T) and T.__origin__ == List


def get_list_element_hint(T):
    return T.__args__[0]
