/* mearie.org subversion repository javascript
 * Copyright (c) 2007, Kang Seonghoon aka lifthrasiir.
 *
 * This file is in public domain; you can use this file freely,
 * but this doesn't necessarily mean you could also use
 * documents using this stylesheet.
 */

var _usepropfind = true;

var _m = location.pathname.match(/^(?:\/\*(\d+)\*)?(\/.*)$/);
var svnpath = _m[2] + (_m[2].charAt(_m[2].length-1) != '/' ? '/' : '');
var svnurlrev = (_m[1] ? parseInt(_m[1]) : -1);

function svnpath2url(path, rev) {
	if (!rev) rev = svnurlrev;
	if (rev < 0) return svnpath + path;
	return '/*' + rev + '*' + svnpath + path;
}

function svnpathexpand(path) {
	if (svnurlrev < 0) return svnpath + path;
	return '/!svn/bc/' + svnurlrev + svnpath + path;
}

////////////////////////////////////////////////////////////////////////////////

function readable_size(bytes) {
	if (bytes < 1000) return bytes + ' bytes';
	if (bytes < 1000000) return String(bytes/1024).match(/^...[^.]?/)[0] + ' KB';
	if (bytes < 1000000000) return String(bytes/1048576).match(/^...[^.]?/)[0] + ' MB';
	return String(bytes/1073741824).match(/^...[^.]?/)[0] + ' GB';
}

function readable_timediff(base, target) {
	var diff = (base.getTime() - target.getTime()) / 1000;
	if (isNaN(diff)) return 'N/A';

	var elems;
	if (diff < 300) {
		elems = [diff/60, 'm', diff%60, 's'];
	} else if ((diff /= 60) < 360) {
		elems = [diff/60, 'h', diff%60, 'm'];
	} else if ((diff /= 60) < 168) {
		elems = [diff/24, ' day#', diff%24, 'h'];
	} else if ((diff /= 24) < 90) {
		elems = [diff/7, ' week#', diff%7, ' day#'];
	} else {
		elems = [diff/365, ' year#', diff/365%1*12, ' month#'];
	}

	var lhs = parseInt(elems[0]), lhsu = elems[1];
	var rhs = parseInt(elems[2]), rhsu = elems[3];
	if (lhs) {
		var result = lhs + lhsu.replace('#', lhs>1 ? 's' : '');
		if (rhs) result += ' ' + rhs + rhsu.replace('#', rhs>1 ? 's' : '');
	} else {
		var result = rhs + rhsu.replace('#', rhs>1 ? 's' : '');
	}
	return result + ' ago';
}

