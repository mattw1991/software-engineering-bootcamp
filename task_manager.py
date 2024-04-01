# Welcome to Task Manager - my final project on CoGrammar's Software Engineering Bootcamp.
# This allows a user to add and manage tasks and new users, and compile stats and reports.

# Notes: 
# 1. Use the following username and password to access the admin rights 
# username: admin
# password: password
# 2. Ensure you open the whole folder for this task in VS Code otherwise the 
# program will look in your root directory for the text files.


# ***********The following functions were created by Matt********************



# find_users function identifies users currently registered. This will be run in other
# functions to ensure a username isn't registered twice, and so tasks can be assigned
# or reassigned as appropriate.
def find_users():

# Use FOR loop to create list of current usernames. Initialise list, open user.txt,
# read and copy each line, separate where ';' occurs, and append the first string
# (the original line up to the first ';') to current_users.
    current_users = []
    with open ("user.txt", "r") as user_file:
        for line in user_file:
            text = line
            text = text.split(';')
            current_users.append(text[0])
    return current_users



# reg_user function allows user to register a new username.
def reg_user():
    print("\nRegister New User")
    
# username_ok is false until the username chosen is not yet in use, and new username
# isn't blank, and doesn't contain ';'.
    username_ok = False

# Until username_ok = false, repeat attempts to register a username.
# Entering 'CANCEL' or any variation of upper/lowercase or blankspace
# will terminate the process.
    while username_ok == False:
        username = input("\nCreate a username, or type CANCEL to abort: ")

# Use find_users function to identify users currently registered.
        current_users = find_users()

# Check there is no ';' as this would disrupt the program's reading of user.txt.
# In this case, username_ok will remain false and user will have to try again.
        username_check = username.find(";")
        if username_check != -1:
            print("';' not permitted in usernames - please try a different username.")

# If password already exists, prompt user to try a different username.
        elif username in current_users:
            print("Username already in use. Please choose a different one.")

# If ENTER pressed before any characters, user will have to try again.
        elif username == "":
            print("Please enter a username before hitting ENTER.")

# Trigger end of process if 'CANCEL' entered - username_ok = True means user will
# not be prompted again.
        elif username.upper().strip(" ") == "CANCEL":
            print("User registration cancelled.")
            username_ok = True

# If none of the above occur, username is ok - set username_ok to True to end loop.
        else:
            username_ok = True

# Request password from user. Initially setting password and password_check as different
# values allows code to run each time the inputs do not match. Runs until both password
# and password_check are the same.
    password_ok = False

# If 'CANCEL' was entered previously, program will skip this loop.
    if username.upper().strip(" ") != "CANCEL":

# While passwords don't match, user will have to keep trying until they are both the same.
        while password_ok == False:

# Prompt input of password. 
            password = input("Choose a password: ")
            password_check = password.find(";")

# Print error message is password contains ';' or is empty and prompt to try again.
            if password_check != -1:         
                print("';' not permitted in passwords - please try a different username.")
            elif password == "":
                print("Password required - please enter a password.")

# If password ok, prompt confirmation. If confirmation not matching, prompt to try again.
            else:
                password_confirm = input("Confirm your password: ")
                if password != password_confirm:
                    print("Passwords do not match - please try again")

# If passwords are acceptable and matching, end loop.
                else:
                    password_ok = True

# Open user.txt and add username and password, separated by ';'. Print confirmation message
# and use undefined 'return' to show end of function.
        with open("user.txt", "a") as out_file:
            out_file.write(f"\n{username};{password}")
        print("New user registered.")
    return



# add_task function allows user to add a new task.
def add_task():

# Use find_users function to identify users currently registered.
    current_users = find_users()

# Request username of person task is assigned to. Checks the original user.txt file 
# to ensure user exists, and, if not, prompts error message. Repeat until valid
# username inputted.
    task_user_ok = False
    while task_user_ok == False:
        task_username = input("Enter username of the person the task is assigned to: ")
        if task_username not in current_users:
            print("User does not exist. Please enter a valid username")
        else:
            task_user_ok = True

# Request user to enter a title, and then description, of the task.
    task_title = input("Please enter the name of the task: ")
    task_description = input("Please enter a description of the task: ")

# Use WHILE loop to request date input and check this against prespecified date format.
# If it doesn't match, request the user to try again.
    while True:
        try:
            task_due_date = input("Due date of task (YYYY-MM-DD): ")
            due_date_time = datetime.strptime(task_due_date, DATETIME_STRING_FORMAT)
            break
        except ValueError:
            print("Invalid datetime format. Please use the format specified")
    
