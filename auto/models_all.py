from datetime import datetime
from typing import ValuesView
from django.contrib.auth.backends import UserModel
from django.db import models
from django.db.models.aggregates import Sum
from django.db.models.expressions import F
from django.db.models.fields import DateField
from django.db.models.lookups import StartsWith
from model_utils import Choices
from django.db import models
from django_pandas.managers import DataFrameManager
from datetime import datetime
from dateutil import rrule
from datetime import date
from django.db.models.functions import ExtractYear, ExtractMonth
from django.utils.functional import cached_property
from django.contrib.auth.models import User

#from DateTime import DateTime, Date
# Create your models here.


class Groom(models.Model):
	name = models.CharField(max_length=50, unique=True, default='')
	def __str__ (self):
        	return self.name

class Froom(models.Model):
	name = models.CharField(max_length=50, unique=True)
	def __str__ (self):
        	return self.name

class Sroom(models.Model):
	name = models.CharField(max_length=50, unique=True)
	def __str__ (self):
        	return self.name


class Ground(models.Model):
	state= Choices(
	(0, 'vacant', 'vacant'),
	(1, 'booked', 'booked'),
	)
	owner = models.CharField(max_length=50, blank=True, null=True)
	room = models.OneToOneField(Groom, on_delete=models.CASCADE, max_length=3, unique=True)
	month = models.DateTimeField(auto_now=True)
	status = models.IntegerField(default=state.vacant, choices=state)
	check_in = models.DateTimeField(auto_now_add=True,  null=True, editable=True)
	#date_created = models.DateTimeField(auto_now_add=True)

	def __str__ (self):
        	 #return "%s" % self.room.name
			 return "{} - {}".format(self.owner, self.room)

class First(models.Model):
	state= Choices(
		(0, 'vacant', 'vacant'),
		(1, 'booked', 'booked'),)
	owner = models.CharField(max_length=50, blank=True, null=True)
	room = models.OneToOneField(Froom, on_delete=models.CASCADE, max_length=3, unique=True)
	status = models.IntegerField(default=state.vacant, choices=state)
	check_in = models.DateTimeField(auto_now_add=True,  null=True, editable=True)
	
	objects = DataFrameManager()
	
	def __str__ (self):
        	 #return "%s" % self.room.name
			 return "{} - {} - {}".format(self.owner, self.room, self.status)


class Second(models.Model):
	state= Choices(
		(0, 'vacant', 'vacant'),
		(1, 'booked', 'booked'),)
	owner = models.CharField(max_length=50, blank=True, null=True)
	room = models.OneToOneField(Sroom, on_delete=models.CASCADE, max_length=3, unique=True)
	status = models.IntegerField(default=state.vacant, choices=state)
	check_in = models.DateTimeField(auto_now_add=True,  null=True, editable=True)
	
	objects = DataFrameManager()
	
	def __str__ (self):
        	 #return "%s" % self.room.name
			 return "{} - {} - {} - {}".format(self.owner, self.room, self.status, self.check_in)

class Gpayment(models.Model):#receives payment by officer on the ground 
	state= Choices(
		(0, 'paid', 'paid'),
		(1, 'unpaid', 'unpaid'),)
	#paymode= Choices((0, 'cash', 'cash'),(1, 'mpesa', 'mpesa'),)
	
	stall = models.ForeignKey(Ground, on_delete=models.CASCADE, max_length=3)
	status = models.IntegerField(default=state.unpaid, choices=state)
	amount = models.IntegerField()
	month = models.DateTimeField() #last paid Month 
	pending = models.IntegerField(max_length=5)
	#mode = models.CharField(default=paymode.cash, choices=paymode, max_length=5)
	received_by = models.CharField(max_length=30)
	#balance = models.IntegerField()
	date_paid = models.DateTimeField(auto_now_add=True)

	@cached_property 
	def amount(self):
		return 3000

	@cached_property 
	def pending(self):
		#gfloor = Gpayment.objects.filter(stall__check_in=Ground.check_in)
		#for i in gfloor:
		#gfloor = Gpayment.objects.all()

		#pending = self.date_paid.month - gfloor.month
		start1 = Ground.check_in
		fstart = datetime.strptime(start1, '%d %b %Y')
		start = fstart.replace(day=1)
		end1 = datetime.now()
		fend = datetime.strptime(end1, '%d %b %Y')
		end = fend.replace(day=1)
		#start = datetime.strptime(gfloor, "%d/%m/%Y")
		#end = datetime.strptime(self.month, "%d/%m/%Y")
		self.pending = (end.year - start.year)*12 + (end.month - start.month)
		pending = self.pending
		return float(pending)
		#return int(str(pending))
	
	def __str__ (self):
			 return "{} - {} - {}".format(self.stall.owner, self.status)

