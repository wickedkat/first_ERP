""" Inventory module

Data table structure:
    * id (string): Unique and random generated identifier
        at least 2 special characters (except: ';'), 2 number, 2 lower and 2 upper case letters)
    * name (string): Name of item
    * manufacturer (string)
    * purchase_year (number): Year of purchase
    * durability (number): Years it can be used
"""

# everything you'll need is imported:
# User interface module
import ui
# data manager module
import data_manager
# common module
import common
# input_mod module
import input_mod


# general variables for inventory
file_name = 'inventory/inventory.csv'
table = data_manager.get_table_from_file(file_name)
id_index = 0
name_index = 1
manuf_index = 2
purchase_index = 3
durab_index = 4


# variables for menu inventory
OPTION = ['0', '1', '2', '3', '4', '5', '6']
title = "Inventory menu:"
options = ["Show table",
        "Add record",
        "Remove record",
        "Update data",
        "Get available items",
        "Get average durability by manufacturers"]
exit_message = "Back to main menu"


# variables for function shown in inv:
title_list = ['Id', 'Name', 'Manufacturer', 'Purchase year', 'Durability']


# variables for inv functions remove and update
id_ = ''
details_update_list_labels = 'Number of category: '
detail_update_title = """Please provide number of category you want to update:
1 - Name, 2 - Manufacturer, 3 - Puchase year, 4 - Durability"""


# ------helpful functions for inv only------
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
        ui.print_result(get_available_items_ERP(table), 'Items without exceeded durability: ')
    elif option == "6":
        ui.print_result(get_average_durability_by_manufacturers(table), 'Average durability for each manufacturer: ')
    elif option == '0':
        raise ValueError
    while option not in OPTION:
        raise KeyError
        menu_control()


# -------------------------------Main inventory module------------------------------------
# starts module sales
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
    record = [id, input_mod.name('Name of item: ', 'Provide data to add'), input_mod.name('Manufacturer: ', ''),
            input_mod.year('Year of purchase: ', ''), input_mod.number('Durability: ', '')]
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
    new_record = input_mod.get_inputs(['New data: '], 'Please provide new data')[0]
    # mam tu problem z wprowadzaniem nowych danych = powinno być to obudowane warunkami. ale nie wiem jak
    for number, line in enumerate(table):
        if line[0] == id_:
            table[number][line_data] = new_record
    data_manager.write_table_to_file(file_name, table)
    show_table(table)
    return table


# -------------------special functions---------------------
# Function returns item without exceeded durability
# You can choose year - only for ERP (not for test purposes)
def get_available_items_ERP(table):
    """
    Question: Which items have not exceeded their durability yet?
    Args:
        table (list): data table to work on
    Returns:
        list: list of lists (the inner list contains the whole row with their actual data types)
    """
    current_year = int(input_mod.year('Year: ', 'Provide year to find items with valid durability'))
    list_available_items = []
    for i in range(len(table)):
        table[i][purchase_index] = int(table[i][purchase_index])
        table[i][durab_index] = int(table[i][durab_index])
        expiration_date = table[i][purchase_index]+table[i][durab_index]
        if expiration_date >= current_year:
            list_available_items.append(table[i])
    return list_available_items


# Function returns item without exceeded durability
# Year is set as 2017 - only for test purposes
def get_available_items(table):
    """
    Question: Which items have not exceeded their durability yet?
    Args:
        table (list): data table to work on
    Returns:
        list: list of lists (the inner list contains the whole row with their actual data types)
    """

    list_available_items = []
    for i in range(len(table)):
        table[i][purchase_index] = int(table[i][purchase_index])
        table[i][durab_index] = int(table[i][durab_index])
        expiration_date = table[i][purchase_index]+table[i][durab_index]
        current_year = 2017
        if expiration_date >= current_year:
            list_available_items.append(table[i])
    return list_available_items


# function gets average durability times for each manufacturer
def get_average_durability_by_manufacturers(table):
    """
    Question: What are the average durability times for each manufacturer?
    Args:
        table (list): data table to work on
    Returns:
        dict: a dictionary with this structure: { [manufacturer] : [avg] }
    """

    dict_average_durability = {}
    list_manufacturers = common.find_unique_elements(table, manuf_index)
    for item in list_manufacturers:
        sum_durability_times = 0
        count = 0
        for element in table:
            if item == element[manuf_index]:
                element[durab_index] = int(element[durab_index])
                sum_durability_times += element[durab_index]
                count += 1
                average_durability = float(
                    round(sum_durability_times/count, 2))
                dict_average_durability.update(
                    {element[manuf_index]: average_durability})
    return dict_average_durability
