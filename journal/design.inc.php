<?php
include_once 'journal.inc.php';

function mearie_journal_show_post($post, $listing) {
	$head = ($listing ? 'h2' : 'h1');
?>
<div class="entry">
<<?php echo $head; ?>>
	<span class="posted-on"><?php echo $post->datetime(!$listing); ?></span>
<?php if ($listing) { ?>
	<a href="<?php echo htmlspecialchars($post->href()); ?>"><?php echo htmlspecialchars($post->title); ?></a>
<?php } else { ?>
	<?php echo htmlspecialchars($post->title); ?>
<?php } ?>
</<?php echo $head; ?>>
<div class="metadata">
<?php if (count($post->tags)) { ?>
	<ul class="tags">
<?php foreach ($post->tags() as $tag) { ?>
		<li><a href="<?php echo htmlspecialchars($tag->href()); ?>"><?php echo htmlspecialchars($tag->name); ?></a></li>
<?php } ?>
	</ul>
<?php } ?>
</div>
<?php
	if ($listing) {
		$cutmsg = '<p><a href="'.htmlspecialchars($post->href()).'">[계속 보기]</a></p>';
		$options = array('cut' => $cutmsg);
	} else {
		$options = array();
	}
	echo $post->contents($options);
?>
<?php if (!$listing && count($comments = $post->comments())) { ?>
<div class="comments">
<?php var_dump($comments); ?>
</div>
<?php } ?>
</div>
<?php
}

function mearie_journal_show_paging($page, $npages) {
	$threshold = 5;

	$startpage = $page - $threshold;
	$showstart = ($startpage > 1);
	if (!$showstart) $startpage = 1;

	$endpage = $page + $threshold;
	$showend = ($endpage < $npages);
	if (!$showend) $endpage = $npages;

	$classes = array(
		-1 => ' class="previous"',
		0 => ' class="current"',
		+1 => ' class="next"',
	);

?>
<div class="paging">
<?php if ($showstart) { ?>
	<a href="?page=1" class="first">&laquo; 1</a> &hellip;
<?php } ?><!--
<?php for ($i = $startpage; $i <= $endpage; ++$i) { ?>
--><?php if ($i > $startpage) echo '<span> &middot; </span>'; ?>
<a href="?page=<?php echo $i; ?>"<?php echo (isset($classes[$i - $page]) ? $classes[$i - $page] : ''); ?>><?php echo $i; ?></a><!--
<?php } ?>
-->
<?php if ($showend) { ?>
	&hellip; <a href="?page=<?php echo $npages; ?>" class="last"><?php echo $npages; ?> &raquo;</a>
<?php } ?>
</div>
<?
}

