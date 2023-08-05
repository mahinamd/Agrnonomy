from django.test import TestCase


# Create your tests here.

def split_and_remove_extra_spaces(input_string):
    split_list = input_string.split(',')
    cleaned_list = [' '.join(item.strip().split()) for item in split_list if item != '']
    tags_list = ['#' + item for item in cleaned_list]
    tags = ", ".join(tags_list)

    return tags

input_string = "  red   apple ,   small banana ,  orange   ,   cherry,"
print(split_and_remove_extra_spaces(input_string))