<?php
include_once 'journal.inc.php';
include_once 'design.inc.php';

$archive = $JOURNAL->getArchiveFromURL($_SERVER['PATH_INFO']);
if (is_null($archive)) $SITE->httpError(404);
$npages = mearie_npages($archive->nposts(), MEARIE_JOURNAL_PAGE_SIZE);
$page = mearie_clamp($_GET['page'], 1, $npages);
$posts = $archive->posts($page);
if (is_null($posts)) $SITE->httpError(404);

////////////////////////////////////////////////////////////////////////////////

$date = mktime(0, 0, 0, $archive->month, 1, $archive->year);
$SITE->startLayout('ko', ': '.date('Y년 n월', $date));

foreach ($posts as $post) {
	mearie_journal_show_post($post, true);
}

mearie_journal_show_paging($page, $npages);
?>
<p><a href="<?php echo $JOURNAL->base; ?>">&laquo; 돌아가기</a></p>
