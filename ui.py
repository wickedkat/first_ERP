""" User Interface (UI) module """
#                             PRINTING TABLE FUNCTIONS

#
def get_max_width_column(table, table_list):
    max_width = []
    for column in range (len(table_list)):
        temp_width = 0
        for row in range (len(table)):
            if len(str(table[row][column])) > temp_width:
                temp_width = len(str(table[row][column]))
    max_width.append(int(temp_width))
    return max_width

def get_total_width_table(max_width, table_list):
    sum_width = len(table_list)*2
    for i in range (len(max_width)):
        sum_width += max_width[i]
    return sum_width

# prints middle part of table
def print_middle_border(sum_width):
    print('|', ('-'*(sum_width-3)), '|')

def print_titles_in_colums(title_list, max_width):
    for j in range(len(title_list)):
        col = title_list[j]
        width = max_width[j]
        print('|', col.center(width),  end='')
    print('|')

def print_table_contents(table, max_width, sum_width, title_list):
    row_number = 1
    for row in table:
        print_middle_border(sum_width)
        for col_i in range(len(row)):
            col = row[col_i]
            width = max_width[col_i]
            if col_i == 0:
                print('|', str(row_number).center(width),  end='')
            else:
                print('|', col.center(width),  end='')
        row_number += 1
        print('|')


def print_table(table, title_list):
    """
    Prints table with data.

    Example:
        /-----------------------------------\
        |   id   |      title     |  type   |
        |--------|----------------|---------|
        |   0    | Counter strike |    fps  |
        |--------|----------------|---------|
        |   1    |       fo       |    fps  |
        \-----------------------------------/

    Args:
        table (list): list of lists - table to display
        title_list (list): list containing table headers

    Returns:
        None: This function doesn't return anything it only prints to console.
    """

    max_width_column = []
    temp_table = table.copy()
    temp_table.append(title_list)
    max_width_column = get_max_width_column(temp_table, title_list)
    sum_width = get_total_width_table(max_width_column, title_list)
    print_titles_in_colums(title_list, max_width_column)
    print_table_contents(table, max_width_column, sum_width, title_list)



def print_result(result, label):
    """
    Displays results of the special functions.

    Args:
        result: result of the special function (string, list or dict)
        label (str): label of the result

    Returns:
        None: This function doesn't return anything it only prints to console.
    """

    print ('{}{}'.format (result, label))


def print_menu(title, list_options, exit_message):
    """
    Displays a menu. Sample output:
        Main menu:
            (1) Store manager
            (2) Human resources manager
            (3) Inventory manager
            (4) Accounting manager
            (5) Sales manager
            (6) Customer relationship management (CRM)
            (0) Exit program

    Args:
        title (str): menu title
        list_options (list): list of strings - options that will be shown in menu
        exit_message (str): the last option with (0) (example: "Back to main menu")

    Returns:
        None: This function doesn't return anything it only prints to console.
    """

    print(f"{title}:")
    for item in range (len(list_options)):
         print(f"     ({item+1}) {list_options[item]}")
    print(f"     (0) {exit_message}")



def get_inputs(list_labels, title):
    """
    Gets list of inputs from the user.
    Sample call:
        get_inputs(["Name","Surname","Age"],"Please provide your personal information")
    Sample display:
        Please provide your personal information
        Name <user_input_1>
        Surname <user_input_2>
        Age <user_input_3>

    Args:
        list_labels (list): labels of inputs
        title (string): title of the "input section"

    Returns:
        list: List of data given by the user. Sample return:
            [<user_input_1>, <user_input_2>, <user_input_3>]
    """
    inputs = []

    print(title)
    for item in list_labels:
        inputs.append(input(item))

    os.system("clear")
    return inputs


def print_error_message(message):
    """
    Displays an error message (example: ``Error: @message``)

    Args:
        message (str): error message to be displayed

    Returns:
        None: This function doesn't return anything it only prints to console.
    """

    print('Error : {}'.format (message)) # your code
