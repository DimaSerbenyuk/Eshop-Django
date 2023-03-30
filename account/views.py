from django.shortcuts import render, redirect
from .forms import CreateUserForm, LoginForm, UpdateUserForm

from payment.forms import ShippingForm
from payment.models import ShippingAddress

from payment.models import Order, OrderItem

from django.contrib.auth.models import User

from django.contrib.sites.shortcuts import get_current_site #there domain name idk when we deploy...62
from . token import user_tokenizer_generate

from django.template.loader import render_to_string
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode


from django.contrib.auth.models import auth
from django.contrib.auth import authenticate

from django.contrib.auth.decorators import login_required

from django.contrib import messages
from django.views.decorators.csrf import csrf_protect 

@csrf_protect 
def register(request):

    form = CreateUserForm()

    if request.method == 'POST':

        form = CreateUserForm(request.POST)

        if form.is_valid():

            user = form.save() # we overwriting that obj

            user.is_active = False #without verification we don't activate account

            user.save()


            # Email verification setup (template)
            current_site = get_current_site(request)

            subject = 'Account verification email'

            message = render_to_string('account/registration/email-verification.html',{

                'user':user,
                'domain':current_site.domain,
                'uid':urlsafe_base64_encode(force_bytes(user.pk)),
                'token': user_tokenizer_generate.make_token(user), 
            })

            user.email_user(subject=subject, message=message)

            return redirect('email-verification-sent')#we want redirect that user to url with name...

        
    context = {'form':form}

    return render(request, 'account/registration/register.html', context=context)

@csrf_protect 
def email_verification(request, uidb64, token):

    unique_id = force_str(urlsafe_base64_decode(uidb64))
    
    user = User.objects.get(pk=unique_id)

    # Success
    if user and user_tokenizer_generate.check_token(user, token):

        user.is_active = True 

        user.save()

        return redirect('email-verification-success')

    # Failed
    else:
        return redirect('email-verification-failed')


    

@csrf_protect 
def email_verification_sent(request):

    return render(request, 'account/registration/email-verification-sent.html')

@csrf_protect 
def email_verification_success(request):

    return render(request, 'account/registration/email-verification-success.html')

@csrf_protect 
def email_verification_failed(request):

    return render(request, 'account/registration/email-verification-failed.html')



@csrf_protect 
def my_login(request):

    form = LoginForm()

    if request.method == 'POST':

        form = LoginForm(request, data=request.POST)

        if form.is_valid():

            username = request.POST.get('username')
            password = request.POST.get('password')

            user = authenticate(request, username=username, password=password)

            if user is not None:

                auth.login(request, user)

                return redirect('dashboard')


    context={'form':form}

    return render(request, 'account/my-login.html', context=context)



@csrf_protect 
# logout
def user_logout(request): # excepts session key to kill

    try:
    
        for key in list(request.session.keys()):

            if key == 'session_key':

                continue
                
            else:
                del request.session[key]

    except KeyError: 

        pass

    messages.success(request, 'Logout success!')

    return redirect('store')

@csrf_protect 
@login_required(login_url='my-login')
def dashboard(request):

    return render(request, 'account/dashboard.html')



@csrf_protect 
@login_required(login_url='my-login')
def profile_management(request):
    
    # Updating Users's username and email

    user_form = UpdateUserForm(instance=request.user)

    if request.method == 'POST':

        user_form = UpdateUserForm(request.POST, instance=request.user)

        if user_form.is_valid():

            user_form.save()

            messages.info(request, 'Account updated!')

            return redirect('dashboard')

    context = {'user_form':user_form}

    return render(request, 'account/profile-management.html', context=context)

@csrf_protect 
@login_required(login_url='my-login')
def delete_account(request):

    user = User.objects.get(id=request.user.id)

    if request.method == 'POST':

        user.delete()
        
        messages.error (request, 'Account deleted!')


        return redirect ('store')



    return render(request, 'account/delete-account.html')




# Shipping view
@csrf_protect 
@login_required(login_url='my-login')
def manage_shipping(request):

    try:
        # Account user with shipment  information
        shipping = ShippingAddress.objects.get(user=request.user.id) 


    except ShippingAddress.DoesNotExist:

        shipping = None

    form = ShippingForm(instance=shipping) # if user has no information it's going to a new object

    if request.method == 'POST':

        form = ShippingForm(request.POST, instance=shipping)# if the user already have the info it's going simply update

        if form.is_valid(): # if valid we want insure that our foreign key(FK) is attached to our user model

            # Assing the user FK on the object
            shippng_user = form.save(commit=False)

            #adding the FK itself
            shippng_user.user = request.user

            shippng_user.save()

            return redirect('dashboard')

    context = {'form': form}

    return render(request, 'account/manage-shipping.html', context=context)

@csrf_protect 
@login_required(login_url='my-login')
def track_orders(request):

    try:
        orders = OrderItem.objects.filter(user=request.user)

        context = {'orders':orders}

        return render(request, 'account/track-orders.html', context=context)

    except:


        return render(request, 'account/track-orders.html')