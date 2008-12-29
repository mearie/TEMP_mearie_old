/* mearie.org global javascript
 * Copyright (c) 2005-2007, Kang Seonghoon aka lifthrasiir.
 *
 * This file is in public domain; you can use this file freely,
 * but this doesn't necessarily mean you could also use
 * documents using this stylesheet.
 */

// shortcut for getElementById
function $(id) { return document.getElementById(id); }

String.prototype.zfill = function(n) {
	var s = this;
	while (s.length < n) s = '0' + s;
	return s;
}

// ISO 8601 parser for Date
Date.prototype.setISO8601 = function(s) {
	var m = s.match(/^(\d{4})(-(\d\d)(-(\d\d)(T(\d\d):(\d\d)(:(\d\d)(\.\d+)?)?)?)?)?(Z|([-+])(\d\d):(\d\d))?$/);
	if (!m) throw Error('MEARIE INTERNAL ERROR: invalid ISO 8601 string');

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
}

// ISO 8601 formatter, properly handing partial format (e.g. datetime attribute)
String.prototype.formatISO8601 = function(lang) {
	var date = new Date();
	date.setISO8601(this);
	var m = this.match(/^(\d{4})(-(\d\d)(-(\d\d)(T(\d\d):(\d\d)(:(\d\d)(\.\d+)?)?)?)?)?(Z|([-+])(\d\d):(\d\d))?$/);

	switch (lang) {
	case 'ko':
		var result = date.getFullYear() + '년';
		if (m[3]) result += ' ' + (date.getMonth()+1) + '월';
		if (m[5]) result += ' ' + date.getDate() + '일';
		if (m[7]) {
			result += (date.getHours()>11 ? ' 오후 ' : ' 오전 ');
			result += ((date.getHours()+11)%12+1) + '시';
		}
		if (m[8]) {
			var min = date.getMinutes();
			if (min == 30) result += ' 반';
			else if (min != 0) result += ' ' + new String(min).zfill(2) + '분';
		}
		if (m[10]) result += ' ' + new String(date.getSeconds()).zfill(2) + '초';
		return result;

	case 'en':
		if (m[7]) {
			var result = new String(date.getMonth()+1).zfill(2) + '/' +
				new String(date.getDate()).zfill(2) + '/' +
				date.getFullYear() + ' ' + ((date.getHours()+11)%12+1);
			if (m[8]) result += ':' + new String(date.getMinutes()).zfill(2);
			if (m[10]) result += ':' + new String(date.getSeconds()).zfill(2);
			return result + (date.getHours()>11 ? ' PM' : ' AM');
		} else {
			var result = date.getFullYear();
			if (m[5]) result = date.getDate() + ', ' + result;
			if (m[3]) result = ['January','February','March','April','May',
				'June','July','August','September','October','November',
				'December'][date.getMonth()] + ' ' + result;
			return result;
		}

	case 'ja':
		var result = date.getFullYear() + '年';
		if (m[3]) result += (date.getMonth()+1) + '月';
		if (m[5]) result += date.getDate() + '日';
		if (m[7]) result += new String(date.getHours()).zfill(2) + '時';
		if (m[8]) result += new String(date.getMinutes()).zfill(2) + '分';
		if (m[10]) result += new String(date.getSeconds()).zfill(2) + '秒';
		return result;
	}

	return this; // fallback
}

// browser check object
var Browser = {};
Browser.isIE = (navigator.userAgent.indexOf('MSIE') >= 0);
Browser.isWebkit = (navigator.userAgent.indexOf('AppleWebkit') >= 0);
Browser.isGecko = !Browser.isWebkit && (navigator.userAgent.indexOf('Gecko') >= 0);
Browser.isGecko19 = Browser.isGecko && (navigator.userAgent.indexOf('rv:1.9') >= 0); // ff3

// cookie class
var Cookies = {
	init: function() {
		var cookies = document.cookie.split('; ');
		var ncookies = cookies.length;
		for (var i = 0; i < ncookies; ++i) {
			var cookie = cookies[i].split('=');
			this[cookie[0]] = decodeURIComponent(cookie[1]);
		}
	},
	create: function(key, value, expires) {
		if (expires) {
			var date = new Date();
			date.setTime(date.getTime() + expires * 86400000);
			var options = "; path=/; expires=" + date.toGMTString();
		} else {
			var options = "; path=/";
		}
		document.cookie = key + "=" + encodeURIComponent(value) + options;
		this[key] = value;
	},
	erase: function(key) {
		this.create(key, '', -365);
		this[key] = undefined;
	}
};
Cookies.init();

////////////////////////////////////////////////////////////////////////////////

