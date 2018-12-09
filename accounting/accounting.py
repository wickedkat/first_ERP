""" Accounting module

Data table structure:
    * id (string): Unique and random generated identifier
        at least 2 special characters (except: ';'), 2 number, 2 lower and 2 upper case letters)
    * month (number): Month of the transaction
    * day (number): Day of the transaction
    * year (number): Year of the transaction
    * type (string): in = income, out = outflow
    * amount (int): amount of transaction in USD
"""

# everything you'll need is imported:
# User interface module
import ui
# data manager module
import data_manager
# common module
import common
import input_mod


# general variables for acc
file_name = 'accounting/items.csv'
table = data_manager.get_table_from_file(file_name)
id_index = 0
month_index = 1
day_index = 2
year_index = 3
type_index = 4
amount_index = 5


# variables for menu acc
OPTION = ['0', '1', '2', '3', '4', '5', '6']
title = "Accounting menu:"
options = ["Show table",
        "Add record",
        "Remove record",
        "Update data",
        "Year with highest profit",
        "Average (per item) profit in a given year"]
exit_message = "Back to main menu"


# variables for function show in acc:
title_list = ['Id', 'Month', 'Day', 'Year', 'Type', 'Amount']


# variables for acc function remove and update
id_ = ''
year = ''
details_update_list_labels = 'Number of category: '
detail_update_title = """Please provide number of category you want to update:
1 - Month', '2 - Day', '3 - Year', '4 - Type', '5 - Amount"""


# ------helpful functions for acc only------
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
        ui.print_result(which_year_max(table), 'The year with max income: ')
    elif option == "6":
        ui.print_result(avg_amount_ERP(table, year), 'The average income for given year: ')
    elif option == '0':
        raise ValueError
    while option not in OPTION:
        raise KeyError
        menu_control()


# converts amount to negative and positive numbers
def categorize_amount(table):
    """
    Making lists of type and amount and converting
    amount into plus or minus number based on type of amount
    arg = table
    Returns list of amount marked by plus or minus
    """

    type_list = [line[type_index] for line in table]
    amount_list = [int(line[amount_index]) for line in table]
    amount_list_convert = []
    for n in range(len(type_list)):
        if type_list[n] == 'out':
            amount_list_convert.append(amount_list[n]*(-1))
        else:
            amount_list_convert.append(amount_list[n])
    return amount_list_convert


# making list of years and assign amount to them
def group_year_and_amount(table):
    """
    Makes nested list of year and amount
    arg - table
    Returns - nested list of year/amount
    """

    amount_list_convert = categorize_amount(table)
    year_list = common.make_list_of_elements(table, year_index)
    year_amount_list = [[year_list[n], amount_list_convert[n]] for n in range(len(year_list))]
    return year_amount_list


# separate amount into groups by year
def divide_amount_per_year(table):
    """
    Takes amount and group them by years into
    many-elemental collections
    """
    nested_of_amount = []
    unique_years = common.find_unique_elements(table, year_index)
    year_amount_list = group_year_and_amount(table)
    for item in unique_years:
        nested_of_amount.append([])
    for n in range(len(unique_years)):
        for line in year_amount_list:
            if line[0] == unique_years[n]:
                nested_of_amount[n].append(line[1])
    return nested_of_amount


# -------------------------Main module accounting-------------------
# starts module acc
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
    record = [id, input_mod.month('Month: ', 'Provide data to add'), input_mod.day('Day: ', ''),
            input_mod.year('Year: ', ''), input_mod.specific('Type: ', '', ['in', 'out'], 'Provide in or out type'),
            input_mod.number('Amount: ', '')]
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


# creates dictionary from set of years and grouped income
# and return year with largest income
def which_year_max(table):
    """
    Question: Which year has the highest profit? (profit = in - out)
    Args:
        table (list): data table to work on
    Returns:
        number
    """

    nested_of_amount = divide_amount_per_year(table)
    unique_years = common.find_unique_elements(table, year_index)
    year_amount_dict = dict(zip(unique_years, nested_of_amount))
    for key, value in year_amount_dict.items():
        year_amount_dict[key] = common.sums_int_list(value)
    sought_year = max(year_amount_dict, key=year_amount_dict.get)
    return int(sought_year)


# Function with inputs for ERP
def avg_amount_ERP(table, year):
    """
    Question: What is the average (per item) profit in a given year? [(profit)/(items count)]
    Args:
        table (list): data table to work on
        year (number)
    Returns:
        number
    """

    year = input_mod.year('Year:', 'Please provide year to get average income')
    nested_of_amount = divide_amount_per_year(table)
    unique_years = common.find_unique_elements(table, year_index)
    year_amount_dict = dict(zip(unique_years, nested_of_amount))
    for key, value in year_amount_dict.items():
        sum = common.sums_int_list(year_amount_dict[key])
        quantity = common.count_elems(year_amount_dict[key])
        avg = sum/quantity
        year_amount_dict[key] = avg
    for key, value in year_amount_dict.items():
        if str(year) == key:
            return year_amount_dict[key]


# Function for test purposes
def avg_amount(table, year):
    """
    Question: What is the average (per item) profit in a given year? [(profit)/(items count)]
    Args:
        table (list): data table to work on
        year (number)
    Returns:
        number
    """

    nested_of_amount = divide_amount_per_year(table)
    unique_years = common.find_unique_elements(table, year_index)
    year_amount_dict = dict(zip(unique_years, nested_of_amount))
    for key, value in year_amount_dict.items():
        sum = common.sums_int_list(year_amount_dict[key])
        quantity = common.count_elems(year_amount_dict[key])
        avg = sum/quantity
        year_amount_dict[key] = avg
    for key, value in year_amount_dict.items():
        if str(year) == key:
            return year_amount_dict[key]
