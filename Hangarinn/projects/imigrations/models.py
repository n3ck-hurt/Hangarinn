from django.db import models

class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True
        ordering = ("-created_at",)

class Category(models.Model):
    name = models.CharField(max_length=100)

    class Meta:
        verbose_name = "Category"
        verbose_name_plural = "Categories"   

    def __str__(self):
        return self.name

class Order(BaseModel):
    class Status(models.TextChoices):
        DRAFT = "draft", "Draft"
        PENDING = "pending", "Pending"
        PAID = "paid", "Paid"
        CANCELLED = "cancelled", "Cancelled"

    number = models.CharField(max_length=32, unique=True)
    customer_name = models.CharField(max_length=255)
    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.DRAFT,
        help_text="Current lifecycle state of the order.",
    )

    def __str__(self) -> str:
        return f"Order {self.number} · {self.get_status_display()}"

class Ticket(BaseModel):
    class Status(models.IntegerChoices):
        OPEN = 1, "Open"
        IN_PROGRESS = 2, "In Progress"
        RESOLVED = 3, "Resolved"
        CLOSED = 4, "Closed"

    title = models.CharField(max_length=200)
    status = models.PositiveSmallIntegerField(
        choices=Status.choices,
        default=Status.OPEN,
    )

    def __str__(self) -> str:
        return f"#{self.pk} {self.title} ({self.get_status_display()})"
