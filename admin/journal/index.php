<?php
include_once 'journal.inc.php';
include_once '../../journal/design.inc.php';

$npages = $JOURNAL->npages(MEARIE_JOURNAL_PAGE_SIZE, true);
$page = mearie_clamp($_GET['page'], 1, $npages);

////////////////////////////////////////////////////////////////////////////////

$SITE->startLayout('ko', '');

if ($page == 1) {
?>
<p class="center">
	<a href="add"><strong>새 글 쓰기</strong></a> |
	<a href="list">글 목록</a> |
	<a href="taglist">태그 목록</a> |
	<a href="../">&uarr; 돌아가기</a>
</p>
<?php
}

foreach ($JOURNAL->postList($page, MEARIE_JOURNAL_PAGE_SIZE, true) as $post) {
	mearie_journal_show_post($post, true);
?>
<form action="<?php echo htmlspecialchars($post->href()); ?>" method="post">
	<input type="hidden" name="actionmap[수정]" value="modify" />
	<input type="hidden" name="actionmap[삭제]" value="delete" />
	<input type="submit" name="action" value="수정" />
	<input type="submit" name="action" value="삭제" />
</form>
<?
}

?>
<hr />
<?php mearie_journal_show_paging($page, $npages); ?>
<div class="feed">피드: <a href="feed"><span>Atom 1.0</span></a></div>
