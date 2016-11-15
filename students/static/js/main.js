function	initJournal() {

	var indicator = $('#ajax-progress-indicator');

	$('.day-box input[type="checkbox"]').click(function(event){
		var box = $(this);
		$.ajax(box.data('url'), {
			'type' : 'POST',
			'async' : true,
			'dataType' : 'json',
			'data' : {
				'pk' : box.data('student-id'),
				'date' : box.data('date'),
				'present' : box.is(':checked') ? '1': '',
				'csrfmiddlewaretoken' : $('input[name="csrfmiddlewaretoken"]').val()
			},
			'beforeSend': function(xhr, settings){
				indicator.show();
			},
			'error' : function(xhr, status, error){
				alert(error);
				indicator.hide();
			},
			'success' : function(data, status, xhr){
				indicator.hide();
			}
		});
	});
}


function initGroupSelector() {
	// look up select element with groups and attach our even handler
	// on field ”change” event
	$('#group-selector select').change(function(event){
		// get value of currently selected group option
		var group = $(this).val();

		if (group) {
			// set cookie with expiration date 1 year since now;
			// cookie creation function takes period in days
			$.cookie('current_group', group, {'path': '/', 'expires': 365});
		}
		else {
			// otherwise we delete the cookie
			$.removeCookie('current_group', {'path': '/'});
		}
		// and reload a page
		location.reload(true);

		return true;
	});
}

function initDateFields() {
	$('input.dateinput').datetimepicker({
		'format':'YYYY-MM-DD'
	}).on('dp.hide', function(event){
		$(this).blur();
	});
}

function initAddStudentPage() {
	var indicator_2 = $('#ajax-loader').html('<img id="loader-img" \\\n\
	src="/static/img/loader.gif"  width="200" height="60" />');
	$('a#add_student').click(function(event){
		var link = $(this);
		$.ajax({
			'url': link.attr('href'),
			'dataType': 'html',
			'type': 'get',

			'beforeSend': function(xhr, settings){
				indicator_2.show();
			},
			'success': function(data, status, xhr){
				// check if we got successfull response from the server
				if (status != 'success') {
					alert('Помилка на сервері. Спробуйте будь-ласка пізніше.');
					return false;
				}
					// update modal window with arrived content from the server
					indicator_2.hide();
					var modal = $('#myModal'),
						html = $(data), form = html.find('#content-column form');
						modal.find('.modal-title').html(html.find('#content-column h2').text());
						modal.find('.modal-body').html(form);

						// init our edit form
						initAddStudentForm(form, modal);

						// setup and show modal window finally
						modal.modal({
							'keyboard': false,
							'backdrop': false,
							'show': true
						});
				},
				'error': function(){
					alert('Помилка на сервері. Спробуйте будь-ласка пізніше.')
					return false;
				}
		});
		return false;
	});
}

function initEditStudentPage() {
	var indicator_3 = $('#ajax-loader').html('<img id="loader-img" \\\n\
 	src="/static/img/loader.gif"  width="200" height="60" />');
	$('a.student-edit-form-link').click(function(event){
		var link = $(this);
		$.ajax({
			'url': link.attr('href'),
			'dataType': 'html',
			'type': 'get',

			'beforeSend': function(xhr, settings){
				indicator_3.show();
			},

			'success': function(data, status, xhr){
				// check if we got successfull response from the server
				if (status != 'success') {
					alert('Помилка на сервері. Спробуйте будь-ласка пізніше.');
					return false;
				}
					// update modal window with arrived content from the server
					indicator_3.hide();
					var modal = $('#myModal'),
						html = $(data), form = html.find('#content-column form');
						modal.find('.modal-title').html(html.find('#content-column h2').text());
						modal.find('.modal-body').html(form);

						// init our edit form
						initEditStudentForm(form, modal);

						// setup and show modal window finally
						modal.modal({
							'keyboard': false,
							'backdrop': false,
							'show': true
						});
				},
				'error': function(){
					alert('Помилка на сервері. Спробуйте будь-ласка пізніше.')
					indicator_3.hide();
					return false;
				}
		});
		return false;
	});
}

function initAddStudentForm(form, modal) {
	// attach datepicker
	initDateFields();

	// close modal window on Cancel button click
	form.find('input[name="cancel_button"]').click(function(event){
		modal.modal('hide');
		return false;
	});

	// make form work in AJAX mode
	form.ajaxForm({
		'dataType': 'html',
		'error': function(){
			alert('Помилка на сервері. Спробуйте будь-ласка пізніше.');
			return false;
		},
		'beforeSend': function(xhr, settings){
			$('.form-horizontal').html('<img id="loader-img" \\\n\
				src="/static/img/loader.gif"  width="200" height="60" /> ');
		},
		'success': function(data, status, xhr) {
			var html = $(data), newform = html.find('#content-column form');

			// copy alert to modal window
			modal.find('.modal-body').html(html.find('.alert'));

			// copy form to modal if we found it in server response
			if (newform.length > 0) {
				modal.find('.modal-body').append(newform);

				// initialize form fields and buttons
				initAddStudentForm(newform, modal);
			} else {
				// if no form, it means success and we need to reload page
				// to get updated students list;
				// reload after 2 seconds, so that user can read
				// success message
				setTimeout(function(){location.reload(true);}, 500);
			}
		}
	});
}

