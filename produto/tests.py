from django.contrib.auth import get_user_model
from django.test import TestCase

from .models import Produto


class ProductTests(TestCase):
    def setUp(self):
        user = get_user_model().objects.create_user(
            "tester", password="test-password-only"
        )
        self.client.force_login(user)

    def test_duplicate_is_a_form_error_not_a_server_error(self):
        Produto.objects.create(nome="Notebook")
        response = self.client.post("/adicionar-produto/", {"nome": " NOTEBOOK "})
        self.assertEqual(response.status_code, 200)
        self.assertIn("nome", response.context["form"].errors)
        self.assertEqual(Produto.objects.count(), 1)

    def test_missing_name_is_a_form_error(self):
        response = self.client.post("/adicionar-produto/", {})
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.context["form"].errors)

    def test_name_whitespace_is_normalized(self):
        self.client.post("/adicionar-produto/", {"nome": "  Blue   notebook "})
        self.assertEqual(Produto.objects.get().nome, "Blue notebook")
