# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.conf import settings
from django.db import models
from django.contrib.auth.models import User


class LoggedInUser(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, related_name='logged_in_user')

class Clarify(models.Model):
    user = models.ForeignKey(User, related_name='user')
    clear = models.BooleanField()
    


