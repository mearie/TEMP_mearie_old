<?php
if (isset($_GET['lang'])) {
	setcookie('mearielang', $_GET['lang']);
	$SITE->moved('language', false);
	exit;
}

switch ($_COOKIE['mearielang']) {
case 'ko':
default:
	$titlemsg = '기본 언어 설정';
	$legendmsg = '아래에서 기본으로 사용할 언어를 선택할 수 있습니다.';
	$browsermsg = '브라우저 설정을 사용';
	$kormsg = ''; $engmsg = ' (영어)'; $jpnmsg = ' (일본어) &mdash; 準備中';
	$submitmsg = '저장'; $cookiemsg = '(쿠키를 사용합니다.)';
	break;
case 'en':
	$titlemsg = 'Configuring Default Language';
	$legendmsg = 'Select the default language below.';
	$browsermsg = 'Use browser default';
	$kormsg = ' (Korean)'; $engmsg = ''; $jpnmsg = ' (Japanese) &mdash; 準備中';
	$submitmsg = 'Save'; $cookiemsg = '(You should enable HTTP cookie.)';
	break;
case 'ja':
	$titlemsg = '基本言語設定';
	$legendmsg = '次で基本に使う言語を選択してください。';
	$browsermsg = 'ブラウザー基本';
	$kormsg = ' (韓国語)'; $engmsg = ' (英語)'; $jpnmsg = ' &mdash; 準備中';
	$submitmsg = '保存'; $cookiemsg = '(クッキーを使います。)';
	break;
}

$SITE->lang_warning = false;
$SITE->startForce();
?>
<h1><?php echo $titlemsg; ?></h1>
<fieldset>
<legend><?php echo $legendmsg; ?></legend>
<form action="?" method="get">
	<input type="radio" id="lang-none" <?php mearie_checked('lang', MEARIE_PREFER_LANGUAGE, ''); ?> /><label for="lang-none"> <?php echo $browsermsg; ?></label><br />
	<input type="radio" id="lang-ko" <?php mearie_checked('lang', MEARIE_PREFER_LANGUAGE, 'ko'); ?> /><label for="lang-ko"> 한국어<?php echo $kormsg; ?></label><br />
	<input type="radio" id="lang-en" <?php mearie_checked('lang', MEARIE_PREFER_LANGUAGE, 'en'); ?> /><label for="lang-en"> English<?php echo $engmsg; ?></label><br />
	<input type="radio" id="lang-ja" <?php mearie_checked('lang', MEARIE_PREFER_LANGUAGE, 'ja'); ?> /><label for="lang-ja"> 日本語<?php echo $jpnmsg; ?></label><br />
	<input type="submit" value="<?php echo $submitmsg; ?>" /> <?php echo $cookiemsg; ?>
</form>
</fieldset>

