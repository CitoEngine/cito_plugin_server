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

import logging
import re
import simplejson
from django.http import HttpResponse, HttpResponseBadRequest
from django.views.decorators.csrf import csrf_exempt
from django.core import serializers
from plugin import runner
from webservice.models import Plugin, APIKey
from django.conf import settings

logger = logging.getLogger('plugin_logger')


def parse_request(request, apikey_object):
    try:
        parsed_json = simplejson.loads(request.body)
    except BaseException, e:
        return HttpResponseBadRequest('Invalid JSON format: %s' % request.body)

    # Check JSON structure
    if not 'plugin' in parsed_json and not 'parameters' in parsed_json:
        return HttpResponseBadRequest('Invalid JSON format, no parameters: %s' % request.body)

    #Fetch plugin information
    try:
        p = Plugin.objects.get(name__iexact=parsed_json['plugin'], accessible_by=apikey_object)
    except Plugin.DoesNotExist:
        return HttpResponseBadRequest('Plugin not found or you do not have permission to access it.')

    if not p.status:
        return HttpResponseBadRequest('Plugin inactive.')

    command = [settings.PLUGIN_DIR + p.plugin_path]
    try:
        param_dict = parsed_json['parameters'][0]
        if isinstance(param_dict, dict):
            for k,v in param_dict.iteritems():
                command.append(k)
                command.append(v)
        else:
            for k in parsed_json['parameters']:
                command.append(k)
    except BaseException, e:
        pass
    logger.info("Running: %s " % command)
    response = runner.RunPlugin().execute([command])
    return HttpResponse(response)


@csrf_exempt
def run_plugin(request, apikey):
    try:
        apikey_object = APIKey.objects.get(uuid__iexact=apikey)
        if apikey_object.status:
            return parse_request(request, apikey_object)
        else:
            return HttpResponse('Invalid or disabled api key: %s' % apikey)
    except BaseException,e:
        return HttpResponseBadRequest("DEBUG: 400 BadRequest %s" % e)


@csrf_exempt
def get_all_plugins(request, apikey):
    try:
        a = APIKey.objects.get(uuid__iexact=apikey)
        jsondump = serializers.serialize('json', Plugin.objects.filter(accessible_by=a), indent=4)
        jsondump = re.sub('"pk": [0-9]{1,5},', '', jsondump)
        jsondump = re.sub('"model": "webservice.plugin",', '', jsondump)
        jsondump = re.sub('"fields"', '"plugins"', jsondump)
        return HttpResponse(jsondump, content_type='application/json')
    except BaseException,e:
        return HttpResponseBadRequest("DEBUG: 400 BadRequest %s" % e)