function initEditStudentForm(form, modal) {
	// attach datepicker
	initDateFields();

	// close modal window on Cancel button click
	form.find('input[name="cancel_button"]').click(function(event){
		modal.modal('hide');
		return false;
	});

	// make form work in AJAX mode
	form.ajaxForm({
		'dataType': 'html',
		'error': function(){
			alert('Помилка на сервері. Спробуйте будь-ласка пізніше.');
			return false;
		},
		'beforeSend': function(xhr, settings){
			$('.form-horizontal').html('<img id="loader-img" \\\n\
			src="/static/img/loader.gif"  width="200" height="60" />');
		},
		'success': function(data, status, xhr) {
			var html = $(data), newform = html.find('#content-column form');

			// copy alert to modal window
			modal.find('.modal-body').html(html.find('.alert'));

			// copy form to modal if we found it in server response
			if (newform.length > 0) {
				modal.find('.modal-body').append(newform);

				// initialize form fields and buttons
				initEditStudentForm(newform, modal);
			} else {

				setTimeout(function(){location.reload(true);}, 500);
			}
		}
	});
}

function initAddGroupPage() {
	var indicator_4 = $('#ajax-loader').html('<img id="loader-img" \\\n\
 	src="/static/img/loader.gif"  width="200" height="00" />');
	
	$('a#add_group').click(function(event){
		var link = $(this);
		$.ajax({
			'url': link.attr('href'),
			'dataType': 'html',
			'type': 'get',

			'beforeSend': function(xhr, settings){
				indicator_4.show();
			},
			'success': function(data, status, xhr){
				// check if we got successfull response from the server
				if (status != 'success') {
					alert('Помилка на сервері. Спробуйте будь-ласка пізніше.');
					return false;
				}
					// update modal window with arrived content from the server
					indicator_4.hide();
					var modal = $('#myModal'),
						html = $(data), form = html.find('#content-column form');
						modal.find('.modal-title').html(html.find('#content-column h2').text());
						modal.find('.modal-body').html(form);

						// init our edit form
						initAddGroupForm(form, modal);

						// setup and show modal window finally
						modal.modal({
							'keyboard': false,
							'backdrop': false,
							'show': true
						});
				},
				'error': function(){
					alert('Помилка на сервері. Спробуйте будь-ласка пізніше.')
					return false;
				}
		});
		return false;
	});
}

function initEditGroupPage() {
	var indicator_5 = $('#ajax-loader').html('<img id="loader-img" \\\n\
 	src="/static/img/loader.gif"  width="200" height="60" />');
	
	$('a.group-edit-form-link').click(function(event){
		var link = $(this);
		$.ajax({
			'url': link.attr('href'),
			'dataType': 'html',
			'type': 'get',

			'beforeSend': function(xhr, settings){
				indicator_5.show();
			},
			'success': function(data, status, xhr){
				// check if we got successfull response from the server
				if (status != 'success') {
					alert('Помилка на сервері. Спробуйте будь-ласка пізніше.');
					return false;
				}
					// update modal window with arrived content from the server
					indicator_5.hide();
					var modal = $('#myModal'),
						html = $(data), form = html.find('#content-column form');
						modal.find('.modal-title').html(html.find('#content-column h2').text());
						modal.find('.modal-body').html(form);

						// init our edit form
						initEditGroupForm(form, modal);

						// setup and show modal window finally
						modal.modal({
							'keyboard': false,
							'backdrop': false,
							'show': true
						});
				},
				'error': function(){
					alert('Помилка на сервері. Спробуйте будь-ласка пізніше.')
					indicator_5.hide();
					return false;
				}
		});
		return false;
	});
}

function initAddGroupForm(form, modal) {

	// close modal window on Cancel button click
	form.find('input[name="cancel_button"]').click(function(event){
		modal.modal('hide');
		return false;
	});

	// make form work in AJAX mode
	form.ajaxForm({
		'dataType': 'html',
		'error': function(){
			alert('Помилка на сервері. Спробуйте будь-ласка пізніше.');
			return false;
		},
		'beforeSend': function(xhr, settings){
			$('.form-horizontal').html('<img id="loader-img" \\\n\
			src="/static/img/loader.gif"  width="200" height="60" />');
		},
		'success': function(data, status, xhr) {
			var html = $(data), newform = html.find('#content-column form');

			// copy alert to modal window
			modal.find('.modal-body').html(html.find('.alert'));

			// copy form to modal if we found it in server response
			if (newform.length > 0) {
				modal.find('.modal-body').append(newform);

				// initialize form fields and buttons
				initAddGroupForm(newform, modal);
			} else {
			
				setTimeout(function(){location.reload(true);}, 500);
			}
		}
	});
}

function initEditGroupForm(form, modal) {
	
	// close modal window on Cancel button click
	form.find('input[name="cancel_button"]').click(function(event){
		modal.modal('hide');
		return false;
	});

	// make form work in AJAX mode
	form.ajaxForm({
		'dataType': 'html',
		'error': function(){
			alert('Помилка на сервері. Спробуйте будь-ласка пізніше.');
			return false;
		},
		'beforeSend': function(xhr, settings){
			$('.form-horizontal').html('<img id="loader-img" \\\n\
			src="/static/img/loader.gif"  width="200" height="60" />');
		},
		'success': function(data, status, xhr) {
			var html = $(data), newform = html.find('#content-column form');

			// copy alert to modal window
			modal.find('.modal-body').html(html.find('.alert'));

			// copy form to modal if we found it in server response
			if (newform.length > 0) {
				modal.find('.modal-body').append(newform);

				// initialize form fields and buttons
				initEditGroupForm(newform, modal);
			} else {
				
				setTimeout(function(){location.reload(true);}, 500);
			}
		}
	});
}

$(document).ready(function(){
	initJournal();
	initGroupSelector();
	initDateFields();
	initAddStudentPage();
	initEditStudentPage();
	initAddGroupPage();
	initEditGroupPage();
});