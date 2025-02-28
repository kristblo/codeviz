This folder should contain the CTAGS tagfiles generated for a given project.

For C++, CTAGS should be called with the following arguments:
ctags  --kinds-C++=* --recurse=yes --language-force=C++ --fields=* --extras=* --exclude=build --exclude=tagfiles -f ./tags_`<projectname>`

Add or remove excluded files/dirs as needed. Kinds, fields and extras all contribute to getting the right information out of CTAGS, but idk exactly which does what.



For C, CTAGS should be called with the following arguments:
????