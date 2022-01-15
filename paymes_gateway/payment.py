import base64, hashlib
import requests 
import json

from .entities import Payment, PaymentStatus


class PaymesPayment:
    BASE_URL = 'https://api.paym.es/v4.6'

    def __init__(
        self,
        secret_key: str,
        public_key: str 
        ) -> None:
        self.secret_key = secret_key
        self.public_key = public_key

        self.__payment_instance = None
        self.__payment_status_instance = None
    
    def __post(self, data: dict, slug: str) -> dict:
        headers = {'Content-Type': 'application/json'}
        r = requests.post(
            f'{self.BASE_URL}/{slug}',
            data=json.dumps(data),
            headers=headers
        )
        return r.json()
    
    def __build_payment_obj(self, initial_data: dict) -> None:
        self.__payment_instance=Payment(
            status=initial_data['status'],
            message=initial_data['message'],
            return_url=initial_data['returnUrl'],
            paymes_order_id=initial_data['paymesOrderId']
        )
    
    def __build_payment_status_obj(self, initial_data: dict) -> None:
        self.__payment_status_instance=PaymentStatus(
            status=initial_data['status'],
            currency=initial_data['results']['currency'],
            price=initial_data['results']['price'],
            type=initial_data['results']['type'],
            message=initial_data['results']['message'],
            order_id=initial_data['results']['orderId'],
            paymes_order_id=initial_data['results']['paymesOrderId'],
            hash=initial_data['results']['hash'],
        )
    
    def get_payment(self) -> Payment:
        return self.__payment_instance
    
    def get_payment_status(self) -> PaymentStatus:
        return self.__payment_status_instance
    
    def generate_hash(self, r: str) -> str:
        hash=base64.b64encode(
            hashlib.sha512(r.encode('utf-8')).digest()
        ).decode()
        return hash
    
    def create_order_hash(self, data: dict) -> None:
        r=(data['orderId'] + str(data['price']) + data['currency'] 
                + data['productName'] + data['buyerName'] 
                + data['buyerPhone'] + data['buyerEmail'] 
                + data['buyerAddress'] + self.secret_key)
        hash = self.generate_hash(r=r)
        return hash

    def create_hash_control(self, paymes_order_id: str):
        r=paymes_order_id + self.secret_key
        hash=self.generate_hash(r)
        return hash

    def create_order(
        self, 
        order_id: str, 
        price: int, 
        currency: str, 
        product_name: str,
        buyer_name: str,
        buyer_phone: str,
        buyer_email: str,
        buyer_address: str
        ) -> dict:
        order_data={
            'publicKey': self.public_key,
            'orderId': order_id,
            'price': price,
            'currency': currency,
            'productName': product_name,
            'buyerName': buyer_name,
            'buyerPhone': buyer_phone,
            'buyerEmail': buyer_email,
            'buyerAddress': buyer_address
        }
        hash=self.create_order_hash(order_data)
        order_data.update({'hash': hash})
        result=self.__post(order_data, 'order_create')
        self.__build_payment_obj(result)
        payment=self.get_payment()
        return payment.return_url

    def get_order_status(self, paymes_order_id: str):
        hash=self.create_hash_control(paymes_order_id)
        order_data={
            'publicKey': self.public_key,
            'paymesOrderId': paymes_order_id,
            'hash': hash
        }
        result=self.__post(order_data, 'status')
        self.__build_payment_status_obj(result)
        return self.get_payment_status()

