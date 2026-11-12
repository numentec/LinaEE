import json
from types import SimpleNamespace
from unittest.mock import Mock, patch

from django.test import TestCase
from rest_framework.test import APIRequestFactory, force_authenticate

from .views import (
	SuggestProductsAPIView,
	parse_description_filter,
	parse_description_text,
	parse_sku_prefix,
	parse_stock_filters,
	parse_text_filters,
)


class ParseDescriptionFilterTests(TestCase):
	def test_description_filter_is_optional(self):
		self.assertIsNone(parse_description_filter({}))
		self.assertIsNone(parse_description_filter({'descrips': '[]'}))
		self.assertIsNone(parse_description_filter({'descrips': '[" "]'}))

	def test_keeps_text_as_received_and_deduplicates(self):
		self.assertEqual(
			parse_description_filter(
				{'descrips': '["Mesa, roble | 2", "Silla", "Mesa, roble | 2"]'}
			),
			'Mesa, roble | 2\x1eSilla',
		)

	def test_rejects_malformed_payload(self):
		for raw in ('not json', '{"a": 1}', '[1, 2]'):
			with self.assertRaisesRegex(ValueError, 'JSON list'):
				parse_description_filter({'descrips': raw})

	def test_rejects_too_many_items(self):
		raw = json.dumps([f'Item {i}' for i in range(31)])

		with self.assertRaisesRegex(ValueError, 'at most 30'):
			parse_description_filter({'descrips': raw})

	def test_rejects_overlong_or_delimiter_items(self):
		with self.assertRaisesRegex(ValueError, 'invalid or too long'):
			parse_description_filter({'descrips': json.dumps(['x' * 101])})

		with self.assertRaisesRegex(ValueError, 'invalid or too long'):
			parse_description_filter({'descrips': json.dumps(['a\x1eb'])})

	def test_rejects_selection_over_byte_budget(self):
		raw = json.dumps(['\u00e9' * 96 + f'{i:02d}' for i in range(30)])

		with self.assertRaisesRegex(ValueError, 'selection is too long'):
			parse_description_filter({'descrips': raw})


class ParseDescriptionTextTests(TestCase):
	def test_text_is_optional_and_trimmed(self):
		self.assertIsNone(parse_description_text({}))
		self.assertIsNone(parse_description_text({'descrip_text': '   '}))
		self.assertEqual(
			parse_description_text({'descrip_text': '  mesa '}), 'mesa'
		)

	def test_rejects_overlong_text(self):
		with self.assertRaisesRegex(ValueError, 'at most 50'):
			parse_description_text({'descrip_text': 'x' * 51})


class ParseSkuPrefixTests(TestCase):
	def test_sku_prefix_is_optional_and_trimmed(self):
		self.assertIsNone(parse_sku_prefix({}))
		self.assertEqual(parse_sku_prefix({'sku_prefix': '  ab-1 '}), 'ab-1')

	def test_rejects_overlong_prefix(self):
		with self.assertRaisesRegex(ValueError, 'at most 50'):
			parse_sku_prefix({'sku_prefix': 'x' * 51})


class ParseTextFiltersTests(TestCase):
	def test_text_filters_are_optional(self):
		self.assertEqual(
			parse_text_filters({}), {'color': None, 'acabado': None}
		)

	def test_trims_values_and_ignores_blank_text(self):
		filters = parse_text_filters({'color': '  Negro ', 'acabado': '   '})

		self.assertEqual(filters, {'color': 'Negro', 'acabado': None})

	def test_rejects_overlong_text(self):
		with self.assertRaisesRegex(ValueError, 'color: must have at most'):
			parse_text_filters({'color': 'x' * 51})


class ParseStockFiltersTests(TestCase):
	def test_empty_filters_are_optional(self):
		filters = parse_stock_filters({})

		self.assertEqual(
			filters,
			{
				'instock': (None, None, None),
				'intransit': (None, None, None),
				'infuture': (None, None, None),
			},
		)

	def test_parses_single_value_and_range_filters(self):
		filters = parse_stock_filters(
			{
				'instock_operator': 'gte',
				'instock_value': '-2',
				'infuture_operator': 'between',
				'infuture_value': '3',
				'infuture_value_to': '8',
			}
		)

		self.assertEqual(filters['instock'], ('gte', -2, None))
		self.assertEqual(filters['intransit'], (None, None, None))
		self.assertEqual(filters['infuture'], ('between', 3, 8))

	def test_rejects_unsupported_operator(self):
		with self.assertRaisesRegex(ValueError, 'unsupported operator'):
			parse_stock_filters(
				{'instock_operator': 'sql', 'instock_value': '1'}
			)

	def test_rejects_non_integer_values(self):
		with self.assertRaisesRegex(ValueError, 'whole-number'):
			parse_stock_filters(
				{'instock_operator': 'eq', 'instock_value': '1.5'}
			)

	def test_rejects_incomplete_or_reversed_ranges(self):
		with self.assertRaisesRegex(ValueError, 'both range bounds'):
			parse_stock_filters(
				{'instock_operator': 'between', 'instock_value': '5'}
			)

		with self.assertRaisesRegex(ValueError, 'must not exceed'):
			parse_stock_filters(
				{
					'instock_operator': 'between',
					'instock_value': '9',
					'instock_value_to': '2',
				}
			)


