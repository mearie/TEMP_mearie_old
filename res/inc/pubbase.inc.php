<?php
define('MEARIE_DOCROOT', '/home/tokigun/mearie/pub/');
require_once 'lib.inc.php';
require_once 'layout.inc.php';

class MeariePubFormatter extends MearieFormatter {
	function _callback_wikilink($m) {
		if ($m[1] == '' || $m[1] == '/') {
			return $m[0];
		} elseif (substr($m[1], 0, 2) == '..') {
			$path = $this->dirgrandparent.substr($m[1], 2);
		} elseif ($m[1]{0} == '.') {
			$path = $this->dirparent.substr($m[1], 1);
		} elseif ($m[1]{0} == '/') {
			$path = substr($m[1], 1);
		} else {
			$path = $this->dirparent.'/'.$m[1];
		}
		$m[0] = '<a href="/'.$path.$m[2].'"';
		if (file_exists(MEARIE_DOCROOT.$path.'.php')) return $m[0];
		if (file_exists(MEARIE_DOCROOT.$path.'.html')) return $m[0];
		if (file_exists(MEARIE_DOCROOT.$path.'/index.html')) return $m[0];
		return $m[0].' class="deadlink"';
	}

	function process_pub($str) {
		$path = $_SERVER['SCRIPT_NAME'];
		if (substr($path, -5) == '.html') $path = substr($path, 0, -5);
		if (substr($path, -6) == '/index') $path = substr($path, 0, -6);

		$this->dircurrent = rtrim(substr($path, 1), '/');
		$this->dirparent = substr(rtrim($this->dircurrent,
			'0123456789abcdefghijklmnopqrstuvwxyz-.@'), 0, -1);
		$this->dirgrandparent = substr(rtrim($this->dirparent,
			'0123456789abcdefghijklmnopqrstuvwxyz-.@'), 0, -1);

		return preg_replace_callback('@<a href="([^:#]*?)(#.*?)?"@',
			array('MeariePubFormatter', '_callback_wikilink'), $str);
	}

	function process($str) {
		$output = MearieFormatter::process($str);
		$output['text'] = $this->process_pub($output['text']);
		return $output;
	}
}

class MeariePubLayout extends MearieMainLayout {
	function __construct($requri) {
		MearieMainLayout::__construct($requri);
		$this->title = '메아리 풉;';
		$this->css = 'pub';
	}

	function get_formatter() {
		return new MeariePubFormatter(array('lang' => $this->lang));
	}

	function show_header() {
		$title = $this->title;
		if (isset($this->subject)) {
			$title = $this->subject.' &mdash; '.$title;
		}

?>
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" xml:lang="<?php echo $this->lang; ?>">
<head>
	<meta http-equiv="Content-Language" content="<?php echo $this->lang; ?>" />
	<meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
	<title><?php echo $title; ?></title>
	<meta name="author" content="Kang Seonghoon (lifthrasiir)" />
	<meta name="generator" content="<?php echo MEARIE_GENERATOR; ?> pub edition" />
	<link rel="stylesheet" media="screen" href="/res/css/<?php echo $this->css; ?>.css" type="text/css" />
	<!--[if IE]><link rel="stylesheet" media="screen" href="/res/css/<?php echo $this->css; ?>.ie.css" type="text/css" /><![endif]-->
<?php if (!is_null($this->morecss)) { ?>
	<link rel="stylesheet" media="screen" href="/res/css/<?php echo $this->morecss; ?>.css" type="text/css" />
	<!--[if IE]><link rel="stylesheet" media="screen" href="/res/css/<?php echo $this->morecss; ?>.ie.css" type="text/css" /><![endif]-->
<?php } ?>
	<link rel="shortcut icon" href="/res/img/icon-pub.ico" type="image/vnd.microsoft.icon" />
	<link rel="icon" href="/res/img/icon-pub-16x16.png" type="image/png" />
	<script type="text/javascript" src="/res/js/global.js"></script>
	<script type="text/javascript">/*<![CDATA[*/var mearie_props = {lang: '<?php echo $this->lang; ?>', preflang: '<?php echo MEARIE_PREFER_LANGUAGE; ?>'};/*]]>*/</script>
<?php if (isset($this->head)) echo $this->head; ?>
</head>
<body class="<?php echo $this->layout; ?>-layout">
<div id="wrap" <?php mearie_lang($this->lang); ?>>
<div id="header">
	<div id="sitename"><a href="<?php echo MEARIE_SITE_PREFIX; ?>">메아리 풉;</a></div>
	<p id="tagline">… 백과사전을 가장한 잡학사전</p>
</div>
<hr />
<div id="body"><a id="top"></a>
<!-- CONTENT FOLLOWS -->
<?php
	}

	function show_namespace() {
		if (substr($_SERVER['SCRIPT_FILENAME'], -11) != '/index.html') return;

		$base = mearie_script_base();
		$dp = opendir($base);
		$files = array();
		while (($f = readdir($dp)) !== false) {
			if ($f == '.' || $f == '..' || $f == 'index.html') continue;
			if (substr($f, -5) == '.html') {
				$fp = fopen($base.$f, 'r');
				$f = substr($f, 0, -5);
			} else {
				$fp = fopen($base.$f.'/index.html', 'r');
			}
			if (preg_match('#^<h1>.*<!--\(-->(.*?)<!--\)-->.*</h1>$#', fgets($fp), $m)) {
				$title = $m[1];
			} else {
				$title = null;
			}
			fclose($fp);
			$files[$f] = $title;
		}
		closedir($dp);
		if (count($files) > 0) {
			asort($files);
			echo "<fieldset class=\"subpages\">\n<legend>하위 페이지들</legend>\n\t<ul>\n";
			foreach ($files as $f => $title) {
				if (is_null($title)) $title = "($f)";
				echo "\t\t<li><div><a href=\"$f\">$title</a></div></li>\n";
			}
			echo "\t</ul>\n</fieldset>\n";
		}
	}

	function show_footer() {
		$this->show_namespace();
?>

<!-- CONTENT ENDS -->
</div>
<hr />
<div id="footer">
<?php
	if (substr($_SERVER['SCRIPT_FILENAME'], -5) == '.html') {
		$pagemtime = filemtime($_SERVER['SCRIPT_FILENAME']);
		switch ($mearie_page_props['lang']) {
		case 'ko': $dtformat = '최근 바뀜: Y년 n월 j일 H시 i분 s초 (T)'; break;
		default: $dtformat = '\L\a\s\t \m\o\d\i\f\i\e\d \o\n: r'; break;
		}
?>
	<p class="pageinfo" title="<?php echo date($dtformat, $pagemtime); ?>"><?php echo date('Y-m-d H:i:s T', $pagemtime); ?></p>
<?php
	}
?>
	<p class="location">
		<a href="<?php echo MEARIE_SITE_PREFIX; ?>about/">About pub.mearie.org</a> |
		<a href="<?php echo MEARIE_SITE_PREFIX; ?>about/copyright">Copyright &copy;2007&ndash;<?php echo date('Y'); ?>, Kang Seonghoon</a>
	</p>
</div>
</div>
</body>
</html>
<?php
	}
}

// vim: ts=4 sw=4
