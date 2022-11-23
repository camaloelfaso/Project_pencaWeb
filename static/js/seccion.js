$(document).ready(function(){
	var estado = false;
	$('#btn-toggle-fixture').on('click',function(){
		$('#section-Grupos').slideToggle();
		if (estado == true) {
			$(this).text("Ver Grupos");
            $('#section-Fixture').slideToggle();
			$('body').css({
				"overflow": "auto" 
			});
			estado = false;
		} else {
			$(this).text("Ver Fixture");
            $('#section-Fixture').slideToggle();
			$('body').css({
				"overflow": "auto"
			});
			estado = true;
		}
	});

	$('#btn-toggle-PencaHome').on('click',function(){
		$('#penca_sist_puntos').slideToggle();
		if (estado == true) {
			$(this).text("Ver sistema de puntuación");
            $('#penca_Ranking').slideToggle();
			$('body').css({
				"overflow": "auto"
			});
			estado = false;
		} else {
			$(this).text("Ver Ranking");
            $('#penca_Ranking').slideToggle();
			$('body').css({
				"overflow": "auto"
			});
			estado = true;
		}
	});    
});