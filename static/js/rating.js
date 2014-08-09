$(function() {
	$( ".starbucks > span" ).click(function() {
		$("#value").val($(this).attr("data-id"));

		var val = $(this).attr("data-id");
		
		$(this).parent().children().removeClass("hover");
		
		for(var i=0; i <= val; i++) {
			$(this).parent().children(".rating-" + i).text("★");
		}
		
		for(var i=val*1+1; i <= 5; i++) {
			$(this).parent().children(".rating-" + i).text("☆");
		}
	});
});
 	
$(function() {
    
  for(var i=5; i >= (5-$("#rating-value").text()); i--) {
			$($(".starbucks-inactive" ).children().get(i-1)).text("★");
	}
	
});
