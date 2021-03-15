"""
Version 1 of the book tracking system

Version 1 looks to establish connection to the database and then gather input from the user
    Valid user input:
        * Add entry
        * Edit entries
        * Delete entries
        * Update CSV file

"""

import sqlite3 as sql
import datetime
import csv


# Represents all possible genres a user can input.
GENRES = ["fiction", "nonfiction", "action", "adventure", "Art", "architecture", "Alternate history",
          "autobiography", "anthology", "biography", "chick lit", "business", "economics", "children's",
          "crafts", "hobbies", "classic", "diary", "crime", "drama", "health", "fantasy", "history",
          "graphic novel", "horror", "memoir", "philosophy", "poetry", "religion", "romance",
          "textbook", "science fiction", "short story", "science", "self help", "thriller", "sports",
          "western", "travel"]

# Following valued represent the upper and lower bounds of the menu options, designed
# to be updated as more menu options introduced.
MENU_UPPER_BOUND = 4
MENU_LOWER_BOUND = 1

def main():
    """ Driver for the first version of the book tracker. Calls required methods. """
    # Establishing the connection to the database by calling the connection method
    connect()

    # Getting the user input
    user_selection = menu()
    user_selection_to_action(user_selection)

    user_continue = True
    while user_continue == True:
        response = str(input("Would you like to do another operation? Enter Y to continue"))
        response = response.upper()
        if response == 'Y':
            # Getting the user input
            user_selection = menu()
            user_selection_to_action(user_selection)
        else:
            user_continue = False

def connect():
    """ Establising the connection to the databse """
    global dataBase, cursor
    dataBase = sql.connect('book_tracking.db')
    cursor = dataBase.cursor()

def clearDatabase():
    """ This method will  """
    query = 'DELETE from books'
    cursor.execute(query)
    dataBase.commit()

def add_book():
    """ Need to gather: Title, Author, page_count, Genre and then add entry to database. """

    # Only constraints for title is title != ''
    title = input(print("\nWhat was the title of the book:   "))
    if len(title) <= 0:
        title = input(print("\nWhat was the title of the book:   "))

    # Author must not be an empty string
    author = input(print("\nWho was the author of this book:   "))
    if len(author) <= 0:
        author = input(print("\nWho was the author of this book:   "))

    # page_count must be an integer > 0
    page_count = - 1
    while page_count < 0:
        try:
            page_count = int(input(print("\nWhat was the page count:   ")))
        except ValueError:
            print('')
    # At this point page_count is guaranteed to be an int > 0
    # print("Page count is", page_count) =====> Test count

    genre = input(print("\nWhat was the genre?   "))
    while not genre in GENRES:
        genre = input(print("\nWhat was the genre?   "))

    # This is a test statement, used to ensure user input was recoreded correctly.
    # print("Title {}, Author {}, Page Count {}, Genre: {}".format(title,author,page_count,genre))

    entry_date = datetime.date.today() # Getting today's date for our records.
    # print(entry_date)

    # Here we change all strings to the lowercase version. This is done just for ease of use.
    title_lower = title.lower()
    author_lower = author.lower()
    genre_lower = genre.lower()

    query = '''
    	insert into books
    	(Title, Author, page_count, Genre, entry_date)
    	values (?, ?, ?, ?, ?) '''

    cursor.execute(query, (title_lower, author_lower, page_count, genre_lower,
                           entry_date))
    dataBase.commit()

def update_entry():
    """ This method will access a certain book in the database and update values stored."""
    # This method will look for a user to input a title and update the entry for that title.

    # Here we need to get the title of the book the user wants to update.
    # Only constraints for title is title != ''
    title = input("\nWhat was the title of the book?   ")
    if len(title) <= 0:
        title = input("\nWhat was the title of the book?   ")
    # Convert title to lowercase version
    title_lower = title.lower()

    # Author must not be an empty string
    author = input("\nWho was the author of this book?   ")
    if len(author) <= 0:
        author = input("\nWho was the author of this book?   ")
    author_lower = author.lower()

    genre = input("\nWhat was the genre?   ")
    while not genre in GENRES:
        genre = input("\nWhat was the genre?   ")
    genre_lower = genre.lower()

    query = ''' update books set Author = ?, Genre = ? where Title = ? '''
    cursor.execute(query, (author_lower,genre_lower,title_lower))
    dataBase.commit()

    # If the query was successful the rowcount will be 1, if not it will be zero.
    # Thus we can check if the update was successful by checking the rowcount.
    if cursor.rowcount < 1:
        print("Query was not successful. Check spelling of title and try again.\n")
    else:
        print("Query update was successful.\n")


