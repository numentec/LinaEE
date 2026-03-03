from django.contrib.auth import get_user_model
from django.test import TestCase

from .models import CatalogMaster
from .serializers import CatalogSerializer


class CatalogMasterRegressionTests(TestCase):
	def setUp(self):
		self.user = get_user_model().objects.create_user(
			username="catalog_creator",
			password="test-pass-123",
		)

	def test_save_assigns_owner_and_seller_from_created_by(self):
		catalog = CatalogMaster(
			company_id="1",
			name="Spring Collection",
			created_by=self.user,
			modified_by=self.user,
		)

		catalog.save()

		self.assertEqual(catalog.owner_id, self.user.id)
		self.assertEqual(catalog.seller_id, self.user.id)

	def test_serializer_create_without_owner_does_not_raise_and_sets_owner(self):
		payload = {
			"company_id": 1,
			"name": "Spring Collection",
			"template": "minimal",
			"orientation": "landscape",
			"status": "draft",
			"settings": {
				"show_price": True,
				"show_brand": True,
				"show_min_max": True,
				"show_sku": True,
				"show_description": True,
				"show_images": True,
			},
			"theme": {
				"density": "comfortable",
				"radius": "md",
				"image_fit": "contain",
			},
			"pages": [
				{
					"id": "page_1",
					"name": "Página 1",
					"layout": "grid_2x4",
					"items": [],
					"locked": False,
				}
			],
		}

		serializer = CatalogSerializer(data=payload)
		self.assertTrue(serializer.is_valid(), serializer.errors)

		catalog = serializer.save(created_by=self.user, modified_by=self.user)

		self.assertEqual(catalog.owner_id, self.user.id)
		self.assertEqual(catalog.seller_id, self.user.id)
		self.assertEqual(catalog.company_id, "1")
