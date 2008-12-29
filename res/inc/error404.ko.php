<?php
global $SITE;
$SITE->title = '404 Not Found &mdash; 메아리';
$SITE->lang = 'ko';
$SITE->morecss = 'error';
$SITE->startForce();
?>
<ul class="toc">
	<li><div><a href="/">첫 화면으로</a></div></li>
</ul>
<h1><span>404</span> Not Found.</h1>
<p><strong>메아리에서 이 문서를 찾을 수 없습니다.</strong> 다음 해결책을 고려해 보십시오.</p>
<ul>
	<li><div>문서를 못 찾은 데 좌절하여 <a href="http://ko.wikipedia.org/wiki/%EC%95%88%EB%85%95%2C_%EC%A0%88%EB%A7%9D%EC%84%A0%EC%83%9D">절망</a>하십시오.</div></li>
	<li><div>왠지 이 문서가 있을 법한 다른 곳을 <a href="http://google.co.kr/">구글</a>로 뒤져 보십시오.</div></li>
	<li><div><a href="http://web.archive.org/web/mearie.org<?php echo htmlspecialchars($_SERVER['REQUEST_URI']); ?>">웹 아카이브</a>에 남아 있을 가능성도 배제할 수는 없습니다.</div></li>
	<li><div>메아리 안의 문서에서 이 화면으로 넘어 왔다면 관리자에게 따져 보십시오.</div></li>
</ul>
<p>이 문서의 고유 주소는 다음과 같습니다.</p>
<pre>http://mearie.org<?php echo htmlspecialchars($_SERVER['REQUEST_URI']); ?></pre>