class ProductsAPIViewStockFilterTests(TestCase):
	@patch('apps.saleapp.views.connections')
	@patch('apps.saleapp.views.SQLQuery')
	def test_stock_filters_are_passed_to_procedure_before_pagination(
		self, sql_query, connections
	):
		sql_query.objects.filter.return_value = [
			SimpleNamespace(content='TEST_SHOPPINGCART_PRODUCTS')
		]
		db_connection = connections.__getitem__.return_value
		cursor_context = db_connection.cursor.return_value
		db_cursor = cursor_context.__enter__.return_value
		ref_cursor = Mock()
		ref_cursor.description = [('id',), ('instock',)]
		ref_cursor.fetchall.return_value = [('SKU-1', 5), ('SKU-2', 8)]
		db_cursor.connection.cursor.return_value = ref_cursor

		request = APIRequestFactory().get(
			'/linapi/saleapp/products/',
			{
				'instock_operator': 'gte',
				'instock_value': '5',
				'color': ' rojo ',
				'acabado': 'mate',
				'descrips': json.dumps(['Mesa roble', 'Silla']),
				'descrip_text': ' mesa ',
				'sku_prefix': ' ab-1 ',
				'page': '1',
				'page_size': '1',
			},
		)
		force_authenticate(
			request, user=SimpleNamespace(is_authenticated=True, pk=1)
		)

		from .views import ProductsAPIView

		response = ProductsAPIView.as_view()(request)

		db_cursor.callproc.assert_called_once_with(
			'TEST_SHOPPINGCART_PRODUCTS',
			[
				'0', '0', '0', '', '01',
				'gte', 5, None,
				None, None, None,
				None, None, None,
				'rojo', 'mate',
				'Mesa roble\x1eSilla',
				'mesa',
				'ab-1',
				ref_cursor,
			],
		)
		self.assertEqual(response.status_code, 200)
		self.assertEqual(response.data['count'], 2)
		self.assertEqual(
			response.data['results'],
			[{'id': 'SKU-1', 'instock': 5}],
		)

	@patch('apps.saleapp.views.connections')
	@patch('apps.saleapp.views.SQLQuery')
	def test_sku_prefix_alone_is_forwarded_as_a_filter(
		self, sql_query, connections
	):
		sql_query.objects.filter.return_value = [
			SimpleNamespace(content='TEST_SHOPPINGCART_PRODUCTS')
		]
		db_connection = connections.__getitem__.return_value
		db_cursor = db_connection.cursor.return_value.__enter__.return_value
		ref_cursor = Mock()
		ref_cursor.description = [('id',)]
		ref_cursor.fetchall.return_value = [('AB-123',)]
		db_cursor.connection.cursor.return_value = ref_cursor

		request = APIRequestFactory().get(
			'/linapi/saleapp/products/', {'sku_prefix': ' ab- '}
		)
		force_authenticate(
			request, user=SimpleNamespace(is_authenticated=True, pk=1)
		)

		from .views import ProductsAPIView

		response = ProductsAPIView.as_view()(request)

		db_cursor.callproc.assert_called_once_with(
			'TEST_SHOPPINGCART_PRODUCTS',
			[
				'0', '0', '0', '', '01',
				None, None, None,
				None, None, None,
				None, None, None,
				None, None,
				None, None,
				'ab-',
				ref_cursor,
			],
		)
		self.assertEqual(response.status_code, 200)


