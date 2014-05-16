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
from webservice.models import Plugin
from webservice.forms import plugin_forms


@login_required(login_url='/login/')
def view_all_plugins(request):
    render_vars = dict()
    try:
        render_vars['plugins'] = Plugin.objects.all()
    except Plugin.DoesNotExist:
        render_vars['plugins'] = None

    return render_to_response('view_all_plugins.html', render_vars, context_instance=RequestContext(request))


@login_required(login_url='/login/')
def add_new_plugin(request):
    if request.method == 'POST':
        form = plugin_forms.PluginForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/plugins/')
    else:
        form = plugin_forms.PluginForm()
    render_vars = dict()
    render_vars['form'] = form
    return render_to_response('generic_form.html', render_vars, context_instance=RequestContext(request))

@login_required(login_url='/login/')
def edit_plugin(request, plugin_id):
    render_vars = dict()
    plugin_object = get_object_or_404(Plugin, pk=plugin_id)
    if request.method == "POST":
        form = plugin_forms.PluginForm(request.POST)
        if form.is_valid():
            form.save(commit=False)
            plugin_object.name = form.cleaned_data.get('name')
            plugin_object.description = form.cleaned_data.get('description')
            plugin_object.plugin_path = form.cleaned_data.get('plugin_path')
            plugin_object.status = form.cleaned_data.get('status')
            plugin_object.accessible_by = form.cleaned_data.get('accessible_by')
            plugin_object.save()
            return redirect('/plugins/')
    else:
        form = plugin_forms.PluginForm(instance=plugin_object)
    render_vars['form'] = form
    return render_to_response('generic_form.html', render_vars, context_instance=RequestContext(request))