from django.conf.urls import url
from . import views


urlpatterns = (
    url(r'^decrypt_text/', views.decrypt_text, name='decrypt_text'),
    url(r'^encrypt_text/', views.encrypt_text, name='encrypt_text'),
    url(r'^detecting_cipher_rotation/', views.detecting_cipher_rotation, name='detecting_cipher_rotation'),
    url(r'^$', views.caesar_cipher_page, name='caesar_cipher_page'),
)