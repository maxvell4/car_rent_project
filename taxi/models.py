from django.db import models
from django.contrib.auth.models import AbstractUser
from django.urls import reverse


class Manufacturer(models.Model):
    name = models.CharField(max_length=255, unique=True)
    country = models.CharField(max_length=255)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return f"{self.name} {self.country}"


class Driver(AbstractUser):
    license_number = models.CharField(max_length=255, unique=True)

    class Meta:
        verbose_name = "driver"
        verbose_name_plural = "drivers"

    def __str__(self):
        return f"{self.username} ({self.first_name} {self.last_name})"

    def get_absolute_url(self):
        return reverse("taxi:driver-detail", kwargs={"pk": self.pk})


class Car(models.Model):
    image = models.ImageField(upload_to='cars/', blank=True, null=True)
    price_per_day = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    model = models.CharField(max_length=255)
    manufacturer = models.ForeignKey(Manufacturer, on_delete=models.CASCADE, related_name="manufacturer")
    drivers = models.ManyToManyField(Driver, related_name="cars")

    def __str__(self):
        return self.model


class CarInsideImage(models.Model):
    car = models.ForeignKey(Car, on_delete=models.CASCADE, related_name='inside_images')
    image_inside = models.ImageField(upload_to='car_inside/')

    def __str__(self):
        return f"Image of {self.car.model}"


class Booking(models.Model):
    car = models.ForeignKey(Car, on_delete=models.CASCADE, related_name="car")
    start_date = models.DateField()
    end_date = models.DateField()
    name = models.CharField(max_length=100)
    email = models.EmailField()

    def __str__(self):
        return f"Booking for {self.car} from {self.start_date} to {self.end_date}"
