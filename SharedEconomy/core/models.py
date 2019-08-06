from django.db import models
from django.contrib.auth.models import User
from datetime import date
from django_countries.fields import CountryField

class Product(models.Model):
	name = models.CharField(max_length=1024)
	desc = models.CharField(max_length=1024)
	price = models.DecimalField(max_digits=9, decimal_places=2)
	imageUrl = models.CharField(max_length=1024, null=True)
	location = CountryField()

	def __str__(self):
		return f'{self.name}-({self.price}) Product'



class Buyer(models.Model):
	user = models.OneToOneField(User, on_delete= models.CASCADE, related_name='buyerUser')
	itemsInCart = models.ManyToManyField(Product, blank=True, related_name='itemsInCart')
	location = CountryField()

	def __str__(self):
		return f'{self.user.username} Buyer'



class Traveller(models.Model):
	origin_choices = (
			('San Fransisco','San Fransisco'),
			('London','London'),
			('New York','New York'),
			('Dubai','Dubai'),
			('Los Angeles','Los Angeles'),
			('Denver','Denver'),
			('Berlin','Berlin'),
			('Singapore','Singapore'),
			('Paris','Paris'),
			('Beijing','Beijing')
		)

	destination_choices = (
			('Kolkata','Kolkata'),
			('New Delhi','New Delhi'),
			('Bangalore','Bangalore'),
			('Mumbai','Mumbai'),
			('Guwahati','Guwahati'),
			('Ahmedabad','Ahmedabad')
		)
	user = models.OneToOneField(User, on_delete= models.CASCADE,  related_name='travellerUser')
	origin = CountryField()
	# origin = models.CharField(max_length=1024,choices=origin_choices)
	destination = CountryField()
	# destination = models.CharField(max_length=1024,choices=origin_choices)
	day = models.DateField(default= date.today)
	maxAlloc = models.IntegerField(default=3)
	itemsToBuy = models.ManyToManyField(Product, null=True)

	def __str__(self):
		return f'{self.user.username} Traveller'



class ProductBuyer(models.Model):
	product = models.ForeignKey(Product, on_delete= models.CASCADE)
	buyer = models.ForeignKey(Buyer, on_delete= models.CASCADE)
	traveller = models.ForeignKey(Traveller, null=True, on_delete= models.SET_NULL)
	timeOfOrder = models.DateTimeField(auto_now_add=True)
	quantity = models.IntegerField(default=1)
	

	def __str__(self):
		return f'{self.product.name} - {self.buyer.user.username}({self.timeOfOrder})'



