from import_export.admin import ImportExportModelAdmin
#from import_export.widgets import ForeignKeyWidget
#from import_export import fields, resources
from import_export import resources
#from .models import Transaction, Reconciliation
from django.contrib import admin
from auto.models import Groom, Froom, Sroom, Ground, First, Second, Gpayment, Fpayment, Spayment, Test, Test1, Test2, Final, Final1, Final2, Vacant, Vacant1, Vacant2


admin.site.register(Groom)
admin.site.register(Froom)
admin.site.register(Sroom)
admin.site.register(Ground)
admin.site.register(First)
admin.site.register(Second)
#admin.site.register(Gpayment)
admin.site.register(Fpayment)
admin.site.register(Spayment)

class GpaymentResource(resources.ModelResource):
	class Meta:
		model = Gpayment
       # import_id_fields = ('Transaction_id',)
	fields = ('id', 'owner', 'status', 'amount', 'pending', 'balance')
	list_filter = ('owner')

class GpaymentAdmin(ImportExportModelAdmin):
    resource_class = GpaymentResource

admin.site.register(Gpayment, GpaymentAdmin)

class TestResource(resources.ModelResource):
	class Meta:
		model = Test
       # import_id_fields = ('Transaction_id',)
	fields = ('id', 'name', 'room')
	list_filter = ('room')

class TestAdmin(ImportExportModelAdmin):
    resource_class = TestResource

admin.site.register(Test, TestAdmin)

class Test1Resource(resources.ModelResource):
	class Meta:
		model = Test1
       # import_id_fields = ('Transaction_id',)
	fields = ('id','name', 'room')
	list_filter = ('room')

class Test1Admin(ImportExportModelAdmin):
    resource_class = Test1Resource

admin.site.register(Test1, Test1Admin)

class Test2Resource(resources.ModelResource):
	class Meta:
		model = Test2
       # import_id_fields = ('Transaction_id',)
	fields = ('id', 'name', 'room')
	list_filter = ('room')

class Test2Admin(ImportExportModelAdmin):
    resource_class = Test2Resource

admin.site.register(Test2, Test2Admin)

class FinalResource(resources.ModelResource):
	class Meta:
		model = Final
       # import_id_fields = ('Transaction_id',)
	fields = ('id', 'name', 'room', 'status')
	list_filter = ('room')

class FinalAdmin(ImportExportModelAdmin):
    resource_class = FinalResource

admin.site.register(Final, FinalAdmin)

class Final1Resource(resources.ModelResource):
	class Meta:
		model = Final1
       # import_id_fields = ('Transaction_id',)
	fields = ('id', 'name', 'room', 'status')
	list_filter = ('room')

class Final1Admin(ImportExportModelAdmin):
    resource_class = Final1Resource

admin.site.register(Final1, Final1Admin)

class Final2Resource(resources.ModelResource):
	class Meta:
		model = Final2
       # import_id_fields = ('Transaction_id',)
	fields = ('id', 'name', 'room', 'status')
	list_filter = ('room')

class Final2Admin(ImportExportModelAdmin):
    resource_class = Final2Resource

admin.site.register(Final2, Final2Admin)

class VacantResource(resources.ModelResource):
	class Meta:
		model = Vacant
       # import_id_fields = ('Transaction_id',)
	fields = ('id', 'name', 'room', 'status')
	list_filter = ('room')

class VacantAdmin(ImportExportModelAdmin):
    resource_class = VacantResource

admin.site.register(Vacant, VacantAdmin)

class Vacant1Resource(resources.ModelResource):
	class Meta:
		model = Vacant1
       # import_id_fields = ('Transaction_id',)
	fields = ('id', 'name', 'room')
	list_filter = ('room')

class Vacant1Admin(ImportExportModelAdmin):
    resource_class = Vacant1Resource

admin.site.register(Vacant1, Vacant1Admin)

class Vacant2Resource(resources.ModelResource):
	class Meta:
		model = Vacant2
       # import_id_fields = ('Transaction_id',)
	fields = ('id', 'name', 'room')
	list_filter = ('room')

class Vacant2Admin(ImportExportModelAdmin):
    resource_class = Vacant2Resource

admin.site.register(Vacant2, Vacant2Admin)