$(function () {
	var loadForm = function () {
		var btn = $(this);
		$.ajax({
			url: btn.attr("data-url"),
			type: 'get',
			dataType: 'json',
			success: function (data) {
				$("#section-indicator-modal .modal-content").html(data.html_form);
				fieldSettings();
				$("#section-indicator-modal").modal("show");
			},
			error: function (xhr, ajaxOptions, thrownError) {
				if(xhr.status==403) {
					window.location.reload();
				}
			},
		});
	};
	var saveIndicatorForm = function(success_message) {
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
						$('div[id=indicator-'+data.indicator_id+']').replaceWith(data.html_indicator);
						$("#user-action-message .user-action-message-description").html(success_message);
						$("#section-indicator-modal").modal("hide");
						$("#user-action-message").fadeIn("slow");
						setTimeout(function() {$("#user-action-message").fadeOut("slow");}, 2000);
					}, 2500);
				}
				else {
					$("#section-indicator-modal .modal-content").html(data.html_form);
					fieldSettings();
					$("#indicator-errors").fadeIn("slow");
					var error_message = "</br>";
					var json_string = JSON.stringify(data.form_errors);
					var json_object = jQuery.parseJSON(json_string);
					$.each(json_object, function(key, value){
						for (var i = 0; i < value.length; i++) {
							error_message += value[i] + "</br>";
						}
					});
					$("#indicator-errors .error-description").html(error_message);
					setTimeout(function() {$("#indicator-errors").fadeOut("slow");}, 10000);
				}
			},
			error: function (xhr, ajaxOptions, thrownError) {
				if(xhr.status==403) {
					window.location.reload();
				} else {
					$("#indicator-errors").fadeIn("slow");
					$("#indicator-errors .error-description").html(thrownError);
					setTimeout(function() {$("#indicator-errors").fadeOut("slow");}, 10000);
				}
			},
			cache: false,
			contentType: false,
			processData: false,
		});
		return false;
	};
	var saveSectionForm = function(success_message) {
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
						$section = $('div[data-id='+data.section_id+']')
						if($section.hasClass('panel-success')){
							$section.removeClass('panel-success');
							$section.addClass('panel-default');
						}
						else if($section.hasClass('panel-default')){
							$section.removeClass('panel-default');
							$section.addClass('panel-success');
						}
						$section.children().first().replaceWith(data.html_section_header);
						// START: Click event to open/close button of current section
						$div = $section.find(".panel-body").first();
						$btn = $section.find(".open-close-panel-btn").first();
						$btn.bind("click", {target: $div}, function(e) {
							$section.parent().parent().find(".open-close-icon").first().toggleClass("fa-expand fa-compress");
							e.data.target.slideToggle();
						});
						$div.hide();
						// END: Click event to open/close button of current section
						$("#user-action-message .user-action-message-description").html(success_message);
						$("#section-indicator-modal").modal("hide");
						$("#user-action-message").fadeIn("slow");
						setTimeout(function() {$("#user-action-message").fadeOut("slow");}, 2000);
					}, 2500);
				}
				else {
					$("#section-indicator-modal .modal-content").html(data.html_form);
					fieldSettings();
					$("#indicator-errors").fadeIn("slow");
					var error_message = "</br>";
					var json_string = JSON.stringify(data.form_errors);
					var json_object = jQuery.parseJSON(json_string);
					$.each(json_object, function(key, value){
						for (var i = 0; i < value.length; i++) {
							error_message += value[i] + "</br>";
						}
					});
					$("#indicator-errors .error-description").html(error_message);
					setTimeout(function() {$("#indicator-errors").fadeOut("slow");}, 10000);
				}
			},
			error: function (xhr, ajaxOptions, thrownError) {
				if(xhr.status==403) {
					window.location.reload();
				} else {
					$("#indicator-errors").fadeIn("slow");
					$("#indicator-errors .error-description").html(thrownError);
					setTimeout(function() {$("#indicator-errors").fadeOut("slow");}, 10000);
				}
			},
			cache: false,
			contentType: false,
			processData: false,
		});
		return false;
	};
	function fieldSettings(){
		$('#fini_code_chrt_type').select2({minimumResultsForSearch: Infinity,});
		$('#trandtype').select2({minimumResultsForSearch: Infinity,});
	}
	$('#sections .panel').on('click', '.section-edit-btn', loadForm);
	$("#section-indicator-modal").on("submit", ".section-edit-form", function(e) {e.preventDefault();saveSectionForm.call(this, "Данные успешно сохранены!");});
	$('.list-group').on('click', '.indicator-edit-btn', loadForm);
	$("#section-indicator-modal").on("submit", ".indicator-edit-form", function(e) {e.preventDefault();saveIndicatorForm.call(this, "Данные успешно сохранены!");});
});