<?php
require_once 'lib.inc.php';

define('MEARIE_COMMENT_FROM_USER', 1);
define('MEARIE_COMMENT_FROM_ADMIN', 2);
define('MEARIE_COMMENT_FROM_TRACKBACK', 3);

class MearieComment {
	var $url;
	var $id;
	var $parentid;
	var $source;
	var $author;
	var $contents;
	var $created_on;
}


function mearie_clamp($value, $min, $max) {
	$value = intval($value);
	return ($value < $min ? $min : ($value > $max ? $max : $value));
}

function mearie_npages($nentries, $pagesize) {
	return intval(($nentries - 1) / $pagesize + 1);
}

function mearie_paging_sql($page, $limit) {
	if ($page < 0 || $limit < 0) return '';
	return ' limit '.$limit.' offset '.(($page - 1) * $limit);
}

class MearieJournalPost {
	var $parent;
	var $id;
	var $url;
	var $title;
	var $tags;
	var $contents;
	var $created_on;
	var $updated_on;
	var $is_public;
	var $is_commentable;

	function __construct(&$parent, $row) {
		$this->parent =& $parent;

		$this->id = $row['id'];
		$this->url = $row['url'];
		$this->title = $row['title'];
		$this->tags = (isset($row['tags']) ? $row['tags'] : null);
		$this->contents = $row['contents'];
		$this->created_on = $row['created_on'];
		$this->updated_on = $row['updated_on'];
		$this->is_public = ($row['is_public'] ? true : false);
		$this->is_commentable = ($row['is_commentable'] ? true : false);
		$this->comments = (isset($row['comments']) ? $row['comments'] : null);
	}

	function href() {
		return $this->parent->getPostHref($this);
	}

	function datetime($full = false) {
		$ampm = (date('G', $this->created_on) > 11 ? '오후' : '오전');
		$result = date('Y년 n월 j일 '.$ampm.' g시 i분', $this->created_on);
		if ($full && $this->created_on != $this->updated_on) {
			$ampm = (date('G', $this->updated_on) > 11 ? '오후' : '오전');
			$result .= date(' (Y년 n월 j일 '.$ampm.' g시 i분 수정)', $this->updated_on);
		}
		return $result;
	}

	function contents($options = array()) {
		$formatter = new MearieFormatter($options + array('uniqid' => 'entry'.$this->id));
		$output = $formatter->process($this->contents);
		return $output['text'];
	}

	function tags() {
		if (is_null($this->tags)) {
			$this->tags = $this->parent->getTagsFromPost($this->id);
		}
		return array_map(array(&$this->parent, 'getTagFromURL'), $this->tags);
	}

	function comments() {
		return $this->parent->getCommentsFromPost($this->id);
	}
}

class MearieJournalArchive {
	function __construct(&$parent, $year, $month) {
		$this->parent =& $parent;

		$this->year = $year;
		$this->month = $month;
	}

	function href() {
		return $this->parent->getArchiveHref($this);
	}

	function posts($page = -1, $limit = MEARIE_JOURNAL_PAGE_SIZE, $showall = false) {
		return $this->parent->getPostsFromArchive($this->year, $this->month,
				$page, $limit, $showall);
	}

	function nposts($showall = false) {
		return $this->parent->npostsInArchive($this->year, $this->month, $showall);
	}
}

class MearieJournalComment {
	var $parent;
	var $id;
	var $post;
	var $contents;
	var $created_on;
	var $created_by;

	function __construct(&$parent, $row) {
		$this->parent =& $parent;

		$this->id = $row['id'];
		$this->post = $row['post'];
		$this->contents = $row['contents'];
		$this->created_on = $row['created_on'];
		$this->created_by = $row['updated_by'];
	}

	function post() {
		return $this->parent->getPostFromID($this->post);
	}

	function href() {
		return $this->parent->getCommentHref($this);
	}

	function datetime() {
		$ampm = (date('G', $this->created_on) > 11 ? '오후' : '오전');
		$result = date('Y년 n월 j일 '.$ampm.' g시 i분', $this->created_on);
		return $result;
	}

