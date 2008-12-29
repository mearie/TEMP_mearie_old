<?php $SITE->startForce(); ?>
<p>메아리 풉; 노트.</p>
<ul>
	<li><code>&lt;&lt;메아리|어쩌구&gt;&gt;</code>를 미디어위키와 같은 방식으로 링크로 처리. XHTML에서 이 sequence는 나올 수 없으므로 변경 가능.</li>
	<li>카테고리 기능. is-a 관계와 has-a 관계를 표현할 수 있는 가장 쉬운 방법임.</li>
	<li>자동 주소 선정.<ul>
		<li>각 페이지는 그 이름에 대한 URL representation을 가지고 있다. (e.g. 카이스트 <code>kaist</code>, 유르 <code>yurr</code>, D 언어 <code>d</code>)</li>
		<li>각 페이지는 category를 가지고 있다. (e.g. 카이스트는 대한민국의 대학교, 유르는 카이스트 사람, D 언어는 C로부터 유래한 언어) 그 중 is-a 관계 정도에 해당하는 것들을 하나 골라서 principal category라고 한다. 만약 principal category가 그 책임을 다른 카테고리에게 delegate할 경우, (편의상) principal category를 쓴다 하더라도 실제 principal category는 delegate된 놈이 된다. (e.g. 대한민국의 대학교는 대학교의 subset, 카이스트 사람은 사람의 subset, C로부터 유래한 언어는 프로그래밍 언어의 subset)</li>
		<li>이런 카테고리 chain은 언젠가 끝을 내야 하는데, 그 끝은 topmost flag로 결정된다. (e.g. 카이스트 &larr; 대한민국의 대학교 [delegate] &larr; 대학교 [topmost].) topmost flag는 principal category가 없을 때 설정된다. 하지만 일반 category는 가질 수 있다. (e.g. 대학교 &larr; 교육기관)</li>
		<li>모든 페이지는 category chain을 기준으로 URL이 결정된다.</li>
	</ul></li>
</ul>

<h2>예시</h2>
<pre>
카이스트 [/university/*country/korea] /university/kaist
	-- 대한민국의 대학교 [/university/*country, delegate] /university/*country/korea
		-- 나라별 대학교 [/university, delegate] /university/*country
			-- 대학교 /university

유르 [/people/*kaist] /people/yurr
	-- 카이스트 사람 [/people, delegate] /people/*kaist
		-- 사람 /people

Tango 라이브러리 [/software/library] /software/library/tango
	-- 라이브러리 [/software] /software/library
		-- 소프트웨어 /software
	-- D 언어 [/programming-language/*c-like] /programming-language/d
		-- C로부터 유래한 프로그래밍 언어 [/programming-language, delegate] /programming-language/*c-like
			-- 프로그래밍 언어 /programming-language
				-- 프로그래밍 /programming

후우라 카후카 [/media/zetsubou-sensei] /media/zetsubou-sensei/fuura-kafuka
	-- 안녕, 절망선생 [/media/*anime] /media/zetsubou-sensei
		-- 일본 애니메이션 [/media, delegate] /media/*anime
			-- (이름 미정) /media

공길동전 [/people/choi-gaya/*cartoon] /media/gonggildong-jeon
	-- 최 가야의 작품 [/people/choi-gaya] /people/choi-gaya/*cartoon
		-- 최 가야 [/people/*cartoonist] /people/choi-gaya
			-- 만화가 [/people, delegate] /people/*cartoonist
				-- 사람 /people

풉; [/irc/hanirc/c0sm0s/*terms] /irc/hanirc/c0sm0s/pub
	-- #c0sm0s 채널의 유행어 [/irc/hanirc/c0sm0s, delegate] /irc/hanirc/c0sm0s/*terms
		-- #c0sm0s 채널 [/irc/hanirc] /irc/hanirc/c0sm0s
			-- HanIRC [/irc/*network] /irc/hanirc
				-- IRC 네트워크 [/irc, delegate] /irc/*network
					-- IRC /irc
						-- 네트워크 프로토콜 [/programming] /programming/network-protocol
							-- 프로그래밍 /programming
</pre>

<h2>디비 스키마</h2>
<pre>
PREFIX_page
	num - 고유번호
	id - URL representation
	path - path expansion (미리 한다.)
	name - 이름
	name_html - HTML 형식의 이름 (보통 자동으로 채워짐)
	contents - 내용 (렌더러에게 전달되는 것)
	parent - principal category

PREFIX_history
	num - 번호
	datetime - 변경된 날짜
	id, path, name, name_html, contents, parent - 위와 동일
	contents_raw - 1이면 contents는 그냥 내용, 0이면 diff

PREFIX_category
	num - 번호
	category - 카테고리 페이지 번호

PREFIX_links
	num - 글 번호
	link - 링크된 글의 번호


e.g.
# num=0은 존재하지 않음. 편의상 "blank"를 담기 위해서 사용.
# num=0 id="" path="/" name="" parent=0 category=0
num=2 id="academia" path="/academia" name="학문" parent=0 category=
num=5 id="science" path="/science" name="과학" parent=0 category=2
num=6 id="*natural" path="/science/*natural" name="자연 과학" parent=5 category=5
num=8 id="biology" path="/biology" name="생물학" parent=0 category=6
num=13 id="species" path="/species" name="생물 종" parent=0 category=8
num=15 id="human" path="/species/human" name="인간" parent=13 category=13
num=37 id="person" path="/person" name="사람" parent=0 category=15
num=38 id="*friend" path="/person/*friend" name="lifthrasiir의 친구" parent=37 category=37
num=39 id="*kaist" path="/person/*kaist" name="카이스트 사람" parent=37 category=37
num=40 id="yurr" path="/person/yurr" name="유르" parent=37 category=38,39
num=88 id="+inklgirl" path="/person/yurr/+inklgirl" name="인클걸" parent=40 category=40,63
</pre>

