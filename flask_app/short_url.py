import random
import string


class ShortUrlGenerator:

    def short_url(self, string_length):

        letters_and_digits = string.ascii_letters + string.digits
        return ''.join(random.choice(letters_and_digits) for i in range(string_length))