# Take today's date as another input. Take these five inputs from this function, plus the
# value 'No' (in reference to whether the task is completed) and add this information,
# with each item separated by ';' to tasks.txt.
    curr_date = date.today()
    with open("tasks.txt", "a") as task_file:
        task_file.write(f"\n{task_username};{task_title};{task_description};{task_due_date};{curr_date};No")
    print("Task added successfully.")
    return



# view_all allows user to view all tasks in task.txt - create string based on information
# in text file and print it. Start by printing line break for display purposes.
def view_all():
    print("")

# Open tasks.txt, read and copy each line, split where ';' occurs, and print as a formatted
# string displaying all the required information.
    with open("tasks.txt", "r") as task_list:
        for line in task_list:
            text = line
            text = text.split(';')
            task_text = f'''Task username: \t\t{text[0]}
Task name: \t\t{text[1]}
Task description: \t{text[2]}
Due date: \t\t{text[3]}
Assigned date: \t\t{text[4]}
Completed?: \t\t{text[5]}'''
            print(task_text)
    return



# view_mine is partially the same as view_all and allows user to see only their own tasks,
# as well as modify them. First, print blankspace for display purposes.        
def view_mine():
    print("")

# Use find_users function to identify users currently registered.
    current_users = find_users()

# Initialise the following variables - these will be used to keep track of which tasks
# are assigned to the current logged on user, for display and editing purposes.
    task_number_displayed = 0
    tasks_available = []
    tasks_display = []
    tasks_line = []

# Open tasks.txt. For each line, copy, and split at ';' to make a list.
    with open("tasks.txt", "r") as task_list:
        for line in task_list:
            text = line
            text = text.split(';')

# If the first item in each line is the same as the logged on user, increment
# task_number_displayed. Add this display number to the list of available 
# task numbers, tasks_available.
            if text[0] == curr_user:
                task_number_displayed += 1
                tasks_available.append(task_number_displayed)

# Set task_text to give this display number, plus details of the task, in a clearly
# readable way. Use 'f' tool to format information in string, then print it.
                task_text = f'''***Task Number {task_number_displayed}***
Task username: \t\t{text[0]}
Task name: \t\t{text[1]}
Task description: \t{text[2]}
Due date: \t\t{text[3]}
Assigned date: \t\t{text[4]}
Completed?: \t\t{text[5]}'''
                print(task_text)

# Add this string to tasks_display, and add the original line from the file to tasks_line.
                tasks_display.append(task_text)
                tasks_line.append(line)

# At this point, all of the current user's tasks will have just been printed on the terminal.
# Use the tasks_available list to show the user which tasks they can select to edit, or -1
# to return to main menu. Prompt user for input.
        print(f"\nPlease enter one of the following tasks number to edit it: {tasks_available}, or '-1' to return to main menu: ")
        
# Initialise task_edit_ok to false - this will become true once a valid input is given.
# Request user to input task number they would like to change, or -1.    
        task_edit_ok = False
        while task_edit_ok == False:
            task_edit = input("Please enter task number or -1: ")

# If the input string can be a positive integer, and if the int version of the str
# is in the list of tasks the user can edit, end loop.
            if task_edit.isdigit() == True and int(task_edit) in tasks_available:
                task_edit_ok = True

# If user inputs -1 to end the task, end the loop.
            elif task_edit == '-1':
                task_edit_ok = True

# If neither of the above occurs, print error message. User will return to input prompt.    
            else:
                print("Input not valid - please enter task number or -1: ")
        
# Change the previous input from str to int for processing.
        task_edit = int(task_edit)

# Proceed as long as user hasn't inputted -1 to return to main menu.
        if task_edit != -1:

# Open tasks.txt. Take each line and put into a new list, task_data.
            with open("tasks.txt", "r") as tasks_file:
                task_data = tasks_file.readlines()

# Find the line requiring indexing using the tasks_line list created earlier.
# When user reads 'task 1' it will be saved in position 0 in this list so ensure
# position (task_edit -1) is used.
                line_for_indexing = tasks_line[task_edit - 1]

# Find the line number in the document corresponding to this line.
                line_to_edit = task_data.index(line_for_indexing)

# Take this line, and split it at ';' to form a list.
                info_to_edit = task_data[line_to_edit]
                info_to_edit = info_to_edit.split(';')

# If info_to_edit[5] = "Yes\n" the task is already marked as complete and cannot now be
# altered again. In this case, print this task for display purposes plus a message with 
# this information, prompting the user to hit ENTER to return to main menue.
                if info_to_edit[5] == "Yes\n":
                    print("\n" + tasks_display[task_edit - 1])
                    input("Task is already complete, and can no longer be modified. Press enter to continue.")
                
