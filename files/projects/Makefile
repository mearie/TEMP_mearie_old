all: vlaah-python pyfunge

vlaah-python:
	svn export http://svn.mearie.org/snippets/vlaah-python/
	tar czvf "vlaah-python-`echo print VERSION | python -i vlaah-python/vlaah/version.py 2> /dev/null`.tar.gz" vlaah-python
	rm -rf vlaah-python

pyfunge:
	wget http://hg.mearie.org/pyfunge/archive/pyfunge-0.5-rc1.tar.gz

