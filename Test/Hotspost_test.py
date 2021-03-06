from Logic.Utils.graph_retweets import GraphRetweets
import igraph as ig
import Logic.Utils.graph_variables as gv

graph_class = GraphRetweets()
[graph_directed, graph_undirected] = graph_class.create()

inf = gv.influentials(graph_directed)
print(len(inf))
edges_weight = graph_undirected.es["weight"]
f = open('weights-25.txt', 'w')
f.write('{')
for item in edges_weight:
    f.write("%s " % item)
    f.write(",")
f.write("0")
f.write('}')
f.close()

graphs = graph_undirected.decompose()  # To get the largest connected component
graphs_count = [g.vcount() for g in graphs]
g = graphs[graphs_count.index(max(graphs_count))]

K = list(set(inf).intersection(g.vs["name"]))
print(len(K))
g = gv.parallel_dijkstra_undirected(g, sorted(K))
Du = g.vs["Dv"]
Vu = g.vs["V"]

nodes = g.vs["name"]
ids = {}
for i in range(g.vcount()):
    ids[nodes[i]] = i

lista = {}
for v in range(g.vcount()):
    lista[g.vs[v]["name"]] = g.vs[v]["V"]

results = gv.groups(lista)

[hotspot_boolean, c, final_hotspots] = gv.graph_hotspots(results, sorted(K), g, 0.111)
print(c)
print(len(final_hotspots))
f = open('hotspots-011-25.txt', 'w')
f.write('{')
for item in final_hotspots:
    f.write("%s " % len(item))
    f.write(",")

f.write("0")
f.write('}')
f.close()
# [hotspot_boolean, c, weights_influentials] = gv.graph_hotspots(results, sorted(K), g, 0.51)
# print(c)
# f = open('weights-between-influentials-27.txt', 'w')
# f.write('{')
# for item in weights_influentials:
#     f.write("%s " % item)
#     f.write(",")
#
# f.write("0")
# f.write('}')
# f.close()