	function contents($options = array()) {
		return nl2br(htmlspecialchars($this->contents)); // XXX
	}
}

class MearieJournalTag {
	var $parent;
	var $url;
	var $name;
	var $title;
	var $contents;

	function __construct(&$parent, $row) {
		$this->parent =& $parent;

		$this->url = $row['url'];
		$this->name = $row['name'];
		if (is_null($this->name)) $this->name = "($this->url)";
		$this->title = $row['title'];
		$this->contents = $row['contents'];
		$this->nposts = (is_null($row['nposts']) ? null : $row['nposts']);
	}

	function href() {
		return $this->parent->getTagHref($this);
	}

	function contents($options = array()) {
		$formatter = new MearieFormatter($options + array('uniqid' => 'tag-'.$this->url));
		$output = $formatter->process($this->contents);
		return $output['text'];
	}

	function posts($page = -1, $limit = MEARIE_JOURNAL_PAGE_SIZE, $showall = false) {
		return $this->parent->getPostsFromTag($this->url, $page, $limit, $showall);
	}

	function nposts() {
		if (is_null($this->nposts)) {
			return count($this->posts());
		} else {
			return $this->nposts;
		}
	}
}

define('MEARIE_JOURNAL_PAGE_SIZE', 3);

class MearieJournal {
	var $db;
	var $base;
	var $prefix;
	var $lasterror;

	var $nposts_cache;
	var $tags_cache;

	function __construct($db, $base, $prefix) {
		$this->db = $db;
		$this->base = $base;
		$this->prefix = $prefix;

		$this->lasterror = $db->error();
		$this->nposts_cache = null;
		$this->tags_cache = array();
	}

	function error() {
		return $this->lasterror;
	}

	function nposts($showall = false) {
		if (is_null($this->nposts_cache)) {
			$where = ($showall ? '' : ' where is_public=1');
			$result = $this->db->query("select count(*) from {$this->prefix}posts $where;");
			$row = $result->fetchone(false);
			$this->nposts_cache = $row[0];
		}
		return $this->nposts_cache;
	}

