from django.test import TestCase
import pytest
from django.urls import reverse
from unittest.mock import patch
from .models import UserProfile

# Create your tests here.

# Мок-данные для API
MOCK_API_RESPONSE = {
    'results': [
        {
            'gender': 'male',
            'name': {'first': 'John', 'last': 'Doe'},
            'phone': '123-456-7890',
            'email': 'john.doe@example.com',
            'location': {
                'city': 'New York',
                'state': 'NY',
                'country': 'USA',
                'street': {'number': 123, 'name': 'Main St'},
                'postcode': '10001'
            },
            'picture': {'thumbnail': 'https://example.com/thumb.jpg'},
            'login': {'uuid': 'test-uuid-1'}
        },
        {
            'gender': 'female',
            'name': {'first': 'Jane', 'last': 'Smith'},
            'phone': '098-765-4321',
            'email': 'jane.smith@example.com',
            'location': {
                'city': 'Los Angeles',
                'state': 'CA',
                'country': 'USA',
                'street': {'number': 456, 'name': 'Broadway'},
                'postcode': '90001'
            },
            'picture': {'thumbnail': 'https://example.com/thumb2.jpg'},
            'login': {'uuid': 'test-uuid-2'}
        }
    ]
}

@pytest.mark.django_db
class TestUserProfile:
    def test_create_user_profile(self):
        """Тест создания пользователя"""
        user = UserProfile.objects.create(
            gender='male',
            first_name='John',
            last_name='Doe',
            phone='123-456-7890',
            email='john@example.com',
            city='New York',
            state='NY',
            country='USA',
            street='123 Main St',
            postcode='10001',
            picture_thumbnail='https://example.com/thumb.jpg',
            uuid='test-uuid'
        )
        assert user.first_name == 'John'
        assert user.last_name == 'Doe'
        assert str(user) == 'John Doe (john@example.com)'

@pytest.mark.django_db
class TestViews:
    @patch('requests.get')
    def test_load_random_users_command(self, mock_get):
        """Тест команды загрузки пользователей"""
        mock_get.return_value.json.return_value = MOCK_API_RESPONSE
        from django.core.management import call_command
        call_command('load_random_users')
        assert UserProfile.objects.count() == 2

    def test_user_list_view(self, client):
        """Тест отображения списка пользователей"""
        # Создаем тестового пользователя
        UserProfile.objects.create(
            gender='male',
            first_name='John',
            last_name='Doe',
            phone='123-456-7890',
            email='john@example.com',
            city='New York',
            state='NY',
            country='USA',
            street='123 Main St',
            postcode='10001',
            picture_thumbnail='https://example.com/thumb.jpg',
            uuid='test-uuid'
        )
        
        # Проверяем отображение списка
        response = client.get(reverse('user_list'))
        assert response.status_code == 200
        content = response.content.decode()
        assert 'John' in content
        assert 'Doe' in content
        
        # Проверяем пагинацию
        response = client.get(f"{reverse('user_list')}?count=1")
        assert response.status_code == 200

    def test_user_detail_view(self, client):
        """Тест отображения детальной информации о пользователе"""
        user = UserProfile.objects.create(
            gender='male',
            first_name='John',
            last_name='Doe',
            phone='123-456-7890',
            email='john@example.com',
            city='New York',
            state='NY',
            country='USA',
            street='123 Main St',
            postcode='10001',
            picture_thumbnail='https://example.com/thumb.jpg',
            uuid='test-uuid'
        )
        
        response = client.get(reverse('user_detail', args=[user.uuid]))
        assert response.status_code == 200
        assert 'John Doe' in response.content.decode()
        assert 'john@example.com' in response.content.decode()

    def test_random_user_view(self, client):
        """Тест отображения случайного пользователя"""
        # Создаем тестовых пользователей
        UserProfile.objects.create(
            gender='male',
            first_name='John',
            last_name='Doe',
            phone='123-456-7890',
            email='john@example.com',
            city='New York',
            state='NY',
            country='USA',
            street='123 Main St',
            postcode='10001',
            picture_thumbnail='https://example.com/thumb.jpg',
            uuid='test-uuid-1'
        )
        UserProfile.objects.create(
            gender='female',
            first_name='Jane',
            last_name='Smith',
            phone='098-765-4321',
            email='jane@example.com',
            city='Los Angeles',
            state='CA',
            country='USA',
            street='456 Broadway',
            postcode='90001',
            picture_thumbnail='https://example.com/thumb2.jpg',
            uuid='test-uuid-2'
        )
        
        response = client.get(reverse('random_user'))
        assert response.status_code == 200
        assert any(name in response.content.decode() for name in ['John Doe', 'Jane Smith'])
