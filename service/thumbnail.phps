<?php
$ruri = $_SERVER['REQUEST_URI'];
if (strpos($ruri, '/..') !== false || strpos($ruri, '/./') !== false) $SITE->httpError(404);
if (!preg_match('#/-(\d+)x(\d+)-/(.*)$#', $ruri, $m)) $SITE->httpError(404);

$width = intval($m[1]);
$height = intval($m[2]);
$path = MEARIE_IMGROOT.$m[3];
$thumbpath = MEARIE_IMGROOT.'.thumb/'.md5($m[3]).'-'.$width.'-'.$height;
if ($width < 10 || $width > 800 || $height < 10 || $height > 600) $SITE->httpError(403);
if (!file_exists($path)) $SITE->httpError(404);

list($width0, $height0, $type) = getimagesize($path);
if (file_exists($thumbpath) && filemtime($thumbpath) > filemtime($path)) {
	header('Content-Type: '.image_type_to_mime_type($type));
	readfile($thumbpath);
} else {
	$suffixmap = array(IMAGETYPE_PNG => 'png', IMAGETYPE_JPEG => 'jpeg');
	if (!array_key_exists($type, $suffixmap)) $SITE->httpError(500);
	$suffix = $suffixmap[$type];
	$im0 = call_user_func('imagecreatefrom'.$suffix, $path);
	$im = imagecreatetruecolor($width, $height);
	imagecopyresampled($im, $im0, 0, 0, 0, 0, $width, $height, $width0, $height0);
	header('Content-Type: '.image_type_to_mime_type($type));
	call_user_func('image'.$suffix, $im);
	call_user_func('image'.$suffix, $im, $thumbpath);
	imagedestroy($im);
	imagedestroy($im0);
}

