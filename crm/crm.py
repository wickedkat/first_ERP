""" Customer Relationship Management (CRM) module

Data table structure:
    * id (string): Unique and random generated identifier
        at least 2 special characters (except: ';'), 2 number, 2 lower and 2 upper case letters)
    * name (string)
    * email (string)
    * subscribed (int): Is she/he subscribed to the newsletter? 1/0 = yes/no
"""

# everything you'll need is imported:
# User interface module
import ui
# data manager module
import data_manager
# common module
import common
import input_mod


# general variables
file_name = 'crm/customers.csv'
table = data_manager.get_table_from_file(file_name)
id_index = 0
name_index = 1
email_index = 2
subs_index = 3
id_ = ''
id = ''

# variables for menu crm
OPTION = ['0', '1', '2', '3', '4', '5', '6']
title = "CRM_menu:"
options = ["Show table",
        "Add record",
        "Remove record",
        "Update data",
        "Get longest name id",
        "Get subscribed emails"]
exit_message = "Back to main menu"


# variables for function show in crm
title_list = ['Id', 'Name', 'Email', 'Subscribed']


# variables for crm function remove and update
id_ = ''
details_update_list_labels = 'Number of category: '
detail_update_title = """Please provide number of category you want to update:
1 - Name', '2 - Email', '3 - Subscription'"""


# ------helpful functions for crm only------
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
        ui.print_result(get_longest_name_id(table), 'Longest name: ')
    elif option == "6":
        ui.print_result(get_subscribed_emails(table), 'Customers subscribed to newsletter: ')
    elif option == '0':
        raise ValueError
    while option not in OPTION:
        raise KeyError
        menu_control()


# -------------------------------Main crm module------------------------------------
# starts module crm
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
    record = [id, input_mod.name('Name: ', 'Provide data to add'), input_mod.email('Email: ', ''),
              input_mod.specific('Subscription: ', '', ['0', '1'], 'Provide 1(yes) or 0(no)')]
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
    line_data = input_mod.number_with_terms(details_update_list_labels, detail_update_title, range(1, 6))
    dict_update = {1: input_mod.name, 2: input_mod.number, 3: input_mod.month, 4: input_mod.day, 5: input_mod.year}
    new_record = input_mod.get_inputs(['New data: '], 'Please provide new data')[0]
    for number, line in enumerate(table):
        if line[0] == id_:
            table[number][line_data] = new_record
    data_manager.write_table_to_file(file_name, table)
    show_table(table)
    return table


# function returns id of longest name in reverse alphabetical order
def get_longest_name_id(table):
    """
        Question: What is the id of the customer with the longest name?
        Args:
            table(list): data table to work on
        Returns:
            string: id of the longest name(if there are more than one, return
                the last by alphabetical order of the names)
        """

    names = [line[name_index] for line in table]
    length_of_names = []
    for item in names:
        n = len(item)
        length_of_names.append(n)
    longest = max(length_of_names)
    list_of_longest = []
    id_name_dict = {}
    for line in table:
        if len(line[name_index]) == longest:
            id_name_dict[line[id_index]] = line[name_index]
    longest_name_reverse_order = max(id_name_dict, key=id_name_dict.get)
    return longest_name_reverse_order


# the question: Which customers has subscribed to the newsletter?
# return type: list of strings (where string is like email+separator+name, separator=";")
def get_subscribed_emails(table):
    """
    Question: Which customers has subscribed to the newsletter?
    Args:
        table (list): data table to work on
    Returns:
        list: list of strings (where a string is like "email;name")
    """

    list_subscribed_customers = []
    for line in table:
        if line[subs_index] == '1':
            email_and_name = str(line[email_index])+';'+str(line[name_index])
            list_subscribed_customers.append(email_and_name)
    return list_subscribed_customers


# functions supports data analyser
# --------------------------------


def get_name_by_id(id):
    """
    Reads the table with the help of the data_manager module.
    Returns the name (str) of the customer with the given id (str) on None om case of non-existing id.

    Args:
        id (str): the id of the customer

    Returns:
        str: the name of the customer
    """

    table = data_manager.get_table_from_file(file_name)
    for line in table:
        if line[id_index] == id:
            return str(line[name_index])


def get_name_by_id_from_table(table, id):
    """
    Returns the name (str) of the customer with the given id (str) on None om case of non-existing id.

    Args:
        table (list of lists): the customer table
        id (str): the id of the customer

    Returns:
        str: the name of the customer
    """

    for line in table:
        if line[id_index] == id:
            return str(line[name_index])


def get_id_name_set():
    """
    Creates dictionery of id and names of customers
    Arg - table
    Returns dict(k,v) (id: name)
    """

    table = data_manager.get_table_from_file(file_name)
    id_name_dict = {line[id_index]: line[name_index] for line in table}
    return id_name_dict
