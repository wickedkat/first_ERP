""" Sales module

Data table structure:
    * id (string): Unique and random generated identifier
        at least 2 special characters (except: ';'), 2 number, 2 lower and 2 upper case letters)
    * title (string): Title of the game sold
    * price (number): The actual sale price in USD
    * month (number): Month of the sale
    * day (number): Day of the sale
    * year (number): Year of the sale
    * customer_id (string): id from the crm
"""

# everything you'll need is imported:
# User interface module
import ui
# data manager module
import data_manager
# common module
import common
#inputs module
import input_mod


# general variables for sales
file_name = 'sales/sales.csv'
table = data_manager.get_table_from_file(file_name)
id_index = 0
title_index = 1
price_index = 2
month_index = 3
day_index = 4
year_index = 5
cust_index = 6
line_data = 1

# variables for sales menu
OPTION = ['0', '1', '2', '3', '4', '5', '6']
title = "Sales menu:"
options = ["Show table",
        "Add record",
        "Remove record",
        "Update data",
        "Id of the item that was sold for the lowest price",
        "Items sold between two given dates"]
exit_message = "Back to main menu"

# variables for functions shown in sales:
title_list = ['Id', 'Title', 'Price', 'Month', 'Day', 'Year', 'ID_cust']

# variables for sales functions: remove and update
id_ = ''
details_update_list_labels = 'Number of category: '
detail_update_title = """Please provide number of category you want to update:
1 - Title', '2 - Price', '3 - Month', '4 - Day', '5 - Year"""

# variables for special functions
month_from = ''
day_from = ''
year_from = ''
month_to = ''
day_to = ''
year_to = ''

def check_update():
    
    return new_record, line_number    


# ------helpful functions for sales only------
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
        ui.print_result(get_lowest_price_item_id(table), 'The id of cheapest game is: ')
    elif option == "6":
        ui.print_table(get_items_sold_between_ERP(table), title_list)
    elif option == '0':
        raise ValueError
    while option not in OPTION:
        raise KeyError
        menu_control()


# takes dates from and dates to and filtered dates from table by them
def compare_dates():
    """
    Function takes dates from input and uses them as borders
    to flitered dates from table
    Returns list of dates
    """

    date_from = [input_mod.year('Year from: ', 'Provide date from'),
                input_mod.month('Month from: ', ''), input_mod.day('Day from: ', '')]
    date_to = [input_mod('Year to: ', 'Provide date to'),
            input_mod.month('Month to: ', ''), input_mod.day('Day to: ', '')]
    date_table = [[int(line[year_index]), int(line[month_index]), int(line[day_index])] for line in table]
    common.string_to_int_list(date_from)
    common.string_to_int_list(date_to)
    list_of_filtred_dates = [line for line in date_table if line > date_from and line < date_to]
    return list_of_filtred_dates


# -------------------------------Main sales module------------------------------------
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
    record = [id, input_mod.name('Game title: ', 'Provide data to add'), input_mod.number('Price: ', ''),
            input_mod.month('Month: ', ''), input_mod.day('Day: ', ''), input_mod.year('Year: ', '')]
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
        details_update_list_labels, detail_update_title, range(1, 6))
    dict_update = {1: input_mod.name, 2: input_mod.number,
                3: input_mod.month, 4: input_mod.day, 5: input_mod.year}

    new_record = ""
    if line_data in dict_update:
        new_record = dict_update[line_data]("new_category : ", "Provide")
 
    
    # mam tu problem z wprowadzaniem nowych danych = powinno być to obudowane warunkami. ale nie wiem jak
    for number, line in enumerate(table):
        if line[0] == id_:
            table[number][line_data] = new_record
    data_manager.write_table_to_file(file_name, table)
    show_table(table)
    return table


# ------------------------Special functions----------------------------


# function returns id of cheapest game.
def get_lowest_price_item_id(table):
    """
    Question: What is the id of the item that was sold for the lowest price?
    if there are more than one item at the lowest price, return the last item by alphabetical order of the title
    Args:
        table (list): data table to work on
    Returns:
         string: id
    """

    id_price_set = {line[id_index]: line[price_index] for line in table}
    for value in id_price_set.values():
        price = min(id_price_set.values())
    for key, value in id_price_set.items():
        if value == price:
            id_of_cheapest = key
    return id_of_cheapest


# function returns table filtered by dates of sale - for ERP only
def get_items_sold_between_ERP(table):
    """
    Question: Which items are sold between two given dates? (from_date < sale_date < to_date)
    Args:
        table (list): data table to work on
        month_from (int)
        day_from (int)
        year_from (int)
        month_to (int)
        day_to (int)
        year_to (int)
    Returns:
        list: list of lists (the filtered table)
    """
    date_list = []
    list_of_filtered_dates = compare_dates()
    for row in list_of_filtered_dates:
        for line in table:
            if row[0] == int(line[year_index]) and row[1] == int(line[month_index]) and row[2] == int(line[day_index]):
                date_list.append(line)
    return date_list


