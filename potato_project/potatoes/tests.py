from django.core.exceptions import ObjectDoesNotExist
from django.db import DatabaseError
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework.test import APIClient, APITestCase

from .models import Potato
from .serializers import PotatoSerializer


class PotatoesListTests(APITestCase):
    def setUp(self):
        self.client = APIClient("potatoes")
        self.url = reverse("potatoes-list")

    def test_get_potatoes_list_success(self):
        # Test data setup
        Potato.objects.create(name="KingTato 1")
        Potato.objects.create(name="QueenTato 1")
        Potato.objects.create(name="PrinceTato 1")
        Potato.objects.create(name="PrincessTato 1")

        response = self.client.get(self.url)

        potatoes = Potato.objects.all()
        serializer = PotatoSerializer(potatoes, many=True)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)
