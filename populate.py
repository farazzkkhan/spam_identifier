import random
from django.contrib.auth import get_user_model
from api.models import Contact

User = get_user_model()

def populate():
    user = User.objects.create_user(username='testuser', phone_number='1234567890', password='password')
    for i in range(100):
        name = f'Contact {i}'
        phone_number = str(random.randint(1000000000, 9999999999))
        is_spam = random.choice([True, False])
        Contact.objects.create(user=user, name=name, phone_number=phone_number, is_spam=is_spam)
