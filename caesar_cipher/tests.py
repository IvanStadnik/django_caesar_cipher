from django.test import TestCase, Client
import json
from .caesar_chiper_module import CaesarCipher


class CaesarCipherTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        text = "To encrypt or decrypt the text, paste it into the box on the left. " \
                    "Select offset and click the appropriate button. If the inserted text is encrypted, " \
                    "then the program using frequency analysis tries to determine the offset, shows " \
                    "you a diagram of frequency analysis of the pasted text and prompts you to decrypt " \
                    "it in the message below the diagram. After either decrypting or encrypting of the " \
                    "text, the diagram shows frequency analysis of the changed text. "
        cls.self_text = text
        cls.text = CaesarCipher(text)

    def test_caesar_encrypt(self):
        """
        Method caesar_encrypt_decrypt(x) with x != 0 should return an encrypted text.
        :return:
        """
        new_text = self.text.caesar_encrypt_decrypt(1)
        self.assertNotEqual(new_text, self.self_text)

    def test_caesar_decrypt(self):
        """
        Method caesar_encrypt_decrypt(x, False) with x != 0 should return a decrypted text.
        :return:
        """
        new_text = self.text.caesar_encrypt_decrypt(1, False)
        self.assertNotEqual(new_text, self.self_text)

    def test_caesar_encrypt_decrypt(self):
        """
        Method caesar_encrypt_decrypt() should correctly decrypt an encrypted text.
        :return:
        """
        new_text = self.text.caesar_encrypt_decrypt(5)
        decrypt_text = CaesarCipher(new_text)
        decrypted_text = decrypt_text.caesar_encrypt_decrypt(5, False)
        self.assertEqual(decrypted_text, self.self_text)

    def test_try_detect_rotation(self):
        """
        Method try_detect_rotation() should return 0 if the text not encrypted.
        :return:
        """
        rotation = self.text.try_detect_rotation()
        self.assertEqual(rotation, 0)

    def test_try_detect_unknown_rotation(self):
        """
        Method try_detect_rotation() should correctly detect rotation.
        :return:
        """
        new_text = self.text.caesar_encrypt_decrypt(5)
        decrypt_text = CaesarCipher(new_text)
        rotation = decrypt_text.try_detect_rotation()
        self.assertEqual(rotation, 5)

    def test_count_frequency(self):
        """
        Method count_frequency(text) should return a float
        :return:
        """
        result = self.text.count_frequency(self.self_text)
        self.assertEqual(type(result), float)

    def test_current_frequency(self):
        """
        method current_frequency() should return a dictionary with 4 keys
        :return:
        """
        result_dictionary = self.text.current_frequency()
        if len(result_dictionary) == 4 and type(result_dictionary) == dict:
            result = True
        else:
            result = False
        self.assertEqual(result, True)

    def test_frequency_of_decrypted_text(self):
        """
        method frequency_of_decrypted_text() should return a dictionary with 3 keys
        :return:
        """
        result_dictionary = self.text.frequency_of_decrypted_text(self.self_text)
        if len(result_dictionary) == 3 and type(result_dictionary) == dict:
            result = True
        else:
            result = False
        self.assertEqual(result, True)


class ViewJsonTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.text = "To encrypt or decrypt the text, paste it into the box on the left. " \
                    "Select offset and click the appropriate button. If the inserted text is encrypted, " \
                    "then the program using frequency analysis tries to determine the offset, shows " \
                    "you a diagram of frequency analysis of the pasted text and prompts you to decrypt " \
                    "it in the message below the diagram. After either decrypting or encrypting of the " \
                    "text, the diagram shows frequency analysis of the changed text. "
        cls.response_1 = '{"message": "Using the method of frequency analysis, the program identified as the offset ' \
                         'value 0.", "frequency": {"standard": [8.167, 1.492, 2.782, 4.253, 12.702, 2.228, 2.015, ' \
                         '6.094, 6.966, 0.772, 4.025, 2.406, 6.749, 7.507, 1.929, 0.095, 5.987, 6.327, 9.056, ' \
                         '2.758, 2.361, 0.15, 1.974], "frequency": [5.033, 0.656, 2.845, 2.845, 11.597, 3.063, ' \
                         '1.969, 3.939, 4.595, 0.219, 1.532, 1.532, 4.814, 5.033, 3.063, 0.656, 5.252, 4.814, ' \
                         '11.16, 1.532, 0.656, 1.313, 3.063], "symbols": ["a", "b", "c", "d", "e", "f", "g",' \
                         ' "h", "i", "k", "l", "m", "n", ' \
                         '"o", "p", "q", "r", "s", "t", "u", "w", "x", "y"], "rotation": 0}}'
        cls.response_2 = '{"ciphered_text": "Yt jshwduy tw ijhwduy ymj yjcy, ufxyj ny nsyt ymj gtc ts ymj qjky. ' \
                         'Xjqjhy tkkxjy fsi hqnhp ymj fuuwtuwnfyj gzyyts. Nk ymj nsxjwyji yjcy nx jshwduyji, ' \
                         'ymjs ymj uwtlwfr zxnsl kwjvzjshd fsfqdxnx ywnjx yt ijyjwrnsj ymj tkkxjy, xmtbx dtz f ' \
                         'inflwfr tk kwjvzjshd fsfqdxnx tk ymj ufxyji yjcy fsi uwtruyx dtz yt ijhwduy ny ns ymj ' \
                         'rjxxflj gjqtb ymj inflwfr. Fkyjw jnymjw ijhwduynsl tw jshwduynsl tk ymj yjcy, ymj inflwfr ' \
                         'xmtbx kwjvzjshd fsfqdxnx tk ymj hmfslji yjcy. ", "frequency": {"symbols": ["b", "c", "d", ' \
                         '"f", "g", "h", "i", "j", "k", "l", "m", "n", "p", "q", "r", "s", "t", "u", "v", "w", "x", ' \
                         '"y", "z"], "standard": [1.492, 2.782, 4.253, 2.228, 2.015, 6.094, 6.966, 0.153, 0.772, ' \
                         '4.025, 2.406, 6.749, 1.929, 0.095, 5.987, 6.327, 9.056, 2.758, 0.978, 2.361, 0.15, 1.974, ' \
                         '0.074], "frequency": [0.656, 1.313, 3.063, 5.033, 0.656, 2.845, 2.845, 11.597, 3.063, ' \
                         '1.969, 3.939, 4.595, 0.219, 1.532, 1.532, 4.814, 5.033, 3.063, 0.656, 5.252, 4.814, ' \
                         '11.16, 1.532]}}'
        cls.response_3 = '{"frequency": {"frequency": [5.033, 0.656, 2.845, 2.845, 11.597, 3.063, 1.969, 3.939, ' \
                         '4.595, 0.219, 1.532, 1.532, 4.814, 5.033, 3.063, 0.656, 5.252, 4.814, 11.16, 1.532, ' \
                         '0.656, 1.313, 3.063], "symbols": ["a", "b", "c", "d", "e", "f", "g", "h", "i", "k", ' \
                         '"l", "m", "n", "o", "p", "q", "r", "s", "t", "u", "w", "x", "y"], "standard": ' \
                         '[8.167, 1.492, 2.782, 4.253, 12.702, 2.228, 2.015, 6.094, 6.966, 0.772, 4.025, 2.406, ' \
                         '6.749, 7.507, 1.929, 0.095, 5.987, 6.327, 9.056, 2.758, 2.361, 0.15, 1.974]}, "ciphered_' \
                         'text": "To encrypt or decrypt the text, paste it into the box on the left. Select' \
                         ' offset and click the appropriate button. If the inserted text is encrypted, then the ' \
                         'program using frequency analysis tries to determine the offset, shows you a diagram of ' \
                         'frequency analysis of the pasted text and prompts you to decrypt it in the message below ' \
                         'the diagram. After either decrypting or encrypting of the text, the diagram shows' \
                         ' frequency analysis of the changed text. "}'
        cls.client = Client()

    def test_detecting_cipher_rotation(self):
        """
        function detecting_cipher_rotation() in views.py should return a json string
        :return:
        """
        request = {'ciphered_text': self.text}
        json_request = json.dumps(request)
        response = self.client.post('/detecting_cipher_rotation/', content_type='application/json', data=json_request)
        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(str(response.content, encoding='utf8'), self.response_1)

    def test_encrypt_text(self):
        """
        function encrypt_text() in views.py should return a json string
        :return:
        """
        request = {'text_for_encrypt': self.text, 'rotation': 5}
        json_request = json.dumps(request)
        response = self.client.post('/encrypt_text/', content_type='application/json', data=json_request)
        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(str(response.content, encoding='utf8'), self.response_2)

    def test_decrypt_text(self):
        """
        function decrypt_text() in views.py should return a json string
        :return:
        """
        request = {'text_for_decrypt': self.text, 'rotation': 0}
        json_request = json.dumps(request)
        response = self.client.post('/decrypt_text/', content_type='application/json', data=json_request)
        self.assertEqual(response.status_code, 200)
        self.assertJSONEqual(str(response.content, encoding='utf8'), self.response_3)
