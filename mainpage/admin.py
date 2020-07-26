from django.contrib import admin
from .models import Posting

class PostingAdmin(admin.ModelAdmin):
    readonly_fields = ('PostingID',)

admin.site.register(Posting, PostingAdmin)
