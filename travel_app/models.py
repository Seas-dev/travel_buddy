from django.db import models
import bcrypt
import datetime

# Create Validators Here
class UserValidator(models.Manager):
	def valid_reg(self,postData):
		errors = {}
		# at least 3 characters for the name and username
		if len(postData['name']) < 3:
			errors['name_len'] = "Your name needs to be at least 3 characters"

		if len(postData['username']) < 3:
			errors['username_len'] = "Your username needs to be at least 3 characters"

		# make sure username is unique
		if len(User.objects.filter(username=postData['username'])) > 0:
			errors['unique_username'] = "Someone else has that username"

		# password should be at least 8 characters
		if len(postData['password']) < 8:
			errors['pw_length'] = "Your password is too short, make it at least 8 characters"

		# password should match one submitted
		if postData['password'] != postData['pw_confirm']:
			errors['pw_not_same'] = "Your confirmation password and password don't match"

		return errors

	def valid_log(self, postData):
		errors = {}
		# make sure the username is in the database
		user = User.objects.filter(username=postData['username'])
		if len(user) != 1:
			errors['no_user'] = "There is no user with that username in the database. Would you like to make an account?"
			return errors
			
		# make sure the password matches the user
		if not bcrypt.checkpw(postData['password'].encode(), user[0].password.encode()):
			errors['invalid_pw'] = "The password entered does not match the account"
		return errors

class TripValidator(models.Manager):
	def valid_trip(self, postData):
		errors = {}
		# no empty entries
		if len(postData['destination']) == 0:
			errors['empty_place'] = "You must enter a destination"

		if len(postData['description']) == 0:
			errors['empty_descrip'] = "You must enter a description"

		if len(postData['travel_date_from']) == 0:
			errors['empty_from'] = "You must enter a date to start the trip"
			return errors

		if len(postData['travel_date_to']) == 0:
			errors['empty_to'] = "You must enter a date to end the trip"
			return errors
		# travel dates should be future-dated
		now = datetime.date.today()
		date_from = datetime.datetime.strptime(postData['travel_date_from'], '%Y-%m-%d').date()
		date_to = datetime.datetime.strptime(postData['travel_date_to'], '%Y-%m-%d').date()
		if now >= date_from:
			errors['future_trip'] = "Your trip must start at least from tomorrow"

		# 'TravelDate To' should not be before the 'travel date from'
		if date_to < date_from:
			errors['past_return'] = "Your trip must end on or after you plan to leave"
		return errors

# Create your models here.
class User(models.Model):
	name = models.CharField(max_length=255)
	username = models.CharField(max_length=255)
	password = models.CharField(max_length=255)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)
	objects = UserValidator()

class Trip(models.Model):
	users = models.ManyToManyField(User, related_name="trips")
	creator = models.ForeignKey(User, related_name='trip_creator', on_delete=models.CASCADE)
	destination = models.CharField(max_length=255)
	description = models.CharField(max_length=255)
	travel_date_from = models.DateField()
	travel_date_to = models.DateField()
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)
	objects = TripValidator()


