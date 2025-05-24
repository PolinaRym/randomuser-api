from django.core.management.base import BaseCommand
from users.models import UserProfile
import requests

class Command(BaseCommand):
    help = 'Загружает 1000 случайных пользователей из randomuser.me'

    def handle(self, *args, **kwargs):
        if UserProfile.objects.exists():
            self.stdout.write(self.style.SUCCESS('Пользователи уже загружены.'))
            return
        url = 'https://randomuser.me/api/?results=1000&nat=us,gb,fr,ru,de'
        response = requests.get(url)
        data = response.json()['results']
        users = []
        for item in data:
            users.append(UserProfile(
                gender=item['gender'],
                first_name=item['name']['first'],
                last_name=item['name']['last'],
                phone=item['phone'],
                email=item['email'],
                city=item['location']['city'],
                state=item['location']['state'],
                country=item['location']['country'],
                street=f"{item['location']['street']['number']} {item['location']['street']['name']}",
                postcode=str(item['location']['postcode']),
                picture_thumbnail=item['picture']['thumbnail'],
                uuid=item['login']['uuid'],
            ))
        UserProfile.objects.bulk_create(users)
        self.stdout.write(self.style.SUCCESS('1000 пользователей успешно загружены!')) 