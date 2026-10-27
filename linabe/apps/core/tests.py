from unittest import mock

from cryptography.fernet import Fernet
from django.core.mail import EmailMessage
from django.core.mail.backends.smtp import EmailBackend as SMTPBackend
from django.db import connection
from django.test import TestCase, override_settings

from apps.core import crypto
from apps.core.mail.backends import ConfigurableEmailBackend, GraphEmailBackend, build_backend
from apps.core.models import EmailSettings
from apps.core.serializers import EmailSettingsSerializer

TEST_KEY = Fernet.generate_key().decode()


@override_settings(SETTINGS_ENCRYPTION_KEY=TEST_KEY)
class CryptoTests(TestCase):

    def test_roundtrip(self):
        self.assertEqual(crypto.decrypt(crypto.encrypt('s3cret')), 's3cret')
        self.assertEqual(crypto.encrypt(''), '')

    def test_secret_is_encrypted_in_db(self):
        conf = EmailSettings.load()
        conf.password = 's3cret'
        conf.save()
        with connection.cursor() as cursor:
            cursor.execute('SELECT password FROM core_email_settings WHERE id = 1')
            raw = cursor.fetchone()[0]
        self.assertNotIn('s3cret', raw)
        self.assertEqual(EmailSettings.load().password, 's3cret')


@override_settings(SETTINGS_ENCRYPTION_KEY=TEST_KEY)
class EmailSettingsModelTests(TestCase):

    def test_singleton(self):
        EmailSettings.load()
        EmailSettings().save()
        self.assertEqual(EmailSettings.objects.count(), 1)

    def test_gmail_clean_normalizes(self):
        conf = EmailSettings(provider='gmail', from_email='a@gmail.com', password='x', is_active=True)
        conf.clean()
        self.assertEqual((conf.host, conf.port, conf.security, conf.username),
                         ('smtp.gmail.com', 587, 'starttls', 'a@gmail.com'))


@override_settings(SETTINGS_ENCRYPTION_KEY=TEST_KEY)
class BackendSelectionTests(TestCase):

    def test_inactive_uses_env_settings(self):
        backend = build_backend(EmailSettings(is_active=False))
        self.assertIsInstance(backend, SMTPBackend)

    def test_smtp(self):
        conf = EmailSettings(is_active=True, provider='smtp', host='mail.x.com', port=465,
                             security='ssl', username='u', password='p')
        backend = build_backend(conf)
        self.assertIsInstance(backend, SMTPBackend)
        self.assertEqual((backend.host, backend.port, backend.use_ssl, backend.use_tls),
                         ('mail.x.com', 465, True, False))

    def test_office365(self):
        conf = EmailSettings(is_active=True, provider='office365', from_email='a@x.com',
                             ms_tenant_id='t', ms_client_id='c', ms_client_secret='s')
        self.assertIsInstance(build_backend(conf), GraphEmailBackend)

    @mock.patch('apps.core.mail.backends.requests.post')
    def test_graph_send(self, post):
        post.side_effect = [
            mock.Mock(status_code=200, json=lambda: {'access_token': 'tok'}),
            mock.Mock(status_code=202),
        ]
        backend = GraphEmailBackend('t', 'c', 's', sender='a@x.com')
        sent = backend.send_messages([EmailMessage('S', 'B', 'a@x.com', ['b@y.com'])])
        self.assertEqual(sent, 1)
        self.assertIn('/users/a@x.com/sendMail', post.call_args_list[1][0][0])

    @mock.patch.object(SMTPBackend, 'send_messages', return_value=1)
    def test_configurable_applies_default_from(self, send):
        conf = EmailSettings.load()
        conf.is_active = True
        conf.from_email = 'ventas@x.com'
        conf.from_name = 'Ventas'
        conf.host = 'mail.x.com'
        conf.reply_to = 'info@x.com'
        conf.save()
        msg = EmailMessage('S', 'B', to=['b@y.com'])
        ConfigurableEmailBackend().send_messages([msg])
        self.assertEqual(msg.from_email, 'Ventas <ventas@x.com>')
        self.assertEqual(msg.reply_to, ['info@x.com'])

    def test_reply_to_for(self):
        conf = EmailSettings(is_active=True, reply_to='info@x.com')
        self.assertEqual(conf.reply_to_for('u@x.com'), ['info@x.com'])

        conf.reply_to_user = True
        self.assertEqual(conf.reply_to_for('u@x.com'), ['u@x.com'])
        # Usuario sin correo: se usa reply_to
        self.assertEqual(conf.reply_to_for(''), ['info@x.com'])

        conf.is_active = False
        self.assertEqual(conf.reply_to_for('u@x.com'), [])


@override_settings(SETTINGS_ENCRYPTION_KEY=TEST_KEY)
class SerializerTests(TestCase):

    def test_secrets_not_exposed_and_kept_when_blank(self):
        conf = EmailSettings.load()
        conf.password = 'p'
        conf.save()
        s = EmailSettingsSerializer(conf, data={'host': 'h', 'password': ''}, partial=True)
        self.assertTrue(s.is_valid(), s.errors)
        s.save()
        self.assertEqual(EmailSettings.load().password, 'p')
        self.assertNotIn('password', s.data)
        self.assertTrue(s.data['has_password'])


@override_settings(SETTINGS_ENCRYPTION_KEY=TEST_KEY)
class EmailSettingsApiTests(TestCase):

    def setUp(self):
        from django.contrib.auth import get_user_model
        from rest_framework.test import APIClient

        self.user = get_user_model().objects.create_user('cfg', 'cfg@x.com', 'pw')
        self.client = APIClient()
        self.client.force_authenticate(self.user)

    def grant_config(self):
        from django.contrib.auth.models import Permission

        self.user.user_permissions.add(Permission.objects.get(codename='acc_config'))

    def test_requires_config_permission(self):
        self.assertEqual(self.client.get('/linapi/settings/email/').status_code, 403)
        self.assertEqual(self.client.post('/linapi/settings/email/test/').status_code, 403)

    def test_get_put_and_test(self):
        self.grant_config()
        resp = self.client.put('/linapi/settings/email/', {
            'is_active': True, 'provider': 'gmail', 'from_email': 'a@gmail.com', 'password': 'app-pw',
        }, format='json')
        self.assertEqual(resp.status_code, 200, resp.data)
        self.assertNotIn('password', resp.data)
        self.assertEqual(resp.data['host'], 'smtp.gmail.com')
        self.assertEqual(EmailSettings.load().modified_by, self.user)

        resp = self.client.put('/linapi/settings/email/', {'provider': 'office365'}, format='json')
        self.assertEqual(resp.status_code, 400)
        self.assertIn('ms_tenant_id', resp.data)

        with mock.patch.object(SMTPBackend, 'send_messages', side_effect=OSError('sin red')):
            resp = self.client.post('/linapi/settings/email/test/', {'to': 'b@y.com'}, format='json')
        self.assertEqual(resp.status_code, 400)
        self.assertFalse(resp.data['ok'])
        self.assertFalse(EmailSettings.load().last_test_ok)
