<?xml version="1.0"?>
<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform" version="1.0">
<xsl:output method="html" />
<!--encoding="utf-8" doctype-system="http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd" doctype-public="-//W3C//DTD XHTML 1.0 Strict//EN"/-->
<xsl:template match="*" />

<!--*************************************************************************-->

<xsl:template match="svn">
<html>
<head>
	<meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
	<title><xsl:value-of select="index/@path"/> — svn.mearie.org</title>
	<meta name="author" content="Kang Seonghoon (lifthrasiir)" />
	<meta name="generator" content="Subversion {@version}" />
	<link rel="stylesheet" media="screen" type="text/css" href="http://mearie.org/res/css/svnview.css" />
	<xsl:comment><![CDATA[[if IE]><link rel="stylesheet" media="screen" href="http://mearie.org/res/css/svnview.ie.css" type="text/css" /><![endif]]]></xsl:comment>
	<link rel="shortcut icon" href="http://mearie.org/res/img/icon-svn.ico" type="image/vnd.microsoft.icon" />
	<script type="text/javascript" src="http://mearie.org/res/js/global.js"></script>
	<script type="text/javascript" src="http://mearie.org/res/js/svnview.js"></script>
	<script type="text/javascript">
		$svn = new SubversionView(
			// revision
			<xsl:value-of select="index/@rev" />,
			// parent dir is present?
			<xsl:value-of select="count(index/updir)" />,
			// directory list
			[<xsl:apply-templates select="index/dir" mode="js" />],
			// file list
			[<xsl:apply-templates select="index/file" mode="js" />]
		);
	</script>
</head>
<body>
<div id="wrap" lang="en" xml:lang="en" class="lang-en">
<div id="header">
	<div id="sitename"><a href="//mearie.org/">svn.mearie.org</a></div>
	<p id="tagline">… a subversion repository for mearie.org</p>
</div>
<hr />
<div id="body"><a id="top"></a>
	<xsl:apply-templates/>
</div>
<hr />
<div id="footer">
	<p class="location">
		<a href="//mearie.org/about/">About mearie.org</a> |
		<a href="//mearie.org/about/contact">Contact</a> |
		<a href="//mearie.org/service/language">Language</a> |
		<a href="//mearie.org/about/copyright">Copyright &#169;1999&#8211;2008, Kang Seonghoon</a>
	</p>
</div>
</div>
</body>
</html>
</xsl:template>

<!--*************************************************************************-->

<xsl:template match="index">
<h1>
	<a href="/" title="svn.mearie.org">svn:</a>
	<span class="path"><xsl:value-of select="@path" /></span>
	<xsl:if test="string-length(@rev) != 0">
		<span class="revision"> (<abbr title="revision">r</abbr><xsl:value-of select="@rev" />)</span>
	</xsl:if>
</h1>
<p><strong>Warning:</strong> Subversion repository is out of date. Use <a href="http://hg.mearie.org/">Mercurial repository</a> for recent changes. (Note that some older projects are not listed there.)</p>

<div id="entries">
	<ul class="extview"><!--
		--><xsl:apply-templates select="updir" /><!--
		--><xsl:apply-templates select="dir" /><!--
		--><xsl:apply-templates select="file" /><!--
	--></ul>
	<div style="clear:both;" />
</div>
<div id="revisions" class="paging">
	<xsl:variable name="rev" select="number(@rev)" />
	<xsl:if test="$rev>1">
	<xsl:if test="$rev>2">
	<xsl:if test="$rev>3">
	<xsl:if test="$rev>4">
	<xsl:if test="$rev>5">
	<xsl:if test="$rev>6">
		<a href="/*1*{@path}">&#171; 1</a> &#8230;
	</xsl:if>
	<a href="/*{-5+$rev}*{@path}"><xsl:value-of select="-5+$rev" /></a>
	<xsl:text> &#183; </xsl:text></xsl:if>
	<a href="/*{-4+$rev}*{@path}"><xsl:value-of select="-4+$rev" /></a>
	<xsl:text> &#183; </xsl:text></xsl:if>
	<a href="/*{-3+$rev}*{@path}"><xsl:value-of select="-3+$rev" /></a>
	<xsl:text> &#183; </xsl:text></xsl:if>
	<a href="/*{-2+$rev}*{@path}"><xsl:value-of select="-2+$rev" /></a>
	<xsl:text> &#183; </xsl:text></xsl:if>
	<a href="/*{-1+$rev}*{@path}" class="previous"><xsl:value-of select="-1+$rev" /></a>
	<xsl:text> &#183; </xsl:text></xsl:if>
	<a href="/*{   $rev}*{@path}" class="current"><xsl:value-of select="   $rev" /></a>
	<span id="revfix0"><xsl:text> &#183; </xsl:text>
	<a href="/*{ 1+$rev}*{@path}" class="next"><xsl:value-of select=" 1+$rev" /></a>
	<span id="revfix1"><xsl:text> &#183; </xsl:text>
	<a href="/*{ 2+$rev}*{@path}"><xsl:value-of select=" 2+$rev" /></a>
	<span id="revfix2"><xsl:text> &#183; </xsl:text>
	<a href="/*{ 3+$rev}*{@path}"><xsl:value-of select=" 3+$rev" /></a>
	<span id="revfix3"><xsl:text> &#183; </xsl:text>
	<a href="/*{ 4+$rev}*{@path}"><xsl:value-of select=" 4+$rev" /></a>
	<span id="revfix4"><xsl:text> &#183; </xsl:text>
	<a href="/*{ 5+$rev}*{@path}"><xsl:value-of select=" 5+$rev" /></a>
	<span id="revfix5">
		&#8230; <a id="revfixtarget" href="{@path}">current &#187;</a>
	</span>
	</span>
	</span>
	</span>
	</span>
	</span>
</div>
</xsl:template>

<!--*************************************************************************-->

<xsl:template match="updir"><!--
--><li class="updir">
	<a class="link" href=".."><span>&#8598; Parent Directory</span></a>
</li><!--
--></xsl:template>

<xsl:template match="dir"><!--
--><li class="dir" id="dirnode{position()-1}">
	<a class="link" href="{@href}"><span><xsl:value-of select="@name" />/</span></a>
</li><!--
--></xsl:template>

<xsl:template match="file"><!--
--><li class="file" id="filenode{position()-1}">
	<a class="link" href="{@href}"><span><xsl:value-of select="@name" /></span></a>
</li><!--
--></xsl:template>

<!--*************************************************************************-->

<xsl:template match="dir" mode="js"><xsl:if test="position() > 1">, </xsl:if>'<xsl:value-of select="@name" />'</xsl:template>
<xsl:template match="file" mode="js"><xsl:if test="position() > 1">, </xsl:if>'<xsl:value-of select="@name" />'</xsl:template>

<!--*************************************************************************-->

</xsl:stylesheet>
