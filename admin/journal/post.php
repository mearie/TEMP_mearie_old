<?php
include_once 'journal.inc.php';
include_once '../../journal/design.inc.php';

$action = '';
if (isset($_POST['action'])) {
	$action = $_POST['action'];
	if (isset($_POST['actionmap'][$action])) {
		$action = $_POST['actionmap'][$action];
	}
}

$message = '';
$isokay = null;
if ($action == 'modify' && isset($_POST['id'])) {
	$update_timestamp = isset($_POST['update_timestamp']);
	$made_into_public = !intval($_POST['prev_is_public']) && isset($_POST['is_public']);
	$tags = (trim($_POST['tags']) ? array_map('trim', explode(',', $_POST['tags'])) : array());
	$data = array(
		'title' => $_POST['title'],
		'tags' => $tags,
		'contents' => $_POST['contents'],
		'created_on' => ($update_timestamp && $made_into_public ? time() : null),
		'updated_on' => ($update_timestamp ? time() : null),
		'is_public' => isset($_POST['is_public']),
	);
	if ($JOURNAL->updatePost(intval($_POST['id']), $data)) {
		$isokay = true;
		$message = '<strong>글을 성공적으로 갱신했음.</strong>';
	} else {
		$isokay = false;
		$message = '<strong>글을 갱신하는 데 실패함.</strong> SQLite 에러 메시지: <code>'.
			htmlspecialchars($JOURNAL->error()).'</code>';
	}
} elseif ($action == 'delete' && isset($_POST['id'])) {
	$id = intval($_POST['id']);
	if ($JOURNAL->deletePost($id)) {
		$isokay = true;
		$message = '<strong>글을 성공적으로 삭제했음.</strong>';
	} else {
		$isokay = false;
		$message = '<strong>글을 지우는 데 실패함.</strong> SQLite 에러 메시지: <code>'.
			htmlspecialchars($JOURNAL->error()).'</code>';
	}
}

$post = $JOURNAL->getPostFromURL($_SERVER['PATH_INFO']);
if (!$message && is_null($post)) $SITE->httpError(404);

////////////////////////////////////////////////////////////////////////////////

$SITE->startLayout('ko', ': '.date('Y년 n월', $post->created_on), $post->title);

if ($message) {
?>
<div class="<?php ($isokay ? 'message' : 'warning'); ?>">
	<?php echo $message; ?>
	<a href="<?php echo htmlspecialchars(is_null($post) ? $JOURNAL->base : $post->href()); ?>">[숨기기]</a>
</div>
<?
} elseif ($action == 'modify') {
?>
<fieldset>
<legend>글 고치기</legend>
<form action="?" method="post">
	<input type="hidden" name="action" value="modify" />
	<input type="hidden" name="id" value="<?php echo $post->id; ?>" />
	<input type="hidden" name="prev_is_public" value="<?php echo intval($post->is_public); ?>" />
	제목: <input type="text" name="title" size="60" value="<?php echo htmlspecialchars($post->title); ?>" /><br />
	태그: <input type="text" name="tags" size="60" value="<?php echo htmlspecialchars(implode(', ', $post->tags)); ?>" /> (,로 구분)<br />
	<textarea name="contents" rows="16" cols="80" style="width: 100%;"><?php echo htmlspecialchars($post->contents); ?></textarea><br />
	<input type="checkbox" id="is_public" <?php mearie_checked('is_public', $post->is_public); ?> /><label for="is_public"> 공개</label>
	<input type="checkbox" id="update_timestamp" name="update_timestamp" value="1" /><label for="update_timestamp"> 수정일 갱신</label><br />
	<input type="submit" value="쓰기" /> 또는 <a href="<?php echo htmlspecialchars($post->href()); ?>">&uarr; 돌아가기</a>
</form>
</fieldset>
<?php
} elseif ($action == 'delete') {
?>
<fieldset>
<legend>글 지우기</legend>
<form action="?" method="post">
	<input type="hidden" name="action" value="delete" />
	<input type="hidden" name="id" value="<?php echo $post->id; ?>" />
	정말로 이 글을 지웁니까?<br />
	<input type="submit" value="지우기" /> 또는 <a href="<?php echo htmlspecialchars($post->href()); ?>">&uarr; 돌아가기</a>
</form>
</fieldset>
<?
}
if (!is_null($post)) {
	mearie_journal_show_post($post, false);
?>
<?php if ($message || !$action) { ?>
<form action="<?php echo htmlspecialchars($post->href()); ?>" method="post">
	<input type="hidden" name="actionmap[수정]" value="modify" />
	<input type="hidden" name="actionmap[삭제]" value="delete" />
	<input type="submit" name="action" value="수정" />
	<input type="submit" name="action" value="삭제" />
</form>
<?php } ?>
<hr />
<p><a href="<?php echo $JOURNAL->base; ?>">&laquo; 돌아가기</a></p>
<?php
}
?>
