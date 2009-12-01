.PHONY: all all-tree clean clean-tree

SELF = Makefile
TREE = Makefile.tree
RESOURCES = res/logo.png
-include ${TREE}
#TYPEMAPS = $(addsuffix .var,$(basename $(subst .ja.,.,$(subst .ko.,.,$(subst .en.,.,${TARGETS})))))
TYPEMAPS =

all: ${TREE} ${TARGETS} ${TYPEMAPS} ${RESOURCES}

clean: ${TREE}
	rm -f ${TARGETS} ${TYPEMAPS} ${RESOURCES}

res/logo.png: res/logo-template.png ${SELF}
	convert $< -fx 'a*#379+(1-a)*#eee' -channel A -fx 1 $@

%.html: %.txt
	res/processor $< -b . -t /res/default.tmpl.html -o $@

%.var: ${TREE}
	echo "URI: `echo "$@" | cut -d. -f1`"; \
	for i in "`echo "$@" | cut -d. -f1`".*; do \
		echo; \
		echo "URI: $$i"; \
		if echo $$i | grep -q '\.html$$'; then \
			echo "Content-Type: text/html; qs=1"; \
		elif echo $$i | grep -q '\.txt$$'; then \
			echo "Content-Type: text/plain; qs=0.5"; \
		fi; \
	done > $@

${TREE}: ${SELF}
	@echo 'TARGETS = index.ko.html index.en.html copyright.ko.html about/kang-seonghoon.ko.html about/kang-seonghoon.en.html' > $@
	@echo 'Regenerated Makefile.tree. Try again.'

