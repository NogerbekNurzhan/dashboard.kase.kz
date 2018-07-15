$(function () {
	var loadForm = function () {
		var btn = $(this);
		$.ajax({
			url: btn.attr("data-url"),
			type: 'get',
			dataType: 'json',
			success: function (data) {
				$("#faq-modal .modal-content").html(data.html_form);
				fieldSettings();
				$("#faq-modal").modal("show");
			},
			error: function (xhr, ajaxOptions, thrownError) {
				if(xhr.status==403) {
					window.location.reload();
				}
			},
		});
	};

	var createForm = function(success_message) {
		var form = $(this);
		var formData = new FormData(form[0]);
		$.ajax({
			url: form.attr("action"),
			data: formData,
			type: form.attr("method"),
			dataType: 'json',
			success: function (data) {
				if (data.form_is_valid) {
					$("#loader").show("slow");
					setTimeout(function() {
						$("#loader").hide("slow");
						if(data.question_exist){
							$("#questions").html(data.html_questions);
						}
						else{
							$('#questions').first().prepend(data.html_question);
						}
						$("#questions").sortable("refresh");
						$("#questions").sortable("option", "disabled", $("#questions .list-group-item").length==1);
						$("#user-action-message .user-action-message-description").html(success_message);
						$('#questions').show();
						$("#faq-modal").modal("hide");
						$("#user-action-message").fadeIn("slow");
						setTimeout(function() {$("#user-action-message").fadeOut("slow");}, 2000);
					}, 2500);
				}
				else {
					$("#faq-modal .modal-content").html(data.html_form);
					fieldSettings();
					$("#faq-errors").fadeIn("slow");
					var error_message = "</br>";
					var json_string = JSON.stringify(data.form_errors);
					var json_object = jQuery.parseJSON(json_string);
					$.each(json_object, function(key, value){
						for (var i = 0; i < value.length; i++) {
							error_message += value[i] + "</br>";
						}
					});
					$("#faq-errors .error-description").html(error_message);
					setTimeout(function() {$("#faq-errors").fadeOut("slow");}, 10000);
				}
			},
			error: function (xhr, ajaxOptions, thrownError, data) {
				if(xhr.status==403) {
					window.location.reload();
				} else {
					$("#faq-errors").fadeIn("slow");
					$("#faq-errors .error-description").html(thrownError);
					setTimeout(function() {
						$("#faq-errors").fadeOut("slow");
					}, 10000);
				}
				if(xhr.status==302){
					window.location.reload();
				}
			},
			cache: false,
			contentType: false,
			processData: false,
		});
		return false;
	};

	var deleteForm = function(success_message) {
		var form = $(this);
		var formData = new FormData(form[0]);
		$.ajax({
			url: form.attr("action"),
			data: formData,
			type: form.attr("method"),
			dataType: 'json',
			success: function (data) {
				if (data.form_is_valid) {
					$("#loader").show("slow");
					setTimeout(function() {
						$("#loader").hide("slow");
						if(data.question_exist){
							$('div[data-id='+data.question_id+']').remove();
						}
						else{
							$("#questions").html(data.html_questions);
						}
						$("#user-action-message .user-action-message-description").html(success_message);
						$("#faq-modal").modal("hide");
						$("#user-action-message").fadeIn("slow");
						setTimeout(function() {
							$("#user-action-message").fadeOut("slow");
						}, 2000);
					}, 2500);
				}
				else {
					$("#faq-modal .modal-content").html(data.html_form);
				}
			},
			cache: false,
			contentType: false,
			processData: false,
		});
		return false;
	};

	var editForm = function(success_message) {
		var form = $(this);
		var formData = new FormData(form[0]);
		$.ajax({
			url: form.attr("action"),
			data: formData,
			type: form.attr("method"),
			dataType: 'json',
			success: function (data) {
				if (data.form_is_valid) {
					$("#loader").show("slow");
					setTimeout(function() {
						$("#loader").hide("slow");
						$('div[data-id='+data.question_id+']').replaceWith(data.html_question);
						$("#user-action-message .user-action-message-description").html(success_message);
						$('#questions').show();
						$("#faq-modal").modal("hide");
						$("#user-action-message").fadeIn("slow");
						setTimeout(function() {$("#user-action-message").fadeOut("slow");}, 2000);
					}, 2500);
				}
				else {
					$("#faq-modal .modal-content").html(data.html_form);
					fieldSettings();
					$("#faq-errors").fadeIn("slow");
					var error_message = "</br>";
					var json_string = JSON.stringify(data.form_errors);
					var json_object = jQuery.parseJSON(json_string);
					$.each(json_object, function(key, value){
						for (var i = 0; i < value.length; i++) {
							error_message += value[i] + "</br>";
						}
					});
					$("#faq-errors .error-description").html(error_message);
					setTimeout(function() {$("#faq-errors").fadeOut("slow");}, 10000);
				}
			},
			error: function (xhr, ajaxOptions, thrownError, data) {
				if(xhr.status==403) {
					window.location.reload();
				} else {
					$("#faq-errors").fadeIn("slow");
					$("#faq-errors.error-description").html(thrownError);
					setTimeout(function() {
						$("#faq-errors").fadeOut("slow");
					}, 10000);
				}
				if(xhr.status==302){
					window.location.reload();
				}
			},
			cache: false,
			contentType: false,
			processData: false,
		});
		return false;
	};

	function fieldSettings() {
		$('#title').on('mouseup', function(){
			autosize(document.querySelectorAll('#title'));
		});
		$('#answer').on('mouseup', function(){
			autosize(document.querySelectorAll('#answer'));
		});
		$('.custom-datetimepicker').datetimepicker({
            locale: 'ru',
            maxDate: moment(),
            showClear: true,
            ignoreReadonly: true,
            format: 'DD.MM.YYYY',
            icons: {time: "fa fa-calendar-o", date: "fa fa-calendar", up: "fa fa-arrow-up", down: "fa fa-arrow-down"},
        });
	}

	$("#faq-сreate-btn").click(loadForm);
	$("#faq-modal").on("submit", ".faq-create-form", function(e) {
		e.preventDefault();
		createForm.call(this, "Новый вопрос успешно создан!");
	});

	$("#questions").on("click", ".faq-delete-btn", loadForm);
	$("#faq-modal").on("submit", ".faq-delete-form", function(e) {
		e.preventDefault();
		deleteForm.call(this, "Вопрос успешно удален!");
	});

	$("#questions").on("click", ".faq-edit-btn", loadForm);
	$("#faq-modal").on("submit", ".faq-edit-form", function(e) {
		e.preventDefault();
		editForm.call(this, "Данные успешно сохранены!");
	});
});