""" Store module

Data table structure:
    * id (string): Unique and random generated identifier
        at least 2 special characters (except: ';'), 2 number, 2 lower and 2 upper case letters)
    * title (string): Title of the game
    * manufacturer (string)
    * price (number): Price in dollars
    * in_stock (number)
"""

# everything you'll need is imported:
# User interface module
import ui
# data manager module
import data_manager
# common module
import common
import input_mod


# general variables for store
file_name = 'store/games.csv'
table = data_manager.get_table_from_file(file_name)
id_index = 0
title_index = 1
manuf_index = 2
price_index = 3
stock_index = 4
manufacturer = ''


# variables for menu store
OPTION = ['0', '1', '2', '3', '4', '5', '6']
title = "Store menu:"
options = ["Show table",
           "Add record",
           "Remove record",
           "Update data",
           "Counts by manufacturers",
           "The average amount of games of a manufacturer"]
exit_message = "Back to main menu"


# variables for function show in store:
title_list = ['Id', 'Title', 'Manufacturer', 'Price', 'In stock']


# variables for store function remove and update
id_ = ''
details_update_list_labels = 'Number of category: '
detail_update_title = """Please provide number of category you want to update:
1 - Title, 2 - Manufacturer, 3 - Price, 4 - In stock"""


# ------helpful functions for store only------
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
        ui.print_result(get_counts_by_manufacturers(table), 'Kinds of game of each manufacturer: ')
    elif option == "6":
        ui.print_result(get_average_by_manufacturerERP(table, manufacturer),
                        'Average amount of games in stock of a manufacturer: ')
    elif option == '0':
        raise ValueError
    while option not in OPTION:
        raise KeyError
        menu_control()


# -------------------------------Main store module------------------------------------
# starts module store
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
    record = [id, input_mod.name('Game title: ', 'Provide data to add'), input_mod.name('Manufacturer: ', ''),
              input_mod.number('Price: ', ''), input_mod.number('In stock: ', '')]
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


# ---------------------Special functions---------------
# counts item by manufacturer
def get_counts_by_manufacturers(table):
    """
    Question: How many different kinds of game are available of each manufacturer?

    Args:
        table (list): data table to work on

    Returns:
         dict: A dictionary with this structure: { [manufacturer] : [count] }
    """

    counted_games = {}
    for item in table:
        if item[manuf_index] in counted_games.keys():
            counted_games[item[manuf_index]] += 1
        else:
            counted_games[item[manuf_index]] = 1
    return counted_games


# function for ERP - manufacturer is an input
def get_average_by_manufacturerERP(table, manufacturer):
    """
    Question: What is the average amount of games in stock of a given manufacturer?

    Args:
        table (list): data table to work on
        manufacturer (str): Name of manufacturer

    Returns:
         number
    """

    manufacturer = input_mod.name('Manufacturer: ', 'Provide name of manufacturer')
    counted_manufacturer = 0
    games_count = 0
    for line in table:
        if manufacturer in line[manuf_index]:
            counted_manufacturer += 1
            games_count += int(line[stock_index])
    average = games_count/counted_manufacturer
    return average


# function for test
def get_average_by_manufacturer(table, manufacturer):
    """
    Question: What is the average amount of games in stock of a given manufacturer?

    Args:
        table (list): data table to work on
        manufacturer (str): Name of manufacturer

    Returns:
         number
    """

    counted_manufacturer = 0
    games_count = 0
    for line in table:
        if manufacturer in line[manuf_index]:
            counted_manufacturer += 1
            games_count += int(line[stock_index])
    average = games_count/counted_manufacturer
    return average
