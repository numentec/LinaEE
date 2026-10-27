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
