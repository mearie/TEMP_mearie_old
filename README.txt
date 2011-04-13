                            __                            
.--------.-----.---.-.----.|__|.-----.  .-----.----.-----.
|        |  -__|  _  |   _||  ||  -__|__|  _  |   _|  _  |
|__|__|__|_____|___._|__|  |__||_____|__|_____|__| |___  |
                                                   |_____|

This is an "entire" source code of mearie.org, the personal
website of Kang Seonghoon.

                          LICENSE

Unless explicitly stated, mearie.org and its contents are
copyright (c) 1999-2011 Kang Seonghoon. Some rights
reserved and their details are as follows:

The contents, i.e. every files that does not constitute the
infrastructure of mearie.org are available under the terms
of Creative Commons Attribution 3.0 Unported license. There
is also a formal license statement at /about/copyright.en.txt.

Every files that does constitute the infrastructure of
mearie.org, including everything in /res and /bin directory,
are available under the terms of the MIT/X11 license. Some
softwares even impose the lower limitation; for example,
/bin/webase.py is put in the public domain.

In general you can do anything with the mearie.org source
code, provided that you properly attribute the author. It
does not mean that you can use it for bad things directed to
the author (e.g. setting up the clone website and adding the
malware to make people wrongly blame the original author);
see section 4(c) of CC-by, for example.

                          BUILDING

mearie.org requires the following softwares:

- Standard UNIX utilities including GNU Make
- Python 2.6 or later, with the following libraries:
  - Mako 0.2.1 or later (http://www.makotemplates.org/)
  - odict (http://pypi.python.org/pypi/odict)
- Pandoc 1.6 or later (http://johnmacfarlane.net/pandoc/)
- Imagemagick (optional, if you want to change res/logo.png)
- Mercurial
- Any web server with the following features:
  - HTTP 1.1 content negotiation, with the language and
    type name extracted from the file name like *.en.txt
    (e.g. Apache mod_negotiation)
  - Python WSGI support (e.g. Apache mod_wsgi)

For each domain:

- mearie.org can be built with a single command, "make all".
- hg.mearie.org uses the normal hgweb setup, but with a
  custom template. You have to add the full path to
  /res/hgweb to the list mercurial.template.path, and set
  the "style" variable in [web] section to "hgweb".
- svn.mearie.org uses the /res/svnview.xsl stylesheet.
- r.mearie.org uses the WSGI script at /bin/response.wsgi.

                        NOT INCLUDED

This repository does not include the response database
(/res/db/response.db), which contains private information.
You have to reconstruct the appropriate SQLite database;
the schema is easy to guess.

Some other mearie.org subdomains are also not included:

- cosmic.mearie.org (intentionally not versioned)
- pub.mearie.org (versioned elsewhere; pub and pub-data)
- noe.mearie.org (versioned elsewhere; noe)

