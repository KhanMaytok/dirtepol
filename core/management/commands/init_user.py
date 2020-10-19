from django.core.management.base import BaseCommand

from core.models import User


class Command(BaseCommand):
    help = 'Init user'

    def handle(self, *args, **kwargs):
        try:
            a = User.objects.get(username='khalo')
            a.is_active = True
            a.is_staff = True
            a.is_superuser = True
            a.save()
        except User.DoesNotExist:
            User.objects.create_user(
                username='khalo',
                email='gventura@maytok.com',
                password='123qweASDASDASD'
            )
