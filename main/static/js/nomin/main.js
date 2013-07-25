
var form = $('#searchForm');

form.submit(function(e) {
	var q = $('.search-query'),
		loading = $('#loading'),
		alertMsg = $('#alertMsg');

	// if (q.val().length == 0) {
	// 	alertMsg.text('esquecendo de algo, amigo? :D');
	// 	q.css('border', '1px solid red');
	// 	// e.preventDefault();
	// } else {
	// 	alertMsg.text('');
	// 	q.css('border', '1px solid #ccc');
	// 	loading.css('display', 'block');
	// }
	// aways prevent to send, because he needs to choose by ajax request below.
	e.preventDefault();
});


$(document).ready(function() {

	var container = $('#movieList'),
		containerTemplate = $('#moviesListTemplate'),
		searchBar = $("#search");

	var q = $('.search-query'),
		loading = $('#loading'),
		alertMsg = $('#alertMsg');

	searchBar.focus();
	searchBar.keyup(function(e) {

		container.hide();

		$.get(
			"/s/?q="+escape(searchBar.val()),
			function(data){

				// parse to add a new field to json. (field to handlebars render image movie.)
				$.each(data['movies'], function(key, val) {
					data['movies'][key].picUrl = getImageUrl(val['pic']);
				});

			    renderJsonToTemplate(container, containerTemplate, data);

				$("tr.movie").click(function(){

					var name = $(this).children('.name').text(),
						movieId = this.id;

					url = '/?q=' + name + '&movieId=' + movieId;

					alertMsg.text('');
					q.css('border', '1px solid #ccc');
					loading.css('display', 'block');
					location.href=url;
					container.hide();
				});

			    container.show();
			}
		);

	});

});


function renderJsonToTemplate (container, containerTemplate, data) {
	// var json 			= JSON.parse(data); // convert text to json object
    var source = containerTemplate.html(); // load template from _cartTemplate.gsp
	var template = Handlebars.compile(source); // render template using Handlebars.js
	var html = template(data);

	container.html(html);
}


function getImageUrl(id) {
	if (id == 0) {
		return 'http://static.opensubtitles.org/gfx/empty_cover.jpg';
	}
	var pad = function (n, width, z) {
		z = z || '0';
		n = n + '';
		return n.length >= width ? n : new Array(width - n.length + 1).join(z) + n;
	}
	var createPath = function (id) {
		return id.substr(6,1) + "/" + id.substr(5,1) + "/" + id.substr(4,1) + "/" + id.substr(3,1);
	}
	var padId = pad(id,7);
	return 'http://static' + ((id % 9) + 1) + '.opensubtitles.org/gfx/thumbs/'+ createPath(padId) + "/" + padId + ".jpg";
}    
