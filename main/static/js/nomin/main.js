
var form = $('#searchForm');

form.submit(function(e) {
	var q = $('.search-query'),
		loading = $('#loading'),
		alertMsg = $('#alertMsg');

	if (q.val().length == 0) {
		alertMsg.text('esquecendo de algo, amigo? :D');
		q.css('border', '1px solid red');
		e.preventDefault();
	} else {
		alertMsg.text('');
		q.css('border', '1px solid #ccc');
		loading.css('display', 'block');
	}
});


$(document).ready(function () {
	$("#search").focus();
	$("#search").autocomplete({
		source: function(request, response) {
			$.getJSON("/s/?q="+escape($('#search').val()),
			function(data){
				var suggestions = [];
			    $.each(data, function (key, val) {
					suggestions.push({"value":val['name']});
			    });
				// suggestions.length = 5; // prune suggestions list to only 5 items
				response(suggestions);
			});
		},
	});
});

