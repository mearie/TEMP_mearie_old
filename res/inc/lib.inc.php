<?php
define('MEARIE_GENERATOR', 'mearieflo 20081108');

if (!defined('MEARIE_DOCROOT')) define('MEARIE_DOCROOT', '/home/lifthrasiir/mearie/');
if (!defined('MEARIE_RESROOT')) define('MEARIE_RESROOT', MEARIE_DOCROOT.'res/');
if (!defined('MEARIE_IMGROOT')) define('MEARIE_IMGROOT', MEARIE_DOCROOT.'img/');

if (isset($_SERVER['prefer-language'])) {
	define('MEARIE_PREFER_LANGUAGE', $_SERVER['prefer-language']);
	define('MEARIE_SITE_PREFIX', '/-'.$_SERVER['prefer-language'].'-/');
} else {
	define('MEARIE_PREFER_LANGUAGE', '');
	define('MEARIE_SITE_PREFIX', '/');
}

////////////////////////////////////////////////////////////////////////////////

class Mearie {
	function __construct($requri) {
		preg_match('#^(?:/-(en|ko|ja)-)?(/.*)$#', $requri, $m);
		$this->lang = $m[1];
		$this->url = $m[2];
	}

	function region() {
		$regions = array('/documents/' => 'document', '/projects/' => 'project', '/journal/' => 'journal', '' => '');
		foreach ($regions as $url => $urlreg) {
			if (substr($this->url, 0, strlen($url)) == $url) return $urlreg;
		}
		return '';
	}

	function moved($uri, $permanent) {
		if ($permanent) {
			header('HTTP/1.1 301 Moved Permanently');
			$title = '301 Moved Permanently';
		} else {
			header('HTTP/1.1 307 Temporary Redirect');
			$title = '307 Temporary Redirect';
		}
		header('Location: '.$uri);
	?>
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" xml:lang="en">
<head>
	<meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
	<title><?php echo $title; ?> &mdash; mearie.org</title>
</head>
<body>
	<p>Requested resource has been moved into <a href="<?php echo htmlspecialchars($url); ?>">here</a><?php if ($permanent) { ?> permanently<?php } ?>.</p>
</body>
</html>
<?php
		exit;
}

	function httpError($code = 404) {
		switch ($code) {
		case 401: header('HTTP/1.1 401 Unauthorized'); break;
		case 403: header('HTTP/1.1 403 Forbidden'); break;
		case 404: default: header('HTTP/1.1 404 Not Found'); break;
		case 500: header('HTTP/1.1 500 Internal Server Error'); break;
		}
		$lang = MEARIE_PREFER_LANGUAGE;
		if (!$lang) $lang = 'ko';
		include MEARIE_RESROOT.'inc/error'.$code.'.'.$lang.'.php';
		$SITE->end();
		exit;
	}
}

////////////////////////////////////////////////////////////////////////////////
// utilities

function mearie_script_base() {
	static $result = null;
	if (is_null($result)) {
		$scriptname = $_SERVER['SCRIPT_FILENAME'];
		$result = substr($scriptname, 0, strrpos($scriptname, '/') + 1);
	}
	return $result;
}

function mearie_lang($lang) {
	echo 'lang="'.$lang.'" xml:lang="'.$lang.'" class="lang-'.$lang.'"';
}

function mearie_checked($name, $curvalue, $value = null) {
	$textvalue = (is_null($value) ? '1' : htmlspecialchars($value));
	if (is_null($value) ? $curvalue : $curvalue == $value) {
		echo 'name="'.$name.'" value="'.$textvalue.'" checked="checked"';
	} else {
		echo 'name="'.$name.'" value="'.$textvalue.'"';
	}
}

function mearie_checked_get($name) { mearie_checked($name, isset($_GET[$name])); }
function mearie_checked_post($name) { mearie_checked($name, isset($_POST[$name])); }

////////////////////////////////////////////////////////////////////////////////
// text preprocessor

