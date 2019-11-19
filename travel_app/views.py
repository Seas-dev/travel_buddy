from django.shortcuts import render, redirect
from travel_app.models import User, Trip
from django.contrib import messages
import bcrypt

# Create your views here.
# ====================
# Renders
# ====================
def index(request):
	request.session['user'] = ""
	return render(request, 'index.html')

def dashboard(request):
	# if the user didn't log in, they should be redirected to the login page
	request.session.setdefault('user', "")
	if request.session['user'] == "":
		return redirect('/')
	user = User.objects.get(id=request.session['user'])
	user_trips = user.trips.all().order_by('travel_date_from')
	other_trips = Trip.objects.all().exclude(users=user).order_by('travel_date_from')
	context = {
		'user': user,
		'user_trips': user_trips,
		'trips': other_trips,
	}
	print('user', user)
	return render(request, 'travels.html', context)

def addTrip(request):
	# if the user didn't log in, they should be redirected to the login page
	request.session.setdefault('user', "")
	if request.session['user'] == "":
		return redirect('/')

	return render(request, 'add_trip.html')

def destination(request, id):
	# if the user didn't log in, they should be redirected to the login page
	request.session.setdefault('user', "")
	if request.session['user'] == "":
		return redirect('/')
		
	trip = Trip.objects.get(id=id)
	# all_participants = trip.users.all()
	# first = all_participants.first()
	other_users = trip.users.all().exclude(id=trip.creator.id)
	context = {
		'trip': trip,
		'others': other_users,
	}
	return render(request, 'destination.html', context)


# ====================
# Redirects
# ====================
def mainPage(request):
	return redirect('/main')

def logout(request):
	# clear all session variables here
	del request.session['user']
	return redirect('/main')

def validReg(request):
	errors = User.objects.valid_reg(request.POST)
	# if good create user, go to dashboard
	if len(errors) == 0:
		# securing the password to go into the database
		hash_pw = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt())
		# creating the user
		user = User.objects.create(name=request.POST['name'],
								username=request.POST['username'],
								password=hash_pw.decode(),)
		# make sure to redirect them to the landing page when they successfully log in
		request.session['user'] = user.id
		return redirect('/dashboard')
	else:
		for value in errors.values():
			messages.error(request,value)
		return redirect('/main')

def validLog(request):
	errors = User.objects.valid_log(request.POST)
	# if good log in user, go to dashboard
	if len(errors) == 0:
		# change redirect and add username or user id to session
		user = User.objects.get(username=request.POST['username'])
		request.session['user'] = user.id
		return redirect('/dashboard')

	for value in errors.values():
		messages.error(request,value)
	return redirect('/main')

def validTrip(request):
	print('successful redirect')
	errors = Trip.objects.valid_trip(request.POST)
	creator = User.objects.get(id=request.session['user'])
	if len(errors) == 0:
		# create trip
		trip = Trip.objects.create(destination=request.POST['destination'],
							description=request.POST['description'],
							travel_date_from=request.POST['travel_date_from'],
							travel_date_to=request.POST['travel_date_to'],
							creator=creator)
		trip.users.add(User.objects.get(id=creator.id))

		return redirect('/dashboard')

	for value in errors.values():
		messages.error(request,value)
	return redirect('/addtrip')

def joinTrip(request):
	user = User.objects.get(id=request.session['user'])
	trip = Trip.objects.get(id=request.POST['trip_id'])
	trip.users.add(user)
	return redirect('/dashboard')