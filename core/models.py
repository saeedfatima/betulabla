from django.db import models
from django.contrib.auth.models import  User
# Each borehole might be linked to a local government area
class LocalGovernment(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Borehole(models.Model):
    borehole_id = models.CharField(max_length=30, null=True, unique=True)
    local_government = models.ForeignKey(LocalGovernment, on_delete=models.CASCADE, related_name='boreholes')
    Address = models.CharField(max_length=255)
    contact_number = models.CharField(max_length=20, null=True)
    installed_date = models.DateField(blank=True)
    
    STATUS_CHOICE = (
        ('ACTIVE','Active'),
        ('IN-PROGRESS','In-progress'),
        ('IN-ACTIVE','In-active')
    )
    status = models.CharField(max_length=50, choices=STATUS_CHOICE, default='Active')  # active/inactive/maintenance
    def __str__(self):
        return f"{self.borehole_id} - {self.Address}"

class Orphan(models.Model):
    full_name = models.CharField(max_length=50)
    Dob = models.DateField(null=True)
    address = models.CharField(max_length=50)
    local_government = models.ForeignKey(LocalGovernment, on_delete=models.SET_NULL, null=True, blank=True, related_name='orphans')
    contact = models.CharField(max_length=20, null=True)
    next_of_kin = models.CharField(max_length=20, null=True)
    registered_date = models.DateField(auto_now_add=True)
    image = models.ImageField(upload_to='reports/', null=True, blank=True)
    

    def __str__(self):
        return f"{self.full_name} {self.local_government}"

# Report model for special projects like Ramadan and Eid feeding projects
class Report(models.Model):
    title = models.CharField(max_length=150)
    description = models.TextField()
    # You can allow multiple images or videos through a related model or a FileField (for simplicity, one image here)
    image = models.ImageField(upload_to='reports/', null=True, blank=True)
    video_url = models.URLField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

# A simple extension for staff - assuming coordinators are staff users
class StaffProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='staffprofile')
    role = models.CharField(max_length=50, choices=(('coordinator', 'Coordinator'), ('head', 'Head')), default='coordinator')
    phone = models.CharField(max_length=20, null=True, blank=True)
    country = models.CharField(max_length=50, default='Nigeria')
    
    # additional details can be added
    def __str__(self):
        return self.user.username