class MearieFormatter {
	function __construct($options = array()) {
		$this->cut = null;
		$this->entities = true;
		$this->uniqid = '';
		$this->abbrs = array(
			'php' => 'PHP: Hypertext Preprocessor',
			'html' => 'HyperText Markup Language',
			'xhtml' => 'Extensible HyperText Markup Language',
			'css' => 'Cascading Style Sheets',
			'irc' => 'Internet Relay Chat',
			'api' => 'Application Programming Interface',
			'stl' => 'Standard Template Library',
		);
		foreach ($options as $key => $value) {
			$this->$key = $value;
		}
	}

	function _callback_table($m, &$stack, &$ncols, &$icols, &$nextrows, &$prev) {
		$str = $m[0];
		if ($m[2] == 'table') {
			if ($m[1] == '/') {
				list($ncols, $icols, $nextrows, $prev) = array_pop($stack);
			} else {
				$stack[] = array($ncols, $icols, $nextrows, $prev);
				$ncols = $icols = 0;
				$nextrows = array();
				$prev = 'td';
			}
		} elseif ($m[2] == 'tr') {
			if ($m[1] == '/') {
				$str = str_repeat("<$prev></$prev>", $ncols - $icols) . $str;
			} else {
				$icols = (count($nextrows) > 0 ? array_shift($nextrows) : 0);
			}
		} elseif ($m[1] != '/') {
			$prev = $m[2];
			$rowspan = $colspan = 1;
			if (preg_match('/rowspan=(["\'])(\d+)\1/', $m[3], $mm)) $rowspan = $mm[2];
			if (preg_match('/colspan=(["\'])(\d+)\1/', $m[3], $mm)) $colspan = $mm[2];

			$icols += $colspan;
			for ($i = 0; $i < $rowspan - 1; ++$i) ++$nextrows[$i];
			if ($ncols < $icols) $ncols = $icols;
		}
		return $str;
	}

