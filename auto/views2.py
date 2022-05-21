from typing import ValuesView
from django.db import models
from django.db.models.expressions import F
from django.db.models.lookups import StartsWith
from model_utils import Choices
from django.db import models
from django_pandas.managers import DataFrameManager
from datetime import datetime
from dateutil import rrule
from datetime import date
from django.db.models.functions import ExtractYear, ExtractMonth
from django.utils.functional import cached_property
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
			 return "{} - {} - {}".format(self.owner, self.room, self.status)


class Gpayment(models.Model):
	state= Choices(
		(0, 'paid', 'paid'),
		(1, 'unpaid', 'unpaid'),)
	stall = models.ForeignKey(Ground, on_delete=models.CASCADE, max_length=3)
	status = models.IntegerField(default=state.unpaid, choices=state)
	amount = models.IntegerField()
	month = models.DateTimeField(auto_now=True) #Month Paid For
	received_by = models.CharField(max_length=50)
	date_paid = models.DateField(auto_now_add=True)

	@cached_property 
	def amount(self):
		return 3000


class Fpayment(models.Model):
	state= Choices(
		(0, 'paid', 'paid'),
		(1, 'unpaid', 'unpaid'),)
	stall = models.ForeignKey(First, on_delete=models.CASCADE, max_length=3)
	status = models.IntegerField(default=state.unpaid, choices=state)
	amount = models.IntegerField()
	month = date = models.DateTimeField(auto_now=True) #Month Paid For
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
	month = date = models.DateTimeField(auto_now=True) #Month Paid For
	received_by = models.CharField(max_length=50)
	date_paid = models.DateField(auto_now_add=True)

	@cached_property 
	def amount(self):
		return 3000





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

