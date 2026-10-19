"""Backend de correo que usa la configuración global (EmailSettings).

Si la configuración de la BD está inactiva se usan las variables EMAIL_* de settings.
"""
import base64
import logging

import requests
from django.conf import settings
from django.core.mail.backends.base import BaseEmailBackend
from django.core.mail.backends.smtp import EmailBackend as SMTPBackend

logger = logging.getLogger(__name__)

GRAPH_TOKEN_URL = 'https://login.microsoftonline.com/{tenant}/oauth2/v2.0/token'
GRAPH_SENDMAIL_URL = 'https://graph.microsoft.com/v1.0/users/{sender}/sendMail'
# Graph rechaza peticiones de más de 4 MB (el MIME viaja en base64)
GRAPH_MAX_REQUEST_BYTES = 4 * 1024 * 1024


class GraphError(Exception):
    pass


class GraphEmailBackend(BaseEmailBackend):
    """Envía mensajes por Microsoft Graph (sendMail) con client credentials."""

    def __init__(self, tenant_id, client_id, client_secret, sender, timeout=20,
                 fail_silently=False, **kwargs):
        super().__init__(fail_silently=fail_silently)
        self.tenant_id = tenant_id
        self.client_id = client_id
        self.client_secret = client_secret
        self.sender = sender
        self.timeout = timeout
        self.token = None

    def open(self):
        if self.token:
            return False
        resp = requests.post(
            GRAPH_TOKEN_URL.format(tenant=self.tenant_id),
            data={
                'grant_type': 'client_credentials',
                'client_id': self.client_id,
                'client_secret': self.client_secret,
                'scope': 'https://graph.microsoft.com/.default',
            },
            timeout=self.timeout,
        )
        if resp.status_code != 200:
            raise GraphError('Autenticación con Microsoft fallida ({}): {}'.format(
                resp.status_code, _graph_error_text(resp)))
        self.token = resp.json()['access_token']
        return True

    def close(self):
        self.token = None

    def send_messages(self, email_messages):
        if not email_messages:
            return 0
        sent = 0
        try:
            new_conn = self.open()
            for message in email_messages:
                self._send(message)
                sent += 1
            if new_conn:
                self.close()
        except Exception:
            logger.exception('Error enviando correo por Microsoft Graph')
            if not self.fail_silently:
                raise
        return sent

    def _send(self, message):
        payload = base64.b64encode(message.message().as_bytes())
        if len(payload) > GRAPH_MAX_REQUEST_BYTES:
            raise GraphError('El mensaje excede el límite de 4 MB de Microsoft Graph')
        resp = requests.post(
            GRAPH_SENDMAIL_URL.format(sender=self.sender),
            data=payload,
            headers={'Authorization': 'Bearer ' + self.token, 'Content-Type': 'text/plain'},
            timeout=self.timeout,
        )
        if resp.status_code != 202:
            raise GraphError('Microsoft Graph rechazó el envío ({}): {}'.format(
                resp.status_code, _graph_error_text(resp)))


def _graph_error_text(resp):
    try:
        data = resp.json()
    except ValueError:
        return resp.text[:300]
    if 'error_description' in data:
        return data['error_description'].split('\r\n')[0]
    err = data.get('error')
    if isinstance(err, dict):
        return err.get('message', '')
    return str(err or data)


def build_backend(conf, fail_silently=False):
    """Devuelve el backend concreto para una instancia de EmailSettings."""
    if not conf.is_active:
        return SMTPBackend(fail_silently=fail_silently)

    if conf.provider == conf.Provider.OFFICE365:
        return GraphEmailBackend(
            tenant_id=conf.ms_tenant_id,
            client_id=conf.ms_client_id,
            client_secret=conf.ms_client_secret,
            sender=conf.from_email,
            timeout=conf.timeout,
            fail_silently=fail_silently,
        )

    return SMTPBackend(
        host=conf.host,
        port=conf.port,
        username=conf.username or None,
        password=conf.password or None,
        use_tls=conf.security == conf.Security.STARTTLS,
        use_ssl=conf.security == conf.Security.SSL,
        timeout=conf.timeout,
        fail_silently=fail_silently,
    )


class ConfigurableEmailBackend(BaseEmailBackend):
    """Lee EmailSettings en cada conexión y delega en SMTP o Graph."""

    def __init__(self, fail_silently=False, **kwargs):
        super().__init__(fail_silently=fail_silently)
        self.conf = None
        self.backend = None

    def _load(self):
        from apps.core.models import EmailSettings

        self.conf = EmailSettings.load()
        self.backend = build_backend(self.conf, fail_silently=self.fail_silently)

    def open(self):
        if self.backend is None:
            self._load()
        return self.backend.open()

    def close(self):
        if self.backend is not None:
            self.backend.close()
            self.backend = None

    def send_messages(self, email_messages):
        if not email_messages:
            return 0
        if self.backend is None:
            try:
                self._load()
            except Exception:
                logger.exception('Error cargando la configuración de correo')
                if not self.fail_silently:
                    raise
                return 0
        if self.conf.is_active:
            for message in email_messages:
                self._apply_defaults(message)
        return self.backend.send_messages(email_messages)

    def _apply_defaults(self, message):
        if not message.from_email or message.from_email == settings.DEFAULT_FROM_EMAIL:
            message.from_email = self.conf.formatted_from
        if self.conf.reply_to and not message.reply_to:
            message.reply_to = [self.conf.reply_to]
