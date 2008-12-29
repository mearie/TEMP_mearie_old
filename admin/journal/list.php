<?php
include_once 'journal.inc.php';
include_once '../../journal/design.inc.php';
$SITE->startLayout('ko', ': 글 목록');

$npages = $JOURNAL->npages(12, true);
$page = mearie_clamp($_GET['page'], 1, $npages);
?>
<h2>모든 글의 목록</h2>
<table style="width: 100%;">
<col style="width: 2em;" />
<col />
<col style="width: 10em;" />
<col style="width: 8.5em;" />
<thead>
	<tr><th>#</th><th>제목</th><th>날짜</th><th>&mdash;</th>
</thead>
<tbody>
<?php
foreach ($JOURNAL->postList($page, 12, true) as $post) {
	$href = htmlspecialchars($post->href());
?>
	<tr>
		<th><?php echo $post->id; ?></th>
		<td><a href="<?php echo $href; ?>"><?php echo htmlspecialchars($post->title); ?></a><?php if (!$post->is_public) { ?> <small>(비공개)</small><?php } ?></td>
		<td><?php echo date('Y/m/d&\n\b\s\p;H:i', $post->created_on); ?></td>
		<td><form action="<?php echo $href; ?>" method="post">
			<input type="hidden" name="actionmap[수정]" value="modify" />
			<input type="hidden" name="actionmap[삭제]" value="delete" />
			<input type="submit" name="action" value="수정" />
			<input type="submit" name="action" value="삭제" />
		</form></td>
	</tr>
<?php
}
?>
</tbody>
</table>
<?php mearie_journal_show_paging($page, $npages); ?>
<p><a href="<?php echo $JOURNAL->base; ?>">&laquo; 돌아가기</a></p>
