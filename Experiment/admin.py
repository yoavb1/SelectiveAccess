from django.contrib import admin
from .models import *
# Register your models here.

class ParticipantAdmin(admin.ModelAdmin):
    fieldsets = [
        ("ID", {"fields": ["id"]}),
        ("condition", { "fields": ["condition"]}),
        ("aid", {"fields": ["aid"]}),
        ("start_time", {"fields": ["start_time"]}),
        ("end_time", {"fields": ["end_time"]}),
        ("total_time", {"fields": ["total_time"]})
    ]

    fieldsets = [
        ("ID", {"fields": ["id"]}),
        ("condition", { "fields": ["condition"]}),
        ("aid", {"fields": ["aid"]}),
        ("start_time", {"fields": ["start_time"]}),
        ("end_time", {"fields": ["end_time"]}),
        ("total_time", {"fields": ["total_time"]})
    ]

class EventsAdmin(admin.ModelAdmin):
    fieldsets = [
        ("id", { "fields": ["user_id"]}),
        ("block", {"fields": ["block"]}),
        ("trial", {"fields": ["trial"]}),
        ("classification", {"fields": ["classification"]}),
        ("pd", {"fields": ["pd"]}),
        ("time", {"fields": ["time"]})
    ]

class NasaAdmin(admin.ModelAdmin):
    fieldsets = [
        ("user_id", { "fields": ["user_id"]}),
        ("system", {"fields": ["system"]}),
        ("mental_demand", {"fields": ["mental_demand"]}),
        ("physical_demand", {"fields": ["physical_demand"]}),
        ("performance", {"fields": ["performance"]}),
        ("effort", {"fields": ["effort"]}),
        ("frustration", {"fields": ["frustration"]}),
    ]
admin.site.register(Participant)
admin.site.register(Events)
admin.site.register(Nasa)


