from django.contrib import admin
from .models import *
from django.http import HttpResponseRedirect
from django.urls import reverse
# Register your models here.
class StudentAdmin(admin.ModelAdmin):
    list_display = ('name', 'regNo', 'section','attnd','AcadamicYear',)
    list_filter = ('section','AcadamicYear','Year','Sem')
    list_editable = ('attnd',)
    list_per_page = 80
    search_fields = ('name','regNo')
class CurrentStudentAdmin(admin.ModelAdmin):
    list_display = ('name', 'regNo','user', 'section', 'attnd', 'Year','Sem')
    list_filter = ('section', 'Year', 'Sem')
    list_editable = ('attnd',)
    search_fields = ('name', 'regNo')
    ordering = ('name', 'regNo')
    list_per_page = 10
    readonly_fields = ['regNo','joinedYear']
    def get_queryset(self, request):
        queryset = super(CurrentStudentAdmin,self).get_queryset(request)
        queryset = queryset.order_by('name','regNo')
        try:
            if request.user.teachers:
                print("he us staff")
                return queryset.filter(teacher=request.user.teachers)
        except:
            if request.user.is_superuser:
                print("super user")
                return queryset

    # def save_model(self, request, obj, form, change):
    #     obj.user = request.user
    #     super(CurrentStudentAdmin, self).save_model(request, obj, form, change)
    #
    #
    # def change_view(self, request, object_id, form_url='', extra_context=None):
    #     if not self.get_queryset(request).filter(id=object_id).exists():
    #         return HttpResponseRedirect(reverse('admin:myapp_mymodel_changelist'))
    #     return super(CurrentStudentAdmin, self).change_view(request, object_id, form_url, extra_context)
    #
    # def history_view(self, request, object_id, extra_context=None):
    #     if not self.queryset_set(request).filter(id=object_id).exists():
    #         return HttpResponseRedirect(reverse('admin:myapp_mymodel_changelist'))
    #
    #     return super(CurrentStudentAdmin, self).history_view(request, object_id, extra_context)

admin.site.register(Student,StudentAdmin)
admin.site.register(CurrentStudent,CurrentStudentAdmin)
admin.site.register(Teachers)


