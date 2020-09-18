all:


# setup
setup: setup_submodules link_libs
setup_submodules: 
	git submodule update --init --recursive --remote --merge

link_libs: plugin/bibtexparser plugin/pyparsing

# note link needs to be relative to link location! - more modern ln has -r option, but not mac.
#plugin/pyparsing: libs/pyparsing/pyparsing/
	#ln -shF ../$< $@
#plugin/bibtexparser: libs/python-bibtexparser/bibtexparser 
	#ln -shF ../$< $@

# create zip
publish/example.zip:
	mkdir -p $(@D)
	cd plugin/; zip -r ../$@ ./ -x \*/tests/\*
	#zip -r $@ plugin/ -x \*/tests/\*

# development
refresh_plugin: 
	calibre-debug -s; calibre-customize -b plugin/
runplug: refresh_plugin
	calibre

ipython: refresh_plugin
	calibre-debug -c "from calibre import ipython; ipython(locals())"

clean: clean_pub
clean_pub:
	rm -rf publish/*
