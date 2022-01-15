import unittest, os

from .payment import PaymesPayment


class PaymesPaymentTest(unittest.TestCase):
    def setUp(self) -> None:
        self.gateway=PaymesPayment(
            secret_key=os.getenv('PAYMES_SECRET_KEY', ''),
            public_key=os.getenv('PAYMES_PUBLIC_KEY', '')
        )
        self.transaction = self.gateway.create_order(
            order_id='123456789',
            price=100,
            currency='TRY',
            product_name='Ürün İsmi',
            buyer_name='Sanan Gojayev',
            buyer_phone='05555555555',
            buyer_email='email@example.com',
            buyer_address='Örnek adres bilgisi'
        )
        self.payment_obj=self.gateway.get_payment()
    
    def test_create_order(self):
        print(self.payment_obj)

        
    def test_get_order_status(self):
        order_status = self.gateway.get_order_status(
            paymes_order_id=self.payment_obj.paymes_order_id
        )
        print(order_status)