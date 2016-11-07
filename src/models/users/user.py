import uuid

from src.common.database import Database
from src.common.utils import Utils
import src.models.users.errors as UserErrors
import src.models.users.constants as UserConstants
from src.models.alerts.alert import Alert


class User(object):
    def __init__(self, email, password, _id = None):
        self.email = email
        self.password = password
        self._id = uuid.uuid4().hex if _id is None else _id

    def __repr__(self):
        return "<User {}>".format(self.email)

    # if __name__ == '__main__':
    @staticmethod
    def is_login_valid(email, password):
        """
        This method verifies that e-mail/password combo (as sent by the site forms)
        is valid or not. Checks that the e-mail exists, and that the password associated
        to that emil is correct.
        :param email: The user's email
        :param password: A sha512 hashed password
        :return: True if valid, False otherwise
        """
        user_data = Database.find_one(UserConstants.COLLECTION, {"email" : email}) # password in sha512->pbkdf2_sha512

        if (user_data is None) :
            # Tell the usee that their e-mail doesn't exist
            raise UserErrors.UserNotExistsError("Your user does not exist")

        if not Utils.check_hashed_password(password, user_data['password']) :
            raise UserErrors.IncorrectPasswordError("Your password was wrong")
        return True

    @staticmethod
    def register_user(email, password):
        """
        This method registers a use using e-mail and password
        The password already comes hashed as sha-512
        :param email: User's email (might be invalid)
        :param passowrd: sha512-hashed password
        :return: True if registered successfully, or False otherwise (exceptions can also be raised)
        """
        user_data = Database.find_one(UserConstants.COLLECTION, {"email" : email})

        if user_data is not None :
            # Tell user they are already registered
            raise UserErrors.UserAlreadyRegistered("The email you used to register already exists ")

        if not Utils.email_is_valid(email) :
            # Tell user that their e-mail is not constructed properly
            raise UserErrors.InvalidEmailError("The email does not have right format.")
        hash_password = Utils.hash_password(password)
        user = User(email, hash_password)
        user.save_to_db()
        #User(email, Utils.hash_password(password)).save_to_db()

        return True

    def save_to_db(self):
        Database.insert(UserConstants.COLLECTION, self.jason())

    def jason(self):
        return {
            "_id" : self._id,
            "email" : self.email,
            "password" : self.password
        }

    @classmethod
    def find_by_email(cls, email):
        return (cls(**Database.find_one(UserConstants.COLLECTION, {'email' : email})))

    def get_alerts(self):
        return Alert.find_by_email(self.email)

