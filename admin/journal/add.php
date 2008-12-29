<?php
include_once 'journal.inc.php';

$message = '';
$isokay = null;
if (isset($_POST['url'])) {
	$tags = (trim($_POST['tags']) ? array_map('trim', explode(',', $_POST['tags'])) : array());
	$data = array(
		'url' => $_POST['url'],
		'title' => $_POST['title'],
		'tags' => $tags,
		'contents' => $_POST['contents'],
		'created_on' => time(),
		'updated_on' => time(),
		'is_public' => isset($_POST['is_public']),
	);
	if ($JOURNAL->addPost($data)) {
		$isokay = true;
		$message = '<strong>새 글이 성공적으로 작성되었음.</strong>';
	} else {
		$isokay = false;
		$message = '<strong>새 글 작성에 실패함.</strong><br />SQLite 에러 메시지: <code>'.
			htmlspecialchars($JOURNAL->error()).'</code>';
	}
}

////////////////////////////////////////////////////////////////////////////////

$SITE->startLayout('ko', '', '');

if ($message) {
?>
<fieldset>
	<?php echo $message; ?>
	<?php if ($isokay) { ?><a href="<?php echo $JOURNAL->base.date('Y/m/').$data['url']; ?>">[숨기기]</a><?php } ?>
</fieldset>
<?php
} else {
?>
<fieldset>
<legend>글 쓰기</legend>
<form action="?" method="post">
	URL: <samp>/<?php echo date('Y/m'); ?>/<input type="text" name="url" value="" /></samp><br />
	제목: <input type="text" name="title" size="60" value="" /><br />
	태그: <input type="text" name="tags" size="60" value="" /> (,로 구분)<br />
	<textarea name="contents" rows="16" cols="80" style="width: 100%;"></textarea><br />
	<input type="checkbox" id="is_public" name="is_public" value="1" /><label for="is_public"> 공개</label><br />
	<input type="submit" value="쓰기" />
</form>
</fieldset>
<p><a href="<?php echo $JOURNAL->base; ?>">&laquo; 돌아가기</a></p>
<?php
}
?>
