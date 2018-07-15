$(function () {
	var loadForm = function () {
		var btn = $(this);
		$.ajax({
			url: btn.attr("data-url"),
			type: 'get',
			dataType: 'json',
			success: function (data) {
				$("#event-modal .modal-content").html(data.html_form);
				fieldSettings();
				$("#event-modal").modal("show");
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
						if(data.event_exist){
							if(data.equal_event_data){
								$('#events').first().prepend(data.html_event);
							}
							else{
								$('#panel-body-language-year').html(data.html_years);
							}
						}
						else{
							if(data.equal_event_data){
								$("#events").html(data.html_events);
								$('#panel-body-language-year').html(data.html_years);
							}
							else{
								$('#panel-body-language-year').html(data.html_years);
							}
						}
						$("#user-action-message .user-action-message-description").html(success_message);
						$('#events').show();
						$("#event-modal").modal("hide");
						$("#user-action-message").fadeIn("slow");
						setTimeout(function() {$("#user-action-message").fadeOut("slow");}, 2000);
					}, 2500);
				}
				else {
					$("#event-modal .modal-content").html(data.html_form);
					fieldSettings();
					$("#event-errors").fadeIn("slow");
					var error_message = "</br>";
					var json_string = JSON.stringify(data.form_errors);
					var json_object = jQuery.parseJSON(json_string);
					$.each(json_object, function(key, value){
						for (var i = 0; i < value.length; i++) {
							error_message += value[i] + "</br>";
						}
					});
					$("#event-errors .error-description").html(error_message);
					setTimeout(function() {$("#event-errors").fadeOut("slow");}, 10000);
				}
			},
			error: function (xhr, ajaxOptions, thrownError, data) {
				if(xhr.status==403) {
					window.location.reload();
				} else {
					$("#event-errors").fadeIn("slow");
					$("#event-errors.error-description").html(thrownError);
					setTimeout(function() {
						$("#event-errors").fadeOut("slow");
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
						if(data.event_exist){
							$('div[data-id='+data.event_id+']').remove();
						}
						else{
							$("#events").html(data.html_events);
							$('#panel-body-language-year').html(data.html_years);
						}
						$("#user-action-message .user-action-message-description").html(success_message);
						$("#event-modal").modal("hide");
						$("#user-action-message").fadeIn("slow");
						setTimeout(function() {
							$("#user-action-message").fadeOut("slow");
						}, 2000);
					}, 2500);
				}
				else {
					$("#event-modal .modal-content").html(data.html_form);
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
						$('div[data-id='+data.event_id+']').replaceWith(data.html_event);
						$("#user-action-message .user-action-message-description").html(success_message);
						$('#events').show();
						$("#event-modal").modal("hide");
						$("#user-action-message").fadeIn("slow");
						setTimeout(function() {$("#user-action-message").fadeOut("slow");}, 2000);
					}, 2500);
				}
				else {
					$("#event-modal .modal-content").html(data.html_form);
					fieldSettings();
					$("#event-errors").fadeIn("slow");
					var error_message = "</br>";
					var json_string = JSON.stringify(data.form_errors);
					var json_object = jQuery.parseJSON(json_string);
					$.each(json_object, function(key, value){
						for (var i = 0; i < value.length; i++) {
							error_message += value[i] + "</br>";
						}
					});
					$("#event-errors .error-description").html(error_message);
					setTimeout(function() {$("#event-errors").fadeOut("slow");}, 10000);
				}
			},
			error: function (xhr, ajaxOptions, thrownError, data) {
				if(xhr.status==403) {
					window.location.reload();
				} else {
					$("#event-errors").fadeIn("slow");
					$("#event-errors.error-description").html(thrownError);
					setTimeout(function() {
						$("#event-errors").fadeOut("slow");
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

	var eventImageDeleteForm = function(success_message) {
		var form = $(this);
		var formData = new FormData(form[0]);
		$.ajax({
			url: form.attr("action"),
			data: formData,
			type: form.attr("method"),
			dataType: 'json',
			success: function (data) {
				if (data.form_is_valid) {
					$("#event-modal .event-image-delete-form .modal-body").html(data.html_images);
					$(".img-check").click(function(){
						$(this).toggleClass("image-check");
						$(this).parent().toggleClass("visiable-image");
					});
					var checkboxes = $(".checkboxes");
					butt = $("#event-delete-images-btn");
					checkboxes.click(function() {
						butt.attr("disabled", !checkboxes.is(":checked"));
					});
					$('[data-toggle="tooltip"]').tooltip();
					$("#event-modal").on("submit", ".event-image-delete-form", eventImageDeleteForm);
				}
				else {
					$("#event-modal .modal-content").html(data.html_form);
					fieldSettings();
					$("#event-errors").fadeIn("slow");
					var error_message = "</br>";
					var json_string = JSON.stringify(data.form_errors);
					var json_object = jQuery.parseJSON(json_string);
					$.each(json_object, function(key, value){
						for (var i = 0; i < value.length; i++) {
							error_message += value[i] + "</br>";
						}
					});
					$("#event-errors .error-description").html(error_message);
					setTimeout(function() {$("#event-errors").fadeOut("slow");}, 10000);
				}
			},
			error: function (xhr, ajaxOptions, thrownError, data) {
				if(xhr.status==403) {
					window.location.reload();
				} else {
					$("#event-errors").fadeIn("slow");
					$("#event-errors.error-description").html(thrownError);
					setTimeout(function() {
						$("#event-errors").fadeOut("slow");
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
		autosize(document.querySelectorAll('.custom-body-textarea'));
		$(".textarea-wrapper").on("click", ".textarea-icon", function () {
			$(".textarea-icon").toggleClass("fa-expand fa-compress");
			$(this).closest('.modal').toggleClass('fullscreen');
			$(this).closest('.textarea-wrapper').toggleClass('fullscreen');
			$("span.cr").toggleClass("invisible");
			$('#event_date').toggleClass("invisible");
			$('#image-form-group').toggleClass("invisible");
			$('#image-field-event').toggleClass("invisible");
			$('.event-image-delete-form').toggleClass("invisible");
			$(".custom-body-textarea").toggleClass("fullscreen");
		});
		$(".textarea-wrapper").on("click", ".fa-expand", function () {autosize.destroy(document.querySelectorAll('.custom-body-textarea'));});
		$(".textarea-wrapper").on("click", ".fa-compress", function () {autosize(document.querySelectorAll('.custom-body-textarea'));});
		$("#event-modal").on("focus", ".textarea-wrapper textarea", function () {autosize.update(document.querySelectorAll('.textarea-wrapper textarea'));});
		$('.body-summernote').summernote({
			height: 200,
			lang: 'ru-RU',
			toolbar: [
				['font', ['bold', 'italic', 'underline', 'clear']],
				['para', ['ul', 'ol']],
				['insert', ['link']],
				['view', ['fullscreen', 'codeview']],
			],
			codemirror: {
				lineNumbers: true,
				theme: 'monokai',
			},
			disableResizeEditor: true,
			dialogsInBody: true,
			dialogsFade: true,
		});
		$(".note-toolbar").on("click", ".btn-fullscreen", function () {
			$(this).closest('.modal').toggleClass('fullscreen');
			$(this).closest('.note-editor').toggleClass('custom-note-editor');
		});
		$('.btn-fullscreen').attr('title', ''); /* Bug with tooltip of .btn-fullscreen in Mozilla Firefox */
		$('form.event-create-form .custom-datetimepicker').datetimepicker({
            locale: 'ru', showClear: true, ignoreReadonly: true, format: 'DD.MM.YYYY',
            icons: {date: "fa fa-calendar", up: "fa fa-arrow-up", down: "fa fa-arrow-down"},
        });
    	$(".img-check").click(function(){
			$(this).toggleClass("image-check");
			$(this).parent().toggleClass("visiable-image");
		});
		var checkboxes = $(".checkboxes");
		butt = $("#event-delete-images-btn");
		checkboxes.click(function() {
			butt.attr("disabled", !checkboxes.is(":checked"));
		});
		$('[data-toggle="tooltip"]').tooltip();
	}

	$("#event-сreate-btn").click(loadForm);
	$("#event-modal").on("submit", ".event-create-form", function(e) {
		e.preventDefault();
		createForm.call(this, "Новое событие успешно создано!");
	});

	$("#events").on("click", ".event-delete-btn", loadForm);
	$("#event-modal").on("submit", ".event-delete-form", function(e) {
		e.preventDefault();
		deleteForm.call(this, "Событие успешно удален!");
	});

	$("#events").on("click", ".event-edit-btn", loadForm);
	$("#event-modal").on("submit", ".event-edit-form", function(e) {
		e.preventDefault();
		editForm.call(this, "Данные успешно сохранены!");
	});

	$("#event-modal").on("submit", ".event-image-delete-form", eventImageDeleteForm);
});