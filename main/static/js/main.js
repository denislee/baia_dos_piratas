$('#searchForm').submit(function(e) {

	var q = $('.search-query');
	var loading = $('#loading'); 
	var alertMsg = $('#alertMsg');

	if (q.val().length == 0) {

		alertMsg.text('esquecendo de algo, amigo? :D');
		q.css('border', '1px solid red');
		e.preventDefault();

	} else {

		alertMsg.text('');
		q.css('border', '1px solid #ccc');
		loading.css('display', 'initial');

	}
	
});