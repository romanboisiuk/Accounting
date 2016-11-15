# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.apps import AppConfig


class StudentsConfig(AppConfig):
    name = 'students'
    verbose_name = 'База студентів'

    def ready(self):
    	from students import signals