class SuggestProductsAPIViewTests(TestCase):
	def _get(self, params):
		request = APIRequestFactory().get(
			'/linapi/saleapp/products/suggest/', params
		)
		force_authenticate(
			request, user=SimpleNamespace(is_authenticated=True, pk=1)
		)
		return SuggestProductsAPIView.as_view()(request)

	@patch('apps.saleapp.views.connections')
	@patch('apps.saleapp.views.SQLQuery')
	def test_short_text_returns_empty_without_querying(
		self, sql_query, connections
	):
		response = self._get({'q': ' a '})

		self.assertEqual(response.status_code, 200)
		self.assertEqual(response.data, [])
		connections.__getitem__.assert_not_called()

	@patch('apps.saleapp.views.connections')
	@patch('apps.saleapp.views.SQLQuery')
	def test_forwards_context_and_text_to_procedure(
		self, sql_query, connections
	):
		sql_query.objects.filter.return_value = [
			SimpleNamespace(content='TEST_SUGGEST')
		]
		db_connection = connections.__getitem__.return_value
		db_cursor = db_connection.cursor.return_value.__enter__.return_value
		ref_cursor = Mock()
		ref_cursor.description = [('name',), ('products',)]
		ref_cursor.fetchall.return_value = [('Mesa roble', 3)]
		db_cursor.connection.cursor.return_value = ref_cursor

		response = self._get(
			{'q': ' mesa ', 'depto': '09', 'cat': '27', 'brands': '1, 2'}
		)

		db_cursor.callproc.assert_called_once_with(
			'TEST_SUGGEST',
			['09', '27', '0', '1,2', '01', 'mesa', ref_cursor],
		)
		self.assertEqual(response.status_code, 200)
		self.assertEqual(
			response.data, [{'name': 'Mesa roble', 'products': 3}]
		)

	@patch('apps.saleapp.views.connections')
	@patch('apps.saleapp.views.SQLQuery')
	def test_rejects_unsafe_brands_list(self, sql_query, connections):
		response = self._get({'q': 'mesa', 'brands': "1') OR ('1'='1"})

		self.assertEqual(response.status_code, 400)
		connections.__getitem__.assert_not_called()

	@patch('apps.saleapp.views.connections')
	@patch('apps.saleapp.views.SQLQuery')
	def test_reports_missing_query_configuration(
		self, sql_query, connections
	):
		sql_query.objects.filter.return_value = []

		response = self._get({'q': 'mesa'})

		self.assertEqual(response.status_code, 503)
		connections.__getitem__.assert_not_called()


