<?php
global $SITE;
$SITE->title = '500 Internal Server Error &mdash; mearie.org';
$SITE->lang = 'en';
$SITE->morecss = 'error';
$SITE->startForce();
?>
<ul class="toc">
	<li><div><a href="/">Main page</a></div></li>
</ul>
<h1><span>500</span> Internal Server Error.</h1>
<p><strong>mearie.org server has a problem and cannot serve this document.</strong> You may do the following:</p>
<ul>
	<li><div>Normally this is because the administrator configured a server incorrectly. Strike him and wait for reaction.</div></li>
	<li><div>If the server is <em>really</em> corrupted, give him some words of consolation.</div></li>
</ul>
<p>You have reached here from:</p>
<pre>http://mearie.org<?php echo htmlspecialchars($_SERVER['REQUEST_URI']); ?></pre>

