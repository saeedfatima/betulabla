from django.contrib import admin
from .models import LocalGovernment, Borehole, Orphan, Report, StaffProfile

class boreholeModel(admin.ModelAdmin):
  list_display = ['borehole_id','local_government','location','contact_number', 'installed_date','status']
  search_fields = ['local_government']
  list_filter = ["local_government"]

class orphanModel(admin.ModelAdmin):
  list_display = ['full_name','Dob','local_government', 'contact', 'address', 'next_of_kin','registered_date']
  search_fields = [ 'local_government','registered_date']
  list_filter = ["local_government"]

admin.site.register(LocalGovernment)
admin.site.register(Borehole, boreholeModel)
admin.site.register(Orphan, orphanModel)
admin.site.register(Report)
admin.site.register(StaffProfile)