from django.contrib import admin

from .models import Application, Company, Project, Role, Talent

admin.site.register(Talent)
admin.site.register(Company)
admin.site.register(Project)
admin.site.register(Role)
admin.site.register(Application)
