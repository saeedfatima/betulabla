from django.contrib import admin
from .models import LocalGovernment, Borehole, Orphan, Report, StaffProfile

class boreholeModel(admin.ModelAdmin):
  list_display = ['borehole_id','local_government','Address','contact_number', 'installed_date','status']
  search_fields = ['local_governments','status']

class orphanModel(admin.ModelAdmin):
  list_display = ['full_name','Dob','local_government', 'contact', 'address', 'next_of_kin','registered_date']
  search_fields = [ 'local_governments','registered_date']

admin.site.register(LocalGovernment)
admin.site.register(Borehole, boreholeModel)
admin.site.register(Orphan, orphanModel)
admin.site.register(Report)
admin.site.register(StaffProfile)