"""
This module creates reports for the marketing department.
This module can run independently from other modules.
Has no own data structure but uses other modules.
Avoud using the database (ie. .csv files) of other modules directly.
Use the functions of the modules instead.
"""

# todo: importing everything you need

# importing everything you need
import ui
import common
from sales import sales
from crm import crm
import input_mod

# variables for menu data analyser
OPTION = ['0', '1', '2', '3', '4', '5', '6', '7']
title = "Data analyser menu:"
options = ["Last buyer name",
           "Last buyer id",
           "Name of client who spends most money (and amount)",
           "ID of client who spends most money (and amount)",
           "Name of most frequent buyer",
           "ID of most frequent buyer",
           "Customers that didn't buy anything"]
exit_message = "Back to main menu"


# ------helpful functions for data analyser only------
# choosing option in menu
def choose():
    """ Function gets input from user
    and starts options from module.
    No arg
    Returns nothing"""
    inputs = input_mod.get_inputs(['Enter a number: '], '')
    option = inputs[0]
    if option == "1":
        ui.print_result(get_the_last_buyer_name(), 'Name of last buyer: ')
    elif option == "2":
        ui.print_result(get_the_last_buyer_id(), 'ID of last buyer: ')
    elif option == "3":
        ui.print_result(get_the_buyer_name_spent_most_and_the_money_spent(), 'Client who spends most: ')
    elif option == "4":
        ui.print_result(get_the_buyer_id_spent_most_and_the_money_spent(), 'ID of client who spends most: ')
    elif option == "5":
        ui.print_result(get_the_most_frequent_buyers_names(num=1), 'Most frequent client: ')
    elif option == "6":
        ui.print_result(get_the_most_frequent_buyers_ids(num=1), 'ID of most frequent client: ')
    elif option == '7':
        ui.print_result(get_poor_customers(), 'Poor people - no profit, only pain in the ass: ')
    elif option == '0':
        raise ValueError
    while option not in OPTION:
        raise KeyError
        menu_control()


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

    pass


def get_the_last_buyer_name():
    """
    Returns the customer _name_ of the customer made sale last.

    Returns:
        str: Customer name of the last buyer
    """

    id_game_sold_last = sales.get_item_id_sold_last()
    id_customer = sales.get_customer_id_by_sale_id(id_game_sold_last)
    return crm.get_name_by_id(id_customer)


def get_the_last_buyer_id():
    """
    Returns the customer _id_ of the customer made sale last.

    Returns:
        str: Customer id of the last buyer
    """

    id_game_sold_last = sales.get_item_id_sold_last()
    return sales.get_customer_id_by_sale_id(id_game_sold_last)


def get_the_buyer_name_spent_most_and_the_money_spent():
    """
    Returns the customer's _name_ who spent the most in sum and the money (s)he spent.

    Returns:
        tuple: Tuple of customer name and the sum the customer spent eg.: ('Daniele Coach', 42)
    """
    sales_per_customer = sales.get_all_sales_ids_for_customer_ids()
    sales_by_name = {crm.get_name_by_id(k): v for k, v in sales_per_customer.items()}
    for k, v in sales_by_name.items():
        sales_by_name[k] = sales.get_the_sum_of_prices(v)
    max_spender_name = (max(sales_by_name, key=sales_by_name.get),
                        sales_by_name[max(sales_by_name, key=sales_by_name.get)])
    return max_spender_name


def get_the_buyer_id_spent_most_and_the_money_spent():
    """
    Returns the customer's _id_ who spent more in sum and the money (s)he spent.

    Returns:
        tuple: Tuple of customer id and the sum the customer spent eg.: (aH34Jq#&, 42)
    """

    sales_per_customer = sales.get_all_sales_ids_for_customer_ids()
    for k, v in sales_per_customer.items():
        sales_per_customer[k] = sales.get_the_sum_of_prices(v)
    max_spender_id = (max(sales_per_customer, key=sales_per_customer.get), sales_per_customer[max(sales_per_customer,
                      key=sales_per_customer.get)])
    return max_spender_id


def get_the_most_frequent_buyers_names(num=1):
    """
    Returns 'num' number of buyers (more precisely: the customer's name) who bought most frequently in an
    ordered list of tuples of customer names and the number of their sales.

    Args:
        num: the number of the customers to return.

    Returns:
        list of tuples: Ordered list of tuples of customer names and num of sales
            The first one bought the most frequent. eg.: [('Genoveva Dingess', 8), ('Missy Stoney', 3)]
    """
    id_in_tupla = 0
    sales_number_in_tupla = 1
    list_of_frequents_buyers = []
    frequents_buyer_id = get_the_most_frequent_buyers_ids(num)
    for item in frequents_buyer_id:
        list_of_frequents_buyers.append((crm.get_name_by_id(item[id_in_tupla]), item[sales_number_in_tupla]))
    return list_of_frequents_buyers


def get_the_most_frequent_buyers_ids(num=1):
    """
    Returns 'num' number of buyers (more precisely: the customer ids of them) who bought more frequent in an
    ordered list of tuples of customer id and the number their sales.

    Args:
        num: the number of the customers to return.

    Returns:
        list of tuples: Ordered list of tuples of customer ids and num of sales
            The first one bought the most frequent. eg.: [(aH34Jq#&, 8), (bH34Jq#&, 3)]
    """

    sales_num_per_cust_dict = sales.get_num_of_sales_per_customer_ids()
    customer_sales_number = list(sales_num_per_cust_dict.items())
    return customer_sales_number[0:num]


def get_poor_customers():
    """
    Returns list of names of people who didn't buy anything.
    Returns: list
    """
    id_name_dict = crm.get_id_name_set()
    all_customers_id = sales.get_all_customer_ids()
    list_of_poor_people = []
    for k, v in id_name_dict.items():
        if k not in all_customers_id:
            list_of_poor_people.append(v)
    return list_of_poor_people
