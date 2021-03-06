from django.shortcuts import render, redirect
from django.contrib import messages
from .models import *
import bcrypt
import datetime

def current_user(request):
	return User.objects.get(id=request.session['user_id'])

def index(request):
	return render(request, "belt_review_app/index.html")

def friends(request):
	if 'user_id' not in request.session:
		return redirect('/')

	else:
		error = True
		if len(current_user(request).friends.all()) == 0:
			error = False

		userfriend = []
		for user in User.objects.all().exclude(friends=current_user(request)):
			print user
			if user != current_user(request):
				userfriend.append(user)

		context = {
			"current_user": current_user(request),
			"error": error,
			"friends": userfriend
		}
		return render(request, "belt_review_app/home.html",context)

def addFriend(request,friendid):
	friend = User.objects.get(id=friendid)
	current_user(request).friends.add(friend)	
	return redirect('/friends')

def removeFriend(request,friendid):
	friend = User.objects.get(id=friendid)
	current_user(request).friends.remove(friend)
	return redirect('/friends')

def userprofile(request,userid):
	if 'user_id' not in request.session:
		return redirect('/')
	else:
		context = {
			"user": User.objects.get(id=userid)
		}
		return render(request, "belt_review_app/userprofile.html",context)





#creating new user
def createUser(request):
	if request.method != 'POST':
		return redirect('/')
	else:
		check = User.objects.validateUser(request.POST)
		if check[0] == False:
			for error in check[1]:
				print error
				messages.error(request,error)
			return redirect('/')

		else:
			dob=str(request.POST.get('dateofbirth'))
			dob_coverted=datetime.datetime.strptime(dob, '%Y-%m-%d').date()
			hashed_pw = bcrypt.hashpw(request.POST.get('password').encode(), bcrypt.gensalt())
			user = User.objects.create(
				name = request.POST.get('name'),
				alias = request.POST.get('alias'),
				email = request.POST.get('email'),
				password = hashed_pw,
				dateofbirth = dob_coverted
			)
			request.session['user_id'] = user.id
		return redirect('/friends')
##login
def login(request):
	if request.method != 'POST':
		return redirect('/')
	else:
		user = User.objects.filter(email= request.POST.get('email')).first()
		if user and bcrypt.checkpw(request.POST.get('password').encode(),user.password.encode()):
			request.session['user_id'] = user.id
			return redirect('/friends')
		else:
			messages.error(request,'invalid')
			return redirect('/')
#logout
def logout(request):
	request.session.delete()
	return redirect('/')



