<?php
global $SITE;
$SITE->title = '401 Authorization Required &mdash; mearie.org';
$SITE->lang = 'en';
$SITE->morecss = 'error';
$SITE->startForce();
?>
<ul class="toc">
	<li><div><a href="/">Main page</a></div></li>
</ul>
<h1><span>401</span> Authorization Required.</h1>
<p><strong>mearie.org requires authorization to check permission for this document.</strong> You may do the following:</p>
<ul>
	<li><div>Refresh this page and input the correct ID and password again.</div></li>
	<li><div>If it doesn't work:<ul>
		<li><div>Turn off caps lock and try again.</div></li>
		<li><div>If you use Korean IME or sorta, check input mode of the IME.</div></li>
		<li><div>Try these twenty-three times more.</div></li>
		<li><div>If these all don't work, contact the administrator.</div></li>
	</ul></div></li>
</ul>
<p>You have reached here from:</p>
<pre>http://mearie.org<?php echo htmlspecialchars($_SERVER['REQUEST_URI']); ?></pre>

