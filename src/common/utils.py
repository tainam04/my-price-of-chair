import re
from passlib.hash import pbkdf2_sha512
class Utils(object):

    @staticmethod
    def email_is_valid(email):
        email_address_matcher = re.compile('^[\w-]+@([\w-]+\.)+[\w]+$')
        return True if email_address_matcher.match(email) else False

    @staticmethod
    def hash_password(password):
        """
        Hashes a password using pbkdf2_sha512
        :param password: The sha512 password from the login/register form
        :return: A sha512->pbkdf2_sha512 encrypted password
        """
        return pbkdf2_sha512.encrypt(password)

    @staticmethod
    def check_hashed_password(password, hashed_password):
        """
        Checks that the password the user sent mtches that of the database
        :param password: sha412-hashed password
        :param hashed_password: pbkdf2_shar512 encrypted password
        :return: True if passwords match, Fase otherwise
        """
        return pbkdf2_sha512.verify(password, hashed_password)