# If a task is not marked as complete, it can be edited. Print the task for the user to see again.
                else:    
                    print(tasks_display[task_edit - 1])

# Initialise option_ok as false - it will remain false until a valid option is inputted.
                    option_ok = False

# Request the user to choose a letter from the options list.
                    print("\nPlease enter one of the following one letter codes to proceed: ")
                    while option_ok == False:
                        print("a: edit 'assigned to', d: edit 'due date', c: mark as 'completed', m: back to main menu")
                        options_list = ['a', 'd', 'c', 'm']
                        task_edit_choice = input("Please enter the code: ")

# Convert to lowercase and remove blankspace. If invalid input, print error message and
# return to input.
                        if task_edit_choice.lower().strip(" ") not in options_list:
                            print("Invalid input - please use one of the codes listed below. ")
                        
# If the letter entered corresponds to an option from the list, end loop and continue.
                        else:
                            option_ok = True
                
# If user wants to reassign the username of the chosen task, initialise new_assigned_user_ok
# as false. This will remain the case until the input matches an existing username. If user 
# selects 'm', this section will be bypassed and function will end without extra processing.           
                        if task_edit_choice != 'm':    
                            if task_edit_choice == 'a':
                                new_assigned_user_ok = False
                                while new_assigned_user_ok == False:

# Prompt user for input. If username does not exist, print error message and repeat loop. 
# If it does, end loop.
                                    new_assigned_user = input('Enter the username you want to assign this task to: ')
                                    if new_assigned_user in current_users:
                                        new_assigned_user_ok = True
                                    else:
                                        print("Username not found - please try again: ")

# Change info_to_edit[0] to the new username. Print confirmation message.
                                info_to_edit[0] = new_assigned_user
                                print(f"Task has been reassigned to {new_assigned_user}.")
                    
# If user wants to change the due date, as in def add_task, request an input for the date.
# If the wrong date format is used, the user will be asked to try again.
                            elif task_edit_choice == 'd':
                                while True:
                                    try:
                                        new_task_due_date = input("Due date of task (YYYY-MM-DD): ")
                                        new_due_date_time = datetime.strptime(new_task_due_date, DATETIME_STRING_FORMAT)
                                        break
                                    except ValueError:
                                        print("Invalid datetime format. Please use the format specified")

# Keep only the first 10 characters (removing the time component) and convert to string.
# Set this string as info_to_edit[3] and print confirmation message.
                                new_date = str(new_due_date_time)[0:10]
                                info_to_edit[3] = new_date
                                print(f"Due date has been modified to {new_date}.")

# If user wants to mark the task as complete, print warning message that if this is done,
# no further changes will be possible.
                            elif task_edit_choice == 'c':
                                print("Once task is marked as complete, user cannot be changed.")

# Initialise complete_task_ok as false. Loop will repeat until Y or N is entered (upper or lower
# case and blankspaces ok). If Y entered, set info_to_edit as "Yes\n" (end of line in tasks.txt
# so \n required), and end loop. If N entered, do nothing and end loop. If neither, print error
# message and request input again. If loop ended, print confirmation message.
                                complete_task_ok = False
                                while complete_task_ok == False:
                                    complete = input("Are you sure you want to mark as complete? Y/N: ")
                                    if complete.upper() == 'Y':
                                        info_to_edit[5] = "Yes\n"
                                        complete_task_ok = True
                                        print("Task marked as complete! It can no longer be edited.")
                                    elif complete.upper() == 'N':
                                        complete_task_ok = True
                                        print("Task not marked as complete and can still be edited.")
                                    else:
                                        print("Invalid input. Please try again - enter 'Y' or 'N' only. ")

# Initialise the new string to go into the text file. Use a FOR loop to concatenate the
# items in the info_to_edit list, separated by semicolons. Only one item will have been
# changed from the original line in the file.
                            new_edited_string = ""
                            for a in range (0, 5):
                                new_edited_string += info_to_edit[a] + ";"
                            new_edited_string += info_to_edit[5]

# Go back to the data originally extracted from the text file, and replace the previous
# line with the new edited line.
                            task_data[line_to_edit] = new_edited_string

# Open the text file and rewrite it with the edited information - all lines except one
# will be the same.
                            with open ("tasks.txt", "w") as tasks_file:
                                for line in task_data:
                                    tasks_file.write(line)                
    return        



# Generate Report Function - this will create two texts files giving some specific
# information on users and tasks. Starts with the user report.
def gen_reports():

