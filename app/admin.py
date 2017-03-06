from django.contrib import admin
from app.models import *

# Register your models here.

admin.site.register(Book)
admin.site.register(Author)
admin.site.register(Tag)
admin.site.register(Comment)
admin.site.register(VerificationToken)
admin.site.register(Contact)