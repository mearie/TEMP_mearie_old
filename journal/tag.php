<?php
include_once 'journal.inc.php';

$tagid = substr(isset($_SERVER['PATH_INFO']) ? $_SERVER['PATH_INFO'] : '', 1);
if ($tagid) {
	$tag = $JOURNAL->getTagFromURL($tagid);
	if (is_null($tag)) $SITE->httpError(404);
}

////////////////////////////////////////////////////////////////////////////////

$SITE->startLayout('ko', ': 태그', $tagid ? $tag->name : null);

if ($tagid) {
?>
<h1><small>태그:</small> <?php echo htmlspecialchars($tag->name); ?></h1>
<?php echo $tag->contents(); ?>
<table class="full">
<tbody>
<?php foreach ($tag->posts() as $post) { ?>
<tr>
	<td><a href="<?php echo htmlspecialchars($post->href()); ?>"><?php echo htmlspecialchars($post->title); ?></a></td>
	<td class="right"><?php echo $post->datetime(); ?></td>
</tr>
<?php } ?>
</tbody>
</table>
<div class="feed">피드: <a href="<?php echo $JOURNAL->base.'feed/'.$tagid; ?>"><span>Atom 1.0</span></a></div>
<?php
} else {
?>
<h1>태그들</h1>
<ul class="taglist">
<?php foreach ($JOURNAL->tagList(-1) as $tag) { ?>
	<li><a href="<?php echo htmlspecialchars($tag->href()); ?>"><?php echo htmlspecialchars($tag->name); ?></a><small>(<?php echo $tag->nposts(); ?>)</small></li>
<?php } ?>
</ul>
<?php
}
?>
<p><a href="<?php echo $JOURNAL->base; ?>">&laquo; 돌아가기</a></p>