class SaleAppEmailSettingsTests(TestCase):
	def setUp(self):
		from django.contrib.auth import get_user_model
		from rest_framework.test import APIClient

		from ..core.models import Cia

		self.cia = Cia.objects.create(codigo='T1', nombre='Test Cia', default=True)
		self.user = get_user_model().objects.create_user('sale', 'sale@x.com', 'pw')
		self.client = APIClient()
		self.client.force_authenticate(self.user)

	def set_conf(self, **fields):
		from .models import SaleAppSettings

		SaleAppSettings.objects.update_or_create(company=self.cia, defaults=fields)

	def create_order(self):
		return self.client.post(
			'/linapi/saleapp/extorder/',
			{
				'customer_name': 'Cliente',
				'customer_email': 'cli@x.com',
				'items': [{'sku': 'A1', 'name': 'Mesa', 'quantity': 1, 'price': '10.00'}],
			},
			format='json',
		)

	def test_attachment_types(self):
		from .models import SaleAppSettings

		self.assertEqual(SaleAppSettings(email_attachments='pdf').attachment_types, ['pdf'])
		self.assertEqual(SaleAppSettings(email_attachments='xlsx').attachment_types, ['xlsx'])
		self.assertEqual(SaleAppSettings(email_attachments='both').attachment_types, ['pdf', 'xlsx'])

	@patch('apps.saleapp.tasks.render_order_xlsx')
	@patch('apps.saleapp.tasks.render_order_pdf')
	def test_task_attaches_all_files_in_one_email(self, render_pdf, render_xlsx):
		from django.core import mail

		from .models import ExtOrderMaster
		from .tasks import send_order_email

		render_pdf.return_value = Mock(getvalue=Mock(return_value=b'pdf'))
		render_xlsx.return_value = Mock(getvalue=Mock(return_value=b'xlsx'))
		order = ExtOrderMaster.objects.create(customer_email='cli@x.com')

		with self.settings(EMAIL_BACKEND='django.core.mail.backends.locmem.EmailBackend'):
			send_order_email(order.id, print_images='1', file_types=['pdf', 'xlsx'])

		self.assertEqual(len(mail.outbox), 1)
		self.assertEqual(
			[name for name, _, _ in mail.outbox[0].attachments],
			[f'Order_{order.id}.pdf', f'Order_{order.id}.xlsx'],
		)
		render_pdf.assert_called_once_with(order, print_images='1')
		render_xlsx.assert_called_once_with(order, print_images=True)

	@patch('apps.saleapp.tasks.render_order_pdf')
	def test_task_reply_to_session_user(self, render_pdf):
		from django.core import mail

		from ..core.models import EmailSettings
		from .models import ExtOrderMaster
		from .tasks import send_order_email

		render_pdf.return_value = Mock(getvalue=Mock(return_value=b'pdf'))
		order = ExtOrderMaster.objects.create(customer_email='cli@x.com')
		conf = EmailSettings.load()
		conf.is_active = True
		conf.reply_to = 'info@x.com'
		conf.save()

		with self.settings(EMAIL_BACKEND='django.core.mail.backends.locmem.EmailBackend'):
			send_order_email(order.id, user_email='sale@x.com')
			conf.reply_to_user = True
			conf.save()
			send_order_email(order.id, user_email='sale@x.com')

		self.assertEqual(
			[m.reply_to for m in mail.outbox], [['info@x.com'], ['sale@x.com']]
		)

	@patch('apps.saleapp.views.send_order_email')
	def test_auto_policy_sends_configured_attachments(self, task):
		self.set_conf(email_policy='auto', email_attachments='both', email_include_images=True)

		response = self.create_order()

		self.assertEqual(response.status_code, 201, response.data)
		self.assertEqual(response.data['email']['action'], 'sent')
		task.delay.assert_called_once_with(
			response.data['id'], print_images='1', file_types=['pdf', 'xlsx'],
			user_email='sale@x.com',
		)

	@patch('apps.saleapp.views.send_order_email')
	def test_ask_and_never_policies_do_not_send(self, task):
		for policy, action in (('ask', 'ask'), ('never', 'none')):
			self.set_conf(email_policy=policy, email_attachments='xlsx')

			response = self.create_order()

			self.assertEqual(response.data['email']['action'], action)
			self.assertEqual(response.data['email']['attachments'], 'xlsx')
		task.delay.assert_not_called()

	def test_settings_put_requires_config_permission(self):
		from django.contrib.auth.models import Permission

		self.assertEqual(self.client.get('/linapi/saleapp/settings/').status_code, 200)
		data = {'email_policy': 'auto', 'email_attachments': 'both'}
		self.assertEqual(
			self.client.put('/linapi/saleapp/settings/', data, format='json').status_code, 403
		)

		self.user.user_permissions.add(Permission.objects.get(codename='acc_config'))
		# Recarga el usuario para descartar la caché de permisos
		self.user = type(self.user).objects.get(pk=self.user.pk)
		self.client.force_authenticate(self.user)
		response = self.client.put('/linapi/saleapp/settings/', data, format='json')

		self.assertEqual(response.status_code, 200, response.data)
		self.assertEqual(response.data['email_attachments'], 'both')
		self.assertEqual(self.cia.saleapp_settings.modified_by, self.user)

	@patch('apps.saleapp.views.send_order_email')
	def test_send_order_email_endpoint(self, task):
		from .models import ExtOrderMaster

		order = ExtOrderMaster.objects.create(customer_email='cli@x.com')
		url = f'/linapi/saleapp/orders/{order.id}/email/'

		response = self.client.post(url, {'attachments': 'zip'}, format='json')
		self.assertEqual(response.status_code, 400)

		response = self.client.post(
			url, {'attachments': 'xlsx', 'include_images': False}, format='json'
		)
		self.assertEqual(response.status_code, 202)
		task.delay.assert_called_once_with(
			order.id, print_images='0', file_types=['xlsx'], user_email='sale@x.com'
		)

		response = self.client.post(url, {'sendto': 'cli@x.com, bad'}, format='json')
		self.assertEqual(response.status_code, 400)

		task.reset_mock()
		response = self.client.post(
			url, {'attachments': 'pdf', 'sendto': 'a@x.com; b@x.com'}, format='json'
		)
		self.assertEqual(response.status_code, 202)
		task.delay.assert_called_once_with(
			order.id, print_images='0', file_types=['pdf'], to=['a@x.com', 'b@x.com'],
			user_email='sale@x.com',
		)


	@patch('apps.saleapp.views.send_order_email')
	def test_send_order_email_toggles_and_link(self, task):
		from datetime import timedelta

		from django.utils import timezone

		from .models import ExtOrderMaster

		order = ExtOrderMaster.objects.create(customer_email='cli@x.com')
		url = f'/linapi/saleapp/orders/{order.id}/email/'
		origin = {'HTTP_ORIGIN': 'https://shop.x.com'}

		# Lista de adjuntos (toggles)
		response = self.client.post(url, {'attachments': ['pdf', 'xlsx']}, format='json')
		self.assertEqual(response.status_code, 202)
		task.delay.assert_called_once_with(
			order.id, print_images='0', file_types=['pdf', 'xlsx'], user_email='sale@x.com'
		)

		# Tipo inválido en la lista / nada seleccionado
		response = self.client.post(url, {'attachments': ['pdf', 'both']}, format='json')
		self.assertEqual(response.status_code, 400)
		response = self.client.post(url, {'attachments': []}, format='json')
		self.assertEqual(response.status_code, 400)

		# Solo el enlace público (la orden nace con enlace vigente)
		task.reset_mock()
		response = self.client.post(
			url, {'attachments': [], 'include_link': True}, format='json', **origin
		)
		self.assertEqual(response.status_code, 202, response.data)
		task.delay.assert_called_once_with(
			order.id, print_images='0', file_types=[], user_email='sale@x.com',
			link_url=f'https://shop.x.com/portal/shared-order/{order.public_token}',
		)

		# FRONTEND_PUBLIC_URL tiene prioridad sobre el Origin
		task.reset_mock()
		with self.settings(FRONTEND_PUBLIC_URL='https://lina.x.com/'):
			response = self.client.post(
				url, {'attachments': ['pdf'], 'include_link': True}, format='json', **origin
			)
		self.assertEqual(response.status_code, 202)
		self.assertEqual(
			task.delay.call_args.kwargs['link_url'],
			f'https://lina.x.com/portal/shared-order/{order.public_token}',
		)

		# Sin forma de construir la URL
		response = self.client.post(url, {'include_link': True, 'attachments': []}, format='json')
		self.assertEqual(response.status_code, 400)

		# Enlace vencido o revocado
		order.public_token_expires_at = timezone.now() - timedelta(minutes=1)
		order.save()
		response = self.client.post(
			url, {'attachments': [], 'include_link': True}, format='json', **origin
		)
		self.assertEqual(response.status_code, 400)
		order.revoke_public_link()
		response = self.client.post(
			url, {'attachments': ['pdf'], 'include_link': True}, format='json', **origin
		)
		self.assertEqual(response.status_code, 400)

	@patch('apps.saleapp.tasks.render_order_pdf')
	def test_task_link_in_body(self, render_pdf):
		from django.core import mail

		from .models import ExtOrderMaster
		from .tasks import send_order_email

		render_pdf.return_value = Mock(getvalue=Mock(return_value=b'pdf'))
		order = ExtOrderMaster.objects.create(customer_name='Cliente', customer_email='cli@x.com')
		link = f'https://shop.x.com/portal/shared-order/{order.public_token}'

		with self.settings(EMAIL_BACKEND='django.core.mail.backends.locmem.EmailBackend'):
			send_order_email(order.id, file_types=[], link_url=link)
			send_order_email(order.id, file_types=['pdf'], link_url=link)

		only_link, both = mail.outbox
		self.assertEqual(only_link.attachments, [])
		self.assertIn(link, only_link.body)
		self.assertIn('valid until', only_link.body)
		self.assertNotIn('attached', only_link.body)
		self.assertEqual(len(both.attachments), 1)
		self.assertIn('attached', both.body)
		self.assertIn(link, both.body)

