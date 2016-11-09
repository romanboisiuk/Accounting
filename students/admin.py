# -*- coding: utf-8 -*-
from django.contrib import admin
from django.core.urlresolvers import reverse
from django.forms import ModelForm, ValidationError

from .models.students import Student
from .models.groups import Group
from .models.monthjournal import MonthJournal

class StudentAdmin(admin.ModelAdmin):
	
	list_display = ['last_name', 'first_name', 'ticket', 'student_group' ]
	list_display_links = ['last_name', 'first_name']
	list_editable = ['student_group']
	ordering = ['last_name']
	list_filter = ['student_group']
	list_per_page = 5
	search_fields = ['last_name', 'first_name', 'ticket', 'middle_name']

	def view_on_site(self, obj):
		return reverse('students_edit', kwargs={'pk' : obj.id})

class GroupAdmin(admin.ModelAdmin):
	list_display = ['title', 'leader']
	search_fields = ['title', 'leader']
	list_filter = ['title']

admin.site.register(Student, StudentAdmin) 
admin.site.register(Group, GroupAdmin) 
admin.site.register(MonthJournal) 
