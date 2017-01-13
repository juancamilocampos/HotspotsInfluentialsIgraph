from Logic.Utils.graph_retweets import GraphRetweets
import igraph as ig
import Logic.Utils.graph_variables as gv

graph_class = GraphRetweets()
[graph_directed, graph_undirected] = graph_class.create()

inf = gv.influentials(graph_directed)
#
# edges_weight = graph_undirected.es["weight"]
# f = open('weights-24.txt', 'w')
# f.write('{')
# for item in edges_weight:
#     f.write("%s " % item)
#     f.write(",")
# f.write("0")
# f.write('}')
# f.close()

print(graph_undirected.vcount())
g = (graph_undirected.decompose(maxcompno=1)[0])  # To get the largest connected component
print(g.vcount())
K = list(set(inf).intersection(g.vs["name"]))
g = gv.parallel_dijkstra_undirected(g, sorted(K))
Du = g.vs["Dv"]
Vu = g.vs["V"]

print(Vu.count('id:twitter.com:100293263'))

nodes = g.vs["name"]
ids = {}
for i in range(g.vcount()):
    ids[nodes[i]] = i

lista = {}
for v in range(g.vcount()):
    lista[g.vs[v]["name"]] = g.vs[v]["V"]

results = gv.groups(lista)

[hotspot_boolean, c, weights_influentials] = gv.graph_hotspots(results, K, g, 1.01)
print(1)
f = open('weights-between-influentials-24.txt', 'w')
f.write('{')
for item in weights_influentials:
    f.write("%s " % item)
    f.write(",")

f.write("0")
f.write('}')
f.close()