$( "#subscribe-btn" ).click(function() {
	$.post( "/api/subscribe", $('#subscribe-form').serialize(), function(info) {
		if (info['subscribe'] == 'success'){
			$('#subscribe-success').show();
			$('#subscribe-model').modal('hide');
		} else {
			$('#subscribe-failed').show();
			$('#subscribe-model').modal('hide');
		}
	});
});
$( "#unsubscribe-link" ).click(function() {
	$.post( "/api/unsubscribe", $('#subscribe-form').serialize(), function(info) {
		if (info['unsubscribe'] == 'success'){
			$('#unsubscribe-success').show();
			$('#subscribe-model').modal('hide');
		} else {
			$('#unsubscribe-failed').show();
			$('#subscribe-model').modal('hide');
		}
	});
});
$( document ).ready(function() {
	var url = new URL(window.location.href);
	var email = url.searchParams.get('email');
	if (email && url.searchParams.get('unsubscribe')){
		$('#subscribe-model').modal('show');
		$('#subscribe-email').val(email);
	}
});