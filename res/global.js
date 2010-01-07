// replaces <m> elements in the original text.
$(function() {
	$('[lang|=ko]').addClass('lang-ko');
	$('[lang|=en]').addClass('lang-en');
	$('[lang|=ja]').addClass('lang-ja');

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
});

