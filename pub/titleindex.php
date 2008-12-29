<?php $SITE->startForce(); ?>
<title>메아리 풉; TitleIndex</title>
<h1>(가짜) TitleIndex</h1>
<p>하도 원하는 사람이 많아서 임시로 만들었음. 대강 대충 만들었으므로 심각하게 사용하지 않길 바람.</p>
<ul><!-- style="-moz-column-count:2; -moz-column-gap:30px; -webkit-column-count:2; -webkit-column-gap:30px; column-count:2; column-gap:30px;"-->
<?php
exec('find . -name "*.html" -printf "%10C@%P\n" | sort -r', $lines);
foreach ($lines as $line) {
	$mtime = intval(substr($line, 0, 10));
	$path = substr($line, 10, -5);
	if (substr($path, -6) == '/index') $path = substr($path, 0, -6);
	$path = '/'.$path;
	echo "\t<li><small>".date('Y-m-d H:i:s', $mtime)."</small> <a href=\"$path\">$path</a></li>\n";
}
?>
</ul>
