<?php
include_once 'journal.inc.php';
include_once 'design.inc.php';

$post = $JOURNAL->getPostFromURL($_SERVER['PATH_INFO']);
if (is_null($post) || !$post->is_public) $SITE->httpError(404);

////////////////////////////////////////////////////////////////////////////////

$SITE->startLayout('ko', ': '.date('Y년 n월', $post->created_on), $post->title);
mearie_journal_show_post($post, false);
?>
<hr />
<p><a href="<?php echo $journal->base; ?>">&laquo; 돌아가기</a></p>