	function npostsInArchive($year, $month, $showall = false) {
		$lbound = mktime(0, 0, 0, $month, 1, $year);
		$ubound = mktime(0, 0, 0, $month + 1, 1, $year);
		$where = ($showall ? '' : ' and is_public=1');
		$result = $this->db->query("select count(*) from {$this->prefix}posts
			where (created_on between ? and ?) $where;", $lbound, $ubound - 1);
		$row = $result->fetchone(false);
		return $row[0];
	}

	function npages($pagesize = MEARIE_JOURNAL_PAGE_SIZE, $showall = false) {
		return mearie_npages($this->nposts($showall), $pagesize);
	}

	function ntags() {
		$result = $this->db->query("select count(*) from {$this->prefix}tags;");
		$row = $result->fetchone(false);
		return $row[0];
	}

	function getArchiveFromURL($url) {
		$path = explode('/', trim($url, '/'));
		$year = intval($path[0]);
		$month = intval($path[1]);
		if ($month < 1 || $month > 12) return null;
		return new MearieJournalArchive($this, $year, $month);
	}

	function getTagFromURL($url) {
		if (!isset($this->tags_cache[$url])) {
			$result = $this->db->query("select * from {$this->prefix}tags
				where url = ?;", $url);
			if ($row = $result->fetchone()) {
				$this->tags_cache[$url] = new MearieJournalTag($this, $row);
			} else {
				return null;
			}
		}
		return $this->tags_cache[$url];
	}

	function getTagsFromPosts($ids) {
		$result = $this->db->query("select P.id, P.tag as url, T.name, T.title,
			T.contents from {$this->prefix}post_tags as P left outer join
			{$this->prefix}tags as T on P.tag = T.url where id in (".
			implode(',', $ids).");");
		$tags = array();
		foreach ($ids as $id) $tags[$id] = array();
		while ($row = $result->fetch()) {
			$tags[$row['id']][] = $row['url'];
			$this->tags_cache[$row['url']] = new MearieJournalTag($this, $row);
		}
		$result->close();
		return $tags;
	}

	function getCommentsFromPost($id) {
		$result = $this->db->query("select * from {$this->prefix}comments
			where post = ?", $id);
		$comments = array();
		while ($row = $result->fetch()) {
			$comments[] = new MearieJournalComment($this, $row);
		}
		$result->close();
		return $comments;
	}

	function getTagsFromPost($id) {
		$result = $this->getTagsFromPosts(array($id));
		return $result[$id];
	}

	function getPostFromURL($url) {
		$path = explode('/', trim($url, '/'));
		$year = intval($path[0]);
		$month = intval($path[1]);
		$url = trim($path[2]);
		if ($month < 1 || $month > 12) return null;
		$lbound = mktime(0, 0, 0, $month, 1, $year);
		$ubound = mktime(0, 0, 0, $month + 1, 1, $year);
		$result = $this->db->query("select * from {$this->prefix}posts
			where (created_on between ? and ?) and url = ? limit 1;",
			$lbound, $ubound - 1, $url);
		if ($row = $result->fetchone()) {
			$row['tags'] = $this->getTagsFromPost($row['id']);
			return new MearieJournalPost($this, $row);
		} else {
			return null;
		}
	}

	function getPostFromID($id) {
		$result = $this->db->query("select * from {$this->prefix}posts
			where id = ? limit 1;", $id);
		if ($row = $result->fetchone()) {
			$row['tags'] = $this->getTagsFromPost($id);
			return new MearieJournalPost($this, $row);
		} else {
			return null;
		}
	}

	function getPostsFromArchive($year, $month, $page = -1, $limit = MEARIE_JOURNAL_PAGE_SIZE, $showall = false) {
		$lbound = mktime(0, 0, 0, $month, 1, $year);
		$ubound = mktime(0, 0, 0, $month + 1, 1, $year);
		$where = ($showall ? '' : ' and is_public=1');
		$result = $this->db->query("select * from {$this->prefix}posts
			where (created_on between ? and ?) $where order by created_on desc".
			mearie_paging_sql($page, $limit), $lbound, $ubound - 1);
		$posts = array();
		while ($row = $result->fetch()) {
			$posts[] = new MearieJournalPost($this, $row);
		}
		$result->close();
		return $posts;
	}

	function getPostsFromTag($tag, $page = -1, $limit = MEARIE_JOURNAL_PAGE_SIZE, $showall = false) {
		$where = ($showall ? '' : ' and is_public=1');
		$result = $this->db->query("select P.* from {$this->prefix}posts as P
			join {$this->prefix}post_tags as R on P.id = R.id where R.tag = ?
			$where order by P.created_on desc".mearie_paging_sql($page, $limit), $tag);
		$posts = array();
		while ($row = $result->fetch()) {
			$posts[] = new MearieJournalPost($this, $row);
		}
		$result->close();
		return $posts;
	}

	function postList($page, $limit = MEARIE_JOURNAL_PAGE_SIZE, $showall = false) {
		$where = ($showall ? '' : ' where is_public=1');
		$result = $this->db->query("select * from {$this->prefix}posts $where
			order by created_on desc".mearie_paging_sql($page, $limit));
		$rows = array();
		while ($row = $result->fetch()) {
			$row['tags'] = array();
			$rows[$row['id']] = $row;
		}
		$result->close();
		foreach ($this->getTagsFromPosts(array_keys($rows)) as $id => $tags) {
			$rows[$id]['tags'] = $tags;
		}
		$posts = array();
		foreach ($rows as $row) {
			$posts[] = new MearieJournalPost($this, $row);
		}
		return $posts;
	}

	function tagList($page, $limit = 12) {
		$result = $this->db->query("select *, (select count(*) from
			{$this->prefix}post_tags where tag = T.url) as nposts from
			{$this->prefix}tags as T order by url asc".mearie_paging_sql($page, $limit));
		$tags = array();
		while ($row = $result->fetch()) {
			$tags[] = new MearieJournalTag($this, $row);
			$this->tags_cache[$row['url']] = new MearieJournalTag($this, $row);
		}
		$result->close();
		return $tags;
	}

	function getPostHref(&$post) {
		return $this->base . date('Y/m/', $post->created_on) . $post->url;
	}

	function getCommentHref(&$comment) {
		return $this->getPostHref($comment->post()) . '#comment' . $comment->id;
	}

	function getArchiveHref(&$archive) {
		return $this->base . $archive->year . '/' . $archive->month . '/';
	}

	function getTagHref(&$tag) {
		return $this->base . 'tag/' . $tag->url;
	}

	function addPost($data) {
		$this->db->exec('begin;');
		if (!$this->db->exec("insert into {$this->prefix}posts(url, title, contents,
				created_on, updated_on, is_public) values(?, ?, ?, ?, ?, ?);",
				$data['url'], $data['title'], $data['contents'],
				$data['created_on'], $data['updated_on'],
				$data['is_public'] ? 1 : 0)) {
			$this->lasterror = $this->db->error();
			$this->db->exec('rollback;');
			return false;
		}
		$id = $this->db->lastinsert();
		foreach ($data['tags'] as $tag) {
			if (!$this->db->exec("insert into {$this->prefix}post_tags(id, tag)
					values(?, ?);", $id, $tag)) {
				$this->lasterror = $this->db->error();
				$this->db->exec('rollback;');
				return false;
			}
		}
		$this->db->exec('commit;');
		return true;
	}

	function updatePost($id, $data) {
		$data += array('title' => null, 'tags' => null, 'contents' => null,
			'created_on' => null, 'updated_on' => null, 'is_public' => null);
		$this->db->exec('begin;');
		if (!$this->db->exec("update {$this->prefix}posts set title=coalesce(?,title),
				contents=coalesce(?,contents), created_on=coalesce(?,created_on),
				updated_on=coalesce(?,updated_on), is_public=coalesce(?,is_public)
				where id=?;", $data['title'], $data['contents'], $data['created_on'],
				$data['updated_on'], $data['is_public'], $id)) {
			$this->lasterror = $this->db->error();
			$this->db->exec('rollback;');
			return false;
		}
		if (!is_null($data['tags'])) {
			if (!$this->db->exec("delete from {$this->prefix}post_tags where id=?;", $id)) {
				$this->lasterror = $this->db->error();
				$this->db->exec('rollback;');
				return false;
			}
			foreach ($data['tags'] as $tag) {
				if (!$this->db->exec("insert into {$this->prefix}post_tags(id,
						tag) values(?, ?);", $id, $tag)) {
					$this->lasterror = $this->db->error();
					$this->db->exec('rollback;');
					return false;
				}
			}
		}
		$this->db->exec('commit;');
		return true;
	}

	function deletePost($id) {
		$this->db->exec('begin;');
		if (!$this->db->exec("delete from {$this->prefix}posts where id=?;", $id)) {
			$this->lasterror = $this->db->error();
			$this->db->exec('rollback;');
			return false;
		}
		if (!$this->db->exec("delete from {$this->prefix}post_tags where id=?;", $id)) {
			$this->lasterror = $this->db->error();
			$this->db->exec('rollback;');
			return false;
		}
		$this->db->exec('commit;');
		return true;
	}

	function addTag($url, $name, $title = null, $desc = null) {
		if (!$this->db->exec("insert into {$this->prefix}tags(url, name, title, contents)
				values(?, ?, ?, ?);", $url, $name, $title, $desc)) {
			$this->lasterror = $this->db->error();
			return false;
		}
		return true;
	}

	function updateTag($url, $name = null, $title = null, $desc = null) {
		if (!$this->db->exec("update {$this->prefix}tags set name=coalesce(?,name),
				title=coalesce(?,title), contents=coalesce(?,contents) where url=?;",
				$name, $title, $desc, $url)) {
			$this->lasterror = $this->db->error();
			return false;
		}
		unset($this->tags_cache[$url]);
		return true;
	}

	function deleteTag($url) {
		if (!$this->db->exec("delete from {$this->prefix}tags where url=?;", $url)) {
			$this->lasterror = $this->db->error();
			return false;
		}
		unset($this->tags_cache[$url]);
		return true;
	}
}

// vim: ts=4 sw=4
