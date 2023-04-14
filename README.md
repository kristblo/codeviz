# codeviz
Welcome to Codeviz, the creatively named service for visulisation of code! The goal of this project is to find useful ways to visualise data structures and flow within (primarily, for now) C/C++ programs. I like diagrams that explain how code works, but I don't necessarily like making them -- and neither do most programmers, I think. Manually made, highly detailed diagrams also lose their relevance quickly (unless they're really high level) as a project develops, making maintainance a more or less futile exercise. So why not automate the process? We have doxygen to give us inheritance diagrams, sure, but that just doesn't do it for me. A script to find include hierarchies takes about an afternoon to write, and gives at least a superficial explanation for how the program is structured. But what about function call hierarchies? Information being passed between threads? Variables being altered by functions, either as return values or pass-by-reference? As far as I have looked, there aren't readily available tools for this -- at least not on a student budget (~0USD/yr). I'm still hammering out the details of what data flow really means, but if you've ever felt like you've got lost in your own (or others') code, you might want to check this out. It's all in python, currently, but I'm working on a translation to C++ and an executable for the sake of simplicity.


### Usage:
* Install graph-tool, which handles generation of pdfs based on graph data. I use Anaconda for this.
   * Probably the hardest step in this whole process tbh.
* In main.py, set the config file name to the name of your config file. Make sure it's saved in the same folder as main.py.
* Look at template_config.cnf and configure your project. It is literally just a text file which I had the hubris to rename to .cnf.
   * Note the lack of spaces between keywords and data (i.e. keyword:data, not keyword: data)
* Probably don't touch the includepattern and sourcepattern fields.
* Set topDirectory to the topmost folder in the C/C++ project you want to analyse. Remember the terminal forward slash (/).
* Set excludedDirectories using python list syntax; Don't waste time looking through build folders etc.
* You can probably leave the whole #logfiles section alone, but MAKE SURE that the folders mentioned there actually exist. These scripts make no attempt at actually creating them.
* Not yet integrated into the config file is the output folder where the PDFs are stored. If you get "directory does not exist" errors, look at main.py and see where graph_draw tries to store stuff (Ctrl+f 'output='). The folder structure at the bottom of this readme should be up to date, however. Again, just make sure these actually exist in the same dir as main.py -- you WILL have to create them yourself.
* The main file has a lot of different sections, many are commented out. I think I've kept the most interesting sections. If the program crashes, comment out sections until it doesn't. Graph-tool seems to be well optimized, but even smaller projects will generate a ton of data, and much of what I have written is N2 and worse. Sorry.
* Get some tea while it does its thing.
* Look at some of the graphs, and feel free to let me know which ones are the most interesting/useful.



### Output folder structure:
* output/
    * arf/
    * blockmodels/
    * hierarchicals/
    * sfdp/

As you can see, these are sorted by graph types rather than by what information the graphs actually contain. IMO, the best graphs are in the SFDP folder. SFDP essentially makes a mass-spring system of the graph, and runs it as an ODE (I think) for a number of iterations. The file names are mass-spring coefficients as defined by the arrays 'gammas' and 'rs' in main.py. Hierachicals are pretty, but I don't see them being developed much as I don't find them very informative. ARF, as far as I've understood, is a less sophisticated version of SFDP. Not even sure what blockmodels actually do. The graph-tool docs are a bit sparse.

dfv2_g30_r1 probably demonstrates the best what I want to achieve (but interactively in a 3D environment down the line) the best. Red nodes are functions, and yellow nodes are data (usually variables). An edge can be understood as a data link, i.e. a function writing to a variable or a variable being used as an argument in a function call. All edges should eventually lead to main.c, otherwise the nodes they connect aren't actually in use in the program. This obvously isn't reliable atm, as most data nodes aren't connected. The clustering should signify that nodes come from the same file, making the visual connection between code structure and data flow clear.


### Reliability:
This is highly experimental for now, but I am reasonably confident that the relations the program does find are correct -- I just have a lot of work left to do. That will happen i C++ however, and this python iteration will not be further developed. There's a lot more experimental python stuff in the dev branch.
