// mearie.org 3.0 global script base
// Copyright (c) 2005-2009, Kang Seonghoon.
// See http://mearie.org/copyright for license information.

// replaces <m> elements in the original text.
$(function() {
	$('span.math').each(function() {
		var size = 1; // by default
		var m = this.className.match(/\bmath-size([0-4]|-[1-4])\b/);
		if (m) size = m[1];

		var code = $(this).text();
		$(this).replaceWith('<img src="http://l.wordpress.com/latex.php?latex=' +
			encodeURIComponent(code) + '&amp;s=' + size + '&amp;bg=ffffff&amp;fg=000000" alt="' +
			code.replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;') +
			'" class="' + this.className + '"/>')
	});
});

