<?php
global $SITE;
$SITE->title = '500 Internal Server Error &mdash; 메아리';
$SITE->lang = 'ko';
$SITE->morecss = 'error';
$SITE->startForce();
?>
<ul class="toc">
	<li><div><a href="/">첫 화면으로</a></div></li>
</ul>
<h1><span>500</span> Internal Server Error.</h1>
<p><strong>메아리 서버에 문제가 있어서 이 문서를 볼 수 없습니다.</strong> 다음 해결책을 고려해 보십시오.</p>
<ul>
	<li><div>보통 관리자가 실수로 서버 설정을 잘못한 경우니까 관리자를 한 번 때려 보고 반응을 지켜 보십시오.</div></li>
	<li><div>어쩌면 진짜로 서버가 맛이 갔을 수도 있으니, 관리자에게 위로의 한 마디를 건냅시다.</div></li>
</ul>
<p>이 문서의 고유 주소는 다음과 같습니다.</p>
<pre>http://mearie.org<?php echo htmlspecialchars($_SERVER['REQUEST_URI']); ?></pre>