# Initialise counters which will increment when the conditions are satisfied.
    total_tasks = 0
    total_completed_tasks = 0
    total_uncompleted_tasks = 0
    total_overdue_tasks = 0

# Open the tasks.txt file. For each line, copy it, and split it where ';' occurs to make
# a list.
    with open ("tasks.txt", "r") as task_file:
        for line in task_file:
            total_tasks += 1
            text = line
            text = text.split(';')

# Task position 3 in this list - this is a string containing the due date. Convert
# this to format datetime.date for comparison with today's date.
            due_date = text[3]
            due_date = datetime.strptime(due_date, "%Y-%m-%d").date()

# If position 5 contains "Yes", increment counter for completed tasks. If not, increment
# counter for uncompleted tasks.
            if text[5] == "Yes\n" or text[5] == "Yes":
                total_completed_tasks += 1
            else:
                total_uncompleted_tasks += 1

# Compare due date with today's date. If the due date is in the past, incrememnt counter
# for total overdue tasks.
            if date.today() > due_date:
                total_overdue_tasks += 1

# Calculate completed and uncompleted tasks as an integer percentage (for clearer display).
    percentage_completed_tasks = round(total_completed_tasks * 100 / total_tasks)
    percentage_uncompleted_tasks = round(total_uncompleted_tasks * 100 / total_tasks)

# Create text to be added to the report, using format tool to include calculated values.
    t_overview_str = f"""***Task Overview***

Total number of tasks: \t\t\t\t{total_tasks}
Total number of tasks complete: \t\t{total_completed_tasks}
Total number of tasks incomplete: \t\t{total_uncompleted_tasks}
Total number of overdue uncompleted tasks: \t{total_overdue_tasks}
Percentage of tasks completed: \t\t\t{percentage_completed_tasks}
Percentage of tasks uncompleted: \t\t{percentage_uncompleted_tasks}"""
    
# Create the file or overwrite the existing one, add this string, and print confirmation.
# The user report has now been generated.
    with open ("task_overview.txt", "w") as t_overview:
        t_overview.write(t_overview_str)

# Now create the tasks report.
# Use find_users function to identify users currently registered.
    current_users = find_users()

# Initialise lists which will be used to keep running totals of various parameters.
    user_totals = [0] * len(current_users)
    user_completed_totals = [0] * len(current_users)
    user_uncompleted_totals = [0] * len(current_users)
    user_uncompleted_overdue = [0] * len(current_users)

# Open text file. Copy each line, separate where ';' occurs, and make results into a list.
    with open ("tasks.txt", "r") as task_file:
        for line in task_file:
            text = line
            text = text.split(';')

# Take text[3] as due date, then convert to datetime.date format.
            due_date = text[3]
            due_date = datetime.strptime(due_date, "%Y-%m-%d").date()

# Find index of username within users list - this will be the index for all list increments.
            user_to_increment = current_users.index(text[0])

# Increment user_totals. Use a check to see if any version of "Yes" exists in the last
# index position. If so, increment user_completed_totals list, at index corresponding to
# correct username. If not, increment relevant index of user_uncompleted totals. If task 
# is overdue, increment relevant index of user_uncompleted_overdue.
            user_totals[user_to_increment] += 1
            complete_check = text[5].find("Yes")
            if complete_check != -1:
                user_completed_totals[user_to_increment] += 1
            else:
                user_uncompleted_totals[user_to_increment] += 1
                if date.today() > due_date:
                    user_uncompleted_overdue[user_to_increment] += 1
            
# Initialise lists to be used for converting values to various percentage statistics.
    user_percent_of_tasks = []
    user_percent_completed = []
    user_percent_uncompleted = []
    user_percent_uncompleted_overdue = []
    
# For each index position in user_totals, as long as a task appears on the task list for
# this user, calculate user's percentage of overall tasks, the percentage of their own
# tasks that are complete and incomplete, and the percentage of their own tasks which are
# incomplete and overdue. Add these results to the previously initialised lists.
    for value in range(0, len(current_users)):
        if user_totals[value] != 0:
            percent_of_tasks = round(user_totals[value] * 100 / total_tasks)
            user_percent_of_tasks.append(percent_of_tasks)
            percent_completed = round(user_completed_totals[value] * 100 / user_totals[value])
            user_percent_completed.append(percent_completed)
            percent_uncompleted = round(user_uncompleted_totals[value] * 100 / user_totals[value])
            user_percent_uncompleted.append(percent_uncompleted)
            percent_uncompleted_overdue = round(user_uncompleted_overdue[value] * 100 / user_totals[value])
            user_percent_uncompleted_overdue.append(percent_uncompleted_overdue)
        
