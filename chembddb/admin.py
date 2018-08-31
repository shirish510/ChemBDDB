from django.contrib import admin


# Register your models here.
from .models import MolGraph, MolProp, Publication, Data, Method
admin.site.register(MolGraph)
admin.site.register(MolProp)
admin.site.register(Publication)
admin.site.register(Data)
admin.site.register(Method)
