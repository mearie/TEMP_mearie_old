<?php
global $SITE;
$SITE->title = '403 Forbidden &mdash; mearie.org';
$SITE->lang = 'en';
$SITE->morecss = 'error';
$SITE->startForce();
?>
<ul class="toc">
	<li><div><a href="/">Main page</a></div></li>
</ul>
<h1><span>403</span> Forbidden.</h1>
<p><strong>mearie.org forbids the access to this document.</strong> You may do the following:</p>
<ul>
	<li><div>If you expected another page by striping letters past last slash, your attempt was so useless that you should go backward.</div></li>
	<li><div>If you feel this document is forbidden to only yourself, ask for the administrator with some <em>*cough*</em> gift <em>*cough*</em>.</div></li>
	<li><div>Evil bot sucks. If you are one, goodbye.</div></li>
</ul>
<p>You have reached here from:</p>
<pre>http://mearie.org<?php echo htmlspecialchars($_SERVER['REQUEST_URI']); ?></pre>

