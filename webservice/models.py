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

import uuid
from django.db import models
from django.contrib.auth.models import User


def generate_uuid():
    return unicode(uuid.uuid4())


class APIKey(models.Model):
    name = models.CharField(max_length=64)
    uuid = models.CharField(unique=True, max_length=64, default=generate_uuid)
    user = models.ForeignKey(User)
    status = models.BooleanField(default=True)

    def __unicode__(self):
        return unicode("Name:[%s], Owner:[%s]" % (self.name, self.user))


class Plugin(models.Model):
    name = models.CharField(max_length=65)
    description = models.TextField()
    date_added = models.DateTimeField(auto_now_add=True)
    plugin_path = models.CharField(max_length=120)
    status = models.BooleanField(default=True)
    accessible_by = models.ManyToManyField(APIKey)

    def __unicode__(self):
        return unicode(self.name)


class Log(models.Model):
    LOGTYPE = (
        (1, 'INFO'),
        (2, 'ERROR'),
    )
    logdate = models.DateTimeField(auto_now_add=True)
    logtype = models.PositiveSmallIntegerField(choices=LOGTYPE, default=1)
    msg = models.TextField()

    def __unicode__(self):
        return unicode('[%s][%s][%s]' % (self.logdate, self.logtype, self.msg))



