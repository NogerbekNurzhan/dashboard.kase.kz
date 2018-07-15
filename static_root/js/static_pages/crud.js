$(function () {
	var loadForm = function () {
		var btn = $(this);
		$.ajax({
			url: btn.attr("data-url"),
			type: 'get',
			dataType: 'json',
			success: function (data) {
				$("#static-page-modal .modal-content").html(data.html_form);
				textArea();
				$("#static-page-modal").modal("show");
			},
			error: function (xhr, ajaxOptions, thrownError) {
				if(xhr.status==403) {
					location.href = '/static_page/';
				}
			},
		});
	};

	var saveForm = function(success_message) {
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
					$('body').tooltip({selector:'[rel=tooltip]'});
					setTimeout(function() {
						$("#loader").hide("slow");
						$("#static-pages").html(data.html_static_pages);
						$("#static-pages").sortable("refresh");
						$("#static-pages").sortable("option", "disabled", $("#static-pages .list-group-item").length == 1);
						$("#user-action-message .user-action-message-description").html(success_message);
						$("#static-page-modal").modal("hide");
						$("#user-action-message").fadeIn("slow");
						setTimeout(function() {$("#user-action-message").fadeOut("slow");}, 2000);
						$('#search-static-pages').val('');
					}, 2500);
				}
				else {
					$("#static-page-modal .modal-content").html(data.html_form);
					textArea();
					$("#static-pages-errors").fadeIn("slow");
					var error_message = "</br>";
					var json_string = JSON.stringify(data.form_errors);
					var json_object = jQuery.parseJSON(json_string);
					$.each(json_object, function(key, value){
						for (var i = 0; i < value.length; i++) {
							error_message += value[i] + "</br>";
						}
					});
					$("#static-pages-errors .error-description").html(error_message);
					setTimeout(function() {$("#static-pages-errors").fadeOut("slow");}, 10000);
				}
			},
			error: function (xhr, ajaxOptions, thrownError) {
				if(xhr.status==403) {
					location.href = '/static_page/';
				} else {
					$("#static-pages-errors").fadeIn("slow")
					$("#static-pages-errors .error-description").html(thrownError);
					setTimeout(function() {$("#static-pages-errors").fadeOut("slow");}, 10000);
				}
			},
			cache: false,
			contentType: false,
			processData: false,
		});
		return false;
	};
	
	function textArea() {
		autosize(document.querySelectorAll('.custom-body-textarea'));
		$(".textarea-wrapper").on("click", ".textarea-icon", function () {
			$(".textarea-icon").toggleClass("fa-expand fa-compress");
			$(this).closest('.modal').toggleClass('fullscreen');
			$(this).closest('.textarea-wrapper').toggleClass('fullscreen');
			$("span.cr").toggleClass("invisible");
			$(".custom-body-textarea").toggleClass("fullscreen");
		});
		$(".textarea-wrapper").on("click", ".fa-expand", function () {autosize.destroy(document.querySelectorAll('.custom-body-textarea'));});
		$(".textarea-wrapper").on("click", ".fa-compress", function () {autosize(document.querySelectorAll('.custom-body-textarea'));});
		$("#static-page-modal").on("focus", ".textarea-wrapper textarea", function () {autosize.update(document.querySelectorAll('.textarea-wrapper textarea'));});
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
	}

	$("#static-page-create-btn").click(loadForm);
	$("#static-page-modal").on("submit", ".static-page-create-form", function(e) {e.preventDefault(); saveForm.call(this, "Новая статическая страница успешно создана!");});

	$("#static-pages").on("click", ".static-page-edit-btn", loadForm);
	$("#static-page-modal").on("submit", ".static-page-edit-form", function(e) {e.preventDefault(); saveForm.call(this, "Данные успешно сохранены!");});

	$("#static-pages").on("click", ".static-page-delete-btn", loadForm);
	$("#static-page-modal").on("submit", ".static-page-delete-form", function(e) {e.preventDefault(); saveForm.call(this, "Статическая страница успешно удалена!");});

	$('#static-page-modal').on('hidden.bs.modal', function () {$("#static-page-modal .modal-content").empty();});
});