from django.db import migrations


def copy_profiles_data(apps, schema_editor):
    OldProfile = apps.get_model('oc_lettings_site', 'Profile')
    NewProfile = apps.get_model('profiles', 'Profile')

    for profile in OldProfile.objects.all():
        NewProfile.objects.create(
            id=profile.id,
            user_id=profile.user_id,
            favorite_city=profile.favorite_city,
        )


def reverse_profiles_data(apps, schema_editor):
    NewProfile = apps.get_model('profiles', 'Profile')
    NewProfile.objects.all().delete()


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0001_initial'),
        ('oc_lettings_site', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(copy_profiles_data, reverse_profiles_data),
    ]
