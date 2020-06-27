import re
import pdb


def validate_credentials(password, email):
    # pdb.set_trace()

    if re.match("(?=.*\d)(?=.*[a-z])(?=.*[A-Z]).{8,}", password) and re.match("[a-z0-9._%+-]+@[a-z0-9.-]+\.[a-z]{2,}$",
                                                                              email):

        return True

    else:
        # print("Must contain at least one number and one uppercase and lowercase letter, and at least 8 or more "
        #       "characters")
        return False
