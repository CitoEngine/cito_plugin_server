"""Copyright 2014 Cyrus Dasadia

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django import forms
from django.shortcuts import get_object_or_404, redirect, render_to_response
from django.template import RequestContext
from webservice.forms import user_forms
from webservice.models import APIKey


@login_required(login_url='/login/')
def view_all_users(request):
    users = User.objects.all()
    return render_to_response('view_all_users.html',
                              {'users': users},
                              context_instance=RequestContext(request))

@login_required(login_url='/login/')
def view_single_user(request, user_id):
    view_user = get_object_or_404(User, pk=user_id)
    apikeys = APIKey.objects.filter(user=view_user)
    return render_to_response('view_user.html',
                              {'view_user': view_user, 'apikeys': apikeys},
                              context_instance=RequestContext(request))


@login_required(login_url='/login/')
def create_user(request):
    render_vars = dict()
    form = user_forms.UserCreationForm()
    if request.method == "POST":
        form = user_forms.UserCreationForm(request.POST)
        if form.is_valid():
            fname = form.cleaned_data.get('fname')
            lname = form.cleaned_data.get('lname')
            username = form.cleaned_data.get('username')
            password1 = form.cleaned_data.get('password1')
            email = form.cleaned_data.get('email')

            user = User.objects.create_user(first_name=fname, last_name=lname,
                                            password=password1, email=email, username=username)
            user.save()
            return redirect('/users/')
    render_vars['form'] = form
    return render_to_response('generic_form.html', render_vars, context_instance=RequestContext(request))

@login_required(login_url='/login/')
def edit_user(request, user_id):
    render_vars = dict()
    user = get_object_or_404(User, pk=user_id)
    if not request.user.is_superuser:
        return render_to_response('unauthorized.html', context_instance=RequestContext(request))
    if request.method == "POST":
        form = user_forms.EditUserForm(request.POST)
        if form.is_valid():
            user.first_name = form.cleaned_data.get('first_name')
            user.last_name = form.cleaned_data.get('last_name')
            user.username = form.cleaned_data.get('username')
            user.email = form.cleaned_data.get('email')
            user.save()
            password = form.cleaned_data.get('password1')
            if password:
                user.set_password(password)
                user.save()
            return redirect('/users/view/%s/' % user.id)
    else:
        form_vars = {'first_name': user.first_name,
                     'last_name': user.last_name,
                     'email': user.email,
                     'username': user.username}
        form = user_forms.EditUserForm(initial=form_vars)
    render_vars['form'] = form
    render_vars['page_title'] = render_vars['box_title'] = 'Editing user: %s ' % user.username
    return render_to_response('generic_form.html', render_vars, context_instance=RequestContext(request))


@login_required(login_url='/login/')
def toggle_user(request):
    if request.method == 'POST':
        try:
            user_id = int(request.POST.get('user_id'))
        except:
            raise forms.ValidationError("Invalid user toggle form received!")
        user = get_object_or_404(User, pk=user_id)
        if user.is_active:
            user.is_active = False
            # If user is disabled so are its keys
            for apikey in APIKey.objects.filter(user=user):
                apikey.status = False
                apikey.save()
        else:
            user.is_active = True
        user.save()

        return redirect('/users/view/%s' % user_id)