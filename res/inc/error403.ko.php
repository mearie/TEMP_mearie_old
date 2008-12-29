<?php
global $SITE;
$SITE->title = '403 Forbidden &mdash; 메아리';
$SITE->lang = 'ko';
$SITE->morecss = 'error';
$SITE->startForce();
?>
<ul class="toc">
	<li><div><a href="/">첫 화면으로</a></div></li>
</ul>
<h1><span>403</span> Forbidden.</h1>
<p><strong>메아리에서 이 문서의 접근을 허용하지 않습니다.</strong> 다음 해결책을 고려해 보십시오.</p>
<ul>
	<li><div>왠지 슬래시 뒤의 글자들을 떼어도 주소가 동작할 것 같아서 한 번 들어 온 거라면, 소용 없으니 원래 페이지로 돌아 가시길 바랍니다.</div></li>
	<li><div>나만 안 보이는 것 같다 생각한다면 관리자에게 떼를 써서 보여 달라고 부탁하십시오.</div></li>
	<li><div>이걸 알아 먹을진 모르겠지만, 당신이 봇이라면 <em>당장 꺼져!</em></div></li>
</ul>
<p>이 문서의 고유 주소는 다음과 같습니다.</p>
<pre>http://mearie.org<?php echo htmlspecialchars($_SERVER['REQUEST_URI']); ?></pre>

