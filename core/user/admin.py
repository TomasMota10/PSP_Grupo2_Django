from django.contrib import admin
from core.category.models import Category
from core.project.models import Participa, Project
from core.user.models import User

admin.site.register(User)
#admin.site.register(Client)
admin.site.register(Project)
admin.site.register(Participa)
admin.site.register(Category)
