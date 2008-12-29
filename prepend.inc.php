<?php
require_once 'lib.inc.php';
require_once 'layout.inc.php';

$SITE = new MearieMainLayout($_SERVER['REQUEST_URI']);
$SITE->start();