# function returns table filtered by dates of sale - this function is for test purpose only
# cannot implement it in this state into test and ERP both
def get_items_sold_between(table, month_from, day_from, year_from, month_to, day_to, year_to):
    """
    Question: Which items are sold between two given dates? (from_date < sale_date < to_date)
    Args:
        table (list): data table to work on
        month_from (int)
        day_from (int)
        year_from (int)
        month_to (int)
        day_to (int)
        year_to (int)
    Returns:
        list: list of lists (the filtered table)
    """
    date_from = [year_from, month_from, day_from]
    date_to = [year_to, month_to, day_to]
    date_table = [[int(line[year_index]), int(line[month_index]), int(line[day_index])] for line in table]
    list_of_dates = [line for line in date_table if line > date_from and line < date_to]
    date_list = []
    for row in list_of_dates:
        for line in table:
            if row[0] == int(line[year_index]) and row[1] == int(line[month_index]) and row[2] == int(line[day_index]):
                date_list.append(line[0:-1])
    common.make_numbers_in_nested(date_list, year_index, month_index, day_index, price_index)
    return date_list


# functions supports data abalyser
# --------------------------------


# gets title of game by sale id.
# Sale table must be readed by data manager
def get_title_by_id(id):
    """
    Reads the table with the help of the data_manager module.
    Returns the title (str) of the item with the given id (str) on None om case of non-existing id.

    Args:
        id (str): the id of the item

    Returns:
        str: the title of the item
    """

    table = data_manager.get_table_from_file(file_name)
    for line in table:
        if line[id_index] == id:
            return line[title_index]


# gets title of game by sale id. Table is in arg.
def get_title_by_id_from_table(table, id):
    """
    Returns the title (str) of the item with the given id (str) on None om case of non-existing id.

    Args:
        table (list of lists): the sales table
        id (str): the id of the item

    Returns:
        str: the title of the item
    """

    for line in table:
        if line[id_index] == id:
            return line[title_index]


# gets id of game, which was recently sold.
# Sale table must be readed by data manager
def get_item_id_sold_last():
    """
    Reads the table with the help of the data_manager module.
    Returns the _id_ of the item that was sold most recently.

    Returns:
        str: the _id_ of the item that was sold most recently.
    """
    table = data_manager.get_table_from_file(file_name)
    date_table = [[int(line[year_index]), int(line[month_index]), int(line[day_index])] for line in table]
    data_max = max(date_table)
    for line in table:
        if (
            data_max[0] == int(line[year_index]) and data_max[1] == int(line[month_index]) and
            data_max[2] == int(line[day_index])
        ):
            return str(line[id_index])


# gets id of game, which was recently sold.
# Table is in arg.
def get_item_id_sold_last_from_table(table):
    """
    Returns the _id_ of the item that was sold most recently.

    Args:
        table (list of lists): the sales table

    Returns:
        str: the _id_ of the item that was sold most recently.
    """

    date_table = [[int(line[year_index]), int(line[month_index]), int(line[day_index])] for line in table]
    data_max = max(date_table)
    for line in table:
        if (
            data_max[0] == int(line[year_index]) and data_max[1] == int(line[month_index]) and
            data_max[2] == int(line[day_index])
        ):
            return str(line[id_index])


# gets title of game, which was recently sold
# Table is in arg.
def get_item_title_sold_last_from_table(table):
    """
    Returns the _title_ of the item that was sold most recently.

    Args:
        table (list of lists): the sales table

    Returns:
        str: the _title_ of the item that was sold most recently.
    """

    date_table = [[int(line[year_index]), int(line[month_index]), int(line[day_index])] for line in table]
    data_max = max(date_table)
    for line in table:
        if (
            data_max[0] == int(line[year_index]) and data_max[1] == int(line[month_index]) and
            data_max[2] == int(line[day_index])
        ):
            return str(line[title_index])


# gets sum of prices for item
# Sale table must be readed by data manager
def get_the_sum_of_prices(item_ids):
    """
    Reads the table of sales with the help of the data_manager module.
    Returns the sum of the prices of the items in the item_ids.

    Args:
        item_ids (list of str): the ids

    Returns:
        number: the sum of the items' prices
    """

    table = data_manager.get_table_from_file(file_name)
    price = 0
    n = 0
    for line in table:
        if item_ids[n] in line:
            price += int(line[price_index])
            n += 1
            if n == len(item_ids):
                break
    return price


# gets sum of prices for item
# Table is in arg.
def get_the_sum_of_prices_from_table(table, item_ids):
    """
    Returns the sum of the prices of the items in the item_ids.

    Args:
        table (list of lists): the sales table
        item_ids (list of str): the ids

    Returns:
        number: the sum of the items' prices
    """

    price = 0
    n = 0
    for line in table:
        if item_ids[n] in line:
            price += int(line[price_index])
            n += 1
            if n == len(item_ids):
                break
    return price


