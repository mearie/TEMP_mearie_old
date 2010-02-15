String.prototype.zfill = function(n) {
	var s = this;
	while (s.length < n) s = '0' + s;
	return s;
};

String.prototype.cut = function(width, trail) {
	if (typeof trail == 'undefined') trail = '…';
	var w = 0;
	for (var i = 0; i < this.length; ++i) {
		w += (this.charAt(i).match(/[\u3000-\u9fff\uac00-\ud7ff\uf900-\ufaff]/) ? 2 : 1);
		if (w > width) return this.substring(0, i) + trail;
	}
	return this;
}

Number.prototype.zfill = function(n) {
	return this.toString().zfill(n);
}

Date.prototype.setISO8601 = function(s) {
	var m = s.match(/^(\d{4})(-(\d\d)(-(\d\d)(T(\d\d):(\d\d)(:(\d\d)(\.\d+)?)?)?)?)?(Z|([-+])(\d\d):(\d\d))?$/);
	if (!m) throw Error('invalid ISO 8601 string');

	var date = new Date(m[1], 0, 1);
	if (m[3]) date.setMonth(m[3] - 1);
	if (m[5]) date.setDate(m[5]);
	if (m[7]) date.setHours(m[7]);
	if (m[8]) date.setMinutes(m[8]);
	if (m[10]) date.setSeconds(m[10]);
	if (m[11]) date.setMilliseconds(parseFloat('0'+m[11]) * 1000);
	var offset = 0;
	if (m[13]) {
		offset = m[14] * 60 + parseInt(m[15]);
		if (m[13] == '-') offset = -offset;
	}
	this.setTime(date.getTime() + (offset - date.getTimezoneOffset()) * 60000);
};

$(function() {
	var lang = document.body.lang;

	// language corrections for MSIE.
	$('[lang|=ko]').addClass('lang-ko');
	$('[lang|=en]').addClass('lang-en');
	$('[lang|=ja]').addClass('lang-ja');

	// replaces <m:math> calls in the original text.
	$('span.math').each(function() {
		var size = 1; // by default
		var m = this.className.match(/\bmath-size([0-4]|-[1-4])\b/);
		if (m) size = m[1];

		var code = $(this).text();
		var img = document.createElement('img');
		img.setAttribute('src', 'http://l.wordpress.com/latex.php?latex=' +
			encodeURIComponent(code) + '&s=' + size + '&bg=eeeeee&fg=444444');
		img.setAttribute('alt', code);
		img.className = this.className;
		$(this).replaceWith(img);
	});

	// fill "activity" section in index pages.
	$('.mearie-activity noscript').each(function(i) {
		var list = $('<ul/>');
		$(this).replaceWith(list);
		var waiting = $('<div style="text-align:center;padding:4em 0">' +
			'<img src="/res/loading.gif" width="32" height="32" alt=""/></div>');
		waiting.insertBefore(list);

		window['__friendfeedcallback'+i] = function(data) {
			var count = 0;
			waiting.remove();
			$.each(data.entries, function(i, entry) {
				var url = entry.rawLink, body = entry.rawBody, via = entry.via.url;
				var shorten = true, iconurl, mainurl, region;
				if (via.match(/^http:\/\/twitter\.com/)) {
					if (lang == 'ko') return; // skip in korean pages
					iconurl = 'http://twitter.com/favicon.ico';
					mainurl = 'http://twitter.com/seonkay/';
					region = (lang=='ko' ? '트위터' : 'Twitter');
					shorten = false;
				} else if (via.match(/^http:\/\/me2day\.net/)) {
					if (lang != 'ko') return; // skip in non-korean pages
					iconurl = 'http://me2day.net/favicon.ico';
					mainurl = 'http://me2day.net/arachneng/';
					region = (lang=='ko' ? '미투데이' : 'Me2day');
					shorten = false;
				} else if (via.match(/^http:\/\/\w+\.tumblr\.com/)) {
					if (lang != 'ko') return; // skip in non-korean pages
					iconurl = 'http://www.tumblr.com/favicon.ico';
					mainurl = 'http://j.mearie.org/';
					region = (lang=='ko' ? '저널' : 'Journal');
					if (body.length < 40) {
						body = '<strong><a href="' + url + '">' + body + '</a></strong>';
					}
				} else if (via.match(/^http:\/\/hg\.mearie\.org/)) {
					iconurl = 'http://mercurial.selenic.com/images/favicon.ico';
					mainurl = via;
					region = (lang=='ko' ? '머큐리얼 저장소' : 'Mercurial repository');
					body = '<strong>' + via.replace(/^http:\/\/hg\.mearie\.org\/|\/$/g, '') + ':</strong> ' + body;
				} else {
					throw new Error('unexpected friendfeed source');
				}

				var when = new Date();
				when.setISO8601(entry.date);
				var whenstr = when.getFullYear().zfill(4) + '-' + (when.getMonth()+1).zfill(2) +
					'-' + when.getDate().zfill(2);
				if (shorten) body = body.cut(120);
				var inner = '<a href="' + mainurl + '">' +
					'<img src="' + iconurl + '" width="16" height="16" alt="' + region + '"/></a>&nbsp;' +
					body + ' <small>(<a href="' + url + '">' + whenstr + '</a>)</small>';
				if (entry.thumbnails && !entry.thumbnails[0].url.match(/^http:\/\/friendfeed.com/)) {
					var th = entry.thumbnails[0];
					inner = '<img src="' + th.url + '" width="' + th.width + '" height="' + th.height +
						'" alt="" class="right"/>' + inner;
				}
				list.append('<li>' + inner + '</li>');
				if (++count >= 5) return false;
			});
		};
		$.ajax({url: 'http://friendfeed-api.com/v2/feed/lifthrasiir?start=0&num=20&raw=1' +
				'&maxcomments=0&maxlikes=0&callback=__friendfeedcallback'+i,
			dataType: 'script'});
	});
});