# If a username has no tasks, just append zeros to the previously initialised lists.        
        else:
            user_percent_of_tasks.append(0)
            user_percent_completed.append(0)
            user_percent_uncompleted.append(0)
            user_percent_uncompleted_overdue.append(0)

# Create a string containing these statistics for each user. Use a FOR loop to run through
# each username and add text containing their statistics.    
    u_overview_str = "***User Overview***\n"
    for number in range(0, len(current_users)):
        u_overview_str += f"""
User: {current_users[number]}
User's total tasks: {user_totals[number]}
Percentage of total tasks assigned to user: {user_percent_of_tasks[number]} %
Percentage of user's tasks completed: {user_percent_completed[number]} %
Percentage of user's tasks uncompleted: {user_percent_uncompleted[number]} %
Percentage of user's tasks uncompleted and overdue: {user_percent_uncompleted_overdue[number]} %\n"""
    
# Open or overwrite the text file with the string containing this information, and
# print confirmation. The second of the two reports has now been made.
    with open ("user_overview.txt", "w") as u_overview:
        u_overview.write(u_overview_str)
    print("\nReports have been generated and saved to the current directory.")
    return    



# disp_stats allows user to display the reports created in gen_reports() in the terminal.
def disp_stats():

# Run gen_reports() so ensure the reports exist and are up to date.
    gen_reports()

# Open each report and, using FOR loops, print the contents in the terminal.
    with open ("task_overview.txt", "r") as task_ov:
        text = task_ov.readlines()
        print("")
        for line in text:
            print(line.strip("\n"))
    with open ("user_overview.txt", "r") as user_ov:
        text = user_ov.readlines()
        print("\n")
        for line in text:
            print(line.strip("\n"))
    return        



# ***************The following was provided as part of this task**************************
        


#=====importing libraries===========
import os
from datetime import datetime, date

DATETIME_STRING_FORMAT = "%Y-%m-%d"

# Create tasks.txt if it doesn't exist
if not os.path.exists("tasks.txt"):
    with open("tasks.txt", "w") as default_file:
        pass

with open("tasks.txt", 'r') as task_file:
    task_data = task_file.read().split("\n")
    task_data = [t for t in task_data if t != ""]


task_list = []
for t_str in task_data:
    curr_t = {}

    # Split by semicolon and manually add each component
    task_components = t_str.split(";")
    curr_t['username'] = task_components[0]
    curr_t['title'] = task_components[1]
    curr_t['description'] = task_components[2]
    curr_t['due_date'] = datetime.strptime(task_components[3], DATETIME_STRING_FORMAT)
    curr_t['assigned_date'] = datetime.strptime(task_components[4], DATETIME_STRING_FORMAT)
    curr_t['completed'] = True if task_components[5] == "Yes" else False

    task_list.append(curr_t)

#====Login Section====
'''This code reads usernames and password from the user.txt file to 
    allow a user to login.
'''
# If no user.txt file, write one with a default account
if not os.path.exists("user.txt"):
    with open("user.txt", "w") as default_file:
        default_file.write("admin;password")

# Read in user_data
with open("user.txt", 'r') as user_file:
    user_data = user_file.read().split("\n")

# Convert to a dictionary
username_password = {}
for user in user_data:
    username, password = user.split(';')
    username_password[username] = password

logged_in = False
while not logged_in:

    print("LOGIN")
    curr_user = input("Username: ")
    curr_pass = input("Password: ")
    if curr_user not in username_password.keys():
        print("User does not exist")
        continue
    elif username_password[curr_user] != curr_pass:
        print("Wrong password")
        continue
    else:
        print("Login Successful!")
        logged_in = True


while True:
    # presenting the menu to the user and 
    # making sure that the user input is converted to lower case.
    print()
    menu = input('''Select one of the following Options below:
r - Registering a user
a - Adding a task
va - View all tasks
vm - View my task
gr - Generate reports
ds - Display statistics
e - Exit
: ''').lower()

    if menu == 'r':
       reg_user()
    elif menu == 'a':
        add_task()
    elif menu == 'va':
        view_all()
    elif menu == 'vm':
        view_mine()
    elif menu == 'gr':
        gen_reports()
    elif menu == 'ds' and curr_user == 'admin': 
        disp_stats()   
    elif menu == 'ds' and curr_user != 'admin':
        print("\nOnly the administrator can display statistics. Please choose another option.")
    elif menu == 'e':
        print('Goodbye!!!')
        exit()
    else:
        print("You have made a wrong choice, Please Try again")