# gets id of customer from id of game
# Sale table must be readed by data manager
def get_customer_id_by_sale_id(sale_id):
    """
    Reads the sales table with the help of the data_manager module.
    Returns the customer_id that belongs to the given sale_id
    or None if no such sale_id is in the table.

    Args:
        sale_id (str): sale id to search for
    Returns:
        str: customer_id that belongs to the given sale id
    """
    table = data_manager.get_table_from_file(file_name)
    for line in table:
        if line[id_index] == sale_id:
            return line[cust_index]


# gets id of customer from id of game
# Table is in arg.
def get_customer_id_by_sale_id_from_table(table, sale_id):
    """
    Returns the customer_id that belongs to the given sale_id
    or None if no such sale_id is in the table.

    Args:
        table: table to remove a record from
        sale_id (str): sale id to search for
    Returns:
        str: customer_id that belongs to the given sale id
    """

    for line in table:
        if line[id_index] == sale_id:
            return line[cust_index]


# gets unique (only one) id of customers
# Sale table must be readed by data manager
def get_all_customer_ids():
    """
    Reads the sales table with the help of the data_manager module.

    Returns:
        set of str: set of customer_ids that are present in the table
    """

    table = data_manager.get_table_from_file(file_name)
    list_customer_ids = common.make_list_of_elements(table, cust_index)
    return set(list_customer_ids)


# gets unique (only one) id of customers
# Table is in arg.
def get_all_customer_ids_from_table(table):
    """
    Returns a set of customer_ids that are present in the table.

    Args:
        table (list of list): the sales table
    Returns:
        set of str: set of customer_ids that are present in the table
    """

    list_customer_ids = common.make_list_of_elements(table, cust_index)
    return set(list_customer_ids)


# makes dictionary of customer id and list of sale id
# Sale table must be readed by data manager
def get_all_sales_ids_for_customer_ids():
    """
    Reads the customer-sales association table with the help of the data_manager module.
    Returns a dictionary of (customer_id, sale_ids) where:
        customer_id:
        sale_ids (list): all the sales belong to the given customer
    (one customer id belongs to only one tuple)

    Returns:
        (dict of (key, value): (customer_id, (list) sale_ids)) where the sale_ids list contains
            all the sales id belong to the given customer_id
    """
    table = data_manager.get_table_from_file(file_name)
    cust_sale_id = {}
    for line in table:
        if line[cust_index] in cust_sale_id:
            cust_sale_id[line[cust_index]].append(line[id_index])
        else:
            cust_sale_id[line[cust_index]] = [line[id_index]]
    return cust_sale_id


# makes dictionary of customer id and list of sale id
# Table is in arg.
def get_all_sales_ids_for_customer_ids_from_table(table):
    """
    Returns a dictionary of (customer_id, sale_ids) where:
        customer_id:
        sale_ids (list): all the sales belong to the given customer
    (one customer id belongs to only one tuple)
    Args:
        table (list of list): the sales table
    Returns:
         (dict of (key, value): (customer_id, (list) sale_ids)) where the sale_ids list contains
         all the sales id belong to the given customer_id
    """

    cust_sale_id = {}
    for line in table:
        if line[cust_index] in cust_sale_id:
            cust_sale_id[line[cust_index]].append(line[id_index])
        else:
            cust_sale_id[line[cust_index]] = [line[id_index]]
    return cust_sale_id


# counts number of transactions for customer
# Sale table must be readed by data manager
def get_num_of_sales_per_customer_ids():
    """
     Reads the customer-sales association table with the help of the data_manager module.
     Returns a dictionary of (customer_id, num_of_sales) where:
        customer_id:
        num_of_sales (number): number of sales the customer made
     Returns:
         dict of (key, value): (customer_id (str), num_of_sales (number))
    """

    table = data_manager.get_table_from_file(file_name)
    cust_sales = {}
    for line in table:
        if line[cust_index] in cust_sales:
            cust_sales[line[cust_index]] += 1
        else:
            cust_sales[line[cust_index]] = 1
    return cust_sales


# counts number of transactions for customer
# Table is in arg.
def get_num_of_sales_per_customer_ids_from_table(table):
    """
     Returns a dictionary of (customer_id, num_of_sales) where:
        customer_id:
        num_of_sales (number): number of sales the customer made
     Args:
        table (list of list): the sales table
     Returns:
         dict of (key, value): (customer_id (str), num_of_sales (number))
    """

    cust_sales = {}
    for line in table:
        if line[cust_index] in cust_sales:
            cust_sales[line[cust_index]] += 1
        else:
            cust_sales[line[cust_index]] = 1
    return cust_sales
