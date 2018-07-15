function passwordStrength(password) { /* Password strength indicator */
	var desc = [{'width':'0px'}, {'width':'20%'}, {'width':'40%'}, {'width':'60%'}, {'width':'80%'}, {'width':'100%'}];
	var descClass = ['', 'progress-bar-danger', 'progress-bar-danger', 'progress-bar-warning', 'progress-bar-success', 'progress-bar-success'];
	var score = 0;
	if (password.length > 6) score++; // if password bigger than 6 give 1 point
	if ((password.match(/[a-z]/)) && (password.match(/[A-Z]/))) score++; // if password has both lower and uppercase characters give 1 point  
	if (password.match(/\d+/)) score++; // if password has at least one number give 1 point
	if ( password.match(/.[!,@,#,$,%,^,&,*,?,_,~,-,(,)]/) ) score++; // if password has at least one special caracther give 1 point
	if (password.length > 10) score++; // if password bigger than 12 give another 1 point
	$("#password-strength-progress-bar").removeClass(descClass[score-1]).addClass(descClass[score]).css(desc[score]); // display indicator
}
$("#user-modal").on("click", "#password-toggle-btn", function(){ // Hide-Show Password
	var fa = $(this).parent().find(".fa");
	if(fa.hasClass("fa-eye-slash")){
		fa.addClass("fa-eye").removeClass("fa-eye-slash");
		$("#new_password").prop('type','text');
	}else{
		fa.addClass("fa-eye-slash").removeClass("fa-eye");
		$("#new_password").prop('type','password');
	}
});