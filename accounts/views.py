from django.shortcuts import render
from django.contrib import messages
from django.shortcuts import redirect, reverse
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.core.mail import EmailMultiAlternatives
import urllib3

from .forms import RegisterForm
from .models import Account
from greatkart.utils import default_token_generator
from carts.models import Cart, CartItem
from carts.views import _cart_id


@login_required(login_url='login')
def dashboard(request):
    return render(request, 'account/dashboard.html')


def login(request, *args, **kwargs):
    if request.method == "POST":
        email = request.POST['email']
        password = request.POST['password']
        next_page = ''
        product_variation = []
        ex_var_list = []
        id = []

        user = auth.authenticate(email=email, password=password)

        if user:
            try:
                cart: Cart = Cart.objects.get(cart_id=_cart_id(request))
                cart_item = CartItem.objects.filter(cart=cart)

                if cart_item.exists():
                    for item in cart_item:
                        variation = item.variations.all()
                        product_variation.append(list(variation))

                    cart_item = CartItem.objects.filter(user=user)

                    for item in cart_item:
                        existing_variation = item.variations.all()
                        ex_var_list.append(list(existing_variation))
                        id.append(item.id)

                    for pr in product_variation:
                        if pr in ex_var_list:
                            index = ex_var_list.index(pr)
                            item_id = id[index]
                            item = CartItem.objects.get(id=item_id)
                            item.quantity += 1
                            item.user = user
                            item.save()
                        else:
                            cart_item = CartItem.objects.filter(cart=cart)
                            for item in cart_item:
                                item.user = user
                                item.save()
            except:
                pass

            auth.login(request, user)

            URL = request.META.get('HTTP_REFERER')
            query = urllib3.util.parse_url(URL).query
            if query:
                params = dict(x.split('=') for x in query.split("&"))
                next_page = params['next']

            messages.success(request, 'You are logged in')
            return redirect(next_page or reverse('dashboard'))

        messages.error(request, 'invalid login credentials')
        return redirect(reverse('login'))
    return render(request, 'account/login.html')


def register(request):
    form = RegisterForm(request.POST or None)
    if request.method == "POST":
        if form.is_valid():
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            email = form.cleaned_data['email']
            phone_number = form.cleaned_data['phone_number']
            password = form.cleaned_data['password']
            username = email.split('@')[0]

            user = Account.objects.create_user(first_name=first_name, last_name=last_name,
                                               email=email, username=username,
                                               password=password)
            user.phone_number = phone_number
            user.save()

            current_site = get_current_site(request)
            mail_subject = "Please active your account"
            try:
                data = {
                    'user': user,
                    'domain': current_site,
                    'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                    'token': default_token_generator.make_token(user)
                }
                template = render_to_string('email/register_verification.html', data)
                text_content = strip_tags(template)
                to_email = email
                from_email = "support@Greatkart.io"
                send_email = EmailMultiAlternatives(mail_subject, text_content, from_email, [to_email])
                send_email.attach_alternative(template, 'text/html')
                send_email.send()
            except:
                messages.error(request, 'email not send please try again')
                return redirect(reverse('register'))

            return redirect(reverse('login') + '?command=verification&email=' + email)

    return render(request, 'account/register.html', {'form': form})


@login_required(login_url='login')
def logout(request):
    if request.method == "POST":
        auth.logout(request)
        messages.success(request, "You are logged out")
        return redirect(reverse('login'))


def activate(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = Account._default_manager.get(pk=uid)
    except (TypeError, ValueError, OverflowError, Account.DoesNotExist):
        user = None

    if user and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        messages.success(request, 'Your account is activated')
        return redirect('login')
    messages.error(request, 'Invalid activation link')
    return redirect('register')


def forgot_password(request):
    if request.method == "POST":
        email = request.POST['email']

        if Account.objects.filter(email__exact=email).exists():
            user = Account.objects.get(email__exact=email)
            current_site = get_current_site(request)
            mail_subject = "Reset your password"
            try:
                data = {
                    'user': user,
                    'domain': current_site,
                    'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                    'token': default_token_generator.make_token(user)
                }
                template = render_to_string('email/reset_password.html', data)
                text_content = strip_tags(template)
                to_email = email
                from_email = "support@Greatkart.io"

                send_email = EmailMultiAlternatives(mail_subject, text_content, from_email, [to_email])
                send_email.attach_alternative(template, 'text/html')
                send_email.send()
            except:
                messages.error(request, 'email not send please try again')
                return redirect(reverse('forgot-password'))

        messages.success(request, f'Thank you we send email verification tp {email}')
        return redirect(reverse('login'))

    return render(request, 'account/forgot_password.html')


def forgot_password_validate(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = Account._default_manager.get(pk=uid)
    except (TypeError, ValueError, OverflowError, Account.DoesNotExist):
        user = None

    if user and default_token_generator.check_token(user, token):
        request.session['uid'] = uid
        messages.success(request, 'Please reset your password')
        return redirect(reverse('reset-password'))

    messages.error(request, 'This link has been expired')
    return redirect('login')


def reset_password(request):
    if request.method == "POST":
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']

        if password == confirm_password:
            uid = request.session.get('uid')
            user = Account.objects.get(pk=uid)
            user.set_password(password)
            user.save()
            messages.success(request, 'Password reset Successful')
            return redirect(reverse('login'))

        messages.error(request, 'Password do not match')
        return redirect(reverse('reset-password'))

    return render(request, 'account/reset_password.html')
