$(document).ready(function() {
	$("#ce").toggle();
	$("#cece").toggle();
	$("#cebian").animate({
		"width": "63px",
		"word-spacing": "1px"
	}, 0);

	var contentHeight = document.body.scrollHeight,
		winHeight = window.innerHeight;
	if (winHeight > contentHeight) {
		$("footer").addClass("navbar-fixed-bottom");
	}


	$("#cebiankaiguan").on("click", function() {
		if ($("#cebiankaiguan").hasClass("glyphicon-menu-right") == true) {
			$("#cebiankaiguan").removeClass("glyphicon-menu-right");
			$("#cebiankaiguan").addClass("glyphicon-menu-left");
			$("#cebian").animate({
				"width": "200px",
			}, 0);
			$("#cebiankaiguan").animate({
				"left": "170px"
			}, 0);
			$("#cebianneirong").css("display", "block");
		} else {
			$("#cebiankaiguan").removeClass("glyphicon-menu-left");
			$("#cebiankaiguan").addClass("glyphicon-menu-right");
			$("#cebian").animate({
				"width": "63px",
			}, 100);
			$("#cebiankaiguan").animate({
				"left": "30px"
			}, 100);
			$("#cebianneirong").css("display", "none");

		}
	});
	
	$("#qiebiao").on("click",function(){
		$("#biao").css("display","block");
		$("#tiao").css("display","none");
	});
	
	$("#qiezhou").on("click",function(){
		$("#biao").css("display","none");
		$("#tiao").css("display","block");
	});
	



});
