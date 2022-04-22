from django.db import migrations

from bake_end.models import Product, Category


class Migration(migrations.Migration):
    dependencies = [
        ('bake_end', '0003_populate_product_slug_field'),
    ]

    operations = [
        migrations.RenameField(
            model_name='Product',
            old_name='category',
            new_name='categories',
        ),
    ]
