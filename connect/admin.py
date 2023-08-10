from django.contrib import admin
from .models import Request, Connection
from .forms import RequestForm, ConnectionForm

# Register your models here.
class RequestAdmin(admin.ModelAdmin):
    form = RequestForm

admin.site.register(Request, RequestAdmin)

class ConnectionAdmin(admin.ModelAdmin):
    form = ConnectionForm


admin.site.register(Connection, ConnectionAdmin)