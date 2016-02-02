from django.shortcuts import render
from django.views.decorators.http import require_POST
from django.http import JsonResponse
from .caesar_chiper_module import CaesarCipher
import json


def caesar_cipher_page(request):
    """
    This function for displaying the front page
    :param request:
    :return:
    """
    from .caesar_chiper_module import LETTERS, STANDARD
    data = dict()
    data['rotations'] = range(26)
    data['title'] = 'Caesar cipher application'
    data['STANDARD'] = STANDARD
    data['LETTERS'] = LETTERS
    return render(request, 'caesar_cipher/index.html', data)


@require_POST
def detecting_cipher_rotation(request):
    """
    This function try's detect rotation of ciphered text
    :param request:
    :return:
    """
    incoming_json = request.body.decode('utf-8')
    json_dict = json.loads(incoming_json)
    data = dict()
    text = CaesarCipher(json_dict['ciphered_text'])
    data['frequency'] = text.current_frequency()
    data['message'] = 'Using the method of frequency analysis, the program identified as the offset ' \
                      'value %d.' % data['frequency']['rotation']
    return JsonResponse(data)


@require_POST
def encrypt_text(request):
    """
    This function returns encrypted text
    :param request:
    :return:
    """
    incoming_json = request.body.decode('utf-8')
    json_dict = json.loads(incoming_json)
    text = CaesarCipher(json_dict['text_for_encrypt'])
    data = dict()
    data['ciphered_text'] = text.caesar_encrypt_decrypt(int(json_dict['rotation']))
    data['frequency'] = text.frequency_of_decrypted_text(data['ciphered_text'])
    return JsonResponse(data)


@require_POST
def decrypt_text(request):
    """
    This function returns decrypted text
    :param request:
    :return:
    """
    incoming_json = request.body.decode('utf-8')
    json_dict = json.loads(incoming_json)
    text = CaesarCipher(json_dict['text_for_decrypt'])
    data = dict()
    data['ciphered_text'] = text.caesar_encrypt_decrypt(int(json_dict['rotation']), False)
    data['frequency'] = text.frequency_of_decrypted_text(data['ciphered_text'])
    return JsonResponse(data)
