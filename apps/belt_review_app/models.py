from __future__ import unicode_literals

from django.db import models
import re
import datetime

class UserManager(models.Manager):
	def validateUser(self, post):
		is_valid = True
		errors = []
		
		if User.objects.filter(email= post.get('email')).first() != None:
			is_valid = False
			errors.append('Need a brand new email')

		if len(post.get('name'))<2 and not re.search(r'\w+',post.get('name')):
			is_valid = False
			errors.append('Name field cannot be blank and numeric')

		if len(post.get('alias'))<2 and not re.search(r'\w+',post.get('alias')):
			is_valid = False
			errors.append('Alias field cannot be blank and not numeric')

		if not re.search(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$',post.get('email')):
			is_valid = False
			errors.append('Enter a valid email address')

		if len(post.get('password')) < 8 :
			is_valid = False
			errors.append('Password length needs to be more than 8 characters')

		if post.get('password') != post.get('passwordconfirm'):
			is_valid = False
			errors.append('password did not match')

		if len(post.get('dateofbirth')) != 10:
			is_valid = False
			errors.append('Enter a valid date of birth (M/D/Y)')

		if len(post.get('dateofbirth')) == 10:
			dob=str(post.get('dateofbirth'))
			# print dob
			dob_coverted=datetime.datetime.strptime(dob, '%Y-%m-%d').date()
			now = datetime.datetime.now().date()
			delta = dob_coverted-now
			# print now
			print delta.days

			if delta.days>0:
				is_valid = False
				errors.append('Future birthday listed')

			if abs(delta.days)<6570:
				is_valid = False
				errors.append('User must be 18 years old')

		return (is_valid, errors)


class User(models.Model):
	name = models.CharField(max_length=255)
	alias = models.CharField(max_length=255)
	email = models.CharField(max_length=255)
	password = models.CharField(max_length=255)
	dateofbirth = models.DateTimeField()
	friends = models.ManyToManyField('self')
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)
	objects = UserManager()

# class Friend(models.Model):
# 	user = models.ForeignKey(User,related_name="quote")
# 	favorites = models.ManyToManyField(User, related_name="favorite_friends")
# 	created_at = models.DateTimeField(auto_now_add=True)
# 	updated_at = models.DateTimeField(auto_now=True)









