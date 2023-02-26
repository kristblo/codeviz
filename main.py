from graph_tool.all import *
from global_utilities import *
from analyse_includes import *
from analyse_functions import *
from data_flow import *
import random

configFileName = 'byggern_project_config.cnf'
includepattern = getIncludePattern(configFileName)
topDirectory = getTopDirectory(configFileName)
excludedDirectories = getExludedDirs(configFileName)

#Get inclusion data
inclusiondata = getProjectInclusionData(topDirectory, excludedDirectories, configFileName)
inclusionMatrix = inclusiondata[0]
inclusionDict = inclusiondata[1]
filesFound = inclusiondata[2]
filesMentioned = inclusiondata[3]
allFiles = filesFound + filesMentioned

#Tokenize the project
tokensPerFile = tokenizeProject(configFileName, filesFound)
# for key in tokensPerFile:
#     print(key, tokensPerFile[key][0:5])

#Get function definitions and calls for entire project
functionData = getProjectFunctionData(configFileName, tokensPerFile)
functionDefinitionsPerFile =  functionData[0]
functionCalls = functionData[1]
functionGlobalDefs = functionData[2]
undefinedCallees = functionData[3]
functionMatrix = functionData[4]

funcdeflog = str(getKeywordFromConfigFile(configFileName, 'functiondeflog'))
for item in functionDefinitionsPerFile:    
    appendStringToFile(funcdeflog, str(item[0])+'\n')
    for name in item[1]:
        appendStringToFile(funcdeflog, str(name)+'\n')

funccalllog = str(getKeywordFromConfigFile(configFileName, 'functioncallog'))
for item in functionCalls:
    appendStringToFile(funccalllog, str(item)+'\n')


#Construct dataNodes
list1 = createNodesFromFcCalls(functionCalls, excludedFcNames)


#Remove file paths to avoid cluttered output
shortenedFileNames =[]
for item in allFiles:
    try:
        shortenedFileNames.append(os.path.basename(item))
    except:
        shortenedFileNames.append(item)

#Get immediate parent directory for clustering
parentDirPerFile = []
for item in filesFound:
    try:
        parentDirPerFile.append(os.path.dirname(item))
    except:
        parentDirPerFile.append("libfiles")
for item in filesMentioned:
    parentDirPerFile.append("libfiles")


uniqueParentDirs = []
for item in parentDirPerFile:
    if(item not in uniqueParentDirs):
        uniqueParentDirs.append(item)

colors = []
for item in uniqueParentDirs:
    colors.append([random.uniform(0.05,0.9), random.uniform(0.05,0.9), random.uniform(0.05,0.9), 1])
    


#Build include graph
maingraph = Graph(directed=True)
for file in (allFiles):
    maingraph.add_vertex()

#Link node text with vertices
vtext = maingraph.new_vertex_property("string")
for i in range(0, len(allFiles)):
    vtext[i] = shortenedFileNames[i]

#Associate vertices with a parent directory
vdir = maingraph.new_vertex_property("string")
for i in range(0, len(allFiles)):
    vdir[i] = parentDirPerFile[i]

vcolor = maingraph.new_vertex_property("vector<float>")
for i in range(0, len(allFiles)):
    for j in range(0, len(colors)):
        if(vdir[i] == uniqueParentDirs[j]):
            vcolor[i]=colors[j]


#Generate edges between includes
for i in range(0, len(inclusionMatrix)):    
    for j in range(0, len(allFiles)):
        if(inclusionMatrix[i][j] == 1):
            maingraph.add_edge(j, i)


#ARF layout
# vpos = arf_layout(maingraph, max_iter=0)
# graph_draw(maingraph,
#             pos=vpos,
#             vertex_text=vtext,
#             vertex_text_position=5,
#             vertex_size=6,
#             vertex_fill_color=vcolor,
#             #ink_scale=0.2,
#             output="arf/includes.pdf")

#Outdegree weighted force-directed layout
# indegmap = maingraph.degree_property_map("out")
# indegmap.a = 2*((indegmap.a**0.5)*0.5+0.4)+2
# ebet = betweenness(maingraph)[1]
# graph_draw(maingraph,
#             #pos=vpos,
#             vertex_text=vtext,
#             vertex_text_position="centered",
#             vertex_size=indegmap,            
#             ink_scale=3,
#             output="weighted-includes.pdf")

