"""Cifrado simétrico (Fernet) para secretos guardados en la BD."""
from cryptography.fernet import Fernet, InvalidToken
from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
from django.db import models


def _fernet():
    key = getattr(settings, 'SETTINGS_ENCRYPTION_KEY', None)
    if not key:
        raise ImproperlyConfigured(
            'SETTINGS_ENCRYPTION_KEY no está definida. Genere una con: '
            'python -c "from cryptography.fernet import Fernet; print(Fernet.generate_key().decode())"'
        )
    try:
        return Fernet(key.encode() if isinstance(key, str) else key)
    except ValueError:
        raise ImproperlyConfigured('SETTINGS_ENCRYPTION_KEY no es una clave Fernet válida')


def encrypt(value):
    if not value:
        return ''
    return _fernet().encrypt(value.encode()).decode()


def decrypt(value):
    if not value:
        return ''
    try:
        return _fernet().decrypt(value.encode()).decode()
    except InvalidToken:
        raise ImproperlyConfigured(
            'No se pudo descifrar un secreto guardado. ¿Cambió SETTINGS_ENCRYPTION_KEY?'
        )


class EncryptedTextField(models.TextField):
    """TextField que se guarda cifrado en la BD y se lee en texto plano."""

    def from_db_value(self, value, expression, connection):
        return decrypt(value)

    def get_prep_value(self, value):
        return encrypt(super().get_prep_value(value))
