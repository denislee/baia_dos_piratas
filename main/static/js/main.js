$('#searchForm').submit(function(e) {

	var q = $('.search-query');
	var loading = $('#loading'); 
	var alertMsg = $('#alertMsg');

	if (q.val().length == 0) {

		alertMsg.text('esquencedo de algo, amigo? :D');
		q.css('border', '2px solid red');
		e.preventDefault();

	} else {

		loading.css('display', 'initial');

	}
	
});