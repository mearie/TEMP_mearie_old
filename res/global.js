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
};

String.prototype.parseColor = function() {
	var m;
	if (m = this.match(/^#([0-9a-fA-F])([0-9a-fA-F])([0-9a-fA-F])$/)) {
		return [parseInt(m[1],16)*17, parseInt(m[2],16)*17, parseInt(m[3],16)*17, 255];
	} else if (m = this.match(/^#([0-9a-fA-F]{2})([0-9a-fA-F]{2})([0-9a-fA-F]{2})$/)) {
		return [parseInt(m[1],16), parseInt(m[2],16), parseInt(m[3],16), 255];
	} else if (m = this.match(/^rgb\((\d+),\s*(\d+),\s*(\d+)\)$/)) {
		return [parseInt(m[1]), parseInt(m[2]), parseInt(m[3]), 255];
	} else if (m = this.match(/^rgba\((\d+),\s*(\d+),\s*(\d+),\s*(\d+)\)$/)) {
		return [parseInt(m[1]), parseInt(m[2]), parseInt(m[3]), parseInt(m[4])];
	} else if (this == 'transparent') {
		return [0, 0, 0, 0];
	} else {
		return null;
	}
};

Number.prototype.zfill = function(n) {
	return this.toString().zfill(n);
};

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

jQuery.noConflict();
jQuery(document).ready(function($) {
	var lang = document.body.lang;

	// CSS corrections for MSIE.
	$('[lang|=ko]').addClass('lang-ko');
	$('[lang|=en]').addClass('lang-en');
	$('[lang|=ja]').addClass('lang-ja');
	$('a[href^="http://"]' +
		':not([href^="http://mearie.org/"])' +
		':not([href^="http://hg.mearie.org/"])' +
		':not([href^="http://pub.mearie.org/"])' +
		':not([href^="http://j.mearie.org/"])' +
		':not([href^="http://r.mearie.org/"])' +
		':not(.interwiki):not(.noicon), ' +
	'a[href^="https://"]:not(.interwiki):not(.noicon), ' +
	'a[href^="ftp://"]:not(.interwiki):not(.noicon), ' +
	'a[href^="irc://"]:not(.interwiki):not(.noicon), ' +
	'a[href^="mailto:"]:not(.interwiki):not(.noicon)').addClass('external');

	// load responses if needed.
	var resplinks = $('.responselink');
	if (resplinks.length == 1 && $('#siteresp').length == 0) {
		var href = resplinks.attr('href');
		var placeholder = $('<div id="siteresp" class="loading-anim"/>');
		placeholder.insertBefore('#sitemeta');
		$.ajax({dataType: 'jsonp', jsonpCallback: '__mearieresponsecallback',
			url: resplinks.attr('href').replace(/#.*$/, '') + '?format=jsonp',
			error: function() {
				placeholder.removeClass('loading-anim');
				placeholder.addClass('loading-error');
				if (lang == 'ko') {
					placeholder.html('<p>응답 데이터를 읽어 올 수 없습니다. 다시 시도해 주세요.</p>');
				} else {
					placeholder.html('<p>Cannot load the responses. Refresh the page to try again.</p>');
				}
			},
			success: function(data) {
				placeholder.removeClass('loading-anim');
				placeholder.replaceWith(data);
				resplinks.attr('href', '#responses');
			}});
	}

	// replaces <m:math> calls in the original text.
	$('span.math').each(function() {
		var size = 1; // by default
		var m = this.className.match(/\bmath-size([0-4]|-[1-4])\b/);
		if (m) size = m[1];

		var getStyleColor = function(el, prop, ieprop) {
			while (true) {
				if (el.currentStyle) { // IE
					var s = el.currentStyle[ieprop];
				} else if (window.getComputedStyle) { // Mozilla etc.
					var s = document.defaultView.getComputedStyle(el, null).getPropertyValue(prop);
				} else {
					return null;
				}

				var color = s.parseColor();
				if (!color) throw Error('getStyleError failed: ' + s);
				if (color[3] == 255) break; // opaque
				el = el.parentNode;
			}
			return (color[0].toString(16).zfill(2) + color[1].toString(16).zfill(2) +
				color[2].toString(16).zfill(2));
		};
		var fg = getStyleColor(this, 'color', 'color') || '444444';
		var bg = getStyleColor(this, 'background-color', 'backgroundColor') || 'eeeeee';

		var code = $(this).text();
		var img = document.createElement('img');
		img.setAttribute('src', 'http://l.wordpress.com/latex.php?latex=' +
			encodeURIComponent(code) + '&s=' + size + '&bg=' + bg + '&fg=' + fg);
		img.setAttribute('alt', code);
		img.className = this.className;
		$(this).replaceWith(img);
	});

	// fill "activity" section in index pages.
	$('.mearie-activity noscript').each(function(i) {
		var list = $('<ul style="display:none"/>');
		$(this).replaceWith(list);
		var waiting = $('<div class="loading-anim"/>');
		waiting.insertBefore(list);

		var maxcount = 5, count = 0, start = 0, perreq = 10;
		var friendfeeddata = null, tumblrdata = null;
		var friendfeedcallback = function(data) {
			friendfeeddata = data;
			if (tumblrdata) process(friendfeeddata, tumblrdata);
		};
		var tumblrcallback = function(data) {
			tumblrdata = {};
			$.each(data.posts, function(i, post) {
				tumblrdata[post.url] = post;
			});
			if (friendfeeddata) process(friendfeeddata, tumblrdata);
		};
		var process = function(data, tumblrdata) {
			$.each(data.entries, function(i, entry) {
				var url = entry.rawLink, body = entry.rawBody, via = entry.via.url;
				var shorten = true, iconurl, mainurl, region;
				if (via.match(/^http:\/\/twitter\.com\//)) {
					if (lang == 'ko') return; // skip in korean pages
					iconurl = 'http://twitter.com/favicon.ico';
					mainurl = 'http://twitter.com/seonkay/';
					region = (lang=='ko' ? '트위터' : 'Twitter');
					shorten = false;
				} else if (via.match(/^http:\/\/me2day\.net\//)) {
					if (lang != 'ko') return; // skip in non-korean pages
					iconurl = 'http://me2day.net/favicon.ico';
					mainurl = 'http://me2day.net/arachneng/';
					region = (lang=='ko' ? '미투데이' : 'Me2day');
					shorten = false;
				} else if (via.match(/^http:\/\/\w+\.tumblr\.com\//)) {
					var post = tumblrdata[url] || {};
					var postlang = (post.url ? 'en' : 'ko');
					if (lang != postlang) return;
					iconurl = 'http://www.tumblr.com/favicon.ico';
					mainurl = 'http://j.mearie.org/';
					region = (lang=='ko' ? '저널' : 'Journal');
					if (body.length < 40 || (post && post['regular-title'])) {
						body = '<strong><a href="' + url + '">' + body + '</a></strong>';
					}
					if (!url.match(/^http:\/\/j\.mearie\.org\//)) {
						// tumblr "link" post doesn't give actual URL
						url = null;
					}
				} else if (via.match(/^http:\/\/hg\.mearie\.org\//)) {
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
				var inner = '<a href="' + mainurl + '" class="noicon">' +
					'<img src="' + iconurl + '" width="16" height="16" alt="' + region + '"/></a>&nbsp;' + body +
					' <small>(' + (url ? '<a href="' + url + '">' + whenstr + '</a>' : whenstr) + ')</small>';
				if (entry.thumbnails && !entry.thumbnails[0].url.match(/^http:\/\/friendfeed.com/)) {
					var th = entry.thumbnails[0];
					inner = '<img src="' + th.url + '" width="' + th.width + '" height="' + th.height +
						'" alt="" class="right"/>' + inner;
				}
				list.append('<li>' + inner + '</li>');
				if (++count >= maxcount) {
					list.css('display', '');
					waiting.remove();
					return false;
				}
			});
			if (count < maxcount) {
				start += perreq;
				invoke(start, perreq);
			}
		};
		var invoke = function(start, num) {
			if (!tumblrdata) { // only read once, and only used for filtering english posts.
				$.ajax({url: 'http://j.mearie.org/api/read/json?start=0&count=' + maxcount + '&tagged=english',
					dataType: 'jsonp',
					success: tumblrcallback});
			}
			$.ajax({url: 'http://friendfeed-api.com/v2/feed/lifthrasiir?start=' + start + '&num=' + num +
					'&raw=1&maxcomments=0&maxlikes=0',
				dataType: 'jsonp',
				success: friendfeedcallback});
		};
		invoke(0, perreq);
	});
});

