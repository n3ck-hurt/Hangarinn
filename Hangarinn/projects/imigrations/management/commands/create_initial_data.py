from django.core.management.base import BaseCommand
from django.utils import timezone
from faker import Faker
import random

from Hangarinn.projects.imigrations.models import Priority, Category, Task, Note, SubTask

class Command(BaseCommand):
    help = "Populate database with initial Priority, Category, and fake Task data"

    def handle(self, *args, **kwargs):
        fake = Faker()
    
        priorities = ["High", "Medium", "Low", "Critical", "Optional"]
        for p in priorities:
            Priority.objects.get_or_create(name=p)
        self.stdout.write(self.style.SUCCESS("✅ Priorities added."))

        categories = ["Work", "School", "Personal", "Finance", "Projects"]
        for c in categories:
            Category.objects.get_or_create(name=c)
        self.stdout.write(self.style.SUCCESS("✅ Categories added."))

        for _ in range(20):
            task = Task.objects.create(
                title=fake.sentence(nb_words=5),
                description=fake.paragraph(nb_sentences=3),
                status=fake.random_element(elements=["Pending", "In Progress", "Completed"]),
                deadline=timezone.make_aware(fake.date_time_this_month()),
                priority=random.choice(Priority.objects.all()),
                category=random.choice(Category.objects.all()),
            )

            for _ in range(random.randint(1, 3)):
                Note.objects.create(
                    task=task,
                    content=fake.paragraph(nb_sentences=2),
                )

            for _ in range(random.randint(1, 5)):
                SubTask.objects.create(
                    task=task,
                    title=fake.sentence(nb_words=4),
                    status=fake.random_element(elements=["Pending", "In Progress", "Completed"]),
                )

        self.stdout.write(self.style.SUCCESS("Fake data generated successfully!"))
