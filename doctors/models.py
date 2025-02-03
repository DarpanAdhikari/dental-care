from django.db import models
from django.contrib.auth.models import User
from accounts.models import Doctor,Patient

class Appointment(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    appointment_date = models.DateTimeField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')

    def __str__(self):
        return f"{self.patient.user.get_full_name()} - {self.doctor.user.get_full_name()}"

class Prescription(models.Model):
    appointment = models.OneToOneField(Appointment, on_delete=models.CASCADE)
    diagnosis = models.TextField()
    medicines = models.TextField() 
    advice = models.TextField()
    def save(self, *args, **kwargs):
        if self.appointment.status != 'completed':
            self.appointment.status = 'completed'
            self.appointment.save()
        super().save(*args, **kwargs)
        
    def __str__(self):
        return f"Prescription for {self.appointment.patient.user.get_full_name()}"
    
class Bill(models.Model):
    appointment = models.OneToOneField(Appointment, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_status = models.BooleanField(default=False)  # Paid or Not Paid
    invoice_num = models.CharField(max_length=150, blank=True, null=True)
    issued_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Bill for {self.appointment.patient.user.get_full_name()}"
    def total_amount(self):
        return self.amount

class Inventory(models.Model):
    item_name = models.CharField(max_length=100)
    quantity = models.IntegerField()
    low_stock_alert = models.IntegerField(default=5)

    def __str__(self):
        return self.item_name
    
class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    def __str__(self):
        return f"Notification for {self.message}"