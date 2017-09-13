/*
 * Script start location: http://www.twirpx.com , the main page
 *
 */

var twirpx = new Object();

twirpx.pi = 0;
twirpx.max_pi = -1;
twirpx.query = 'мансийский';
twirpx.sart = $('[name="__SART"]').val();
twirpx.all_links = [];


twirpx.messages = {
	start_search: function () { return 'Search [STARTED]' },
	parse_links: function () { return 'Links parsing [STARTED]' },
	next_: function (index) { return 'Tab ' + (index + 1) + ' requested' },
	next_break: function () { return 'twirpx.next [STOPPED]' }
};
twirpx.message = twirpx.messages;

twirpx.parse_links = function (data) {
	$(data).find('.file-link').each(function (index) {
	  twirpx.all_links.push($(this).attr('href'));
	});
};

twirpx.print_links = function () {
	for (var i = 0; i < twirpx.all_links.length; i ++) {
		console.log(twirpx.all_links[i]);
	}
};

twirpx.next = function () {
	twirpx.sart = $('[name="__SART"]').val();
	if ( twirpx.pi < twirpx.max_pi ) {
		$.post('/search/', {
			SearchCID: 0,
			SearchECID: 0,
			SearchQuery: twirpx.query,
			SearchScope: 'site',
			SearchUID: 0,
			'__SART': twirpx.sart,
			pi: twirpx.pi
		},
		function (data) {
			twirpx.pi ++;
			twirpx.parse_links(data);
			console.log(twirpx.message.next_(twirpx.pi));
			twirpx.next();
		});
	}
	else console.log(twirpx.messages.next_break());
};

$.post('/search/', {
	SearchQuery: twirpx.query,
	SearchScope: 'site',
	'__SART': twirpx.sart
},
function (data) {
	twirpx.max_pi = Number($(data).find(".pager li a").last().html());
	twirpx.parse_links(data);
	twirpx.pi = 1;
	console.log(twirpx.message.next_(twirpx.pi));
	twirpx.next();
});
