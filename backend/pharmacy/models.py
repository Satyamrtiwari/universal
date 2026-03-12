from django.db import models

class Pharmacy(models.Model):
    name = models.CharField(max_length=200)
    address = models.TextField()
    area_village = models.CharField(max_length=100)
    pincode = models.CharField(max_length=6)
    phone_number = models.CharField(max_length=15)
    
    def __str__(self):
        return f"{self.name} - {self.area_village}"

class Medicine(models.Model):
    name = models.CharField(max_length=200, unique=True)
    description = models.TextField(null=True, blank=True)
    
    def __str__(self):
        return self.name

class Stock(models.Model):
    pharmacy = models.ForeignKey(Pharmacy, on_delete=models.CASCADE, related_name='stocks')
    medicine = models.ForeignKey(Medicine, on_delete=models.CASCADE, related_name='available_at')
    quantity = models.IntegerField(default=0)
    is_available = models.BooleanField(default=True)
    last_updated = models.DateTimeField(auto_now=True)
    
    class Meta:
        unique_together = ('pharmacy', 'medicine')

    def __str__(self):
        return f"{self.medicine.name} at {self.pharmacy.name}"
