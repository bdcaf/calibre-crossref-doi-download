link_libs: plugin/bibtexparser

plugin/bibtexparser: libs/python-bibtexparser/bibtexparser 
	ln -shF ../$< $@
	# note link needs to be relative to link location! - more modern ln has -r option, but not mac.

publish/example.zip:
	mkdir -p $(@D)
	cd plugin/; zip -r ../$@ ./ -x \*/tests/\*
	#zip -r $@ plugin/ -x \*/tests/\*