def user_selection_to_action(user_selection):
    """ This method takes in the response returned from menu() and decides on what action to tale. """
    # Simple if block designed to be updated as more menu options introduced.
    if user_selection == 1:
        add_book()
    elif user_selection == 2:
        update_entry()
    elif user_selection == 3:
        show_all()
    elif user_selection == 4:
        user_choice = str(input(print("Are you really sure you wish to clear the dataBase? Enter 'Y' to confirm\n")))
        user_choice = user_choice.upper()
        if user_choice == 'Y':
            clearDatabase()
            print("Database has successfully been cleared.")
        else:
            print("Database had not been cleared\n")
    else:
        # If code reaches here we know sanitization failed.
        print("Invalid entry. SANITIZATION FAILED")

def menu():
    """
    Displays menu for the user, returns an integer value representing user selection

    Menu options:

        * 1: Add a book
        * 2: Update an entry in the database
        * 3: Show all books in the database

    """

    user_option_sanitized = -1 # Value of -1 means that user input has not been sanitized.

    while user_option_sanitized < 0:
        # Print the menu
        print("Please select one of the following options.\n")
        print("1: Add a book\n")
        print("2: Update an entry in the database\n")
        print("3: Show all books currently stored in the database\n")
        print("4: Clear the database\n")

        # Get the user input, if user inputs anything other than an integer menu() is recalled.
        try:
            print("Please enter an integer value representing your choice.\n")
            user_option = int(input())
        except ValueError:
            user_option = -1
            menu()
        # Sanitize the user input, user_option must be either 1 or 2
        # This loop is determined by two constants defined above
        if user_option >= MENU_LOWER_BOUND and user_option <= MENU_UPPER_BOUND:
            # Update the value of the sanitized user input
            user_option_sanitized = user_option
            return user_option_sanitized




def show_all():
    """ show_all will display all entries in the database. """
    # Establishing the query
    cursor.execute('SELECT * FROM books')
    # Getting responses from the query
    rows = cursor.fetchall()
    # Displaying everything in rows.
    for row in rows:
        print(row)

# This method is added in case an error occurs with the database resulting in it wiping
# The .csv file will populate the database.
def load_database():
    """ This method will take the books stored in the book_tracking.csv and populate the database with all entries. """
    # Step 1) Read all books from .csv file.
    with open("book_tracking.csv",mode='r') as book_file:
        book_reader = csv.reader(book_file, delimiter = ',')
        line_count = 0

        for line in book_reader:
            if line_count == 0:
                # We do not want to write the column names to the database.
                line_count+=1
            else:
                query = '''
                    	insert into books
                    	(Title, Author, page_count, Genre, entry_date)
                    	values (?, ?, ?, ?, ?) '''

                cursor.execute(query, (line[0], line[1], line[2], line[3],
                                       line[4]))
                dataBase.commit()
                print("Done pushing to database")
                line_count+=1



# This method is added to make tracking what books have been read easier. It will read all entries in the databse
# and populate the .csv will all books.
def write_to_csv():
    """ This method will take all entries in the databse and add them to book_tracking.csv. """

    # ToDo: Make it so only newly completed books will be added to .csv.

    # Step 1) Gather all entries from the database.
    cursor.execute('SELECT * FROM books')
    rows = cursor.fetchall()

    # Step 2) Open connection to .csv file
    with open("book_tracking.csv",mode='a') as book_file:
        book_writer = csv.writer(book_file,delimiter = ',')
        # For each row of the database: write it to the .csv
        for row in rows:
            book_writer.writerow(row)




if __name__ == "__main__":
    main()