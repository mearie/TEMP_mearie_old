<?php $SITE->startForce(); ?>
<title>메아리 풉; WantedPages</title>
<h1>(가짜) WantedPages</h1>
<ul style="-moz-column-count:2; -moz-column-gap:30px; -webkit-column-count:2; -webkit-column-gap:30px; column-count:2; column-gap:30px;">
<?php
exec('find . -name "*.html"', $lines);
$links = array();
foreach ($lines as &$line) {
	$data = file_get_contents($line);
	$line = substr($line, 1, -5);
	if (substr($line, -6) == '/index') $line = substr($line, 0, -6);
	$dir = substr(rtrim($line, '0123456789abcdefghijklmnopqrstuvwxyz-.@'), 0, -1);
	$pdir = substr(rtrim($dir, '0123456789abcdefghijklmnopqrstuvwxyz-.@'), 0, -1);

	preg_match_all('@<a href="([^:#]+?)(?:#.*?)?"@', $data, $ilinks);
	foreach ($ilinks[1] as $link) {
		$path = rtrim($link, '/');
		if (substr($path, 0, 2) == '..') {
			$path = $pdir.substr($path, 1);
		} elseif ($path{0} == '.') {
			$path = $dir.substr($path, 1);
		} elseif ($path{0} != '/') {
			$path = $dir.'/'.$path;
		}
		$links[$path] = null;
	}
	unset($data);
}
$links = array_diff_key($links, array_flip($lines));
ksort($links);
foreach ($links as $link => $_) {
	echo "\t<li><a href=\"$link\">$link</a></li>\n";
}
?>
</ul>