var _loadhandlers = [];
function addLoadHandler(func) { _loadhandlers.push(func); }
function addLoadHandlerForIE(func) { if (Browser.isIE) addLoadHandler(func); }
function addPreloadHandler(func) { func(); } // do it now!
function addPreloadHandlerForIE(func) { if (Browser.isIE) addPreloadHandler(func); }

window.onload = function() {
	var nhandlers = _loadhandlers.length;
	for (var i = 0; i < nhandlers; ++i) _loadhandlers[i]();
};

////////////////////////////////////////////////////////////////////////////////
// browser workarounds

// workaround implemetation of max-width for MSIE
addLoadHandlerForIE(function() {
	var elem = document.createElement('div');
	elem.id = 'xx-hiddendiv';
	elem.style.width = '100%';
	document.body.appendChild(elem);
});

// avoiding CSS background-image flicker
addLoadHandlerForIE(function() {
	try {
		document.execCommand('BackgroundImageCache', false, true);
	} catch (e) {}
});

function windowWidthIE() {
	var div = $('xx-hiddendiv');
	return (div ? div.clientWidth : document.body.clientWidth);
}

function checkWindowWidthIE(percent, em) {
	/* typical windows uses 96dpi, so 4/3px per 1pt */
	//return (windowWidthIE() * percent > parseFloat(document.body.currentStyle.fontSize) * 133.3 * em);
	return (windowWidthIE() * percent > (12 * parseFloat(document.body.currentStyle.fontSize)) * 133.3 * em);
}

// addition of class="lang-XX" with xml:lang for MSIE
/* moved to formatter
addLoadHandler(function() {
	var elems = document.body.getElementsByTagName('*');
	var nelems = elems.length;
	for (var i = 0; i < nelems; ++i) {
		var lang = elems[i].getAttribute('xml:lang');
		if (lang) elems[i].className += ' lang-' + lang;
	}
});
*/

// addition of quotes of <q>
addLoadHandlerForIE(function() {
	var elems = document.body.getElementsByTagName('q');
	var nelems = elems.length;
	for (var i = 0; i < nelems; ++i) {
		var ielems = elems[i].getElementsByTagName('q');
		var inelems = ielems.length;
		for (var j = 0; j < inelems; ++j) {
			ielems[i].innerHTML = '&lsquo;' + ielems[i].innerHTML + '&rsquo;';
		}
	}
	for (var i = 0; i < nelems; ++i) {
		var firstchar = elems[i].innerHTML.charCodeAt(0);
		if (firstchar == 8220 || firstchar == 8216) continue;
		elems[i].innerHTML = '&ldquo;' + elems[i].innerHTML + '&rdquo;';
	}
});

// addition of datetime string for <ins>, <del> etc.
// this is hard to implement only using CSS because even attr() in CSS3 is insufficient.
addLoadHandler(function() {
	if (typeof mearie_props == 'undefined') return;

	var preflang = mearie_props.preflang || 'ko';
	var affixes;
	switch (preflang) {
	case 'ko': affixes = ['', '에 더함:', '', '에 지움:']; break;
	case 'en': affixes = ['Added on ', ':', 'Deleted on ', ':']; break;
	case 'ja': affixes = ['', 'に追加:', '', 'に削除:']; break;
	default: return;
	}

	var elems = document.body.getElementsByTagName('*');
	var nelems = elems.length;
	for (var i = nelems - 1; i >= 0; --i) {
		var datetime = elems[i].getAttribute('datetime');
		if (!datetime) continue;
		var baseindex = (elems[i].tagName.toLowerCase() == 'ins' ? 0 : 2);
		elems[i].innerHTML = '<span class="datetime-at"><span>(</span>' +
			affixes[baseindex] + datetime.formatISO8601(preflang) +
			affixes[baseindex+1] + '<span>) </span></span>' +
			elems[i].innerHTML;
	}
});

// adjustment for damn center alignment!
// mearie.org requires pixel-perfect alignment, but many browsers don't...
addLoadHandler(function() {
	if (Browser.isGecko19) { // tested w/ firefox 3.0.1
		document.getElementById('body').style.width = '640.1px';
		document.getElementById('footer').style.width = '640.1px';
	} else if (Browser.isWebkit) { // tested w/ safari 3
		document.getElementById('body').style.width = '641px';
		document.getElementById('footer').style.width = '641px';
	}
});

////////////////////////////////////////////////////////////////////////////////
// utility functions

function toggle(id) {
	var obj = $(id);
	if (obj.style.display == 'none') {
		obj.style.display = '';
		return true;
	} else {
		obj.style.display = 'none';
		return false;
	}
}

