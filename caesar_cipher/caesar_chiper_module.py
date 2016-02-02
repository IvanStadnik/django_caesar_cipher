STANDARD = {'a': 8.167, 'b': 1.492, 'c': 2.782, 'd': 4.253, 'e': 12.702, 'f': 2.228, 'g': 2.015, 'h': 6.094, 'i': 6.966,
            'j': 0.153, 'k': 0.772, 'l': 4.025, 'm': 2.406, 'n': 6.749, 'o': 7.507, 'p': 1.929, 'q': 0.095, 'r': 5.987,
            's': 6.327, 't': 9.056, 'u': 2.758, 'v': 0.978, 'w': 2.361, 'x': 0.150, 'y': 1.974, 'z': 0.074}


class CaesarCipher:
    """
    This class gives ability for encrypting, decrypting a string in English
    using Caesar cipher. It also gives option for counting frequency
    diagram for detecting cipher rotation
    """
    letters = [chr(x) for x in range(ord('a'), ord('z') + 1)]
    standard = STANDARD
    len_letters = len(letters)

    def __init__(self, text):
        self.__text = text

    def caesar_encrypt_decrypt(self, rotation=0, encrypt=True):
        """
        This method can encrypt or decrypt a text.
        If [encrypt=True] it encrypts a text, else decrypts.
        It returns a string.
        :param rotation:
        :param encrypt:
        :return:
        """
        new_text = ''
        letters_upper = [x.upper() for x in self.letters]
        symbol_present = None
        rotation = rotation if encrypt is True else rotation * -1
        for symbol in self.__text:
            if symbol in self.letters:
                symbol_present = self.letters[:]
            elif symbol in letters_upper:
                symbol_present = letters_upper
            if symbol_present:
                position = (symbol_present.index(symbol) + rotation + self.len_letters) % self.len_letters
                new_text += symbol_present[position]
                symbol_present = None
            else:
                new_text += symbol
        return new_text

    def get_frequency(self, text=''):
        """
        This method returns the dictionary of frequency of each letter
        in a text. If text has not been passed, it takes current one.
        :param text:
        :return:
        """
        if not text:
            text = self.__text.lower()
        else:
            text = text.lower()
        text_len = len(text)
        count_symbols = {i: text.count(i) for i in self.letters if i in text}
        frequency = {i: round((count_symbols[i] / text_len) * 100, 3) for i in count_symbols}
        return frequency

    def count_frequency(self, decrypted_text):
        """
        This method returns different between frequency of
        decrypted text and standard frequency.
        :param decrypted_text:
        :return:
        """
        frequency = self.get_frequency(decrypted_text)
        text_frequency = [abs((frequency[i] - self.standard[i])) for i in frequency]
        return sum(text_frequency)

    def try_detect_rotation(self):
        """
        This method takes a text, and try to detect its offset,
        by looping of all possible combinations.
        :return:
        """
        all_frequencies = [self.count_frequency(self.caesar_encrypt_decrypt(rot, False)) for rot in range(26)]
        rotation = all_frequencies.index(min(all_frequencies))
        return rotation

    def current_frequency(self, text=''):
        """
        This method returns a dictionary, which consist of a such elements:
        result['rotation'] - suggested offset of the text;
        result['standard'] - standard values of frequency of the symbols
        which are in the given text
        result['frequency'] = current values of frequency of the symbols
        which are in the given text
        result['symbols'] = symbols for the diagram
        :param text:
        :return:
        """
        result = dict()
        if not text:
            result['rotation'] = self.try_detect_rotation()
            frequency = self.get_frequency()
        else:
            frequency = self.get_frequency(text)
        symbols = list(sorted(frequency.keys()))
        symbols_frequency = [frequency[i] for i in symbols]
        result['symbols'] = symbols
        result['frequency'] = symbols_frequency
        result['standard'] = [self.standard[i] for i in self.letters if i in symbols]
        return result
