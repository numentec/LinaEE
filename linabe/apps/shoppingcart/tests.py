import json
from types import SimpleNamespace
from unittest.mock import Mock, patch

from django.test import TestCase
from rest_framework.test import APIRequestFactory, force_authenticate

from .views import (
	SuggestProductsAPIView,
	parse_description_filter,
	parse_description_text,
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
	@patch('apps.shoppingcart.views.connections')
	@patch('apps.shoppingcart.views.SQLQuery')
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
			'/linapi/shoppingcart/products/',
			{
				'instock_operator': 'gte',
				'instock_value': '5',
				'color': ' rojo ',
				'acabado': 'mate',
				'descrips': json.dumps(['Mesa roble', 'Silla']),
				'descrip_text': ' mesa ',
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
				ref_cursor,
			],
		)
		self.assertEqual(response.status_code, 200)
		self.assertEqual(response.data['count'], 2)
		self.assertEqual(
			response.data['results'],
			[{'id': 'SKU-1', 'instock': 5}],
		)


class SuggestProductsAPIViewTests(TestCase):
	def _get(self, params):
		request = APIRequestFactory().get(
			'/linapi/shoppingcart/products/suggest/', params
		)
		force_authenticate(
			request, user=SimpleNamespace(is_authenticated=True, pk=1)
		)
		return SuggestProductsAPIView.as_view()(request)

	@patch('apps.shoppingcart.views.connections')
	@patch('apps.shoppingcart.views.SQLQuery')
	def test_short_text_returns_empty_without_querying(
		self, sql_query, connections
	):
		response = self._get({'q': ' a '})

		self.assertEqual(response.status_code, 200)
		self.assertEqual(response.data, [])
		connections.__getitem__.assert_not_called()

	@patch('apps.shoppingcart.views.connections')
	@patch('apps.shoppingcart.views.SQLQuery')
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

	@patch('apps.shoppingcart.views.connections')
	@patch('apps.shoppingcart.views.SQLQuery')
	def test_rejects_unsafe_brands_list(self, sql_query, connections):
		response = self._get({'q': 'mesa', 'brands': "1') OR ('1'='1"})

		self.assertEqual(response.status_code, 400)
		connections.__getitem__.assert_not_called()

	@patch('apps.shoppingcart.views.connections')
	@patch('apps.shoppingcart.views.SQLQuery')
	def test_reports_missing_query_configuration(
		self, sql_query, connections
	):
		sql_query.objects.filter.return_value = []

		response = self._get({'q': 'mesa'})

		self.assertEqual(response.status_code, 503)
		connections.__getitem__.assert_not_called()
