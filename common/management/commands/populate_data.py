
from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from products.models import Category, Product
from faker import Faker
import random

User = get_user_model()

class Command(BaseCommand):
    help = 'Populates the database with mock data for testing.'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Starting data population...'))
        fake = Faker()

        # 1. Create Users
        self.stdout.write('Creating users...')
        users_to_create = [
            {'username': 'testuser1', 'email': 'test1@example.com', 'password': 'password123', 'first_name': 'Alice', 'last_name': 'Smith'},
            {'username': 'testuser2', 'email': 'test2@example.com', 'password': 'password123', 'first_name': 'Bob', 'last_name': 'Johnson'},
            {'username': 'testuser3', 'email': 'test3@example.com', 'password': 'password123', 'first_name': 'Charlie', 'last_name': 'Brown'},
            {'username': 'testuser4', 'email': 'test4@example.com', 'password': 'password123', 'first_name': 'Diana', 'last_name': 'Prince'},
        ]

        for user_data in users_to_create:
            if not User.objects.filter(username=user_data['username']).exists():
                User.objects.create_user(**user_data)
                self.stdout.write(f'  Created user: {user_data['username']}')
            else:
                self.stdout.write(f'  User already exists: {user_data['username']}')

        # 2. Create Categories
        self.stdout.write('Creating 100 product categories...')
        categories = []
        for i in range(100):
            category_name = fake.unique.word().capitalize() + ' Category'
            category, created = Category.objects.get_or_create(name=category_name)
            if created:
                categories.append(category)
                # self.stdout.write(f'  Created category: {category.name}')
            else:
                categories.append(category) # Add existing ones to list for product creation
                # self.stdout.write(f'  Category already exists: {category.name}')
        self.stdout.write(self.style.SUCCESS(f'Finished creating {len(categories)} categories.'))

        # 3. Create Products (around 500 products, 5 per category on average)
        self.stdout.write('Creating products...')
        products_created = 0
        if categories:
            for _ in range(500):
                product_name = fake.catch_phrase()
                product_description = fake.paragraph(nb_sentences=3)
                product_price = round(random.uniform(5.0, 1000.0), 2)
                category = random.choice(categories)

                if not Product.objects.filter(name=product_name).exists():
                    Product.objects.create(
                        name=product_name,
                        description=product_description,
                        price=product_price,
                        category=category
                    )
                    products_created += 1
            self.stdout.write(self.style.SUCCESS(f'Finished creating {products_created} products.'))
        else:
            self.stdout.write(self.style.WARNING('No categories found, skipping product creation.'))

        self.stdout.write(self.style.SUCCESS('Data population complete!'))
