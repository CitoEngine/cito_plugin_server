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
from django.shortcuts import render_to_response, redirect, get_object_or_404
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from webservice.models import APIKey
from webservice.forms import api_forms


@login_required(login_url='/login/')
def view_all_apikeys(request):
    render_vars = dict()
    try:
        render_vars['apikeys'] = APIKey.objects.all()
        render_vars['server'] = '%s:%s' % (request.META['SERVER_NAME'], request.META['SERVER_PORT'])
    except APIKey.DoesNotExist:
        render_vars['apikeys'] = None
    print request.META
    return render_to_response('view_all_apikeys.html', render_vars, context_instance=RequestContext(request))


@login_required(login_url='/login/')
def add_new_key(request):
    if request.method == 'POST':
        form = api_forms.APIForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/apikeys/')
    else:
        form = api_forms.APIForm()
    render_vars = dict()
    render_vars['form'] = form
    return render_to_response('generic_form.html', render_vars, context_instance=RequestContext(request))

@login_required(login_url='/login/')
def edit_key(request, apikey_id):
    render_vars = dict()
    api_key_object = get_object_or_404(APIKey, pk=apikey_id)
    if request.method == "POST":
        form = api_forms.APIEditForm(request.POST)
        if form.is_valid():
            api_key_object.name = form.cleaned_data.get('name')
            api_key_object.user = form.cleaned_data.get('user')
            api_key_object.status = form.cleaned_data.get('status')
            api_key_object.save()
            return redirect('/apikeys/')
    else:
        form = api_forms.APIEditForm(instance=api_key_object)
    render_vars['form'] = form
    return render_to_response('generic_form.html', render_vars, context_instance=RequestContext(request))