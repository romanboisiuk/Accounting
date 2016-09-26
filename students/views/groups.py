# -*- coding: utf-8 -*-

from django.shortcuts import render
from django.http import HttpResponse

def groups_list(request):
	groups = (
		{'id' : 1,
		'leader': u'Кузь Ігор',
		'number' : 'ІМЗ-13'},
		{'id' : 2,
		'leader': u'Зварич Марко',
		'number' : 'ІМЗ-23'},
		{'id' : 3,
		'leader': u'Колодій Тарас',
		'number' : 'ІМЗ-33'}
		)
	return render(request, 'students/groups_list.html', {'groups': groups})

def groups_add(request):
	return HttpResponse('<h1>Group Add Form</h1>')

def groups_edit(request, gid):
	return HttpResponse('<h1>Edit Group %s </h1>' % gid)

def groups_delete(request, gid):
	return HttpResponse('<h1>Delete Group %s </h1>' % gid)	
