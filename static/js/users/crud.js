$(function () {
    var loadForm = function () {
        var btn = $(this);
        $.ajax({
            url: btn.attr("data-url"),
            type: 'get',
            dataType: 'json',
            success: function (data) {
                $("#user-modal .modal-content").html(data.html_form);
                customFields();
                $("#user-modal").modal("show");
            },
            error: function (xhr, ajaxOptions, thrownError) {
                if(xhr.status==403) {
                    location.href = '/user/';
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
            success: function (data, textStatus, xhr) {
                if (data.form_is_valid) {
                    $("#loader").show("slow");
                    $('body').tooltip({selector:'[rel=tooltip]'});
                    setTimeout(function() {
                        $("#loader").hide("slow");
                        $("#users").html(data.html_users);
                        $("#user-action-message .user-action-message-description").html(success_message);
                        $("#user-modal").modal("hide");
                        $("#user-action-message").fadeIn("slow");
                        setTimeout(function() {$("#user-action-message").fadeOut("slow");}, 2000);
                        $('#search-users').val('');
                    }, 2500);
                }
                else {
                    $("#user-modal .modal-content").html(data.html_form);
                    customFields();
                    $("#user-errors").fadeIn("slow");
                    var error_message = "</br>";
                    var json_string = JSON.stringify(data.form_errors);
                    var json_object = jQuery.parseJSON(json_string);
                    $.each(json_object, function(key, value){
                        for (var i = 0; i < value.length; i++) {
                            error_message += value[i] + "</br>";
                        }
                    });
                    $("#user-errors .error-description").html(error_message);
                    setTimeout(function() {$("#user-errors").fadeOut("slow");}, 10000);
                }
            },
            error: function (xhr, ajaxOptions, thrownError) {
                if(xhr.status==403) {
                    location.href = '/user/';
                } else {
                    $("#user-errors").fadeIn("slow")
                    $("#user-errors .error-description").html(thrownError);
                    setTimeout(function() {$("#user-errors").fadeOut("slow");}, 10000);
                }
            },
            cache: false,
            contentType: false,
            processData: false,
        });
        return false;
    };
    
    function customFields() {
        $('.custom-datetimepicker').datetimepicker({
            locale: 'ru', maxDate: moment(), showClear: true, ignoreReadonly: true,
            icons: {time: "fa fa-calendar-o", date: "fa fa-calendar", up: "fa fa-arrow-up", down: "fa fa-arrow-down"},
        });
        $('#user_permissions').select2();
        $("#new_password").keyup(function() {passwordStrength($(this).val());});
        if($('#user_role_1').attr("checked")=="checked"){
            $('.user-permissions-wrapper').show();
        }
        else{
            $('.user-permissions-wrapper').hide();
        }
        $('input[type="radio"][name="user_role"]').click(function () {
            if($(this).attr("value")=="1"){$('.user-permissions-wrapper').show();}else{$('.user-permissions-wrapper').hide();}
        });
    }
 
    $("#user-create-btn").click(loadForm);
    $("#user-modal").on("submit", ".user-create-form", function(e) {e.preventDefault(); saveForm.call(this, "Новый пользователь успешно создан!");});
 
    $("#users").on("click", ".user-edit-btn", loadForm);
    $("#user-modal").on("submit", ".user-edit-form", function(e) {e.preventDefault(); saveForm.call(this, "Данные пользователя успешно сохранены!");});
 
    $("#users").on("click", ".user-delete-btn", loadForm);
    $("#user-modal").on("submit", ".user-delete-form", function(e) {e.preventDefault(); saveForm.call(this, "Пользователь успешно удален!");});
 
    $("#users").on("click", ".user-password-change-btn", loadForm);
    $("#user-modal").on("submit", ".user-password-change-form", function(e) {e.preventDefault(); saveForm.call(this, "Пароль пользователя успешно обновлен!");});
 
    $('#user-modal').on('hidden.bs.modal', function () {$("#user-modal .modal-content").empty();});
});