function convert_plaintext(str, noelement) {
	str = str.replace(/^\n*|\n*$/g, '');
	str = str.replace(/(http:\/\/+[\w\/\-%&#=.,?+$]+)/g, '\001a href="$1"\002$1\001/a\002');
	str = str.replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;');
	str = str.replace(/(\r?\n|^)(\s+)/g,'$1<span style="white-space:pre;">$2</span>');
	str = str.replace(/\r?\n/g,'&nbsp;<br />').replace(/\1/g,'<').replace(/\2/g,'>');
	if (noelement) return str;
	var prenode = document.createElement('pre');
	prenode.innerHTML = str;
	return prenode;
}

function gather_xml_elements(node, elems) {
	var result = [];
	var childs = node.childNodes, nchilds = childs.length, nelems = elems.length;
	for (var i = 0; i < nchilds; ++i) {
		if (childs[i].nodeType == 1/*ELEMENT_NODE*/) {
			var tagname = childs[i].tagName;
			for (var j = 0; j < nelems; ++j) {
				if (elems[j] == tagname) {
					if (!result[j]) result[j] = childs[i];
					break;
				}
			}
		}
	}
	return result;
}

function create_xhr_object() {
	try { return new XMLHttpRequest(); } catch (e) {
	try { return new ActiveXObject("Msxml3.XMLHTTP"); } catch (e) {
	try { return new ActiveXObject("Msxml2.XMLHTTP.5.0"); } catch (e) {
	try { return new ActiveXObject("Msxml2.XMLHTTP.4.0"); } catch (e) {
	try { return new ActiveXObject("Msxml2.XMLHTTP.3.0"); } catch (e) {
	try { return new ActiveXObject("Msxml2.XMLHTTP"); } catch (e) {
	try { return new ActiveXObject("Microsoft.XMLHTTP"); } catch (e) {
		return null;
	}}}}}}}
}

function retrieve_svn_info_from_headers(url, callback) {
	var req = create_xhr_object();
	if (!req) return false;
	req.open("HEAD", url, true);
	req.onreadystatechange = function() {
		if (req.readyState != 4) return;
		if (req.status < 200 || req.status >= 300) callback(null);

		var etag = req.getResponseHeader('ETag').match(/^(W\/)?"(\d+)\/(.*)"$/);
		var result = {path: etag[3], collection: etag[1] == 'W/',
			revision: parseInt(etag[2]), cdate: new Date(NaN),
			mdate: new Date(NaN), lastauthor: 'N/A'};
		if (!result.collection) {
			result.size = parseInt(req.getResponseHeader('Content-Length'));
		}
		callback(result);
	};
	req.send('');
	return true;
}

function parse_propfind_response(resp) {
	var result = {};
	if (resp.getElementsByTagNameNS) {
		var nodes = resp.getElementsByTagNameNS('DAV:', 'response');
	} else {
		var nodes = resp.getElementsByTagName('D:response');
	}
	for (var i = 0; i < nodes.length; ++i) {
		var elems = gather_xml_elements(nodes[i], ['D:href', 'D:propstat']);
		var iresult = {path: elems[0].firstChild.nodeValue};
		elems = gather_xml_elements(elems[1], ['D:prop']);
		elems = gather_xml_elements(elems[0], [
			'lp1:resourcetype', 'lp1:getcontentlength',
			'lp1:getcontenttype', 'lp1:creationdate',
			'lp1:getlastmodified', 'lp1:version-name', 
			'lp1:creator-displayname', 'lp3:md5-checksum']);
		iresult.collection = elems[0].hasChildNodes();
		iresult.revision = parseInt(elems[5].firstChild.nodeValue);
		iresult.cdate = new Date();
		iresult.cdate.setISO8601(elems[3].firstChild.nodeValue);
		iresult.mdate = new Date(elems[4].firstChild.nodeValue);
		iresult.lastauthor = elems[6].firstChild.nodeValue;
		if (!iresult.collection) {
			iresult.size = parseInt(elems[1].firstChild.nodeValue);
		}
		result[iresult.path] = iresult;
	}
	return result;
}

function retrieve_svn_info_from_props(url, callback) {
	var req = create_xhr_object();
	if (!req) return false;
	req.open("PROPFIND", url, true);
	req.setRequestHeader('Depth', '1');
	req.setRequestHeader('Content-Type', 'text/xml');
	req.onreadystatechange = function() {
		if (req.readyState != 4) return;
		if (req.status < 200 || req.status >= 300) callback(null);
		callback(parse_propfind_response(req.responseXML));
	};
	req.send('<?xml version="1.0" encoding="utf-8" ?><propfind xmlns="DAV:">' +
		'<prop><resourcetype/><getcontentlength/><getcontenttype/>' +
		'<creationdate/><getlastmodified/><version-name/><creator-displayname/>' +
		'<md5-checksum xmlns="http://subversion.tigris.org/xmlns/dav/"/>' +
		'</prop></propfind>');
	return true;
}

function parse_logreport_response(resp) {
	var result = [];
	if (resp.getElementsByTagNameNS) {
		var nodes = resp.getElementsByTagNameNS('svn:', 'log-item');
	} else {
		var nodes = resp.getElementsByTagName('S:log-item');
	}
	for (var i = 0; i < nodes.length; ++i) {
		var elems = gather_xml_elements(nodes[i], ['D:version-name',
			'D:creator-displayname', 'S:date', 'D:comment']);
		var iresult = {revision: parseInt(elems[0].firstChild.nodeValue),
			author: elems[1].firstChild.nodeValue, date: new Date(),
			comment: elems[3].firstChild.nodeValue};
		iresult.date.setISO8601(elems[2].firstChild.nodeValue);
		result.push(iresult);
	}
	return result;
}

function retrieve_svn_log_report(path, rev, callback) {
	var req = create_xhr_object();
	if (!req) return false;
	try {
		req.open("REPORT", svnpath2url(path, rev), true);
	} catch (e) {
		alert('Log view is not supported on this browser.');
		return false; // maybe MSIE 7
	}
	req.setRequestHeader('Content-Type', 'text/xml');
	req.onreadystatechange = function() {
		if (req.readyState != 4) return;
		if (req.status < 200 || req.status >= 300) callback(null);
		callback(parse_logreport_response(req.responseXML));
	};
	req.send('<?xml version="1.0" encoding="utf-8" ?><log-report xmlns="svn:">' +
		'<start-revision>1</start-revision><end-revision>' + rev +
		'</end-revision><path/></log-report>');
	return true;
}

function retrieve_svn_data(url, callback) {
	var req = create_xhr_object();
	if (!req) return false;
	req.open("GET", url, true);
	req.onreadystatechange = function() {
		if (req.readyState != 4) return;
		if (req.status < 200 || req.status >= 300) callback(null);
		callback(req);
	};
	req.send('');
	return true;
}

////////////////////////////////////////////////////////////////////////////////

var svncurrev, svnupdir, svndirs, svnfiles, extview;

function SubversionView(rev, updir, dirs, files) {
	svncurrev = rev;
	svnupdir = updir;
	svndirs = dirs;
	svnfiles = files;
}

function update_svn_info(path, node, lognode) {
	return function(info) {
		if (!info) return;
		var desc = '<a href="#">revision ' + info.revision + '</a>'
		desc += ' (' + info.lastauthor;
		if (info.mdate.getTime()) {
			desc += ', ' + readable_timediff(new Date(), info.mdate);
		}
		desc += ')';
		if (!info.collection) desc += ', ' + readable_size(info.size);
		node.innerHTML = desc;

		node.firstChild.onclick = function() {
			if (lognode.style.display == 'none' && retrieve_svn_log_report(
					path, svncurrev, update_svn_log(path, lognode))) {
				lognode.style.display = '';
			} else {
				lognode.style.display = 'none';
			}
			return false;
		};
	};
}

function update_svn_log(path, node) {
	return function(log) {
		var result = '<dl>';
		for (var i = log.length - 1; i >= 0; --i) {
			var rev = log[i].revision, date = log[i].date;
			var timediff = readable_timediff(new Date(), date);
			var comment = convert_plaintext(log[i].comment, true);
			result += '<dt><a href="' + encodeURI(svnpath2url(path, rev));
			result += '">revision ' + rev + '</a> (' + log[i].author + ' @ ';
			result += '<span title="' + date + '">' + timediff + '</span>)';
			result += '</dt><dd><pre>' + comment + '</pre></dd>';
		}
		result += '</dl>';
		node.innerHTML = result;
	};
}

function update_description_text(req) {
	$('body').insertBefore(convert_plaintext(req.responseText), $('revisions'));
}

function update_description_html(req) {
	var bqnode = document.createElement('blockquote');
	bqnode.appendChild(req.responseXML);
	$('body').insertBefore(bqnode, $('revisions'));
}

var propcallbacks = {};
function retrieve_svn_info(path, callback) {
	if (_usepropfind) {
		propcallbacks[svnpathexpand(path)] = callback;
	} else {
		return retrieve_svn_info_from_headers(svnpath2url(path), callback);
	}
}

function enable_extview() {
	$('entries').className = 'extview';
	var nsvndirs = svndirs.length, nsvnfiles = svnfiles.length;
	var apply = function(prefix, num, path) {
		var infonode = document.createElement('span');
		infonode.id = prefix + 'info' + num;
		infonode.className = 'info';
		infonode.innerHTML = '(information not available)';
		$(prefix + 'node' + num).appendChild(infonode);

		var lognode = document.createElement('div');
		lognode.id = prefix + 'log' + num;
		lognode.className = 'log';
		lognode.style.display = 'none';
		$(prefix + 'node' + num).appendChild(lognode);

		retrieve_svn_info(path, update_svn_info(path, infonode, lognode));
	};
	for (var i = 0; i < nsvndirs; ++i) apply('dir', i, svndirs[i]);
	for (var i = 0; i < nsvnfiles; ++i) apply('file', i, svnfiles[i]);

	// fix revision bar
	retrieve_svn_info_from_headers('/', function(infos) {
		var diff = infos.revision - svncurrev;
		if (diff < 0) {
			return; // impossible!
		} else if (diff < 6) {
			$('revfix' + diff).style.display = 'none';
		} else {
			var curnode = $('revfixtarget');
			curnode.href = '/*' + infos.revision + '*' +
				curnode.href.replace(/^http:\/\/[^\/]+/, '');
			curnode.innerHTML = infos.revision + ' &#187;';
		}
	});

	if (_usepropfind) {
		retrieve_svn_info_from_props(location.pathname, function(infos) {
			for (var path in infos) {
				var info = infos[path];
				path = path.replace(/\/$/,'');
				if (propcallbacks[path]) propcallbacks[path](info);
			}
		});
	}
}

/*
function disable_extview() {
	Cookies.create('svn_extview', 0);

	$('index-wrap').className = '';
	var nsvndirs = svndirs.length, nsvnfiles = svnfiles.length;
	for (var i = 0; i < nsvndirs; ++i) {
		$('dirnode' + i).removeChild($('dirinfo' + i));
		$('dirnode' + i).removeChild($('dirlog' + i));
	}
	for (var i = 0; i < nsvnfiles; ++i) {
		$('filenode' + i).removeChild($('fileinfo' + i));
		$('filenode' + i).removeChild($('filelog' + i));
	}
}
*/

function subversion_init() {
	var debug = (location.search == '?debug');
	if (!debug && !navigator.userAgent.match(/Gecko\/|MSIE 7|Version\/3[.0-9]* Safari/)) return;

	/*
	// add some menus
	var altdiv = $('alternative');
	var prevrev = '&laquo; previous', nextrev = 'next &raquo;', currev = 'current';
	if (svncurrev > 1) {
		prevrev = '<a href="' + encodeURI(svnpath2url('', svncurrev-1)) + '">' + prevrev + '</a>';
	}
	currev = '<a href="' + encodeURI(svnpath2url('', -1)) + '">' + currev + '</a>';
	if (svnurlrev >= 0) {
		nextrev = '<a href="' + encodeURI(svnpath2url('', svncurrev+1)) + '">' + nextrev + '</a>';
	}
	altdiv.innerHTML += '<p style="float:left;">' + prevrev + ' &mdash; ' + currev +
		' &mdash; ' + nextrev + '</p><p style="float:right;">' +
		'<input type="checkbox" id="extview" /><label for="extview"> ' +
		'Extended view</label></p>';
	var extviewbox = $('extview');
	extviewbox.onclick = function() {
		if (extview) disable_extview(); else enable_extview();
		extview = !extview;
	};
	*/

	enable_extview();

	// find readme file and show it
	var nsvnfiles = svnfiles.length;
	for (var i = 0; i < nsvnfiles; ++i) {
		if (svnfiles[i].match(/^README/i)) {
			var callback = (svnfiles[i].match(/htm/i) ?
				update_description_html : update_description_text);
			retrieve_svn_data(svnpath2url(svnfiles[i]), callback);
			break;
		}
	}
}

addLoadHandler(subversion_init);

