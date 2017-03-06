from django.shortcuts import render, redirect, get_object_or_404, get_list_or_404, resolve_url
from django.http.response import *
from django.db.models import F
from app.models import *
from app.forms import *
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.db import transaction
from django.utils.crypto import get_random_string
from django.core.exceptions import ObjectDoesNotExist
from django.core.mail import send_mail, send_mass_mail
from django.template.loader import render_to_string
from django.utils.html import escape
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q
import hashlib
from django.views.decorators.http import etag

# Create your views here.

def index(request):
	ctx = {}

	book_list = Book.objects.all()
	ctx['book_count'] = book_list.count()
	ctx['books'] = paginate_books(request, 5, book_list)

	return render(request, 'app/index.html', ctx)


def about(request):
	return HttpResponse('ABOUT PAGE')


def contact_etag(request):
	content = str(request)
	return hashlib.sha1(content.encode('utf-8')).hexdigest()


@etag(contact_etag)
def contact(request):
	ctx = {}
	if request.method == 'POST':
		form = ContactForm(request.POST)

		if form.is_valid():
			form.save()
			return render(request, 'app/contact/contact_success.html', {})
	else:
		form = ContactForm()

	ctx['form'] = form
	return render(request, 'app/contact/contact_form.html', ctx)


@login_required
def book_add(request):
	ctx = {}
	fail = False
	errors = {}
	ctx['errors'] = errors

	if request.method == 'POST':
		book_form = BookForm(request.POST, request.FILES)
		authors_str = request.POST.get('authors_str', None)
		tags_str = request.POST.get('tags_str', None)

		is_authors_ok = authors_str is not None and authors_str != ''
		is_tags_ok = tags_str is not None and tags_str != ''

		if not is_authors_ok:
			errors['authors_str'] = True
		if not is_tags_ok:
			errors['tags_str'] = True

		if book_form.is_valid():
			if is_authors_ok and is_tags_ok:
				book = book_form.save(commit=False)
				book.user = request.user
				book.save()

				split = authors_str.split(',')
				authors = []
				tags = []
				
				for author_name in split:
					author_name = author_name.strip()
					if author_name == '':
						continue
					author = Author.objects.get_or_create(name=author_name)[0]
					author.book_set.add(book)
					authors.append(author_name)

				split = tags_str.split(',')
				for tag_title in split:
					tag_title = tag_title.strip()
					if tag_title == '':
						continue
					tag = Tag.objects.get_or_create(title=tag_title)[0]
					tag.book_set.add(book)
					tags.append(tag_title)
			else:
				fail = True
		else:
			for error in book_form.errors:
				errors[error] = True
			fail = True

		if fail:
			transaction.rollback()
			# messages.error(request, 'Error adding your book')
		else:
			return redirect(resolve_url(to='index')) 

	return render(request, 'app/book/add.html', ctx)


def book_details(request, id):
	id = int(id)
	ctx = {}
	if id is not None:
		book = get_object_or_404(Book, pk=id)
		ctx['book'] = book
		return render(request, 'app/book/details.html', ctx)

def book_get(request, id):
	id = int(id)
	if id is not None:
		book = get_object_or_404(Book, pk=id)
		book.downloads=F('downloads')+1
		book.save()

		f = book.pdf.file
		f.open('r')
		data = f.readlines()

		response = HttpResponse(data, content_type='application/pdf')
		response['Content-Disposition'] = 'attachment; filename="%s.pdf"' %(book.title)

		return response


def author(request, id):
	ctx = {}
	author = get_object_or_404(Author, pk=id)
	ctx['author'] = author

	book_list = author.book_set.all()
	ctx['books'] = paginate_books(request, 5, book_list)

	return render(request, 'app/author/details.html', ctx)

def author_list(request):
	ctx = {}
	authors = Author.objects.order_by('name')
	ctx['authors'] = authors
	return render(request, 'app/author/list.html', ctx)


def tag(request, id):
	ctx = {}
	tag = get_object_or_404(Tag, pk=id)
	ctx['tag'] = tag

	book_list = tag.book_set.all()
	ctx['books'] = paginate_books(request, 5, book_list)

	return render(request, 'app/tag/details.html', ctx)


def tag_list(request):
	ctx = {}
	tags = Tag.objects.order_by('title')
	ctx['tags'] = tags
	return render(request, 'app/tag/list.html', ctx)


@login_required
def comment(request):
	ctx = {}
	form = CommentForm(request.POST)
	id = int(request.POST.get('book', -1))
	book = get_object_or_404(Book, pk=id)
	if form.is_valid():
		content = form.cleaned_data['content']
		comment = form.save(commit=False)
		comment.user = request.user
		comment.save()
		comment.book_set.add(book)

		url = resolve_url(to='book_details',id=id)
		return redirect(url)
	else:
		return HttpResponse('Bad %s' %(form.errors))

	
