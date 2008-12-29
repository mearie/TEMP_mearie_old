<?php
include_once 'journal.inc.php';
include_once '../../journal/design.inc.php';
$SITE->startLayout('ko', ': 태그 목록');

$message = '';
if (!isset($_POST['action'])) {
	// do nothing
} elseif ($_POST['action'] == 'add') {
	if ($JOURNAL->addTag($_POST['url'], $_POST['name'])) {
		$message = '<strong>새 태그가 성공적으로 추가되었음.</strong>';
	} else {
		$message = '<strong>새 태그 추가에 실패함.</strong><br />SQLite 에러 메시지: <code>'.
			htmlspecialchars($JOURNAL->error()).'</code>';
	}
} elseif ($_POST['action'] == 'modify') {
	if ($JOURNAL->updateTag($_POST['url'], $_POST['name'], $_POST['title'], $_POST['desc'])) {
		$message = '<strong>태그가 성공적으로 갱신됨.</strong>';
	} else {
		$message = '<strong>태그 갱신에 실패함.</strong><br />SQLite 에러 메시지: <code>'.
			htmlspecialchars($JOURNAL->error()).'</code>';
	}
} elseif ($_POST['action'] == 'delete') {
	if ($JOURNAL->deleteTag($_POST['url'])) {
		$message = '<strong>태그를 성공적으로 삭제함.</strong>';
	} else {
		$message = '<strong>태그를 삭제하지 못 함.</strong><br />SQLite 에러 메시지: <code>'.
			htmlspecialchars($JOURNAL->error()).'</code>';
	}
}

define('MEARIE_JOURNAL_TAGPAGE_SIZE', 12);
$npages = mearie_npages($JOURNAL->ntags(), MEARIE_JOURNAL_TAGPAGE_SIZE);
$page = mearie_clamp($_GET['page'], 1, $npages);
?>
<?php if ($message) { ?>
<fieldset><?php echo $message; ?> <a href="?page=<?php echo $page; ?>">[숨기기]</a></fieldset>
<?php } ?>
<h2>모든 태그의 목록</h2>
<table style="width: 100%;">
<col style="width: 8em;" />
<col />
<col style="width: 4.5em;" />
<thead>
	<tr><th>ID</th><th>정보</th><th>&mdash;</th>
</thead>
<tbody>
<?php
$i = 0;
foreach ($JOURNAL->tagList($page, MEARIE_JOURNAL_TAGPAGE_SIZE) as $tag) {
	$url = htmlspecialchars($tag->url);
?>
	<tr>
		<th><a href="<?php echo htmlspecialchars($tag->href()); ?>"><?php echo $url; ?></a></th>
		<td><form action="?page=<?php echo $page; ?>" method="post">
			<input type="hidden" name="action" value="modify" />
			<input type="hidden" name="url" value="<?php echo $url; ?>" />
			<input type="text" name="name" value="<?php echo htmlspecialchars($tag->name); ?>" size="12" style="font-weight: bold; width: 20%;" />
			<input type="text" name="title" value="<?php echo htmlspecialchars($tag->title); ?>" size="36" style="width: 60%;" />
			<input type="submit" value="수정" /><input type="button" value="<?php echo ($tag->contents ? '▼' : '▽'); ?>" style="padding: 0;" onclick="toggle('desc<?php echo $i; ?>');" /><br />
			<textarea id="desc<?php echo $i; ?>" name="desc" rows="2" cols="60" style="width: 99%; display: none;"><?php echo htmlspecialchars($tag->contents); ?></textarea>
		</form></td>
		<td><form action="?page=<?php echo $page; ?>" method="post" onsubmit="return confirm('정말로 진행합니까?');">
			<input type="hidden" name="action" value="delete" />
			<input type="hidden" name="url" value="<?php echo $url; ?>" />
			<input type="submit" value="삭제" />
		</form></td>
	</tr>
<?php
	++$i;
}
?>
</tbody>
</table>
<?php mearie_journal_show_paging($page, $npages); ?>
<fieldset>
	<legend>태그 추가</legend>
	<form action="?page=<?php echo $page; ?>" method="post">
		<input type="hidden" name="action" value="add" />
		ID <input type="text" name="url" size="16" /> &rarr;
		이름 <input type="text" name="name" size="16" />
		<input type="submit" value="추가" />
	</form>
</fieldset>
<p><a href="<?php echo $JOURNAL->base; ?>">&laquo; 돌아가기</a></p>