class PublicOrderLinkTests(TestCase):
	"""Enlace público de solo lectura de una orden."""

	def setUp(self):
		from django.contrib.auth import get_user_model
		from django.core.cache import cache
		from rest_framework.test import APIClient

		from ..core.models import Cia

		cache.clear()  # contadores del throttle
		Cia.objects.create(codigo='T1', nombre='Test Cia', default=True)
		self.user = get_user_model().objects.create_user(
			'sale', 'sale@x.com', 'pw', first_name='Ana', last_name='Venta', tel1='555-1234'
		)
		self.client = APIClient()
		self.client.force_authenticate(self.user)
		self.anon = APIClient()

	def create_order(self, **extra):
		payload = {
			'customer_id': 'CID-777',
			'customer_name': 'Cliente',
			'customer_email': 'cli@secret.com',
			'customer_cel': '555-SECRET',
			'items': [{'sku': 'A1', 'name': 'Mesa', 'quantity': 2, 'price': '10.00'}],
		}
		payload.update(extra)
		response = self.client.post('/linapi/saleapp/extorder/', payload, format='json')
		self.assertEqual(response.status_code, 201, response.data)
		from .models import ExtOrderMaster
		return ExtOrderMaster.objects.get(pk=response.data['id'])

	def public_url(self, order, suffix=''):
		return f'/linapi/saleapp/public/orders/{order.public_token}/{suffix}'

	def test_token_issued_on_create_with_ttl(self):
		from datetime import timedelta
		from django.utils import timezone
		from .models import ExtOrderMaster

		order = self.create_order(public_token='hacked', public_token_expires_at='2099-01-01T00:00:00Z')
		self.assertTrue(order.public_token)
		self.assertNotEqual(order.public_token, 'hacked')
		delta = order.public_token_expires_at - timezone.now()
		self.assertTrue(timedelta(days=14, hours=23) < delta <= timedelta(days=15))

		response = self.client.post('/linapi/saleapp/extorderonly/', {'customer_name': 'X'}, format='json')
		self.assertEqual(response.status_code, 201)
		self.assertTrue(ExtOrderMaster.objects.get(pk=response.data['id']).public_token)

	def test_client_cannot_overwrite_token(self):
		order = self.create_order()
		token = order.public_token
		self.client.patch(
			f'/linapi/saleapp/extorderonly/{order.id}/', {'public_token': 'x', 'name': 'N'}, format='json'
		)
		order.refresh_from_db()
		self.assertEqual(order.public_token, token)
		self.assertEqual(order.name, 'N')

	def test_revoke_survives_later_save_and_renew_rotates(self):
		order = self.create_order()
		url = f'/linapi/saleapp/extorder/{order.id}/public-link/'
		old_token = order.public_token

		self.assertEqual(self.client.delete(url).status_code, 200)
		order.refresh_from_db()
		order.save()
		order.refresh_from_db()
		self.assertIsNone(order.public_token)
		self.assertEqual(self.anon.get(f'/linapi/saleapp/public/orders/{old_token}/').status_code, 404)

		response = self.client.post(url)
		self.assertEqual(response.status_code, 200)
		self.assertTrue(response.data['public_token'])
		self.assertNotEqual(response.data['public_token'], old_token)

	def test_renew_keeps_token_and_extends_expiry(self):
		from datetime import timedelta
		from django.utils import timezone

		order = self.create_order()
		order.public_token_expires_at = timezone.now() - timedelta(days=1)
		order.save()
		response = self.client.post(f'/linapi/saleapp/extorder/{order.id}/public-link/')
		self.assertEqual(response.data['public_token'], order.public_token)
		self.assertGreater(response.data['public_token_expires_at'], timezone.now() + timedelta(days=14))

	def test_link_management_requires_login(self):
		order = self.create_order()
		response = self.anon.post(f'/linapi/saleapp/extorder/{order.id}/public-link/')
		self.assertEqual(response.status_code, 401)

	def test_public_view_with_stale_auth_header(self):
		order = self.create_order()
		self.anon.credentials(HTTP_AUTHORIZATION='Token stale-invalid-token')
		response = self.anon.get(self.public_url(order))

		self.assertEqual(response.status_code, 200)
		self.assertEqual(response['Cache-Control'], 'no-store')
		self.assertIn('noindex', response['X-Robots-Tag'])
		self.assertEqual(set(response.data), {
			'id', 'name', 'customer_name', 'delivery_to', 'carrier_tag', 'status',
			'total', 'created_at', 'modified_at', 'public_token_expires_at', 'items', 'seller',
		})
		self.assertEqual(response.data['seller'], {'name': 'Ana Venta', 'email': 'sale@x.com', 'phone': '555-1234'})
		self.assertEqual(set(response.data['items'][0]), {'id', 'sku', 'name', 'quantity', 'price', 'image'})
		self.assertNotIn('secret', json.dumps(response.data, default=str).lower())

	def test_unknown_inactive_expired_and_cancelled(self):
		from datetime import timedelta
		from django.utils import timezone

		self.assertEqual(self.anon.get('/linapi/saleapp/public/orders/nope/').status_code, 404)

		order = self.create_order()
		self.assertEqual(self.anon.get(self.public_url(order).upper()).status_code, 404)

		order.is_active = False
		order.save()
		self.assertEqual(self.anon.get(self.public_url(order)).status_code, 404)

		order.is_active = True
		order.public_token_expires_at = timezone.now() - timedelta(seconds=1)
		order.save()
		response = self.anon.get(self.public_url(order))
		self.assertEqual(response.status_code, 410)
		self.assertEqual(response.data['code'], 'expired')

		order.public_token_expires_at = timezone.now() + timedelta(days=1)
		order.status = 'cancelled'
		order.save()
		for suffix in ('', 'pdf/', 'xlsx/'):
			response = self.anon.get(self.public_url(order, suffix))
			self.assertEqual(response.status_code, 410)
			self.assertEqual(response.data['code'], 'cancelled')

		response = self.client.post(f'/linapi/saleapp/extorder/{order.id}/public-link/')
		self.assertEqual(response.status_code, 400)

	def test_throttle(self):
		from rest_framework.throttling import ScopedRateThrottle

		order = self.create_order()
		rates = dict(ScopedRateThrottle.THROTTLE_RATES, public_order='2/min')
		with patch.object(ScopedRateThrottle, 'THROTTLE_RATES', rates):
			codes = [self.anon.get(self.public_url(order)).status_code for _ in range(3)]
		self.assertEqual(codes, [200, 200, 429])

	@patch('apps.saleapp.utils.HTML')
	def test_public_pdf_hides_contact_and_ignores_print_images(self, html):
		order = self.create_order()
		response = self.anon.get(self.public_url(order, 'pdf/') + '?print_images=file:///etc')

		self.assertEqual(response.status_code, 200)
		self.assertEqual(response['Content-Type'], 'application/pdf')
		rendered = html.call_args.kwargs['string']
		for secret in ('cli@secret.com', '555-SECRET', 'CID-777', '/etc', 'img src'):
			self.assertNotIn(secret, rendered)
		self.assertIn('Cliente', rendered)
		self.assertIn('sale@x.com', rendered)

	@patch('apps.saleapp.utils.HTML')
	def test_private_pdf_only_accepts_print_images_flag(self, html):
		from .utils import render_order_pdf

		order = self.create_order()
		render_order_pdf(order, print_images='http://evil/x')
		self.assertNotIn('evil', html.call_args.kwargs['string'])
		render_order_pdf(order, print_images='1')
		self.assertIn('fotos/A1.jpg', html.call_args.kwargs['string'])

	def test_real_pdf_with_null_seller(self):
		order = self.create_order()
		order.created_by = None
		order.save()
		self.assertIsNone(self.anon.get(self.public_url(order)).data['seller'])
		response = self.anon.get(self.public_url(order, 'pdf/'))
		self.assertEqual(response.status_code, 200)
		self.assertTrue(response.content.startswith(b'%PDF'))

	def test_public_xlsx_hides_contact(self):
		from io import BytesIO
		from openpyxl import load_workbook

		order = self.create_order()
		response = self.anon.get(self.public_url(order, 'xlsx/'))
		self.assertEqual(response.status_code, 200)

		ws = load_workbook(BytesIO(response.content)).active
		values = {str(c.value) for row in ws.iter_rows() for c in row if c.value is not None}
		self.assertIn('Cliente', values)
		self.assertIn('Mesa', values)
		for secret in ('cli@secret.com', '555-SECRET', 'CID-777 Cliente'):
			self.assertNotIn(secret, values)

	def test_preview_route_removed(self):
		order = self.create_order()
		response = self.anon.get(f'/linapi/saleapp/orders/{order.id}/preview/')
		self.assertEqual(response.status_code, 404)


