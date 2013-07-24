
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


var suggestCallBack; // global var for autocomplete jsonp

$(document).ready(function () {

	$("#search").focus();

	$("#search").autocomplete({
		source: function(request, response) {
			$.getJSON("http://suggestqueries.google.com/complete/search?callback=?",
				{ 
					"hl":"en",// Language
					"ds":"yt",// Restrict lookup to youtube
					"jsonp":"suggestCallBack", // jsonp callback function name
					"q":request.term, // query term
					"client":"youtube" // force youtube style response, i.e. jsonp
				}
				);
			suggestCallBack = function (data) {
				
				var suggestions = [];

				$.each(data[1], function(key, val) {
					suggestions.push({"value":val[0]});
				});

				suggestions.length = 5; // prune suggestions list to only 5 items
				response(suggestions);
			};
		},
	});
});


