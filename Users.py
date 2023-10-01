# Needed for email_verified_at, created_at, and updated_at.
import datetime
from datetime import datetime


# May be needed if there is an issue installing the MySQL-connector.
# The path I appended led to my MySQL-connector installation location.
import sys
sys.path.append('c:/PATH_TO_MYSQL-CONNECTOR_INSTALLATION_LOCATION')


# MySQL-connector connection to database.
import mysql.connector
db_connection = mysql.connector.connect(
    user="ENTER_MYSQL_USER",
    password="ENTER_MYSQL_USER_PASSWORD",
    host="ENTER_HOST_NAME",
    port="ENTER_PORT_NUMBER",
    database="ENTER_DATABASE_NAME"
    )
print(db_connection)


def insert_edit_delete(mysql_command, inputs):
    cursor = db_connection.cursor()
    cursor.execute(mysql_command, inputs)
    db_connection.commit()
    cursor.close()


class User:
    def __init__(self):
        pass

    def __init__(self, username, password, first_name, middle_name, last_name, email, profile_image, email_verified_at, remember_token, created_at, updated_at):
        self.username = username                        # User's username.
        self.password = password                        # User's password.
        self.first_name = first_name                    # User's first name.
        self.middle_name = middle_name                  # User's middle name.
        self.last_name = last_name                      # User's last name.
        self.email = email                              # User's email.
        self.profile_image = profile_image              # User's profile image.
        self.email_verified_at = email_verified_at      # Date when the user's email was verified/updated.
        self.remember_token = remember_token            # Token to authenticate user while traversing the website's pages.
        self.created_at = created_at                    # Date and time at which the user was created.
        self.updated_at = updated_at                    # Date and time at which the user was updated.

    def findUser(username):
        cursor = db_connection.cursor()
        cursor.execute("SELECT ID, username, first_name, middle_name, last_name, email, profile_image, email_verified_at, remember_token, created_at, updated_at FROM users WHERE username=%s", (username,))
        result = (0,1,2,3,4,5,6,7,8,9)
        for returned_id, username, firstname, middlename, lastname, email, profile_image, email_verified_at, remember_token, created_at, updated_at in cursor.fetchall():
            result = (returned_id, username, firstname, middlename, lastname, email, profile_image, email_verified_at, remember_token, created_at, updated_at)
        cursor.close()
        return result
    def findUser_Password(username):
        cursor = db_connection.cursor()
        cursor.execute("SELECT password FROM users WHERE username=%s", (username,))
        result = (0,1)
        for password in cursor.fetchall():
            result = (username, password)
        cursor.close()
        return result
    
    def createUser(username, password, first_name, middle_name, last_name, email, profile_image, remember_token):
        check = User.findUser(username)
        if check == (0,1,2,3,4,5,6,7,8,9):
            email_verified_at = datetime.now()
            created_at = email_verified_at
            updated_at = email_verified_at
            insert_edit_delete("INSERT INTO users (username, password, first_name, middle_name, last_name, email, profile_image, email_verified_at, remember_token, created_at, updated_at) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",
                               (username, password, first_name, middle_name, last_name, email, profile_image, email_verified_at, remember_token, created_at, updated_at))
            return True
        else:
            return False

    def updateUser(username, first_name, middle_name, last_name, email, profile_image):
        result = User.findUser(username)
        if result != (0,1,2,3,4,5,6,7,8,9):
            if first_name is None: first_name = result[2]
            if middle_name is None: middle_name = result[3]
            if last_name is None: last_name = result[4]
            prior_email = result[5]
            if profile_image is None: profile_image = result[6]
            updated_at = datetime.now()
            email_verified_at = result[7]
            if email is None:
                email = prior_email
            elif (prior_email != email):
                email_verified_at = updated_at
            insert_edit_delete("UPDATE users SET first_name=%s, middle_name=%s, last_name=%s, email=%s, profile_image=%s, email_verified_at=%s, updated_at=%s WHERE username=%s",
                                (first_name, middle_name, last_name, email, profile_image, email_verified_at, updated_at, username))
            return True
        else:
            return False

    def updatePassword(username, password):
        result = User.findUser_Password(username)
        if result != (0,1):
            if password is None:
                password = result[1]
            else:
                updated_at = datetime.now()
            insert_edit_delete("UPDATE users SET password=%s, updated_at=%s WHERE username=%s",
                                (password, updated_at, username))
            return True
        else:
            return False

    def removeUser(username):
        result = User.findUser(username)
        if result != (0,1,2,3,4,5,6,7,8,9):
            insert_edit_delete("DELETE FROM users WHERE username=%s", (username,))
            return True
        else:
            return False