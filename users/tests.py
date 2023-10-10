from django.test import Client, RequestFactory
import pytest
from django.urls import resolve, reverse
from rest_framework.test import APITestCase
from rest_framework import status
import json
from users.models import UsersModel
from django.test import TestCase
from django.urls import reverse
# https://docs.djangoproject.com/en/4.0/topics/testing/overview/
# https://www.django-rest-framework.org/api-guide/testing/
# pytestmark = pytest.mark.django_db

from rest_framework.test import APITestCase

class UsersTestCase(APITestCase):

   

    def test_created_user(self):

        created = self.client.post("/users/",{
                "username":"teste",
                "email":"teste@gamil.com",
                "password":"123"

        })
        user = UsersModel.objects.get(username="teste",email="teste@gamil.com")
        user_json = created.json()
        self.assertEqual(created.status_code,201)
        self.assertEqual(user_json['id'],str(user.id))
    
    def test_created_user_error_required_email(self):

        created = self.client.post("/users/",{
                "username":"teste",
                
                "password":"123"

        })

        self.assertEqual(created.status_code,400)
        
    def test_created_user_error_required_username(self):

            created = self.client.post("/users/",{
                    
                    "email":"teste@gamil.com",
                    "password":"123"

            })

            self.assertEqual(created.status_code,400)
    
    def test_created_user_error_required_password(self):

            created = self.client.post("/users/",{
                    "username":"teste",
                    "email":"teste@gamil.com",
                    

            })

            self.assertEqual(created.status_code,400)
    def test_created_user_error_required(self):

        created = self.client.post("/users/",{})

        self.assertEqual(created.status_code,400)

        
    def test_login_user(self):

        self.client.post("/users/",{
                "username":"teste2",
                "email":"teste2@gamil.com",
                "password":"123"

        })

        login = self.client.post("/users/token/",{
                "username":"teste2",
                "password":"123"

        })
        
        user_json = login.json()
        self.assertEqual(login.status_code,200)
        self.assertTrue(user_json["refresh"])
        self.assertTrue(user_json["access"])
        
       