from decimal import Decimal

from django.contrib.auth import get_user_model
from django.db import IntegrityError, transaction
from django.test import TestCase
from produto.models import Produto

from .models import Compra
from .views import purchase_summary


class PurchaseTests(TestCase):
    def setUp(self):
        self.product = Produto.objects.create(nome="Notebook")
        self.user = get_user_model().objects.create_user(
            "tester", password="test-password-only"
        )

    def test_weighted_average_uses_decimal_prices(self):
        Compra.objects.create(produto=self.product, quantidade=2, preco="0.10")
        Compra.objects.create(produto=self.product, quantidade=1, preco="0.40")
        row = purchase_summary()[0]
        self.assertEqual(row["total_gasto"], Decimal("0.60"))
        self.assertEqual(row["valor_medio"], Decimal("0.20"))
        self.assertEqual(row["quantidade_total"], 3)

    def test_summary_uses_two_queries_for_multiple_products(self):
        for i in range(5):
            product = Produto.objects.create(nome=f"Item {i}")
            Compra.objects.create(produto=product, quantidade=2, preco="3.50")
        with self.assertNumQueries(2):
            self.assertEqual(len(purchase_summary()), 5)

    def test_zero_quantity_rejected_at_database_boundary(self):
        with self.assertRaises(IntegrityError), transaction.atomic():
            Compra.objects.create(produto=self.product, quantidade=0, preco="1.00")

    def test_negative_price_rejected(self):
        with self.assertRaises(IntegrityError), transaction.atomic():
            Compra.objects.create(produto=self.product, quantidade=1, preco="-1.00")

    def test_pages_require_login(self):
        for path in ("/compras/", "/adicionar-compra/", "/adicionar-produto/"):
            self.assertEqual(self.client.get(path).status_code, 302)

    def test_form_validates_quantity_and_price(self):
        self.client.force_login(self.user)
        for values in (
            {"quantidade": 0, "preco": "1"},
            {"quantidade": 1, "preco": "-1"},
        ):
            result = self.client.post(
                "/adicionar-compra/", {"produto": self.product.id, **values}
            )
            self.assertEqual(result.status_code, 200)
            self.assertTrue(result.context["form"].errors)
        self.assertEqual(Compra.objects.count(), 0)

    def test_valid_purchase_redirects_to_summary(self):
        self.client.force_login(self.user)
        result = self.client.post(
            "/adicionar-compra/",
            {"produto": self.product.id, "quantidade": 2, "preco": "4.50"},
        )
        self.assertRedirects(result, "/compras/")
        self.assertEqual(Compra.objects.get().preco, Decimal("4.50"))