# #Hierarchical block something layout
# htest = minimize_nested_blockmodel_dl(maingraph)
# draw_hierarchy(htest, 
#                 vertex_text=vtext,
#                 vertex_text_position="centered",
#                 vertex_color=vcolor,
#                 output="hierarchicals/hierarchical_test.pdf")


#Filter out libfiles from the graph drawing
libvcs = maingraph.new_vertex_property("bool")
for i in range(0, maingraph.num_vertices()):
    if(vdir[i] == "libfiles"):
        libvcs[i] = False
    else:
        libvcs[i] = True
libsfiltered = GraphView(maingraph)
libsfiltered.set_vertex_filter(libvcs)
# vpos = arf_layout(libsfiltered, max_iter=0)
# graph_draw(libsfiltered,
#             pos=vpos,
#             vertex_text=vtext,
#             vertex_text_position=5,
#             vertex_color=vcolor,
#             output="arf/libfiles_filtered.pdf")

# #Hierarchical filtered
# hfiltered = minimize_nested_blockmodel_dl(libsfiltered)
# draw_hierarchy(hfiltered,
#                 vertex_text=vtext,
#                 vertex_text_position="centered",
#                 vertex_color=vcolor,
#                 output="hierarchicals/hierarchical_filtered.pdf")

# #Minimized blockmodel finds clusters without the nesting
# blocktest = minimize_blockmodel_dl(maingraph)
# blocktest.draw(ink_scale=0.5,
#                 vertex_text=vtext,
#                 vertex_text_position=5,
#                 vertex_size=6,
#                 output="blockmodels/blockmodel_test.pdf")

# #Minimized and filtered
# blockfiltered = minimize_blockmodel_dl(libsfiltered)
# blockfiltered.draw(ink_scale=0.5,
#                 vertex_text=vtext,
#                 vertex_text_position=5,
#                 vertex_size=6,
#                 output="blockmodels/blockmodel_filtered_test.pdf")



#########################################
#Idea for clustering by folder:
#Use ARF with two sets of edges: folders and include paths
#Generate the ARF layout with folder edges, creating strong clustering
#for files that are close to one another in the directories.
#Draw the graph with the include path edges visible
#########################################
#ARF layout
# dirDistanceG = Graph(directed=False)
# dirDistanceG.add_vertex(len(allFiles))
# distanceMatrix = inclusiondata[4]

# for i in range(0, len(distanceMatrix)):
#     for j in range(0, len(distanceMatrix[i])):     
#             #if(distanceMatrix[i][j] == 0):
#                 dirDistanceG.add_edge(i, j)

# vtext=dirDistanceG.new_vertex_property("string")
# for i in range(0, len(allFiles)):
#     vtext[i] = shortenedFileNames[i]


# edgeweights = dirDistanceG.new_edge_property("int")
# for i in range(0, len(distanceMatrix)):
#     for j in range(0, len(distanceMatrix[i])):
#         lincoord = i*len(distanceMatrix) + j
#         edgeweights.a[lincoord]=((distanceMatrix[i][j])*(0.05)+0.01)*(-1)


# vcolor = dirDistanceG.new_vertex_property("vector<float>")
# for i in range(0, len(allFiles)):
#     for j in range(0, len(colors)):
#         if(vdir[i] == uniqueParentDirs[j]):
#             vcolor[i]=colors[j]


# vpos = arf_layout(dirDistanceG, 
#                     weight=edgeweights,
#                     d=0.5,
#                     a=10,
#                     max_iter=500)

# #Filter out all 144² edges in order to not fuck with the drawer
# efilt = dirDistanceG.new_edge_property("bool")
# for item in efilt.a:
#     item = False
# dirDistanceG.set_edge_filter(efilt)
# #draw
# graph_draw(dirDistanceG,
#             pos=vpos,
#             vertex_text=vtext,
#             vertex_text_position=5,
#             vertex_size=6,
#             output_size=(1200,1200),
#             vertex_fill_color=vcolor,
#             ink_scale=1,
#             #fit_view=False,
#             #fit_view_ink=False,
#             output="arf/dirDists.pdf")