class RevertOrderToPendingTests(TestCase):
	"""Volver una orden a 'pending' requiere permiso o ser superuser."""

	def setUp(self):
		from django.contrib.auth import get_user_model
		from rest_framework.test import APIClient

		from ..core.models import Cia

		Cia.objects.create(codigo='T1', nombre='Test Cia', default=True)
		self.user = get_user_model().objects.create_user('sale', 'sale@x.com', 'pw')
		self.client = APIClient()
		self.client.force_authenticate(self.user)

	def create_order(self, status='processed'):
		from .models import ExtOrderMaster

		response = self.client.post(
			'/linapi/saleapp/extorder/',
			{
				'customer_name': 'Cliente',
				'customer_email': 'cli@x.com',
				'items': [{'sku': 'A1', 'name': 'Mesa', 'quantity': 1, 'price': '10.00'}],
			},
			format='json',
		)
		self.assertEqual(response.status_code, 201, response.data)
		order = ExtOrderMaster.objects.get(pk=response.data['id'])
		if status != 'pending':
			ExtOrderMaster.objects.filter(pk=order.pk).update(status=status)
			order.refresh_from_db()
		return order

	def set_status(self, order, status, route='extorderonly'):
		return self.client.patch(
			f'/linapi/saleapp/{route}/{order.pk}/', {'status': status}, format='json'
		)

	def grant_via_group(self):
		from django.contrib.auth import get_user_model
		from django.contrib.auth.models import Group, Permission

		group = Group.objects.create(name='reopeners')
		group.permissions.add(Permission.objects.get(codename='revert_order_to_pending'))
		self.user.groups.add(group)
		# Usuario recargado: descarta la caché de permisos de la instancia
		self.user = get_user_model().objects.get(pk=self.user.pk)
		self.client.force_authenticate(self.user)

	def test_denied_without_permission_on_both_routes(self):
		for route in ('extorderonly', 'extorder'):
			order = self.create_order()
			response = self.set_status(order, 'pending', route)
			self.assertEqual(response.status_code, 403, response.data)
			order.refresh_from_db()
			self.assertEqual(order.status, 'processed')

	def test_other_transitions_do_not_need_permission(self):
		order = self.create_order(status='pending')
		self.assertEqual(self.set_status(order, 'pending').status_code, 200)
		self.assertEqual(self.set_status(order, 'processed').status_code, 200)
		self.assertEqual(self.set_status(order, 'shipped').status_code, 200)

	def test_allowed_with_group_permission(self):
		self.grant_via_group()
		for route in ('extorderonly', 'extorder'):
			order = self.create_order()
			response = self.set_status(order, 'pending', route)
			self.assertEqual(response.status_code, 200, response.data)
			order.refresh_from_db()
			self.assertEqual(order.status, 'pending')

	def test_allowed_for_superuser(self):
		from django.contrib.auth import get_user_model

		admin = get_user_model().objects.create_superuser('boss', 'boss@x.com', 'pw')
		order = self.create_order()
		self.client.force_authenticate(admin)
		self.assertEqual(self.set_status(order, 'pending').status_code, 200)

	def test_perm_is_exposed_to_frontend(self):
		response = self.client.get('/linapi/user_perms/cur/')
		self.assertEqual(response.status_code, 200)
		self.assertIs(response.data['perms']['saleapp.revert_order_to_pending'], False)


