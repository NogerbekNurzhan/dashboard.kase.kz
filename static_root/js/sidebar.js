$(document).ready(function () {
	$('#sidebarMenuBtn').on('click', function () {
		$('.dashboard-wrapper nav.dashboard-sidebar').toggleClass('active');
		$('.dashboard-wrapper .dashboard-content .dashboard-container').toggleClass('active');
	});
});
$('#navbar').on('show.bs.collapse', function () {
	$('.dashboard-content').addClass('transparent');
});
$('#navbar').on('hide.bs.collapse', function () {
	$('.dashboard-content').removeClass('transparent');
});
function behaviorOfHeaderBtn(){
	if($(window).width()<768){
		$("#sidebarMenuBtn").click(function(){
			if($('.dashboard-sidebar').hasClass('active')){
				$('.navbar-toggle').prop('disabled', true);
				$('.dashboard-wrapper').addClass('disabled-dashboard-wrapper');
			}else{
				$('.navbar-toggle').prop('disabled', false);
				$('.dashboard-wrapper').removeClass('disabled-dashboard-wrapper');
			}
		});
	}
}
$(document).ready(behaviorOfHeaderBtn);
$(window).bind('resize', behaviorOfHeaderBtn);