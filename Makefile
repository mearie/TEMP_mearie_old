.PHONY: all clean clean-all

HGREPO = .hg
SELF = Makefile
TREE = Makefile.tree
CACHEDIR = res/cache

HG = hg -R ${HGREPO}/..
PYTHON = python
CONVERT = convert
PROCESSOR = ${PYTHON} bin/processor -c ${CACHEDIR} -b ${HGREPO}/..
GENERATOR = bin/generator

all: ${TREE}

-include ${TREE}

all: ${TARGETS}

clean: ${TREE}
	@rm -f ${TARGETS} bin/mearie/*.pyc
	@rm -rf ${CACHEDIR}

clean-all: clean
	@rm -f ${TREE}

res/logo.png: res/logo-template.png ${SELF}
	${CONVERT} $< -fx 'a^1.3*#379+(1-a^1.3)*#eee' -channel A -fx 1 $@

%.html: %.txt
	${PROCESSOR} $< -o $@

index.ko.html index.en.html: recent.json

define JOURNAL_ARCHIVE
$(1)index.ko.html: $$(wildcard $(1)*/*.ko.html)
endef

$(foreach path,$(wildcard journal/*/index.ko.txt),$(eval $(call JOURNAL_ARCHIVE,$(dir ${path}))))

${TREE}: ${HGREPO} ${SELF}
	${GENERATOR} $</.. $@
	@echo Regenerated Makefile.tree. Try again.

