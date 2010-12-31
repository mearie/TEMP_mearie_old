<?xml version="1.0"?>
<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform" version="1.0">
<xsl:output method="html" encoding="utf-8" doctype-system="about:legacy-compat" omit-xml-declaration="yes"/>
<xsl:template match="*" />

<!--*************************************************************************-->

<xsl:template match="svn">
<html lang="en">
<head>
<meta charset="utf-8"/>
<title><xsl:value-of select="index/@path"/> | svn.mearie.org</title>
<meta name="author" content="Kang Seonghoon" />
<meta name="generator" content="Subversion {@version}" />
<link rel="stylesheet" media="screen" type="text/css" href="http://mearie.org/res/global.css" />
<xsl:comment><![CDATA[[if IE]><link rel="stylesheet" media="screen" href="http://mearie.org/res/global.ie.css" type="text/css" /><![endif]]]></xsl:comment>
<link rel="shortcut icon" href="http://mearie.org/res/icon-svn.ico" type="image/vnd.microsoft.icon" />
<script type="text/javascript" src="https://ajax.googleapis.com/ajax/libs/jquery/1.4.4/jquery.min.js"></script> 
<script type="text/javascript" src="http://mearie.org/res/global.js"></script> 
</head>
<body lang="en" class="lang-en">
<div id="sitebody">
<xsl:apply-templates/>
</div>
<hr/>
<div id="siteside">
<div class="slogan">
	<a href="http://mearie.org/"><img class="logo" src="http://mearie.org/res/logo.png" width="117" height="117" alt="Go to mearie.org front page." /></a>
</div>
<div class="menu">
	<p class="domain"><a href="/">svn.mearie.org</a></p>
	<xsl:variable name="rev" select="number(index/@rev)" />
	<ul>
	<li><a href="/*{$rev}*{index/@path}">Revision <xsl:value-of select="$rev"/></a><ul>
	<xsl:if test="$rev>1">
	<li><a href="/*{($rev)-1}*{index/@path}">Prior revision (r<xsl:value-of select="($rev)-1"/>)</a></li>
	</xsl:if>
	<li><a href="/*{($rev)+1}*{index/@path}">Next revision (r<xsl:value-of select="($rev)+1"/>)</a></li>
	<li><a href="/{index/@path}">Latest revision</a></li>
	</ul></li>
	</ul>
</div> 
</div>
<hr/>
<div id="sitemeta"> 
<div class="tray"> 
	Powered by <a href="http://subversion.apache.org/">Subversion</a><xsl:text> </xsl:text><xsl:value-of select="@version"/>
</div> 
<form action="http://www.google.com/cse" class="search"><div> 
	<input type="hidden" name="cx" value="017879559261112115196:ygyuirvfnku"/> 
	<input type="text" name="q" size="30"/> 
	<input type="submit" name="sa" value="Google Search" class="button"/> 
</div></form> 
<div class="copyright">Copyright © 1999–2011 Kang Seonghoon. <a href="http://mearie.org/about/copyright">Some Rights Reserved.</a></div> 
</div> 
</body>
</html>
</xsl:template>

<!--*************************************************************************-->

<xsl:template match="index">
<h1><xsl:value-of select="@path" /></h1>
<p><strong>Warning:</strong> Subversion repository is no longer in use.<xsl:text> </xsl:text>
	<xsl:choose>
		<xsl:when test="starts-with(@path,&quot;/2008/shuffle&quot;)">The current Mercurial repository is available at
			<code class="url"><a href="http://hg.mearie.org/shuffle/">http://hg.mearie.org/shuffle/</a></code>.</xsl:when>
		<xsl:when test="starts-with(@path,&quot;/angolmois&quot;)">The current Mercurial repository is available at
			<code class="url"><a href="http://hg.mearie.org/angolmois/">http://hg.mearie.org/angolmois/</a></code>.</xsl:when>
		<xsl:when test="starts-with(@path,&quot;/delight&quot;)">The current Mercurial repository is available at
			<code class="url"><a href="http://hg.mearie.org/delight/core/">http://hg.mearie.org/delight/core/</a></code>.</xsl:when>
		<xsl:when test="starts-with(@path,&quot;/hinata/naru/spec&quot;)">The current Mercurial repository is available at
			<code class="url"><a href="http://hg.mearie.org/hinata/naru-spec/">http://hg.mearie.org/hinata/naru-spec/</a></code>.</xsl:when>
		<xsl:when test="starts-with(@path,&quot;/hinata/twilight&quot;)">The current Mercurial repository is available at
			<code class="url"><a href="http://hg.mearie.org/hinata/twilight/">http://hg.mearie.org/hinata/twilight/</a></code>.</xsl:when>
		<xsl:when test="starts-with(@path,&quot;/snippets/pytransdate&quot;) or starts-with(@path,&quot;/snippets/tags/pytransdate&quot;)">The current Mercurial repository is available at
			<code class="url"><a href="http://hg.mearie.org/pytransdate/">http://hg.mearie.org/pytransdate/</a></code>.</xsl:when>
		<xsl:when test="starts-with(@path,&quot;/snippets/vlaah-python&quot;) or starts-with(@path,&quot;/snippets/tags/vlaah-python&quot;)">The current Mercurial repository is available at
			<code class="url"><a href="http://hg.mearie.org/vlaah-python/">http://hg.mearie.org/vlaah-python/</a></code>.</xsl:when>
		<xsl:when test="starts-with(@path,&quot;/tinicube&quot;)">The current Mercurial repository is available at
			<code class="url"><a href="http://hg.mearie.org/tinicube/">http://hg.mearie.org/tinicube/</a></code>.</xsl:when>
		<xsl:otherwise>Use <a href="http://hg.mearie.org/">Mercurial repository</a> for recent changes. (Note that some older projects are not listed there.)</xsl:otherwise>
	</xsl:choose>
</p>

<ul>
	<xsl:apply-templates select="updir" />
	<xsl:apply-templates select="dir" />
	<xsl:apply-templates select="file" />
</ul>
</xsl:template>

<xsl:template match="updir"><!--
--><li class="updir"><a class="link" href=".."><em>&#8593; Parent Directory</em></a></li><!--
--></xsl:template>

<xsl:template match="dir"><!--
--><li class="dir"><a class="link" href="{@href}"><strong><xsl:value-of select="@name" />/</strong></a></li><!--
--></xsl:template>

<xsl:template match="file"><!--
--><li class="file"><a class="link" href="{@href}"><xsl:value-of select="@name" /></a></li><!--
--></xsl:template>

<!--*************************************************************************-->

</xsl:stylesheet>
