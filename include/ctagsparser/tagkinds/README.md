This directory contains classes dedicated to representing the various "kinds" of
CTAGS. That is, for each instance of kind:`<kind>` there is in a CTAGS tagfile,
there should be one class here named `<kind>`tag. They should inherit from the
parent class tagObject. Beyond that, there may not be any particular patterns.
Each tag kind may need to be treated in its own way.

The purpose is to make the information in a CTAG tagfile compatible with the classes
defined in datanodes.