	function process_table($str) {
		if (stripos($str, '<table') !== false) {
			$callback = create_function('$m', 'static $stack=array(), $ncols, $icols, $nextrows, $prev;
				return MearieFormatter::_callback_table($m, $stack, $ncols, $icols, $nextrows, $prev);');
			$str = preg_replace_callback('#<(/?)(table|th|tr|td)\b(.*?)>#', $callback, $str);
		}
		return $str;
	}

	function url_to_path($path) {
		if ($path{0} == '/') {
			return MEARIE_DOCROOT.substr($path, 1);
		} else {
			return mearie_script_base().$path;
		}
	}

	function _callback_image($m) {
		if ($m[3]) $m[2] = $m[3];

		$attrs = array();
		foreach (explode('" ', substr(rtrim($m[2]), 0, -1)) as $attr) {
			list($key, $value) = explode('="', $attr, 2);
			$attrs[$key] = $value;
		}

		$src = $attrs['src'];
		if ($src{0} == '@') $src = '/img/'.substr($src, 1);
		if (strpos($src, '://') !== false) {
			// do nothing
		} else {
			$isrc = $this->url_to_path($src);
			list($width, $height) = @getimagesize($isrc);
			if ($width && $height) {
				$twidth = (array_key_exists('width', $attrs) ? $attrs['width'] : '');
				$theight = (array_key_exists('height', $attrs) ? $attrs['height'] : '');
				if (substr($twidth, -1) == '%') $twidth = round($width * substr($twidth, 0, -1) / 100);
				if (substr($theight, -1) == '%') $theight = round($height * substr($theight, 0, -1) / 100);
				if ($twidth) {
					if (!$theight) $theight = round($height * $twidth / $width);
				} else {
					if ($theight) $twidth = round($width * $theight / $height);
					else { $twidth = $width; $theight = $height; }
				}
				$attrs['width'] = $twidth;
				$attrs['height'] = $theight;

				if (substr($src, 0, 5) == '/img/') {
					if (array_key_exists('class', $attrs) && strpos($attrs['class'], 'thumb') !== false) {
						$src = '/img/-'.$twidth.'x'.$theight.'-/'.substr($src, 5);
					}
				}
			}
		}
		$attrs['src'] = $src;

		$attrstr = '';
		foreach ($attrs as $key => $value) $attrstr .= ' '.$key.'="'.$value.'"';
		$result = '<img'.$attrstr.' />';
		if ($m[1]) {
			$result = '<a href="'.$src.'">'.$result.'</a>';
		}
		if ($m[4]) {
			$class = 'image-frame'.(isset($attrs['class']) ? ' '.$attrs['class'] : '');
			$result = '<div class="'.$class.'" style="width:'.$attrs['width'].'px">'.$result.'<div class="caption">'.$m[4].'</div></div>';
		}
		return $result;
	}

	function process_image($str) {
		if (stripos($str, '<img') !== false) {
			$callback = array('MearieFormatter', '_callback_image');
			$str = preg_replace_callback('#(<a>)?<img ([^<>]*?)/>(?(1)</a>)|<img ([^<>]*?)>(.*?)</img>#', $callback, $str);
		}
		return $str;
	}

	function process_footnote($str, $prefix = '') {
		if (strpos($str, '<!--((') === false) return $str;
		if ($prefix) $prefix .= '.';

		$parts = preg_split('#<!--(FOOTNOTE|\(\((?:[a-z0-9._-]+(?::|\)\)))?|\)\))-->#', $str, -1, PREG_SPLIT_DELIM_CAPTURE);

		$stack = array('');
		$modestack = array(false);
		$stacktop = 0;
		$num = 0;
		$footnotes = array();
		for ($i = 1; $i < count($parts); $i += 2) {
			$stack[$stacktop] .= $parts[$i-1];
			$tag = $parts[$i];
			if ($tag{0} == '(') {
				if (strlen($tag) == 2) { // <!--((-->
					++$num;
					$stack[$stacktop++] .= "<a href=\"#fn-$prefix$num\" class=\"footnotelink\">".
						"<span>(</span>$num)</a>";
					$stack[$stacktop] = "\t<div id=\"fn-$prefix$num\" class=\"footnote\">".
						"<span class=\"footnotelabel\">$num)</span> ";
					$modestack[] = true;
				} elseif ($tag{strlen($tag)-1} == ':') { // <!--((label:-->
					$label = substr($tag, 2, -1);
					$stack[$stacktop] .= "\t<div id=\"fn-$prefix$label\" class=\"footnote\">".
						"<span class=\"footnotelabel\">$label</span> ";
					$modestack[] = false;
				} else { // <!--((label))-->
					$label = substr($tag, 2, -2);
					$stack[$stacktop] .= "<a href=\"#fn-$prefix$label\" class=\"footnotelink\">".
						"<span>[</span>$label<span>]</span></a>";
				}
			} elseif ($tag{0} == ')') { // <!--))-->
				if (array_pop($modestack)) {
					$footnotes[] = $stack[$stacktop--]."</div>\n";
				}
			} else { // <!--FOOTNOTE-->, etc
				natsort($footnotes);
				$stack[$stacktop] .= "<div class=\"footnotes\">\n".implode('', $footnotes)."</div>\n";
				$footnotes = array();
			}
		}
		$str = $stack[0].$parts[count($parts)-1];
		if (count($footnotes)) {
			natsort($footnotes);
			$str .= "<div class=\"footnotes\">\n".implode('', $footnotes)."</div>\n";
		}
		while ($stacktop > 0) {
			$str .= $stack[$stacktop--]."</div>\n";
		}
		return $str;
	}

	function process_entities($str) {
		$trans = array(
			'&iexcl;'=>'&#161;', '&cent;'=>'&#162;', '&pound;'=>'&#163;', '&curren;'=>'&#164;',
			'&yen;'=>'&#165;', '&brvbar;'=>'&#166;', '&sect;'=>'&#167;', '&uml;'=>'&#168;',
			'&copy;'=>'&#169;', '&ordf;'=>'&#170;', '&laquo;'=>'&#171;', '&not;'=>'&#172;',
			'&shy;'=>'&#173;', '&reg;'=>'&#174;', '&macr;'=>'&#175;', '&deg;'=>'&#176;',
			'&plusmn;'=>'&#177;', '&sup2;'=>'&#178;', '&sup3;'=>'&#179;', '&acute;'=>'&#180;',
			'&micro;'=>'&#181;', '&para;'=>'&#182;', '&middot;'=>'&#183;', '&cedil;'=>'&#184;',
			'&sup1;'=>'&#185;', '&ordm;'=>'&#186;', '&raquo;'=>'&#187;', '&frac14;'=>'&#188;',
			'&frac12;'=>'&#189;', '&frac34;'=>'&#190;', '&iquest;'=>'&#191;', '&Agrave;'=>'&#192;',
			'&Aacute;'=>'&#193;', '&Acirc;'=>'&#194;', '&Atilde;'=>'&#195;', '&Auml;'=>'&#196;',
			'&Aring;'=>'&#197;', '&AElig;'=>'&#198;', '&Ccedil;'=>'&#199;', '&Egrave;'=>'&#200;',
			'&Eacute;'=>'&#201;', '&Ecirc;'=>'&#202;', '&Euml;'=>'&#203;', '&Igrave;'=>'&#204;',
			'&Iacute;'=>'&#205;', '&Icirc;'=>'&#206;', '&Iuml;'=>'&#207;', '&ETH;'=>'&#208;',
			'&Ntilde;'=>'&#209;', '&Ograve;'=>'&#210;', '&Oacute;'=>'&#211;', '&Ocirc;'=>'&#212;',
			'&Otilde;'=>'&#213;', '&Ouml;'=>'&#214;', '&times;'=>'&#215;', '&Oslash;'=>'&#216;',
			'&Ugrave;'=>'&#217;', '&Uacute;'=>'&#218;', '&Ucirc;'=>'&#219;', '&Uuml;'=>'&#220;',
			'&Yacute;'=>'&#221;', '&THORN;'=>'&#222;', '&szlig;'=>'&#223;', '&agrave;'=>'&#224;',
			'&aacute;'=>'&#225;', '&acirc;'=>'&#226;', '&atilde;'=>'&#227;', '&auml;'=>'&#228;',
			'&aring;'=>'&#229;', '&aelig;'=>'&#230;', '&ccedil;'=>'&#231;', '&egrave;'=>'&#232;',
			'&eacute;'=>'&#233;', '&ecirc;'=>'&#234;', '&euml;'=>'&#235;', '&igrave;'=>'&#236;',
			'&iacute;'=>'&#237;', '&icirc;'=>'&#238;', '&iuml;'=>'&#239;', '&eth;'=>'&#240;',
			'&ntilde;'=>'&#241;', '&ograve;'=>'&#242;', '&oacute;'=>'&#243;', '&ocirc;'=>'&#244;',
			'&otilde;'=>'&#245;', '&ouml;'=>'&#246;', '&divide;'=>'&#247;', '&oslash;'=>'&#248;',
			'&ugrave;'=>'&#249;', '&uacute;'=>'&#250;', '&ucirc;'=>'&#251;', '&uuml;'=>'&#252;',
			'&yacute;'=>'&#253;', '&thorn;'=>'&#254;', '&yuml;'=>'&#255;', '&OElig;'=>'&#338;',
			'&oelig;'=>'&#339;', '&Scaron;'=>'&#352;', '&scaron;'=>'&#353;', '&Yuml;'=>'&#376;',
			'&fnof;'=>'&#402;', '&circ;'=>'&#710;', '&tilde;'=>'&#732;', '&Alpha;'=>'&#913;',
			'&Beta;'=>'&#914;', '&Gamma;'=>'&#915;', '&Delta;'=>'&#916;', '&Epsilon;'=>'&#917;',
			'&Zeta;'=>'&#918;', '&Eta;'=>'&#919;', '&Theta;'=>'&#920;', '&Iota;'=>'&#921;',
			'&Kappa;'=>'&#922;', '&Lambda;'=>'&#923;', '&Mu;'=>'&#924;', '&Nu;'=>'&#925;',
			'&Xi;'=>'&#926;', '&Omicron;'=>'&#927;', '&Pi;'=>'&#928;', '&Rho;'=>'&#929;',
			'&Sigma;'=>'&#931;', '&Tau;'=>'&#932;', '&Upsilon;'=>'&#933;', '&Phi;'=>'&#934;',
			'&Chi;'=>'&#935;', '&Psi;'=>'&#936;', '&Omega;'=>'&#937;', '&alpha;'=>'&#945;',
			'&beta;'=>'&#946;', '&gamma;'=>'&#947;', '&delta;'=>'&#948;', '&epsilon;'=>'&#949;',
			'&zeta;'=>'&#950;', '&eta;'=>'&#951;', '&theta;'=>'&#952;', '&iota;'=>'&#953;',
			'&kappa;'=>'&#954;', '&lambda;'=>'&#955;', '&mu;'=>'&#956;', '&nu;'=>'&#957;',
			'&xi;'=>'&#958;', '&omicron;'=>'&#959;', '&pi;'=>'&#960;', '&rho;'=>'&#961;',
			'&sigmaf;'=>'&#962;', '&sigma;'=>'&#963;', '&tau;'=>'&#964;', '&upsilon;'=>'&#965;',
			'&phi;'=>'&#966;', '&chi;'=>'&#967;', '&psi;'=>'&#968;', '&omega;'=>'&#969;',
			'&thetasym;'=>'&#977;', '&upsih;'=>'&#978;', '&piv;'=>'&#982;', '&ensp;'=>'&#8194;',
			'&emsp;'=>'&#8195;', '&thinsp;'=>'&#8201;', '&zwnj;'=>'&#8204;', '&zwj;'=>'&#8205;',
			'&lrm;'=>'&#8206;', '&rlm;'=>'&#8207;', '&ndash;'=>'&#8211;', '&mdash;'=>'&#8212;',
			'&lsquo;'=>'&#8216;', '&rsquo;'=>'&#8217;', '&sbquo;'=>'&#8218;', '&ldquo;'=>'&#8220;',
			'&rdquo;'=>'&#8221;', '&bdquo;'=>'&#8222;', '&dagger;'=>'&#8224;', '&Dagger;'=>'&#8225;',
			'&bull;'=>'&#8226;', '&hellip;'=>'&#8230;', '&permil;'=>'&#8240;', '&prime;'=>'&#8242;',
			'&Prime;'=>'&#8243;', '&lsaquo;'=>'&#8249;', '&rsaquo;'=>'&#8250;', '&oline;'=>'&#8254;',
			'&frasl;'=>'&#8260;', '&euro;'=>'&#8364;', '&image;'=>'&#8465;', '&weierp;'=>'&#8472;',
			'&real;'=>'&#8476;', '&trade;'=>'&#8482;', '&alefsym;'=>'&#8501;', '&larr;'=>'&#8592;',
			'&uarr;'=>'&#8593;', '&rarr;'=>'&#8594;', '&darr;'=>'&#8595;', '&harr;'=>'&#8596;',
			'&crarr;'=>'&#8629;', '&lArr;'=>'&#8656;', '&uArr;'=>'&#8657;', '&rArr;'=>'&#8658;',
			'&dArr;'=>'&#8659;', '&hArr;'=>'&#8660;', '&forall;'=>'&#8704;', '&part;'=>'&#8706;',
			'&exist;'=>'&#8707;', '&empty;'=>'&#8709;', '&nabla;'=>'&#8711;', '&isin;'=>'&#8712;',
			'&notin;'=>'&#8713;', '&ni;'=>'&#8715;', '&prod;'=>'&#8719;', '&sum;'=>'&#8721;',
			'&minus;'=>'&#8722;', '&lowast;'=>'&#8727;', '&radic;'=>'&#8730;', '&prop;'=>'&#8733;',
			'&infin;'=>'&#8734;', '&ang;'=>'&#8736;', '&and;'=>'&#8743;', '&or;'=>'&#8744;',
			'&cap;'=>'&#8745;', '&cup;'=>'&#8746;', '&int;'=>'&#8747;', '&there4;'=>'&#8756;',
			'&sim;'=>'&#8764;', '&cong;'=>'&#8773;', '&asymp;'=>'&#8776;', '&ne;'=>'&#8800;',
			'&equiv;'=>'&#8801;', '&le;'=>'&#8804;', '&ge;'=>'&#8805;', '&sub;'=>'&#8834;',
			'&sup;'=>'&#8835;', '&nsub;'=>'&#8836;', '&sube;'=>'&#8838;', '&supe;'=>'&#8839;',
			'&oplus;'=>'&#8853;', '&otimes;'=>'&#8855;', '&perp;'=>'&#8869;', '&sdot;'=>'&#8901;',
			'&lceil;'=>'&#8968;', '&rceil;'=>'&#8969;', '&lfloor;'=>'&#8970;', '&rfloor;'=>'&#8971;',
			'&lang;'=>'&#9001;', '&rang;'=>'&#9002;', '&loz;'=>'&#9674;', '&spades;'=>'&#9824;',
			'&clubs;'=>'&#9827;', '&hearts;'=>'&#9829;', '&diams;'=>'&#9830;',
		);
		return strtr($str, $trans);
	}

	function _callback_cdata($m) {
		return htmlspecialchars($m[1]);
	}

	function _callback_lang($m) {
		$res = $m[1].'lang="'.$m[2].'" xml:lang="'.$m[2].'"';
		if (strpos($m[1].$m[3], 'class="') !== false) {
			return str_replace('class="', 'class="lang-'.$m[2].' ', $res.$m[3]);
		} else {
			return $res.' class="lang-'.$m[2].'"'.$m[3];
		}
	}

	function _callback_abbr($m) {
		$key = strtolower($m[1]);
		if (array_key_exists($key, $this->abbrs)) {
			return '<abbr title="'.htmlspecialchars($this->abbrs[$key]).'">'.$m[1].'</abbr>';
		} else {
			return $m[1];
		}
	}

	function process($str) {
		$starttime = explode(' ', microtime());

		$output = array('lang' => $this->lang);

		// language directive
		if (preg_match('/^<!--LANG:(.*)-->$/m', $str, $m)) {
			$output['lang'] = trim($m[1]);
			$str = str_replace($m[0], '', $str);
		}

		// title directive
		if (preg_match('/<title(?:\s+lang="'.$output['lang'].'")?>(.*)<\/title>/', $str, $m)) {
			$output['title'] = trim($m[1]);
			$str = str_replace($m[0], '', $str);
		}
		$str = preg_replace('/<title\s+lang=".*">.*<\/title>/', '', $str);

		// subject directive
		if (preg_match('/<h1>(.*)<\/h1>/', $str, $m)) {
			$h1 = $m[1];
			if (preg_match('/<!--\(-->(.*)<!--\)-->/', $h1, $mm)) {
				$output['subject'] = trim($mm[1]);
				$h1 = str_replace($mm[0], $mm[1], $h1);
				$str = str_replace($m[0], '<h1>'.$h1.'</h1>', $str);
			}
		}

		// simple string conversion
		$str = preg_replace_callback('/<!\[CDATA\[(.+?)]]>/s',
			array('MearieFormatter', '_callback_cdata'), $str);
		$str = preg_replace('/<li(\s.*?)?>/', '<li\1><div>', $str);
		$str = str_replace('</li>', '</div></li>', $str);
		$str = str_replace('&-', '&#8203;', $str);
		$str = preg_replace('#<a>([a-z0-9]+://.*?)</a>#', '<a href="\1">\1</a>', $str);
		$str = preg_replace_callback('/(<[^>]+)\blang="(.*?)"([^>]*>)/',
			array('MearieFormatter', '_callback_lang'), $str);
		$str = preg_replace('#(href=|src=)"/(?!img/|-\w+-/)#', '\1"'.MEARIE_SITE_PREFIX, $str);
		$str = preg_replace('#(<(?:ins|del) [^>]*datetime="[^"]+)K("[^>]*>)#', '\1+09:00\2', $str);

		if (!is_null($this->cut)) {
			$pos = strpos($str, '<!--CUT-->');
			if ($pos !== false) $str = substr($str, 0, $pos) . $this->cut;
		} else {
			$str = str_replace('<!--CUT-->', '', $str);
		}

		// some advanced string conversion
		if (!empty($this->abbrs)) {
			$str = preg_replace_callback('#<abbr>(.*?)</abbr>#',
				array(&$this, '_callback_abbr'), $str);
		}
		if (!$this->entities) $str = $this->process_entities($str);
		$str = $this->process_table($str);
		$str = $this->process_image($str);
		$str = $this->process_footnote($str, $this->uniqid);

		$endtime = explode(' ', microtime());
		$str .= sprintf("\n<!-- processed in %.4f sec -->\n",
			($endtime[1] - $starttime[1]) + ($endtime[0] - $starttime[0]));

		$output['text'] = $str;
		return $output;
	}
}

////////////////////////////////////////////////////////////////////////////////
// database interface

class MearieSqlite3Handle {
	var $handle;

