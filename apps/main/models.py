from __future__ import unicode_literals
from django.db import models
import re, bcrypt

class UserManager(models.Manager):
    def basic_validator(self, postData):
        errors={}
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9.+_-]+\.[a-zA-Z0-9]+$')
        if not EMAIL_REGEX.match(postData['email']):
            errors['email'] = ("Invalid email address.")
        if User.objects.filter(email=postData['email']):
            errors["email_exists"] = "This email address is already linked to another account."
        if len(postData['first']) <3:
            errors['first']  = "First name should be longer than 3 character."
        if len(postData['last']) <3:
            errors['last']  = "Last name should be longer than 3 character."
        if len(postData['pw']) <8:
            errors['pw']  = "Password must be longer than 8 characters."
        if postData['pw'] != postData['pw2']:
            errors ['pw2'] = "Sorry, try again. Your passwords dont appear to match."
        return errors

    def loginVal(self, postData):
        print(postData)
        user = User.objects.filter(email=postData["email"])
        errors = {}
        if not user:
            errors['email']="Email not found in database. Please try again."
        if user and not bcrypt.checkpw(postData['pw'].encode(), user[0].password.encode()):
            errors['pw'] = "invalid password"
        return errors

class JobManager(models.Manager):
    def job_validator(self, postData):
        errors={}
        if len(postData['title']) <3:
            errors['title'] = "Your job title must contain more than 3 letters."
        if len(postData['desc']) <3:
            errors['desc'] = "Your job description must have more than 3.14 characters."
        if len(postData['loc']) <5:
            errors['loc'] = "Your job locaiton  must have more than 5 characters."
        return errors

class User(models.Model):
    first = models.CharField(max_length=225)
    last = models.CharField(max_length=225)
    email = models.CharField(max_length=225)
    password = models.CharField(max_length=225)
    objects = UserManager()
  # trips = this users trips

class Job(models.Model):
    title = models.CharField(max_length=225)
    description = models.CharField(max_length=225)
    location = models.CharField(max_length=225)
    user = models.ForeignKey(User, related_name ="trips")
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now_add=True)
    objects = JobManager()