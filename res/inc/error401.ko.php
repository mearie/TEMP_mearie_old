<?php
global $SITE;
$SITE->title = '401 Authorization Required &mdash; 메아리';
$SITE->lang = 'ko';
$SITE->morecss = 'error';
$SITE->startForce();
?>
<ul class="toc">
	<li><div><a href="/">첫 화면으로</a></div></li>
</ul>
<h1><span>401</span> Authorization Required.</h1>
<p><strong>메아리에서 권한을 확인하려 인증을 요구합니다.</strong> 다음 해결책을 고려해 보십시오.</p>
<ul>
	<li><div>새로고침을 눌러 보고 정확한 아이디와 암호를 입력하십시오.</div></li>
	<li><div>내가 생각하기에 제대로 입력했는데 안 된다면:<ul>
		<li><div>캡스락을 꺼 놓고 입력해 보십시오.</div></li>
		<li><div>혹시나 모르니 자판을 한글에서 영어 모드로 바꿔 보십시오.</div></li>
		<li><div>한 스물 세 번 정도 더 입력해 보십시오.</div></li>
		<li><div>그래도 안 되면 관리자한테 따지십시오.</div></li>
	</ul></div></li>
</ul>
<p>이 문서의 고유 주소는 다음과 같습니다.</p>
<pre>http://mearie.org<?php echo htmlspecialchars($_SERVER['REQUEST_URI']); ?></pre>

