<?php
include_once 'journal.inc.php';

$tagid = substr(isset($_SERVER['PATH_INFO']) ? $_SERVER['PATH_INFO'] : '', 1);
if ($tagid) {
	$tag = $JOURNAL->getTagFromURL($tagid);
	if (is_null($tag)) $SITE->httpError(404);
	$callback = array(&$tag, 'posts');
} else {
	$callback = array(&$JOURNAL, 'postList');
}

header('Content-Type: application/atom+xml');
echo '<?xml version="1.0" encoding="utf-8" ?>';
?>

<feed xmlns="http://www.w3.org/2005/Atom">
<?php if ($tagid) { ?>
	<title>mearie.org journal: <?php echo htmlspecialchars($tag->name); ?></title>
	<subtitle type="text">해당 태그로부터 최근 10개의 글 보기</subtitle>
	<id>urn:urn-4:org.mearie.ko.journal.tag.<?php echo htmlspecialchars($tag->url); ?></id>
	<icon>http://mearie.org/res/icon-journal.ico</icon>
	<updated><?php echo date('c'); ?></updated>
	<link rel="alternate" type="text/html" hreflang="ko" href="http://mearie.org/journal/tag/<?php echo htmlspecialchars($tag->url); ?>" />
	<link rel="self" type="application/atom+xml" href="http://mearie.org/journal/feed/<?php echo htmlspecialchars($tag->url); ?>" />
<?php } else { ?>
	<title>mearie.org journal</title>
	<subtitle type="text">최근 10개의 글 보기</subtitle>
	<id>urn:urn-4:org.mearie.ko.journal</id>
	<icon>http://mearie.org/res/icon-journal.ico</icon>
	<updated><?php echo date('c'); ?></updated>
	<link rel="alternate" type="text/html" hreflang="ko" href="http://mearie.org/journal/" />
	<link rel="self" type="application/atom+xml" href="http://mearie.org/journal/feed" />
<?php } ?>
	<author>
		<name>강 성훈</name>
		<uri>http://mearie.org/</uri>
	</author>
	<rights>Copyright © 1999–2007, Kang Seonghoon. Some Rights Reserved.</rights>
<?php foreach (call_user_func($callback, 1, 10) as $post) { ?>
	<entry>
		<title><?php echo $post->title; ?></title>
		<link rel="alternate" type="text/html" hreflang="ko" href="http://mearie.org<?php echo htmlspecialchars($post->href()); ?>" />
		<id>urn:urn-4:org.mearie.ko.journal.post.<?php echo $post->id; ?></id>
		<published><?php echo date('c', $post->created_on); ?></published>
		<updated><?php echo date('c', $post->updated_on); ?></updated>
		<content type="xhtml" xml:lang="ko" xml:base="http://mearie.org/">
			<div xmlns="http://www.w3.org/1999/xhtml">
<?php echo $post->contents(array('cut' => '<p>[…]</p>', 'entities' => false)); ?>
			</div>
		</content>
	</entry>
<?php } ?>
</feed>
