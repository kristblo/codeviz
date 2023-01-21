from graph_tool.all import *
from compile_project import *

maingraph = Graph(directed=True)

for fileObject in graphNodes:
    maingraph.add_vertex()



vnodemap = maingraph.new_vertex_property("object")
for i in range(0, len(graphNodes)):
    vnodemap[i] = graphNodes[i]

vtext = maingraph.new_vertex_property("string")
for i in range(0, len(graphNodes)):
    vtext[i] = vnodemap[i].name


for vertex in maingraph.vertices():
    for include in vnodemap[vertex].shortIncludes:
        for incvx in maingraph.vertices():
            if(include == vnodemap[incvx].shortpath):                    
                maingraph.add_edge(incvx, vertex)




graph_draw(maingraph, 
           ink_scale=0.2,
           vertex_text=vtext,
           output="graphtoolstest.pdf")