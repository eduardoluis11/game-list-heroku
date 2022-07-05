# This is the Django library that will allow me to create forms
from django import forms

""" As for the HTML page’s forms, I don’t need to store passwords, so I don’t need to hide what the users are typing 
on the inputs. So, I can us the Django form generator to create the forms for the “Add Game” functionality. I don’t 
have any hard limits. All of the inputs will accept text and numbers, so I can make them use “CharField”. The title 
can have a limit of 255 characters, but the store and console names could have a 64 character limit.

The fields will be "Title", "Console", "Store".
"""
class AddGameForm(forms.Form):
    title = forms.CharField(max_length=255)
    console = forms.CharField(max_length=64)
    store = forms.CharField(max_length=64)


""" This will create the sign up page form. 

The form for creating a user will have 4 fields: username, password, confirm password, and email. As to how to create 
each field of the form, I will need to check this page of the documentation: 
https://docs.djangoproject.com/en/4.0/topics/forms/ .

I will put the same limitations from the gamelist_user table's fields into each the the 4 forms. The limitations for
each field are the following: "username" varchar(150), "password" varchar(128) (same goes for "confirm password"), 
and "email" varchar(254). 

There's a specific field for emails. It's really similar fo CharField (source: 
https://docs.djangoproject.com/en/4.0/ref/forms/fields/#emailfield .)
"""
# class SignUpForm(forms.Form):
#     username = forms.CharField(max_length=150)
#     email = forms.EmailField(max_length=254)
#     password = forms.CharField(max_length=128)
#     confirm_password = forms.CharField(max_length=128)



