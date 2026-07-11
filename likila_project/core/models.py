from django.db import models

class Event(models.Model):
    STATUS_CHOICES = [
        ('upcoming', 'Upcoming'),
        ('active', 'Active'),
        ('draft', 'Draft'),
        ('expired', 'Expired'),
    ]
    name        = models.CharField(max_length=200)
    date        = models.DateField()
    price       = models.DecimalField(max_digits=10, decimal_places=2)
    deposit     = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    departure   = models.CharField(max_length=200, blank=True)
    included    = models.TextField(blank=True, help_text='Comma-separated items')
    excluded    = models.TextField(blank=True, help_text='Comma-separated items')
    description = models.TextField(blank=True)
    status      = models.CharField(max_length=20, choices=STATUS_CHOICES, default='upcoming')
    image       = models.ImageField(upload_to='events/', blank=True, null=True)
    image_url   = models.URLField(blank=True, help_text='External image URL (overrides uploaded image)')
    created_at  = models.DateTimeField(auto_now_add=True)
    updated_at  = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['date']

    def __str__(self):
        return self.name

    @property
    def display_image(self):
        if self.image_url:
            return self.image_url
        if self.image:
            return self.image.url
        return None


class Service(models.Model):
    STATUS_CHOICES = [('active', 'Active'), ('draft', 'Draft')]
    ICON_CHOICES = [
        ('mountain', 'Mountain / Hiking'),
        ('culture',  'Cultural / Village'),
        ('horse',    'Pony Trekking'),
        ('transport','Transport'),
        ('event',    'Events / Festivals'),
        ('custom',   'Custom Itineraries'),
    ]
    name        = models.CharField(max_length=200)
    description = models.TextField()
    icon        = models.CharField(max_length=30, choices=ICON_CHOICES, default='mountain')
    price       = models.CharField(max_length=50, blank=True, help_text='e.g. 500 or leave blank')
    status      = models.CharField(max_length=20, choices=STATUS_CHOICES, default='active')
    sort_order  = models.PositiveIntegerField(default=0)
    created_at  = models.DateTimeField(auto_now_add=True)
    updated_at  = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['sort_order', 'id']

    def __str__(self):
        return self.name


class GalleryPhoto(models.Model):
    photo       = models.ImageField(upload_to='gallery/', blank=True, null=True)
    url         = models.URLField(blank=True, help_text='External URL (used if no file uploaded)')
    caption     = models.CharField(max_length=200)
    year        = models.PositiveIntegerField(null=True, blank=True)
    category    = models.CharField(max_length=100, blank=True)
    sort_order  = models.PositiveIntegerField(default=0)
    created_at  = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['sort_order', '-id']

    def __str__(self):
        return self.caption

    @property
    def display_url(self):
        if self.photo:
            return self.photo.url
        return self.url


class Inquiry(models.Model):
    first_name  = models.CharField(max_length=100)
    last_name   = models.CharField(max_length=100, blank=True)
    email       = models.EmailField(blank=True)
    phone       = models.CharField(max_length=30, blank=True)
    service     = models.CharField(max_length=200, blank=True)
    message     = models.TextField()
    is_read     = models.BooleanField(default=False)
    created_at  = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.first_name} {self.last_name} — {self.service}'


class SiteSetting(models.Model):
    key         = models.CharField(max_length=100, unique=True)
    value       = models.TextField(blank=True)
    updated_at  = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.key
