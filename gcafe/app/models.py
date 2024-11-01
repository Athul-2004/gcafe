# cafe/models.py
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import timedelta

class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    contact = models.CharField(max_length=15)

    def __str__(self):
        return self.user.username

class System(models.Model):
    SYSTEM_TYPES = [
        ('PC', 'PC'),
        ('PS4', 'PlayStation 4'),
        ('PS5', 'PlayStation 5'),
        ('XBOX', 'XBOX One')
    ]
    system_type = models.CharField(max_length=5, choices=SYSTEM_TYPES)
    is_available = models.BooleanField(default=True)

    def __str__(self):
        return f'{self.system_type} - Available: {self.is_available}'

    def update_availability(self):
        # Check if the system is booked in the future and update its availability
        current_time = timezone.now()
        has_future_bookings = Booking.objects.filter(
            system=self,
            end_time__gt=current_time
        ).exists()

        self.is_available = not has_future_bookings
        self.save()

class Game(models.Model):
    title = models.CharField(max_length=100)
    system = models.ForeignKey('System', on_delete=models.CASCADE)
    description = models.CharField(max_length=200, default="placeholder description")
    image = models.ImageField(upload_to='games/', default='games/default_game_image.jpg')

    def __str__(self):
        return self.title
    
class Booking(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    system = models.ForeignKey(System, on_delete=models.CASCADE)
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    start_time = models.DateTimeField(default=timezone.now)
    end_time = models.DateTimeField()
    bill_amount = models.DecimalField(max_digits=6, decimal_places=2, blank=True, null=True)

    def __str__(self):
        return f'{self.customer} booked {self.game} on {self.system}'

    def is_system_available(self):
        # Check if the system is available during the requested time range
        overlapping_bookings = Booking.objects.filter(
            system=self.system,
            end_time__gt=self.start_time,
            start_time__lt=self.end_time
        ).exists()

        return not overlapping_bookings

    def calculate_bill(self):
        # Calculate the duration in hours and compute the bill amount
        duration = self.end_time - self.start_time
        hours = duration.total_seconds() / 3600
        self.bill_amount = hours * 1200  # Assuming $1200 per hour
        self.save()

    def save(self, *args, **kwargs):
        # Before saving the booking, calculate the bill
        if not self.bill_amount:
            self.calculate_bill()
        super(Booking, self).save(*args, **kwargs)