<?php
global $SITE;
$SITE->title = '404 Not Found &mdash; mearie.org';
$SITE->lang = 'en';
$SITE->morecss = 'error';
$SITE->startForce();
?>
<ul class="toc">
	<li><div><a href="/">Main page</a></div></li>
</ul>
<h1><span>404</span> Not Found.</h1>
<p><strong>mearie.org cannot access this document.</strong> You may do the following:</p>
<ul>
	<li><div><a href="http://google.co.kr/">Google</a> for more likely address of the document;</div></li>
	<li><div>Search <a href="http://web.archive.org/web/mearie.org<?php echo htmlspecialchars($_SERVER['REQUEST_URI']); ?>">Web Archive</a> for older version of this document, or;</div></li>
	<li><div>Lynch the administrator if you reached here from a document in mearie.org. Also:</div></li>
	<li><div>Report this page to <a href="http://www.plinko.net/404/">404 Research Lab</a> so they answer here is too bit plain.</div></li>
</ul>
<p>You have reached here from:</p>
<pre>http://mearie.org<?php echo htmlspecialchars($_SERVER['REQUEST_URI']); ?></pre>

