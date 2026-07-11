from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from core.models import Event, Service, GalleryPhoto, Inquiry, SiteSetting
from decimal import Decimal
import datetime

User = get_user_model()

class Command(BaseCommand):
    help = 'Seed the database with demo data'

    def add_arguments(self, parser):
        parser.add_argument('--flush', action='store_true', help='Clear existing data first')

    def handle(self, *args, **options):
        if options['flush']:
            Event.objects.all().delete()
            Service.objects.all().delete()
            GalleryPhoto.objects.all().delete()
            Inquiry.objects.all().delete()
            SiteSetting.objects.all().delete()
            self.stdout.write('Flushed existing data.')

        # Admin
        if not User.objects.filter(email='admin@likilatours.co.ls').exists():
            User.objects.create_superuser(
                username='admin', email='admin@likilatours.co.ls',
                password='Likila@Admin2025', first_name='Likila', last_name='Admin',
            )
            self.stdout.write(self.style.SUCCESS('Admin created: admin@likilatours.co.ls / Likila@Admin2025'))

        # Events
        if not Event.objects.exists():
            Event.objects.bulk_create([
                Event(name='Afriski Winter Festival', date=datetime.date(2025,8,30),
                      price=Decimal('1800'), deposit=Decimal('200'), departure='Botha-Buthe',
                      included='Festival Ticket,Transport,Water per person,Free WiFi en route',
                      excluded='Activities,Beverages',
                      description='Annual winter festival at Afriski Mountain Resort.',
                      status='upcoming',
                      image_url='https://images.unsplash.com/photo-1578662996442-48f60103fc96?w=800&q=75'),
                Event(name='Mohale Dam Scenic Tour', date=datetime.date(2025,7,15),
                      price=Decimal('950'), deposit=Decimal('150'), departure='Maseru',
                      included='Transport,Licensed Guide,Packed Lunch',
                      excluded='Personal expenses,Souvenirs',
                      description='Breathtaking views of Mohale Dam and surrounding highland scenery.',
                      status='upcoming',
                      image_url='https://images.unsplash.com/photo-1547471080-7cc2caa01a7e?w=800&q=75'),
            ])
            self.stdout.write(self.style.SUCCESS('Events seeded'))

        # Services
        if not Service.objects.exists():
            svcs = [
                ('Mountain Tours','Guided excursions through highland terrain, including Maletsunyane Falls and Sani Pass.','mountain',1),
                ('Cultural Village Tours','Immersive stays in traditional Basotho villages — food, music, and old customs.','culture',2),
                ('Pony Trekking','Traverse scenic highland routes on the legendary Basotho pony.','horse',3),
                ('Transport & Transfers','Reliable transfers across Lesotho and to South Africa with WiFi en route.','transport',4),
                ('Event Packages','Festival passes, group bookings, all-inclusive packages.','event',5),
                ('Custom Itineraries','Bespoke travel plans for any group size or interest.','custom',6),
            ]
            Service.objects.bulk_create([Service(name=n,description=d,icon=i,sort_order=o) for n,d,i,o in svcs])
            self.stdout.write(self.style.SUCCESS('Services seeded'))

        # Gallery
        if not GalleryPhoto.objects.exists():
            photos = [
                ('https://images.unsplash.com/photo-1547471080-7cc2caa01a7e?w=600&q=75','Mohale Dam',2023,'Scenic Tour'),
                ('https://images.unsplash.com/photo-1529156069898-49953e39b3ac?w=600&q=75','Mountain Hiking',2023,'Mountain Tour'),
                ('https://images.unsplash.com/photo-1469854523086-cc02fe5d8800?w=600&q=75','Group Travel',2023,'Group Tour'),
                ('https://images.unsplash.com/photo-1541417904950-b855846fe074?w=600&q=75','Lesotho Highlands',2023,'Scenic Tour'),
                ('https://images.unsplash.com/photo-1506905925346-21bda4d32df4?w=600&q=75','Sani Pass',2023,'Mountain Tour'),
            ]
            GalleryPhoto.objects.bulk_create([GalleryPhoto(url=u,caption=c,year=y,category=cat,sort_order=i) for i,(u,c,y,cat) in enumerate(photos)])
            self.stdout.write(self.style.SUCCESS('Gallery seeded'))

        # Inquiries
        if not Inquiry.objects.exists():
            Inquiry.objects.bulk_create([
                Inquiry(first_name='Thabo',last_name='Mokhesi',email='thabo@email.com',phone='+266 5000 0001',service='Mountain Tour',message='Book for 8 people in September.'),
                Inquiry(first_name='Sarah',last_name='Dlamini',email='sarah@email.com',service='Afriski Winter Festival',message='More info on the Afriski package and deposit payment.'),
                Inquiry(first_name='David',last_name='Khumalo',email='david@mail.co.za',service='Custom Itinerary',message='Company retreat for 20 people. Can you quote?'),
                Inquiry(first_name='Palesa',last_name='Ntsekhe',email='palesa@gmail.com',service='Pony Trekking',message='Available July? Family of 5 with 2 children.',is_read=True),
            ])
            self.stdout.write(self.style.SUCCESS('Inquiries seeded'))

        # Settings
        defaults = {'business_name':'Likila Travel & Tours','tagline':'Your Destination is Our Concern',
                    'location':'Botha-Buthe, Lesotho','email':'info@likilatours.co.ls','whatsapp':'',
                    'facebook':'','stat_travellers':'2000+','stat_destinations':'50+','stat_countries':'5+','stat_years':'9+'}
        for k,v in defaults.items():
            SiteSetting.objects.get_or_create(key=k, defaults={'value':v})
        self.stdout.write(self.style.SUCCESS('Settings seeded'))
        self.stdout.write(self.style.SUCCESS('\nDone! Run: python manage.py runserver'))
