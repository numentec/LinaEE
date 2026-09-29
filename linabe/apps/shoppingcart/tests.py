from types import SimpleNamespace
from unittest.mock import Mock, patch

from django.test import TestCase
from rest_framework.test import APIRequestFactory, force_authenticate

from .views import parse_stock_filters


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
				ref_cursor,
			],
		)
		self.assertEqual(response.status_code, 200)
		self.assertEqual(response.data['count'], 2)
		self.assertEqual(
			response.data['results'],
			[{'id': 'SKU-1', 'instock': 5}],
		)
