.PHONY: all clean clean-all

HGREPO = .hg
SELF = Makefile
TREE = Makefile.tree
RESOURCES = res/logo.png
-include ${TREE}

HG = hg -R ${HGREPO}/..
CONVERT = convert
PROCESSOR = res/processor
GENERATOR = res/generator

all: ${TREE} ${TARGETS} ${RESOURCES}

clean: ${TREE}
	rm -f ${TARGETS} ${RESOURCES}

clean-all: clean
	rm -f ${TREE}

res/logo.png: res/logo-template.png ${SELF}
	${CONVERT} $< -fx 'a^1.3*#379+(1-a^1.3)*#eee' -channel A -fx 1 $@

%.html: %.txt
	${PROCESSOR} $< -b . -t /res/default.tmpl.html -o $@

${TREE}: ${HGREPO} ${SELF}
	${GENERATOR} $</.. > $@
	@echo 'Regenerated Makefile.tree. Try again.'

