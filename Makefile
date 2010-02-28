.PHONY: all clean clean-all

HGREPO = .hg
SELF = Makefile
TREE = Makefile.tree
RESOURCES = res/logo.png
CACHEDIR = res/cache

HG = hg -R ${HGREPO}/..
CONVERT = convert
PROCESSOR = res/processor -c ${CACHEDIR} -b ${HGREPO}/..
GENERATOR = res/generator

all: ${TREE}

-include ${TREE}

all: ${TARGETS} ${RESOURCES}

clean: ${TREE}
	rm -f ${TARGETS} ${RESOURCES}
	rm -rf ${CACHEDIR}

clean-all: clean
	rm -f ${TREE}

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
	${GENERATOR} $</.. > $@ || (rm $@; exit 1)
	@echo 'Regenerated Makefile.tree. Try again.'

