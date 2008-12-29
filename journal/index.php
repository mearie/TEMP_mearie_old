<?php
include_once 'journal.inc.php';
include_once 'design.inc.php';

$npages = $JOURNAL->npages();
$page = mearie_clamp($_GET['page'], 1, $npages);

////////////////////////////////////////////////////////////////////////////////

$SITE->startLayout('ko', '');
if ($page == 1) {
	if (MEARIE_PREFER_LANGUAGE == 'en') {
?>
<p lang="en" xml:lang="en"><strong>mearie.org journal</strong> is a set of scribblings written by lithrasiir; this is like a blog but only trackbacks are permitted. Sorry that mearie.org journal is written in Korean and I have no plan to make English journal currently.</p>
<?
	} else {
?>
<p><strong>메아리 저널</strong>은 블로그인 척 하는 lifthrasiir의 잡담 모음입니다. 블로그의 형태를 하고는 있지만 댓글은 달 수 없으며, <em>오로지 트랙백만 허용됩니다.</em> 여기에 올라 온 글은 모두 저의 정신 상태 및 의견 및 오해를 듬뿍 담고 있으며, 그 이상의 무언가는 없습니다. <a href="about">(더 보기)</a></p>
<?php
	}
}

foreach ($JOURNAL->postList($page) as $post) {
	mearie_journal_show_post($post, true);
}

?>
<hr />
<?php mearie_journal_show_paging($page, $npages); ?>
<div class="feed">피드: <a href="feed"><span>Atom 1.0</span></a></div>
