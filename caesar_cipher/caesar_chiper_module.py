LETTERS = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't',
           'u', 'v', 'w', 'x', 'y', 'z']
STANDARD = [8.167, 1.492, 2.782, 4.253, 12.702, 2.228, 2.015, 6.094, 6.966, 0.153, 0.772, 4.025, 2.406, 6.749,
            7.507, 1.929, 0.095, 5.987, 6.327, 9.056, 2.758, 0.978, 2.361, 0.150, 1.974, 0.074]


class CaesarCipher:
    """
    This class gives ability for encrypting, decrypting a string in English
    using Caesar cipher. It also gives option for counting frequency
    diagram for detecting cipher rotation
    """
    letters = LETTERS
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
        for symbol in self.__text:
            if symbol in self.letters:
                symbol_present = self.letters[:]
            elif symbol in letters_upper:
                symbol_present = letters_upper
            # If symbol is a letter we must encrypt or decrypt it
            if symbol_present:
                position = symbol_present.index(symbol)
                if encrypt:
                    new_position = position + int(rotation)
                    if new_position >= self.len_letters:
                        new_position -= self.len_letters
                    new_text += symbol_present[new_position]
                else:
                    new_position = position - int(rotation)
                    if new_position < 0:
                        new_position += self.len_letters
                    new_text += symbol_present[new_position]
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
        count_symbols = {}
        frequency = {}
        for i in text:
            if i in self.letters:
                if count_symbols.get(i):
                    count_symbols[i] += 1
                else:
                    count_symbols[i] = 1
        for i in count_symbols:
            frequency[i] = round((count_symbols[i] / text_len) * 100, 3)
        return frequency

    def count_frequency(self, decrypted_text):
        """
        This method returns different between frequency of
        decrypted text and standard frequency. It returns a float.
        :param decrypted_text:
        :return:
        """
        standard_dict = dict(zip(self.letters, self.standard))
        text_frequency = 0.0
        frequency = self.get_frequency(decrypted_text)
        for i in frequency:
            text_frequency += abs((frequency[i] - standard_dict[i]))
        return text_frequency

    def try_detect_rotation(self):
        """
        This method takes a text, and try to detect its offset,
        by looping of all possible combinations.
        :return:
        """
        all_frequencies = []
        for rot in range(26):
            decrypted_text = self.caesar_encrypt_decrypt(rot, False)
            all_frequencies.append(self.count_frequency(decrypted_text))
        # we should return the minimum difference, between
        # frequency of the decrypted text and standard frequency
        rotation = all_frequencies.index(min(all_frequencies))
        return rotation

    def current_frequency(self):
        """
        This method returns a dictionary, which consist of a such elements:
        result['rotation'] - suggested offset of the text;
        result['standard'] - standard values of frequency of the symbols
        which are in the given text
        result['frequency'] = current values of frequency of the symbols
        which are in the given text
        result['symbols'] = symbols for the diagram
        :return:
        """
        frequency = self.get_frequency()
        result = dict()
        result['rotation'] = self.try_detect_rotation()
        symbols = list(sorted(frequency.keys()))
        symbols_frequency = [frequency[i] for i in symbols]
        result['symbols'] = symbols
        result['frequency'] = symbols_frequency
        result['standard'] = []
        for i in range(self.len_letters):
            if self.letters[i] in symbols:
                result['standard'].append(self.standard[i])
        return result

    def frequency_of_decrypted_text(self, decrypted_text):
        """
        This method returns a dictionary, which consist of a such elements:
        result['standard'] - standard values of frequency of the symbols
        which are in the given text
        result['frequency'] = current values of frequency of the symbols
        which are in the given text
        result['symbols'] = symbols for the diagram
        :param decrypted_text:
        :return:
        """
        frequency = self.get_frequency(decrypted_text)
        result = dict()
        symbols = list(sorted(frequency.keys()))
        symbols_frequency = [frequency[i] for i in symbols]
        result['symbols'] = symbols
        result['frequency'] = symbols_frequency
        result['standard'] = []
        for i in range(self.len_letters):
            if self.letters[i] in symbols:
                result['standard'].append(self.standard[i])
        return result
