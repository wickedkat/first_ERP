""" Human resources module

Data table structure:
    * id (string): Unique and random generated identifier
        at least 2 special characters (except: ';'), 2 number, 2 lower and 2 upper case letters)
    * name (string)
    * birth_year (number)
"""

# everything you'll need is imported:
# User interface module
import ui
# data manager module
import data_manager
# common module
import common
import input_mod


# general variables for hr module
file_name = 'hr/persons.csv'
table = data_manager.get_table_from_file(file_name)
id_index = 0
name_index = 1
year_index = 2
current_year = 2018  # there can also be input function for year


# variables for menu hr
OPTION = ['0', '1', '2', '3', '4', '5', '6']

title = "HR menu:"
options = ["Show table",
           "Add record",
           "Remove record",
           "Update data",
           "The oldest person",
           "Who is the closest to the average age?"]
exit_message = "Back to main menu"


# variables for function show in hr:
title_list = ['Id', 'Name', 'Birth Year']


# variables for hr function remove and update
id_ = ''
details_update_list_labels = 'Number of category: '
detail_update_title = """Please provide number of category you want to update:
1 - Name', '2 - Year of birth'"""


# ------helpful functions for hr only------
# choosing option in menu
def choose():
    """ Function gets input from user
    and starts options from module.
    No arg
    Returns nothing"""
    inputs = input_mod.get_inputs(['Enter a number: '], '')
    option = inputs[0]
    if option == "1":
        show_table(table)
    elif option == "2":
        add(table)
    elif option == "3":
        remove(table, id_)
    elif option == "4":
        update(table, id_)
    elif option == "5":
        ui.print_result(get_oldest_person(table), 'The oldest person/s: ')
    elif option == "6":
        ui.print_result(get_persons_closest_to_average(table), 'Person/s whos age is closest to average: ')
    elif option == '0':
        raise ValueError
    while option not in OPTION:
        raise KeyError
        menu_control()


# finds average age for hr table
def find_average_age(table):
    """
    Function sums all age's data from table and
    divide it by quantity if age records
    Returns average age for table (number)
    """

    age_list = [current_year - int(line[year_index]) for line in table]
    age_sum = common.sums_int_list(age_list)
    average_age = age_sum/len(age_list)
    return average_age


# finds difference between age and average age
def odds_between_age_and_avg(table):
    """
    Counts difference between age and average age
    Returns list of numbers
    """

    average_age = find_average_age(table)
    age_list = [current_year - int(line[year_index]) for line in table]
    odds_age_and_avg = [abs(round(age - average_age)) for age in age_list]
    return odds_age_and_avg


# -------------------------Main module HR-------------------
# starts module hr
def start_module():
    """
    Starts this module and displays its menu.
     * User can access default special features from here.
     * User can go back to main menu from here.
    Returns:
        None
    """

    while True:
        ui.print_menu(title, options, exit_message)
        try:
            choose()
        except ValueError:
            break
        except KeyError:
            ui.print_error_message('There is no such option')


# shows all data in table
def show_table(table):
    """
    Display a table
    Args:
        table (list): list of lists to be displayed.
    Returns:
        None
    """
    table = data_manager.get_table_from_file(file_name)
    ui.print_table(table, title_list)


# adds record to table
def add(table):
    """
    Asks user for input and adds it into the table.
    Args:
        table (list): table to add new record to
    Returns:
        list: Table with a new record
    """

    id = common.generate_random(table)
    record = [id, input_mod.name('Name: ', 'Provide data to add'), input_mod.year('Year of birth: ', '')]
    table.append(record)
    data_manager.write_table_to_file(file_name, table)
    show_table(table)
    return table


# removes record from table
def remove(table, id_):
    """
    Remove a record with a given id from the table.

    Args:
        table (list): table to remove a record from
        id_ (str): id of a record to be removed

    Returns:
        list: Table without specified record.
    """
    show_table(table)
    line_number = input_mod.number_with_terms('Line: ', 'Please provide number of line you want to remove',
                                       range(1, (len(table) + 1)))
    id_ = common.convert_input_to_id(table, line_number)
    for line in table:
        if line[0] == id_:
            table.remove(line)
    data_manager.write_table_to_file(file_name, table)
    show_table(table)
    return table


# updates record in table
def update(table, id_):
    """
    Updates specified record in the table. Ask users for new data.

    Args:
        table (list): list in which record should be updated
        id_ (str): id of a record to update

    Returns:
        list: table with updated record
    """
    line_number = input_mod.number_with_terms('Line: ', 'Please provide number of line you want to update',
                                       range(1, (len(table) + 1)))
    id_ = common.convert_input_to_id(table, line_number)
    line_data = input_mod.number_with_terms(
        details_update_list_labels, detail_update_title, range(1, 3))
    dict_update = {1: input_mod.name, 2: input_mod.year}
    new_record = ""
    if line_data in dict_update:
        new_record = dict_update[line_data]("New record: ", "Provide new data")
    for number, line in enumerate(table):
        if line[0] == id_:
            table[number][line_data] = new_record
    data_manager.write_table_to_file(file_name, table)
    show_table(table)
    return table


# function returns list of oldest persons
def get_oldest_person(table):
    """
    Question: Who is the oldest person?
    Args:
        table (list): data table to work on
    Returns:
        list: A list of strings (name or names if there are two more with the same value)
    """

    oldest_persons_list = []
    dict_name_year = {line[name_index]: line[year_index] for line in table}
    for key, value in dict_name_year.items():
        if value == min(dict_name_year.values()):
            oldest_persons_list.append(key)
    return oldest_persons_list


# returns person whos age is closest to average
def get_persons_closest_to_average(table):
    """
    Question: Who is the closest to the average age?
    Args:
        table (list): data table to work on
    Returns:
        list: list of strings (name or names if there are two more with the same value)
    """

    average_persons_list = []
    odds_age_and_avg = odds_between_age_and_avg(table)
    name_list = [line[name_index]for line in table]
    dict_name_diff_age = dict(zip(name_list, odds_age_and_avg))
    for key, value in dict_name_diff_age.items():
        if value == min(dict_name_diff_age.values()):
            average_persons_list.append(key)
    return average_persons_list
