jQuery.noConflict();
/*@cc_on
jQuery.each(['article', 'aside', 'canvas', 'details', 'figcaption', 'figure',
	'footer', 'header', 'hgroup', 'menu', 'nav', 'section', 'summary'],
	function() { document.createElement(this); });
@*/
jQuery(document).ready(function($) {

////////////////////////////////////////////////////////////////////////////////

var languageName = function(lang, displaylang) {
	switch (displaylang) {
	case 'ko':
		return {'ko': '한국어', 'en': '영어', 'ja': '일본어'}[lang] ||
			('지원하지 않는 언어 (' + lang + ')');
	case 'en':
	default:
		return {'ko': 'Korean', 'en': 'English', 'ja': 'Japanese'}[lang] ||
			('Unsupported language (' + lang + ')');
	case 'ja':
		return {'ko': '韓国語', 'en': '英語', 'ja': '日本語'}[lang] ||
			('サポートしていない言語 (' + lang + ')');
	}
};

var zfill = function(s, n) {
	s = s.toString();
	while (s.length < n) s = '0' + s;
	return s;
};

var cutString = function(s, width, trail) {
	if (typeof trail == 'undefined') trail = '…';
	var w = 0;
	for (var i = 0; i < s.length; ++i) {
		// we approximate east-asian width using the most prevalent ideographic blocks
		w += (s.charAt(i).match(/[\u3000-\u9fff\uac00-\ud7ff\uf900-\ufaff]/) ? 2 : 1);
		if (w > width) return s.substring(0, i) + trail;
	}
	return s;
};

var parseColor = function(s) {
	var m;
	if (m = s.match(/^#([0-9a-fA-F])([0-9a-fA-F])([0-9a-fA-F])$/)) {
		return [parseInt(m[1],16)*17, parseInt(m[2],16)*17, parseInt(m[3],16)*17, 255];
	} else if (m = s.match(/^#([0-9a-fA-F]{2})([0-9a-fA-F]{2})([0-9a-fA-F]{2})$/)) {
		return [parseInt(m[1],16), parseInt(m[2],16), parseInt(m[3],16), 255];
	} else if (m = s.match(/^rgb\((\d+),\s*(\d+),\s*(\d+)\)$/)) {
		return [parseInt(m[1]), parseInt(m[2]), parseInt(m[3]), 255];
	} else if (m = s.match(/^rgba\((\d+),\s*(\d+),\s*(\d+),\s*(\d+)\)$/)) {
		return [parseInt(m[1]), parseInt(m[2]), parseInt(m[3]), parseInt(m[4])];
	} else if (s == 'transparent') {
		return [0, 0, 0, 0];
	} else {
		return null;
	}
};

var getStyleColor = function(el, prop, ieprop) {
	while (true) {
		if (el.currentStyle) { // IE
			var s = el.currentStyle[ieprop];
		} else if (window.getComputedStyle) { // Mozilla etc.
			var s = document.defaultView.getComputedStyle(el, null).getPropertyValue(prop);
		} else {
			return null;
		}

		var color = parseColor(s);
		if (!color) throw Error('getStyleError failed: ' + s);
		if (color[3] == 255) break; // opaque
		el = el.parentNode;
	}
	return (zfill(color[0].toString(16), 2) + zfill(color[1].toString(16), 2) +
		zfill(color[2].toString(16), 2));
};

var dateFromISO8601 = function(s) {
	var m = s.match(/^(\d{4})(-(\d\d)(-(\d\d)(T(\d\d):(\d\d)(:(\d\d)(\.\d+)?)?)?)?)?(Z|([-+])(\d\d):(\d\d))?$/);
	if (!m) throw Error('invalid ISO 8601 string');

	var d = new Date(m[1], 0, 1);
	if (m[3]) d.setMonth(m[3] - 1);
	if (m[5]) d.setDate(m[5]);
	if (m[7]) d.setHours(m[7]);
	if (m[8]) d.setMinutes(m[8]);
	if (m[10]) d.setSeconds(m[10]);
	if (m[11]) d.setMilliseconds(parseFloat('0'+m[11]) * 1000);
	var offset = 0;
	if (m[13]) {
		offset = m[14] * 60 + parseInt(m[15]);
		if (m[13] == '-') offset = -offset;
	}
	d.setTime(d.getTime() + (offset - d.getTimezoneOffset()) * 60000);
	return d;
};

// allows a design modification using the query. (debugging only)
var m = location.search.match(/[&?]design=([a-z0-9-]+)(?:&|$)/i);
var nolinkfix = false;
if (!m || m[1] != 'none') {
	// april fools!
	var d = new Date;
	if (d.getFullYear() == 2011 && d.getMonth() == 3 && d.getDate() == 1) {
		m = ['', 'april1'];
		nolinkfix = true;
	}
}
if (m && m[1] != 'none') {
	var design = m[1];
	$('head').append('<link rel="stylesheet" media="screen" href="http://mearie.org/res/design-' +
			design + '.css" type="text/css" />');
	if ($.browser.msie) {
		$('head').append('<link rel="stylesheet" media="screen" href="http://mearie.org/res/design-' +
				design + '.ie.css" type="text/css" />');
	}
	$('body').addClass('design-' + design);
	if (!nolinkfix) {
		$('a').attr('href', function() {
			if (this.href.match(/:\/\/(?![^\/]*mearie\.org(?:\/|$))|[&?]design=/i)) return this.href;
			return this.href + (this.href.indexOf('?') < 0 ? '?' : '&') + 'design=' + design;
		});
	}
}

var lang = document.body.lang;
var userlang = (navigator.language || navigator.userLanguage || lang).replace(/-.*$/, '');

// show a warning if the page language doesn't match with the browser language.
// note: it uses UI language; retrieving a language from accept-language header seems to be hard:
//       http://groups.google.com/group/mozilla-labs-jetpack/browse_thread/thread/8459ccb6a7246656
if (userlang != lang && !(location.host == 'j.mearie.org' || location.host == 'arachneng.egloos.com')) {
	var langl = languageName(lang, userlang);
	var userlangl = languageName(userlang, userlang);
	var message = {
		'ko': '<strong>이 문서는 ' + userlangl + '로 제공되지 않습니다.</strong> ' +
			langl + ' 문서를 대신 보여 주고 있습니다.',
		'en': '<strong>This document is not available in ' + userlangl + '.</strong> ' +
			'The version in ' + langl + ' is in the display instead.',
		'ja': '<strong>このページは' + userlangl + 'で提供されないです。</strong> ' +
			langl + 'バージョンを代わりに見せてくれています。'};
	var warning = '<div class="warning" lang="' + userlang + '"><p>' +
			(message[userlang] || message['en']) + '</p></div>';
	var match;
	if ((match = $('#sitebody hgroup')).length > 0) {
		match.after(warning);
	} else if ((match = $('#sitebody h1')).length > 0) {
		match.after(warning);
	} else {
		$('#sitebody').prepend(warning);
	}
}

// the client-side localization for journal.
$('article').each(function() {
	var article = $(this);
	//if (article.find('footer .tags a[href$=/english]').length > 0) {
	if (article.find('footer .tags a[href*=/english]').length > 0) {
		article.attr('lang', 'en');
		article.find('h2 a.permalink').text(
			article.find('h2 a.permalink').text().replace(/^(\d+)년 (\d+)월 (\d+)일$/, function(_,y,m,d) {
				return ['','January','February','March','April','May','June','July','August','September',
					'October','November','December'][m] + ' ' + d + ', ' + y;
			}));
		article.find('.postmore a').text('More…');
		article.find('footer dt.when').text('Posted on');
		article.find('footer dt.share').text('Share');
		article.find('footer dt.share').text('Share');
		article.find('footer dt.notes').text('Notes');
		article.find('footer dd.notes a').text(article.find('footer dd.notes a').text().replace(/^(\d+)개$/, '$1'));
		article.find('footer dt.tags').text('Tags');
	}
});
if (userlang == 'en') {
	$('#siteresp .notes').attr('lang', 'en');
} else {
	$('#siteresp .notes li').each(function() {
		var action = $(this).find('.action');
		action.html(action.html()
			.replace(/(<a .*?class="?tumblelog.*?>.*?<\/a>) posted this/gi, '$1 님이 이 글을 올림')
			.replace(/(<a .*?>.*?<\/a>) liked this/gi, '$1 님이 이 글을 좋아함')
			.replace(/(<a .*?class="?tumblelog.*?>.*?<\/a>) reblogged this from (<a .*?class="?source_tumblelog.*?>.*?<\/a>) and added/gi, '$1 님이 $2 님의 글을 퍼가고 덧붙임')
			.replace(/(<a .*?class="?tumblelog.*?>.*?<\/a>) reblogged this from (<a .*?class="?source_tumblelog.*?>.*?<\/a>)/gi, '$1 님이 $2 님의 글을 퍼감')
		);
	});
}

// CSS corrections for MSIE.
$('[lang|=ko]').addClass('lang-ko');
$('[lang|=en]').addClass('lang-en');
$('[lang|=ja]').addClass('lang-ja');
$('a[href^="http://"]:not([href^="http://mearie.org/"])' +
		    ':not([href^="http://hg.mearie.org/"])' +
		    ':not([href^="http://pub.mearie.org/"])' +
		    ':not([href^="http://noe.mearie.org/"])' +
		    ':not([href^="http://j.mearie.org/"])' +
		    ':not([href^="http://r.mearie.org/"])' +
		    ':not(.interwiki):not(.noicon), ' +
	'a[href^="https://"]:not(.interwiki):not(.noicon), ' +
	'a[href^="ftp://"]:not(.interwiki):not(.noicon), ' +
	'a[href^="irc://"]:not(.interwiki):not(.noicon), ' +
	'a[href^="mailto:"]:not(.interwiki):not(.noicon)').addClass('external');
$('.noicon .external').removeClass('external');

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
				if (body.match(/^RT /)) return; // ignore retweets
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

			var when = dateFromISO8601(entry.date);
			var whenstr = zfill(when.getFullYear(), 4) + '-' + zfill(when.getMonth()+1, 2) +
				'-' + zfill(when.getDate(), 2);
			if (shorten) body = cutString(body, 120);
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

////////////////////////////////////////////////////////////////////////////////

});