# #Adding include edges
# incDistanceG = GraphView(dirDistanceG,directed=True)
# for i in range(0, len(inclusionMatrix)):    
#     for j in range(0, len(allFiles)):
#         if(inclusionMatrix[i][j] == 1):
#             incDistanceG.add_edge(j, i)
            
# graph_draw(incDistanceG,
#             pos=vpos,
#             vertex_text=vtext,
#             vertex_text_position=5,
#             vertex_size=6,
#             output_size=(1200,1200),
#             #vertex_fill_color=vcolor,
#             ink_scale=1,
#             #fit_view=False,
#             #fit_view_ink=False,
#             output="arf/dircluster_incedges.pdf")


##################################################
#Grouped sfdp: Make parentdir a vertex prop map,
#and let the edges be includes from the start.
#Use group=vprop
##################################################
# groupedsfdp = Graph(directed=True)
# groupedsfdp.add_vertex(len(allFiles))

# vparents = groupedsfdp.new_vertex_property("int")
# parentnums = []
# for i in range(0, len(uniqueParentDirs)):
#     parentnums.append(i)

# for i in range(0, len(parentDirPerFile)):
#     for j in range(0, len(uniqueParentDirs)):
#         if(parentDirPerFile[i] == uniqueParentDirs[j]):
#             vparents[i] = parentnums[j]        

# vtext = groupedsfdp.new_vertex_property("string")
# for i in range(0, len(allFiles)):
#     vtext[i] = shortenedFileNames[i]

# for i in range(0, len(inclusionMatrix)):
#     for j in range(0, len(inclusionMatrix[i])):
#         if(inclusionMatrix[i][j] == 1):
#             groupedsfdp.add_edge(j, i)

# vcolor = groupedsfdp.new_vertex_property("vector<float>")
# for i in range(0, len(allFiles)):
#     for j in range(0, len(colors)):
#         if(vdir[i] == uniqueParentDirs[j]):
#             vcolor[i]=colors[j]




# vpos = sfdp_layout(groupedsfdp,
#                     gamma=50, #default 0.3, repulsion between groups
#                     r=0.3, #default 1, attraction between "connected components"
#                     groups=vparents)
# graph_draw(groupedsfdp,
#             pos=vpos,
#             vertex_text=vtext,
#             vertex_text_position=5,
#             vertex_size=10,
#             output_size=(1200,1200),
#             vertex_fill_color=vcolor,
#             ink_scale=1,
#             #fit_view=False,
#             #fit_view_ink=False,
#             output="sfdp/grouped_simple.pdf")

# #Test the effect of gamma and r
# gammas = [0.3, 1, 3, 10, 30]
# rs = [1, 5, 10, 20, 50]
# for gamma in gammas:
#     for r in rs:
#         vpos = sfdp_layout(groupedsfdp,
#                             gamma=gamma,
#                             r=r,
#                             groups=vparents)

#         op_string = "sfdp/grouped_g" + str(gamma) + "_r" + str(r) + ".pdf"
#         graph_draw(groupedsfdp,
#                     pos=vpos,
#                     vertex_size=6,
#                     vertex_fill_color=vcolor,
#                     ink_scale=1,
#                     output=op_string)


#############################################################################
#################################FUNCTIONS###################################
#############################################################################
functionGraph = Graph(directed=True)
for function in functionGlobalDefs:
    functionGraph.add_vertex()
for callee in undefinedCallees:
    functionGraph.add_vertex()

vtext = functionGraph.new_vertex_property("string")
for i in range(0, len(functionGlobalDefs)):    
    vtext[i] = functionGlobalDefs[i].name
for i in range(0, len(undefinedCallees)):
    vtext[len(functionGlobalDefs)+i] = undefinedCallees[i]

for i in range(0, len(functionMatrix)):
    for j in range(0, len(functionMatrix[i])):
        if functionMatrix[i][j] == 1:
            functionGraph.add_edge(j, i)


vpos = arf_layout(functionGraph, max_iter=0)
graph_draw(functionGraph,
            pos=vpos,
            vertex_text=vtext,
            vertex_text_position=5,
            vertex_size=6,
            #vertex_fill_color=vcolor,
            #ink_scale=0.2,
            output="arf/functions.pdf")
