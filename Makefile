all:


# setup
setup: setup_submodules link_libs
setup_submodules: 
	git submodule update --init --recursive --remote --merge

link_libs: 

# note link needs to be relative to link location! - more modern ln has -r option, but not mac.
#plugin/pybtex: libs/pybtex-0.22.2/pybtex/
	#ln -shF ../$< $@
#plugin/pyparsing: libs/pyparsing/pyparsing/
	#ln -shF ../$< $@
#plugin/bibtexparser: libs/python-bibtexparser/bibtexparser 
	#ln -shF ../$< $@

# create zip
publish/crossref-doi-download.zip: plugin/
	mkdir -p $(@D)
	cd plugin/; zip -r ../$@ ./ -x \*/tests/\*
	#zip -r $@ plugin/ -x \*/tests/\*

# development
refresh_plugin: link_libs
	calibre-debug -s; calibre-customize -b plugin/
runplug: refresh_plugin
	calibre-debug -g

ipython: refresh_plugin
	calibre-debug helper/debug.py

clean: remove_plugin remove_linked clean_pub
clean_pub:
	rm -rf publish/*
remove_linked:
	find plugin -type l -delete

remove_plugin:
	# list plugins with calibre-customize -l
	calibre-customize -r "Crossref DOI Metadata Downloader"