class SaleAppCsvEncodingTests(TestCase):
	def setUp(self):
		from django.contrib.auth import get_user_model
		from rest_framework.test import APIClient

		from ..core.models import Cia
		from .models import ExtOrderMaster

		self.cia = Cia.objects.create(codigo='T1', nombre='Test Cia', default=True)
		self.user = get_user_model().objects.create_user('sale', 'sale@x.com', 'pw')
		self.client = APIClient()
		self.client.force_authenticate(self.user)
		response = self.client.post(
			'/linapi/saleapp/extorder/',
			{
				'customer_name': 'Cliente',
				'customer_email': 'cli@x.com',
				'items': [{'sku': 'ÑA1', 'name': 'Mesa', 'quantity': 1, 'price': '10.00'}],
			},
			format='json',
		)
		self.order = ExtOrderMaster.objects.get(pk=response.data['id'])

	def set_encoding(self, encoding):
		from .models import SaleAppSettings

		SaleAppSettings.objects.update_or_create(
			company=self.cia, defaults={'csv_encoding': encoding}
		)

	def test_render_order_csv_encodings(self):
		from .utils import render_order_csv

		bom = b'\xef\xbb\xbf'
		self.assertTrue(render_order_csv(self.order).getvalue().startswith('ÑA1'.encode('utf-8')))
		self.assertTrue(
			render_order_csv(self.order, encoding='utf-8-sig').getvalue().startswith(bom + 'ÑA1'.encode('utf-8'))
		)
		self.assertTrue(render_order_csv(self.order, encoding='cp1252').getvalue().startswith(b'\xd1A1'))

	def test_unencodable_chars_are_replaced_in_cp1252(self):
		from .utils import render_order_csv

		self.order.items.update(sku='A→1')
		self.assertTrue(render_order_csv(self.order, encoding='cp1252').getvalue().startswith(b'A?1'))

	def test_download_uses_company_setting(self):
		url = f'/linapi/saleapp/orders/{self.order.id}/csv/'

		response = self.client.get(url)
		self.assertEqual(response['Content-Type'], 'text/csv; charset=utf-8')
		self.assertTrue(response.content.startswith('ÑA1'.encode('utf-8')))

		self.set_encoding('utf-8-sig')
		response = self.client.get(url, {'cia': self.cia.id})
		self.assertEqual(response['Content-Type'], 'text/csv; charset=utf-8')
		self.assertTrue(response.content.startswith(b'\xef\xbb\xbf'))

		self.set_encoding('cp1252')
		response = self.client.get(url)
		self.assertEqual(response['Content-Type'], 'text/csv; charset=windows-1252')
		self.assertTrue(response.content.startswith(b'\xd1A1'))

	def test_settings_validate_csv_encoding(self):
		from django.contrib.auth.models import Permission

		self.user.user_permissions.add(Permission.objects.get(codename='acc_config'))
		self.user = type(self.user).objects.get(pk=self.user.pk)
		self.client.force_authenticate(self.user)

		self.assertEqual(self.client.get('/linapi/saleapp/settings/').data['csv_encoding'], 'utf-8')
		for encoding in ('utf-8', 'utf-8-sig', 'cp1252'):
			response = self.client.put('/linapi/saleapp/settings/', {'csv_encoding': encoding}, format='json')
			self.assertEqual(response.status_code, 200, response.data)
			self.assertEqual(response.data['csv_encoding'], encoding)
		response = self.client.put('/linapi/saleapp/settings/', {'csv_encoding': 'latin-9'}, format='json')
		self.assertEqual(response.status_code, 400)

	@patch('apps.saleapp.views.send_order_email')
	def test_csv_email_uses_company_setting(self, task):
		self.set_encoding('cp1252')
		response = self.client.post(f'/linapi/saleapp/orders/{self.order.id}/email-csv/')
		self.assertEqual(response.status_code, 202)
		self.assertEqual(task.delay.call_args.kwargs['csv_encoding'], 'cp1252')