class Clearance(models.Model):
	gpayment = models.ForeignKey(Gpayment, on_delete=models.CASCADE, max_length=100)
	#amount = models.IntegerField()
	received_by = models.CharField(max_length=30)
	date_received = models.DateField(auto_now_add=True)

class Banked(models.Model):
	clearance = models.ForeignKey(Clearance, on_delete=models.CASCADE, max_length=100)
	banked_by = models.ForeignKey(User, on_delete=models.CASCADE, max_length=30)
	date_banked = models.DateField(auto_now_add=True)

#class tbl_payment(models.Model):
 #       class Status(models.TextChoices):
  #          paid = 'Paid', 'Paid'
   #         partial = 'Partial', 'Partial'
    #        unpaid = 'Unpaid', 'Unpaid'
            
     #   document_id                     = models.ForeignKey(tbl_invoice, on_delete=models.CASCADE)
      #  client_id                       = models.ForeignKey(tbl_customer, on_delete=models.CASCADE)
       # total_amount                    = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True)
        #paid_amount                     = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True)
        #balance                         = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True)
        #date                            = models.DateField(blank=True, null=True)
        #status                          = models.CharField(max_length=50, choices=Status.choices)
    
        #def save(self, *args, **kwargs):
         #   self.balance = self.total_amount - self.paid_amount
            
          #  if self.balance >= 0:
           #     self.status = Status.paid
            #elif self.paid_amount == 0:
             #   self.status = Status.unpaid
            #else:
             #   self.status = Status.partial
    
            #super(tbl_payment, self).save(*args, **kwargs)

class Fpayment(models.Model):
	state= Choices(
		(0, 'paid', 'paid'),
		(1, 'unpaid', 'unpaid'),)
	stall = models.ForeignKey(First, on_delete=models.CASCADE, max_length=3)
	status = models.IntegerField(default=state.unpaid, choices=state)
	amount = models.IntegerField()
	month = models.DateTimeField(auto_now=True) #Month Paid For
	received_by = models.CharField(max_length=50)
	date_paid = models.DateField(auto_now_add=True)

	@cached_property 
	def amount(self):
		return 3000

class Spayment(models.Model):
	state= Choices(
		(0, 'paid', 'paid'),
		(1, 'unpaid', 'unpaid'),)
	stall = models.ForeignKey(Second, on_delete=models.CASCADE, max_length=3)
	status = models.IntegerField(default=state.unpaid, choices=state)
	amount = models.IntegerField()
	month = models.DateTimeField(auto_now=True) #Month Paid For
	received_by = models.CharField(max_length=50)
	date_paid = models.DateField(auto_now_add=True)

	@cached_property 
	def amount(self):
		return 3000

class Test(models.Model):
	name = models.CharField(max_length=50, blank=True, null=True)
	room = models.CharField(max_length=50, blank=True, null=True)
	
	def __str__ (self):
        	 #return "%s" % self.room.name
			 return "{} - {}".format(self.name, self.room)

class Test1(models.Model):
	name = models.CharField(max_length=50, blank=True, null=True)
	room = models.CharField(max_length=50, blank=True, null=True)
	
	def __str__ (self):
        	 #return "%s" % self.room.name
			 return "{} - {}".format(self.name, self.room)


class Test2(models.Model):
	name = models.CharField(max_length=50, blank=True, null=True)
	room = models.CharField(max_length=50, blank=True, null=True)
	
	def __str__ (self):
        	 #return "%s" % self.room.name
			 return "{} - {}".format(self.name, self.room)

class Final(models.Model):
	name = models.CharField(max_length=50, blank=True, null=True)
	room = models.CharField(max_length=50, blank=True, null=True)
	status = models.CharField(max_length=50, blank=True, null=True)
	
	def __str__ (self):
			 return "{} - {} - {}".format(self.name, self.room, self.status)


class Final1(models.Model):
	name = models.CharField(max_length=50, blank=True, null=True)
	room = models.CharField(max_length=50, blank=True, null=True)
	status = models.CharField(max_length=50, blank=True, null=True)
	
	def __str__ (self):
			 return "{} - {} - {}".format(self.name, self.room, self.status)


class Final2(models.Model):
	name = models.CharField(max_length=50, blank=True, null=True)
	room = models.CharField(max_length=50, blank=True, null=True)
	status = models.CharField(max_length=50, blank=True, null=True)
	
	def __str__ (self):
			 return "{} - {} - {}".format(self.name, self.room, self.status)

class Vacant(models.Model):
	name = models.CharField(max_length=50, blank=True, null=True)
	room = models.CharField(max_length=50, blank=True, null=True)

	
	def __str__ (self):
			 return "{} - {}".format(self.name, self.room)