	function __construct($path) {
		$this->handle = sqlite3_open($path);
	}

	function __destruct() {
		if (!is_null($this->handle)) $this->close();
	}

	function close() {
		sqlite3_close($this->handle);
		$this->handle = null;
	}

	function _preprocess($sql, $args) {
		for ($i = count($args) - 1; $i >= 0; --$i) {
			if (is_null($args[$i])) {
				$args[$i] = 'NULL';
			} elseif (is_bool($args[$i])) {
				$args[$i] = ($args[$i] ? '1' : '0');
			} elseif (!is_int($args[$i]) && !is_float($args[$i])) {
				$args[$i] = "'".str_replace("'", "''", $args[$i])."'";
			}
		}
		$i = 0;
		$sql = preg_replace('/\?/e', '$args[$i++]', $sql);
		return $sql;
	}

	function query($sql) {
		$args = func_get_args();
		array_shift($args);
		return $this->querysql($this->_preprocess($sql, $args));
	}

	function querysql($sql) {
		$result = sqlite3_query($this->handle, $sql);
		if ($result === false) return null;
		return new MearieSqlite3Resultset($result);
	}

	function exec($sql) {
		$args = func_get_args();
		array_shift($args);
		return $this->execsql($this->_preprocess($sql, $args));
	}

	function execsql($sql) {
		return sqlite3_exec($this->handle, $sql);
	}

	function lastinsert() {
		return sqlite3_last_insert_rowid($this->handle);
	}

	function error() {
		return sqlite3_error($this->handle);
	}
}

class MearieSqlite3ResultSet {
	var $handle;

	function __construct($handle) {
		$this->handle = $handle;
	}

	function __destruct() {
		if (!is_null($this->handle)) $this->close();
	}

	function close() {
		sqlite3_query_close($this->handle);
		$this->handle = null;
	}

	function fetch($assoc = true) {
		if ($assoc) {
			return sqlite3_fetch_array($this->handle);
		} else {
			return sqlite3_fetch($this->handle);
		}
	}

	function fetchone($assoc = true) {
		$result = $this->fetch($assoc);
		$this->close();
		return $result;
	}

	function fetchall($assoc = true) {
		$resultall = array();
		while ($result = $this->fetch($assoc)) {
			$resultall[] = $result;
		}
		$this->close();
		return $resultall;
	}
}

function mearie_db($path = null) {
	if (is_null($path)) $path = MEARIE_RESROOT.'mearie.db';
	return new MearieSqlite3Handle($path);
}

// vim: ts=4 sw=4
