from django.core.management.base import BaseCommand
from pharmacy.models import Pharmacy, Medicine, Stock

class Command(BaseCommand):
    help = 'Seed data for the pharmacy app'

    def handle(self, *args, **kwargs):
        # Create Medicines
        paracetamol, _ = Medicine.objects.get_or_create(name='Paracetamol', description='Pain reliever')
        amoxicillin, _ = Medicine.objects.get_or_create(name='Amoxicillin', description='Antibiotic')
        cetirizine, _ = Medicine.objects.get_or_create(name='Cetirizine', description='Antihistamine')
        
        # Create Pharmacies
        pharmacy1, _ = Pharmacy.objects.get_or_create(
            name='Nabha Central Pharmacy', 
            address='Main Bazaar, Nabha',
            area_village='Nabha',
            pincode='147201',
            phone_number='01765-220001'
        )
        
        pharmacy2, _ = Pharmacy.objects.get_or_create(
            name='Village Health Meds', 
            address='Bus Stand, Rohti Chhapra',
            area_village='Rohti Chhapra',
            pincode='147202',
            phone_number='01765-220002'
        )
        
        # Add Stock
        Stock.objects.get_or_create(pharmacy=pharmacy1, medicine=paracetamol, defaults={'quantity': 100, 'is_available': True})
        Stock.objects.get_or_create(pharmacy=pharmacy1, medicine=cetirizine, defaults={'quantity': 50, 'is_available': True})
        Stock.objects.get_or_create(pharmacy=pharmacy2, medicine=paracetamol, defaults={'quantity': 30, 'is_available': True})
        Stock.objects.get_or_create(pharmacy=pharmacy2, medicine=amoxicillin, defaults={'quantity': 20, 'is_available': True})
        
        self.stdout.write(self.style.SUCCESS('Successfully seeded pharmacy data!'))
