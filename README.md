# codeviz

Project for the visualisation of C code inspired by the star charts found in various video games and a love for visual documentation.

Scope, ish:
1. Open a (c) file
2. Find and store the full include paths of all relevant files starting from a top directory ("the project")
3. Find and store all functions (defs, decs and calls) in the project
4. Find and store all variables of simple data types like int, char, str, vec
5. Find and store more complex data types like structs, maybe expand to C++ concepts like classes
6. Find relations in the code
7. Visualise them
------
I think I'm writing a tokenizer. Basically something that parses .c and .h files , creates tables/matrices/whatever of all the contents aprnd feeds that to a graphics engine (currently graph-tool, possibly UE later if I don't lose interest).

#cnf
I made a simple configuration file format to help building a project.
My "compiler" will look for the following keywords in the file, and insert whatever comes after them on the same line in the relevant places in the code.

includepattern: regex pattern to find include statements, for adjustment per language.
sourcepattern: regex pattern to find source files by looking for file endings.
topDirectory: absolute path to the project
excludedDirectories: subdirectories to be ignored by the compiler, mostly relevant for the include paths. Some of my algorithms are at least O2, so not having to scan through large libraries, for instance, is relevant.
includelog: where to put include paths diagnostics.
