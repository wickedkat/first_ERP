""" Common module
implement commonly used functions here
"""

import random

# ------------------------------FUNCTIONS TO CREATE ID--------------------------
# variables for generating random id
NUMBERS = '0123456789'
LETTERS = 'abcdefghijklmnoprstuwxyz'
SIGNS = "!#$%&'()*+,-./:_<=>?@][`^{|}~"
id_index = 0


# creates id
def create_id():
    elem_id1 = ''.join(random.sample(NUMBERS, 2))
    elem_id2 = ''.join(random.sample(LETTERS, 2))
    elem_id3 = ''.join(random.sample(SIGNS, 2))
    elem_id4 = ''.join(random.sample(LETTERS, 2)).upper()
    id = elem_id1 + elem_id2 + elem_id3 + elem_id4
    return id


# checks if id is in table - if not, returns it
def generate_random(table):
    """
    Generates random and unique string. Used for id/key generation:
        - at least 2 special characters (except: ';'), 2 number, 2 lower and 2 upper case letter
        - it must be unique in the table (first value in every row is the id)

    Args:
        table (list): Data table to work on. First columns containing the keys.

    Returns:
        string: Random and unique string
    """

    generated = ''
    id_table = [line[id_index] for line in table]
    generated = create_id()
    if id in id_table:
        generate_random(table)
    else:
        return generated

# ---------------------------------OTHER HELPING FUNCTIONS-------------------


# takes input (line number) and finds ID of line number
def convert_input_to_id(table, line_number):
    """Function takes number of line provided by user
    and returns unique id of item in this line.
    Returns id as string"""
    list_of_id = [line[id_index] for line in table]
    for i, id in enumerate(list_of_id, 1):
        if i == int(line_number):
            return list_of_id[i-1]


# little function converts strings in table into integers
def string_to_int_list(any_list):
    """
    Function takes elements from any list
    and converts them into integers
    Return list
    """
    n = 0
    while n < len(any_list):
        any_list[n] = int(any_list[n])
        n += 1
    return(any_list)


# finds only unique elements of any list by index
def find_unique_elements(table, index):
    """
    Function finds unique elements in lists
    by index and returns them as list
    Returns list of set
    """

    unique_elems = list(set(line[index] for line in table))
    return unique_elems


# creates list of any element from list
def make_list_of_elements(table, index):
    """
    Takes category from table by index
    and returns it as list
    """

    list_of_elements = [line[index] for line in table]
    return list_of_elements


# converts data in nested into integers
def make_numbers_in_nested(nested, ind1, ind2, ind3, ind4):
    """
    Converts numbers into integers
    in nested list by indexes
    Returns nested list with integers
    """

    n = 0
    while n < len(nested):
        nested[n][ind1] = int(nested[n][ind1])
        nested[n][ind2] = int(nested[n][ind2])
        nested[n][ind3] = int(nested[n][ind3])
        nested[n][ind4] = int(nested[n][ind4])
        n += 1
    return nested


# function sums list
def sums_int_list(any_list):
    """
    Sums integers in list
    Returns number
    """

    summ = 0
    for n in any_list:
        summ += n
    return summ


# counts elements in list
def count_elems(any_list):
    """
    Counts elements in list
    Return number
    """
    counter = 0
    for item in any_list:
        counter += 1
    return counter