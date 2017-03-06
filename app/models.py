from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Book(models.Model):
	title = models.CharField(max_length=144, unique=True)
	authors = models.ManyToManyField('Author')
	pdf = models.FileField(upload_to='books/pdf')
	abstract = models.CharField(max_length=255)
	pub_date = models.DateTimeField(auto_now_add=True)
	votes = models.FloatField(default=0.0)
	downloads = models.IntegerField(default=0)
	tags = models.ManyToManyField('Tag')
	cover = models.FileField(upload_to='books/cover', null=True, blank=True)
	comments = models.ManyToManyField('Comment', blank=True)
	user = models.ForeignKey(User)

	class Meta:
		get_latest_by = "pub_date"
		ordering = ['-pub_date']

	def delete(self, *args, **kwargs):
		self.pdf.delete()
		self.cover.delete()
		super(Book, self).delete(*args, **kwargs)

	# def save(self, *args, **kwargs):
	# 	split = self.title.split(' ')
	# 	out = ''
	# 	for item in split:
	# 		item = item.strip().capitalize()
	# 		out += ' %s' %item

	# 	self.title = out.strip()
	# 	super(Book, self).save(*args, **kwargs)

	def __str__(self):
		return self.title

	def pdf_url(self):
		return self.pdf


class Author(models.Model):
	name = models.CharField(max_length=144)

	# def save(self, *args, **kwargs):
	# 	split = self.name.split(' ')
	# 	out = ''
	# 	for item in split:
	# 		item = item.strip().capitalize()
	# 		out += ' %s' %item

	# 	self.name = out.strip()
	# 	super(Author, self).save(*args, **kwargs)

	def __str__(self):
		return self.name

class Tag(models.Model):
	title = models.CharField(max_length=144, primary_key=True)

	# def save(self, *args, **kwargs):
	# 	self.title = self.title.strip().capitalize()
	# 	super(Tag, self).save(*args, **kwargs)

	def __str__(self):
		return self.title

class Comment(models.Model):
	user = models.ForeignKey(User)
	content = models.CharField(max_length=144)
	votes = models.IntegerField(default=0)

	def __str__(self):
		return self.content

class VerificationToken(models.Model):
	token = models.URLField(primary_key=True)
	user = models.ForeignKey(User)

	def __str__(self):
		return self.token


class Contact(models.Model):
	name = models.CharField(max_length=144)
	email = models.EmailField()
	subject = models.CharField(max_length=144)
	body = models.CharField(max_length=500)

	def __str__(self):
		return self.name