from app.models import *
from django.forms import ModelForm, Form, EmailField, CharField
from django.contrib.auth.models import User


class BookForm(ModelForm):
	class Meta:
		model = Book
		fields = ['title', 'pdf']

class AuthorForm(ModelForm):
	class Meta:
		model = Author
		fields = ['name']

class CommentForm(ModelForm):
	class Meta:
		model = Comment
		fields = ['content']

class UserForm(ModelForm):
	email = EmailField()
	re_password = CharField(max_length=128)
	class Meta:
		model = User
		fields = ['username', 'email', 'password', 're_password', 'first_name', 'last_name']

	def clean(self):
		cleaned_data = super(UserForm, self).clean()
		password = cleaned_data.get("password")
		re_password = cleaned_data.get("re_password")

		if password is not None and re_password is not None and password != re_password:
			msg = u"Password and Re-password fields must match."
			self.add_error('password', msg)
			self.add_error('re_password', msg)

class ContactForm(ModelForm):
	class Meta:
		model = Contact
		fields = ['name', 'email', 'subject', 'body']