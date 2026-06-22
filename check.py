import django; django.setup()
from clubs.models import ClubApplication
for a in ClubApplication.objects.all():
    print(f'PK={a.pk}, email="{a.email}"')
print('done')