def user(request, id):
	ctx = {}
	user = get_object_or_404(User, pk=id)
	ctx['user'] = user

	book_list = user.book_set.all()
	ctx['books'] = paginate_books(request, 5, book_list)

	return render(request, 'app/user/details.html', ctx)

def user_login(request):
	ctx = {}
	fail = False
	if request.method == 'POST':
		username = request.POST.get('user', None)
		password = request.POST.get('password', None)
		remember = request.POST.get('remember', None)
		next_page = request.POST.get('next', 'index')
		if not next_page:
			next_page = 'index'

		is_username_ok = username is not None and username != ''
		is_password_ok = password is not None and password != ''
		if is_username_ok and is_password_ok:
			user = authenticate(username=username, password=password)

			if user is not None and user.is_active:
				login(request=request, user=user)
				return redirect(next_page)
			else:
				fail = True

		else:
			fail = True

	if fail:
		messages.error(request, 'Wrong user or password')

	return render(request, 'app/user/login.html', ctx)

def user_logout(request):
	logout(request)
	return redirect(request.GET.get('next', '/'))


def user_register(request):
	ctx = {}
	fail = False
	errors = {}
	if request.method == 'POST':
		email = request.POST.get('email', None)
		password = request.POST.get('password', None)
		re_password = request.POST.get('re_password', None)

		is_email_ok = email is not None and email != ''
		is_password_ok = password is not None and password != ''
		is_re_password_ok = re_password is not None and re_password != ''

		exists_email = False

		form = UserForm(request.POST)
		if is_email_ok:
			try:
				User.objects.get(email=email)
				error = '<ul class="errorlist"><li>A user with that email address already exists.</li></ul>'
				form.errors['email'] = error
			except ObjectDoesNotExist:
				pass

		if not is_password_ok:
			error = '<ul class="errorlist"><li>This field is required.</li></ul>'
			form.errors['password'] = error

		if not is_re_password_ok:
			error = '<ul class="errorlist"><li>This field is required.</li></ul>'
			form.errors['re_password'] = error

		if form.is_valid() and is_email_ok:
			user = form.save(commit=False)
			user.set_password(password)
			user.is_active = False
			user.save()

			return send_verification_token(user)
			# ctx['user'] = user
			# return render(request, 'app/user/register_ok.html', ctx)

	else:
		form = UserForm()

	ctx['form'] = form
	return render(request, 'app/user/register.html', ctx)

def send_verification_token(user):
	if user:
		ctx = {}
		token_str = get_random_string(length=48)
		token = VerificationToken.objects.create(user=user,token=token_str)

		ctx['user'] = user
		ctx['token'] = token
		email_from = 'Share! <noreply@share.com>'
		email_to = [user.email]
		email_subject = 'Activate your user registration to: Share!'
		email_body = render_to_string('app/user/activate_email.html', ctx)
		return HttpResponse(email_body)
		# send email to user with verification token
		# send_mail(email_subject, email_body, email_from, email_to, fail_silently=True)

def user_activate(request, token_str):
	ctx = {}
	token = get_object_or_404(VerificationToken, token=str(token_str))
	user = token.user
	user.is_active = True
	user.save()
	token.delete()

	return render(request,'app/user/activate_ok.html', ctx)


def search(request):
	ctx = {}
	q = request.GET.get('q', None)
	print(q)
	if q is not None and q != '':
		query = Q(title__icontains=q) | Q(abstract__icontains=q)

		book_list = list(Book.objects.filter(query))

		authors = list(Author.objects.filter(name__icontains=q))
		for author in authors:
			books = list(author.book_set.all())
			for book in books:
				if not book_list.__contains__(book):
					book_list.append(book)

		tags = list(Tag.objects.filter(title__icontains=q))
		for tag in tags:
			books = list(tag.book_set.all())
			for book in books:
				if not book_list.__contains__(book):
					book_list.append(book)

		comments = list(Comment.objects.filter(content__icontains=q))
		for comment in comments:
			books = list(comment.book_set.all())
			for book in books:
				if not book_list.__contains__(book):
					book_list.append(book)

		ctx['books'] = paginate_books(request, 5, book_list)
		return render(request, 'app/search/results.html', ctx)
	else:
		return redirect(resolve_url(to='index'))


def paginate_books(request, num=5, book_list=Book.objects.all()):
	paginator = Paginator(book_list, num)
	page = request.GET.get('page')
	try:
		books = paginator.page(page)
	except PageNotAnInteger:
		books = paginator.page(1)
	except EmptyPage:
		books = paginator.page(paginator.num_pages)

	return books
