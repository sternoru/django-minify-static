$(function(){
	$('#fade').click(function(){
		$('.sample-text').fadeIn(3000, function(){
			$(this).fadeOut(3000);
		});
	})
})
