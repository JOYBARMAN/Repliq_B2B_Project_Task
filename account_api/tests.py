from django.test import TestCase
from rest_framework.test import APITestCase
from rest_framework import status



class TestMerchantAccountApi(APITestCase):
    def setUp(self):
        print("Successfully Done")

    # test merchant account register api
    def test_merchant_account_register(self):
        payload ={
            "email":"test@gmail.com",
            "name":"test",
            "check_condition":"True",
            "password":"12345678",
            "password2":"12345678"
        }
        headers = {
        'Content-Type': 'application/json'
        }
        response = self.client.post('/api/merchant/register/', data=payload,format="json", **headers)
        self.assertEquals(response.status_code,status.HTTP_201_CREATED)
        # self.assertEquals(response.data['email'],payload['email'])
     


    
