<?php
require_once 'lib.inc.php';
require_once 'journallib.inc.php';

class MearieJournalLayout extends MearieMainLayout {
	function startLayout($lang, $title, $subject = null) {
		$this->title = '메아리 저널'.$title;
		if (defined('MEARIE_JOURNAL_ADMIN')) $this->title .= ' (관리)';
		$this->lang = $lang;
		$this->css = 'journal';
		$this->head = "\t<link rel=\"alternate\" type=\"application/atom+xml\" href=\"/journal/feed\" />\n";
		if (!is_null($subject)) $this->subject = $subject;

		$this->startForce(1);
	}
}

$SITE = new MearieJournalLayout($_SERVER['REQUEST_URI']);

function mearie_create_journal() {
	$base = (defined('MEARIE_JOURNAL_ADMIN') ? '/journal/admin/' : '/journal/');
	return new MearieJournal(mearie_db(), $base, 'journal_');
}

$JOURNAL = mearie_create_journal();

