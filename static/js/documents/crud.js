$(function () {
	var loadForm = function () {
		var btn = $(this);
		$.ajax({
			url: btn.attr("data-url"),
			type: 'get',
			dataType: 'json',
			success: function (data) {
				$("#document-modal .modal-content").html(data.html_form);
				fieldSettings();
				$("#document-modal").modal("show");
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
						if(typeof data.equal_data_add !== "undefined"){
							if(data.documents_exist){
								if(data.equal_data_add){
									$('#documents .dd-list').first().prepend(data.html_document);
								}
							}
							else{
								if(data.equal_data_add){
									window.location.reload();
								}
								else{
									$('#panel-body-year-tab').html(data.html_years);
								}
							}
						}
						if(typeof data.equal_tab !== "undefined"){
							if(data.documents_exist){
								if(data.equal_tab){
									$('#documents .dd-list').first().prepend(data.html_document);
								}
							}
							else{
								if(data.equal_tab){
									window.location.reload();
								}
								else{
									$('#panel-body-year-tab').html(data.html_tabs);
								}
							}
						}
						$("#user-action-message .user-action-message-description").html(success_message);
						$('#document-search').val('');
						$("#document-search-result").hide();
						$('#documents').show();
						activateTooltip();
						$("#document-modal").modal("hide");
						$("#user-action-message").fadeIn("slow");
						setTimeout(function() {$("#user-action-message").fadeOut("slow");}, 2000);
					}, 2500);
				}
				else {
					$("#document-modal .modal-content").html(data.html_form);
					fieldSettings();
					$("#documents-errors").fadeIn("slow");
					var error_message = "</br>";
					var json_string = JSON.stringify(data.form_errors);
					var json_object = jQuery.parseJSON(json_string);
					$.each(json_object, function(key, value){
						for (var i = 0; i < value.length; i++) {
							error_message += value[i] + "</br>";
						}
					});
					$("#documents-errors .error-description").html(error_message);
					setTimeout(function() {$("#documents-errors").fadeOut("slow");}, 10000);
				}
			},
			error: function (xhr, ajaxOptions, thrownError, data) {
				if(xhr.status==403) {
					window.location.reload();
				} else {
					$("#documents-errors").fadeIn("slow");
					$("#documents-errors .error-description").html(thrownError);
					setTimeout(function() {$("#documents-errors").fadeOut("slow");}, 10000);
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

						console.log(data);
						if(typeof data.equal_data_add !== "undefined"){
							if(data.documents_exist_start){
								if(data.equal_data_add){
									$('li[data-id='+data.document_id+']').replaceWith(data.html_document);
								}
								else{
									if(!data.documents_exist_end){
										window.location.reload();
									}
									else{
										$('#panel-body-year-tab').html(data.html_years);
										$('li[data-id='+data.document_id+']').remove();
									}
								}
							}
							else{
								if(!data.documents_exist_end){
									window.location.reload();
								}
								else{
									$('#panel-body-year-tab').html(data.html_years);
									$('li[data-id='+data.document_id+']').remove();
								}
							}
						}
						if(typeof data.equal_tab !== "undefined"){
							if(data.documents_exist_start){
								if(data.equal_tab){
									$('li[data-id='+data.document_id+']').replaceWith(data.html_document);
								}
								else{
									if(!data.documents_exist_end){
										window.location.reload();
									}
									else{
										$('#panel-body-year-tab').html(data.html_tabs);
										$('li[data-id='+data.document_id+']').remove();
									}
								}
							}
							else{
								if(!data.documents_exist_end){
									window.location.reload();
								}
								else{
									$('#panel-body-year-tab').html(data.html_tabs);
									$('li[data-id='+data.document_id+']').remove();
								}
							}
						}

						$("#user-action-message .user-action-message-description").html(success_message);
						$('#document-search').val('');
						$("#document-search-result").hide();
						$('#documents').show();
						activateTooltip();
						$("#document-modal").modal("hide");
						$("#user-action-message").fadeIn("slow");
						setTimeout(function() {$("#user-action-message").fadeOut("slow");}, 2000);
					}, 2500);
				}
				else {
					$("#document-modal .modal-content").html(data.html_form);
					fieldSettings();
					$("#documents-errors").fadeIn("slow");
					var error_message = "</br>";
					var json_string = JSON.stringify(data.form_errors);
					var json_object = jQuery.parseJSON(json_string);
					$.each(json_object, function(key, value){
						for (var i = 0; i < value.length; i++) {
							error_message += value[i] + "</br>";
						}
					});
					$("#documents-errors .error-description").html(error_message);
					setTimeout(function() {$("#documents-errors").fadeOut("slow");}, 10000);
				}
			},
			error: function (xhr, ajaxOptions, thrownError, data) {
				if(xhr.status==403) {
					window.location.reload();
				} else {
					$("#documents-errors").fadeIn("slow");
					$("#documents-errors .error-description").html(thrownError);
					setTimeout(function() {$("#documents-errors").fadeOut("slow");}, 10000);
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
						if(data.documents_exist){
							$('#documents').nestable('remove', data.document_id);
						}
						else{
							window.location.reload();
						}
						$("#user-action-message .user-action-message-description").html(success_message);
						$('#document-search').val('');
						$("#document-search-result").hide();
						$('#documents').show();
						activateTooltip();
						$("#document-modal").modal("hide");
						$("#user-action-message").fadeIn("slow");
						setTimeout(function() {$("#user-action-message").fadeOut("slow");}, 2000);
					}, 2500);
				}
				else {
					$("#document-modal .modal-content").html(data.html_form);
					fieldSettings();
					$("#documents-errors").fadeIn("slow");
					var error_message = "</br>";
					var json_string = JSON.stringify(data.form_errors);
					var json_object = jQuery.parseJSON(json_string);
					$.each(json_object, function(key, value){
						for (var i = 0; i < value.length; i++) {
							error_message += value[i] + "</br>";
						}
					});
					$("#documents-errors .error-description").html(error_message);
					setTimeout(function() {$("#documents-errors").fadeOut("slow");}, 10000);
				}
			},
			error: function (xhr, ajaxOptions, thrownError) {
				if(xhr.status==403) {
					window.location.reload();
				} else {
					$("#documents-errors").fadeIn("slow");
					$("#documents-errors .error-description").html(thrownError);
					setTimeout(function() {$("#documents-errors").fadeOut("slow");}, 10000);
				}
			},
			cache: false,
			contentType: false,
			processData: false,
		});
		return false;
	};

	function fieldSettings() {
		$('#tab').select2({
			'data': null
		});
		$('.custom-datetimepicker').datetimepicker({
			locale: 'ru',
			showClear: true,
			ignoreReadonly: true,
			icons: {
				time: "fa fa-calendar-o",
				date: "fa fa-calendar",
				up: "fa fa-arrow-up",
				down: "fa fa-arrow-down"
			},
		});
		$("#src_url").on("input", function() {
			$("#file-field-document").toggleClass("disabled-field", !!$('#src_url').val());
			$("#file-field-document").next("div.alert").toggleClass("disabled-field", !!$('#src_url').val());
		});
		$("#src").on("change", function() {
			$("#src_url").toggleClass("disabled-field", !!$('#src').val());
			$('label[for="src_url"]').toggleClass("disabled-field", !!$('#src').val());
		});
		$( "#file-field-clear-btn" ).click(function() {
			$("#src_url").removeClass("disabled-field");
			$('label[for="src_url"]').removeClass("disabled-field");
		});
	}

	$("#document-сreate-btn").on("click", loadForm);
	$("#document-modal").on("submit", ".document-create-form", function(e) {
		e.preventDefault();
		createForm.call(this, "Новый документ успешно создан!");
	});

	$("#documents .dd-list").on("click", ".document-edit-btn", loadForm);
	$("#document-modal").on("submit", ".document-edit-form", function(e) {
		e.preventDefault();
		editForm.call(this, "Данные успешно сохранены!");
	});

	$("#document-search-result").on("click", ".document-edit-btn", loadForm);

	$("#documents .dd-list").on("click", ".document-delete-btn", loadForm);
	$("#document-modal").on("submit", ".document-delete-form", function(e) {
		e.preventDefault();
		deleteForm.call(this, "Документ успешно удален!");
	});

	$("#document-search-result").on("click", ".document-delete-btn", loadForm);

	$('#document-modal').on('hidden.bs.modal', function () {
		$("#document-modal .modal-content").empty();
	});
});