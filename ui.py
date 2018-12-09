""" User Interface (UI) module """
#                             PRINTING TABLE FUNCTIONS

# gets lenght of the longest word in column
max_length_column = []


# define max length of colums in table
def max_length(table, title_list):
    max_length_column = []
    for column in range(len(title_list)):
        temp = 0
        for row in range(len(table)):
            if len(str(table[row][column])) > temp:
                temp = len(str(table[row][column]))
                temp = int(temp)
        max_length_column.append(temp)
    return max_length_column


# define added length of table based on column length
def sum_length_table(max_length_column, title_list):
    sum_length = len(title_list)*2
    for i in range(len(max_length_column)):
        sum_length += max_length_column[i]
    return sum_length


# prints upper part of table
def print_top_border(sum_length):
    print('/', ('-'*(sum_length-3)), '\\')


# prints middle part of table
def print_middle_border(sum_length):
    print('|', ('-'*(sum_length-3)), '|')


# prints bottom part of table
def print_bottom_border(sum_length):
    print('\\', ('-'*(sum_length-3)), '/')


# prints columns title - each module has diffrent title_list
def print_columns_title(title_list, max_length_column):
    for col_i in range(len(title_list)):
        col = title_list[col_i]
        width = max_length_column[col_i]
        print('|', col.center(width),  end='')
    print('|')


# prints what is in table - table is diffrent for each module
def print_items_table(table, max_length_column, sum_length, title_list):
    row_number = 1
    for row in table:
        print_middle_border(sum_length)
        for col_i in range(len(row)):
            col = row[col_i]
            width = max_length_column[col_i]
            if col_i == 0:
                print('|', str(row_number).center(width),  end='')
            else:
                print('|', col.center(width),  end='')
        row_number += 1
        print('|')


# print table based on tilte list and table from modules
def print_table(table, title_list):
    """
    Prints table with data.
    Args:
        table (list): list of lists - table to display
        title_list (list): list containing table headers
    Returns:
        None: This function doesn't return anything it only prints to console.
    """

    max_length_column = []
    temp_table = table.copy()
    temp_table.append(title_list)
    max_length_column = max_length(temp_table, title_list)
    sum_length = sum_length_table(max_length_column, title_list)
    print_top_border(sum_length)
    print_columns_title(title_list, max_length_column)
    print_items_table(table, max_length_column, sum_length, title_list)
    print_bottom_border(sum_length)

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


#prints main menu of every module
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


#gets input from user, matches it with labels and returns as a list


def print_error_message(message):
    """
    Displays an error message (example: ``Error: @message``)

    Args:
        message (str): error message to be displayed

    Returns:
        None: This function doesn't return anything it only prints to console.
    """

    print('Error : {}'.format (message)) # your code
