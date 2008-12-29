<?php
require_once 'lib.inc.php';

class MearieMainLayout extends Mearie {
	function __construct($requri) {
		Mearie::__construct($requri);

		$this->title = 'mearie.org';
		$this->header = 'mearie.org';
		$this->lang = 'ko';
		$this->lang_warning = true;
		$this->css = 'global';
		$this->morecss = null;
		$this->layout = 'full';

		if (preg_match('/\.(ko|en|ja)\./', $_SERVER['SCRIPT_NAME'], $m)) {
			$this->lang = $m[1];
		}
		if (substr($_SERVER['SCRIPT_NAME'], -5) == '.html') {
			$this->convert_level = 2;
		} else {
			$this->convert_level = 0;
		}
	}

	function get_formatter() {
		return new MearieFormatter(array('lang' => $this->lang));
	}

	function show_header() {
		/*
		if (isset($props['region'])) {
			$region = $props['region'];
		} else {
			$region = $SITE->region();
		}
		*/

		/*
		// postprocess header
		$header = $props['header'];
		$header = preg_replace('#""|"(.+?)"(/[a-z0-9-/?&=%.+]*)#i', '<a href="\2">\1</a>', $header);
		$header = str_replace('<a href=""></a>', '', $header); // remove null link
		$header = str_replace('mearie.org', '<a class="sitename" href="/">mearie.org</a>', $header);
		if (MEARIE_PREFER_LANGUAGE) {
			$header = preg_replace('#href="/(?!-\w+-/)#', 'href="'.MEARIE_SITE_PREFIX, $header);
		}
		*/

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
	<meta name="generator" content="<?php echo MEARIE_GENERATOR; ?>" />
	<link rel="stylesheet" media="screen" href="/res/css/<?php echo $this->css; ?>.css" type="text/css" />
	<!--[if IE]><link rel="stylesheet" media="screen" href="/res/css/<?php echo $this->css; ?>.ie.css" type="text/css" /><![endif]-->
<?php if (!is_null($this->morecss)) { ?>
	<link rel="stylesheet" media="screen" href="/res/css/<?php echo $this->morecss; ?>.css" type="text/css" />
	<!--[if IE]><link rel="stylesheet" media="screen" href="/res/css/<?php echo $this->morecss; ?>.ie.css" type="text/css" /><![endif]-->
<?php } ?>
	<link rel="shortcut icon" href="/res/img/icon.ico" type="image/vnd.microsoft.icon" />
	<link rel="icon" href="/res/img/icon-16x16.png" type="image/png" />
	<script type="text/javascript" src="/res/js/global.js"></script>
	<script type="text/javascript">/*<![CDATA[*/var mearie_props = {lang: '<?php echo $this->lang; ?>', preflang: '<?php echo MEARIE_PREFER_LANGUAGE; ?>'};/*]]>*/</script>
<?php if (isset($this->head)) echo $this->head; ?>
</head>
<body class="<?php echo $this->layout; ?>-layout">
<div id="wrap" <?php mearie_lang($this->lang); ?>>
<div id="header">
<?php if ($this->lang == 'ko') { ?>
	<div id="sitename"><a href="<?php echo MEARIE_SITE_PREFIX; ?>">메아리</a></div>
	<p id="tagline">… 세상에 울려 퍼지는 나의 생각.</p>
<?php } else if (true || $this->lang == 'en') { ?>
	<div id="sitename"><a href="<?php echo MEARIE_SITE_PREFIX; ?>">mearie.org</a></div>
	<p id="tagline">… ever-echoing thoughts since 1999.</p>
<?php } ?>
</div>
<hr />
<div id="body"><a id="top"></a>
<!-- CONTENT FOLLOWS -->
<?php if ($this->lang_warning && MEARIE_PREFER_LANGUAGE && $this->lang != MEARIE_PREFER_LANGUAGE) { ?>
<div class="warning notavail" lang="<?php echo MEARIE_PREFER_LANGUAGE; ?>" xml:lang="<?php echo MEARIE_PREFER_LANGUAGE; ?>" class="lang-<?php echo MEARIE_PREFER_LANGUAGE; ?>">
<?php if (MEARIE_PREFER_LANGUAGE == 'ko') { ?>
	<p><strong>이 문서는 선택한 언어(한국어)로 제공되지 않습니다.</strong> 아래에서 원하는 언어를 선택해 주세요.</p>
<?php } elseif (MEARIE_PREFER_LANGUAGE == 'en') { ?>
	<p><strong>This document is not available in your preferred language (English).</strong> Please select other language if you want.</p>
<?php } elseif (MEARIE_PREFER_LANGUAGE == 'ja') { ?>
	<p><strong>このページは選択した言語(日本語)で提供されないです。</strong> 他の言語を選択してください。</p>
<?php } ?>
</div>
<?php } ?>
<?php
	}

	function show_footer() {
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
		<a href="<?php echo MEARIE_SITE_PREFIX; ?>about/">About mearie.org</a> |
		<a href="<?php echo MEARIE_SITE_PREFIX; ?>about/contact">Contact</a> |
		<a href="<?php echo MEARIE_SITE_PREFIX; ?>service/language">Language</a> |
		<a href="<?php echo MEARIE_SITE_PREFIX; ?>about/copyright">Copyright &copy;1999&ndash;<?php echo date('Y'); ?>, Kang Seonghoon</a>
	</p>
</div>
</div>
</body>
</html>
<?php
	}

	function start() {
		if ($this->convert_level > 0) ob_start();
		@include_once mearie_script_base().'prepend0.inc.php';
	}

	function startForce($newlevel = 2) {
		$this->convert_level = $newlevel;
		$this->start();
	}

	function end() {
		@include_once mearie_script_base().'append0.inc.php';
		if ($this->convert_level > 0) {
			$text = ob_get_clean();
			if ($this->convert_level > 1) {
				$formatter = $this->get_formatter();
				$output = $formatter->process($text);
				foreach ($output as $key => $value) {
					$this->$key = $value;
				}
				$text = $output['text'];
			}
			$this->show_header();
			echo $text;
			$this->show_footer();
		}
	}
}

// vim: ts=4 sw=4