class Vacant1(models.Model):
	name = models.CharField(max_length=50, blank=True, null=True)
	room = models.CharField(max_length=50, blank=True, null=True)

	
	def __str__ (self):
			 return "{} - {}".format(self.name, self.room)

class Vacant2(models.Model):
	name = models.CharField(max_length=50, blank=True, null=True)
	room = models.CharField(max_length=50, blank=True, null=True)

	
	def __str__ (self):
			 return "{} - {}".format(self.name, self.room)
#.annotate(
 #   remaining_balance=ExpressionWrapper(F('months') * F('monthly_payment'), output_field=models.FloatField()))

#print(list(rrule.rrule(rrule.MONTHLY, dtstart=date(2013, 11, 1), until=date(2014, 2, 1))))
#def amount(self):
#		start = self.Stall.check_in
#		end = self.date_paid

#		return (end - start)
		#.strftime("%B")
		#return self.net_amount + (self.net_amount * vat_rate)

	#@property
	#def month(self):
		#self.stall.check_in = self.stall.check_in.strftime("%B")
	#	if self.stall.check_in:
	#		return self.stall.check_in.strftime("%B")
	#	return "No date entry"

	#@property
	#def period(self):
	#	p = self.month.count()
			#return self.stall.check_in.strftime("%B")
	#	return "p"

@cached_property 
	def month(self):
		self.month = self.date_paid
		start1 = self.stall.check_in
		if start == None:
			self.month = (start1.replace(day=1) + datetime.timedelta(days=32)).replace(day=1)
		else:
			self.month = (start.replace(day=1) + datetime.timedelta(days=32)).replace(day=1)

	
		return self.month
		##########################
@cached_property 
	def pending(self):
		start1 = self.stall.check_in
		start = start1.replace(day=1)
		#end1 = datetime.now()
		end1 = self.month
		#fend = datetime.strptime(str(end1), '%d %b %y')
		end = end1.replace(day=1)
		self.pending = (end.year - start.year)*12 + (end.month - start.month)
		return self.pending
		#######################

#@cached_property 
	#def pending(self):
	#	gfloor = Gpayment.objects.filter(stall__check_in=Ground.check_in)
		#for i in gfloor:
	#	gfloor = Gpayment.objects.all()
	#	pending = self.date_paid.month - gfloor.month
	#	start = datetime.strptime(gfloor, "%d/%m/%Y")
	#	end = datetime.strptime(self.month, "%d/%m/%Y")
	#	self.pending = (end.year - start.year)*12 + (end.month - start.month)
	#	pending = self.pending
	#	return int(str(pending))


	#############################
	@cached_property 
	def month(self):
		month = Gpayment.objects.order_by( '-date_paid')
		if month.date_paid != None:
			self.month = (self.date_paid.replace(day=1)).month+1
			#self.month = next1.month + 1
			return self.month
		else:
			self.month = (self.stall.check_in.replace(day=1)).month+1
			#self.month = next1.month + 1
			return self.month
		#start = start1.replace(day=1)

		#month = Gpayment.objects.order_by('-date_paid')
		#date = self.stall.check_in.month 
		#super(Gpayment, self).save(*args, **kwargs) 
		#self.month = None
		
		#start = self.stall.check_in.month + 1
		#self.month = (start1.replace(day=1) + datetime.timedelta(days=32)).replace(day=1)
		##################################
		@cached_property 
	def month(self):
		from datetime import date, timedelta
		from calendar import monthrange

		days_in_month = lambda dt: monthrange(dt.year, dt.month)[1]
		month = Gpayment.objects.order_by( '-date_paid')
		if month.date_paid.month - month.stall.check_in.month <= 0:
			self.month = self.stall.check_in.replace(day=1) + timedelta(days_in_month(self.stall.check_in))
			#self.month = next1.month + 1
			#return self.month
		else:
			self.month = self.date_paid.replace(day=1) + timedelta(days_in_month(self.date_paid))

		#self.month = today.replace(day=1) + timedelta(days_in_month(today))
		return self.month
		
##############################################
	@cached_property 
	def month(self):
		from datetime import date, timedelta
		from calendar import monthrange

		days_in_month = lambda dt: monthrange(dt.year, dt.month)[1]
		#month = Gpayment.objects.order_by( '-date_paid')
		if self.date_paid.month - self.stall.check_in.month == 0:
			self.month = self.stall.check_in.replace(day=1) + timedelta(days_in_month(self.stall.check_in))
			#self.month = next1.month + 1
			#return self.month
		else:
			self.month = self.date_paid.replace(day=1) + timedelta(days_in_month(self.date_paid))

		#self.month = today.replace(day=1) + timedelta(days_in_month(today))
		return self.month
	
	###############################3