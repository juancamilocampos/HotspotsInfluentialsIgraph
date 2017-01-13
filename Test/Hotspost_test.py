from Logic.Utils.graph_retweets import GraphRetweets
import igraph as ig
import Logic.Utils.graph_variables as gv

graph_class = GraphRetweets()
[graph_directed, graph_undirected] = graph_class.create()

inf = gv.influentials(graph_directed)

edges_weight = graph_undirected.es["weight"]
f = open('weights-271.txt', 'w')
f.write('{')
for item in edges_weight:
    f.write("%s " % item)
    f.write(",")
f.write("0")
f.write('}')
f.close()

print(graph_undirected.vcount())
g = (graph_undirected.decompose(maxcompno=1)[0])  # To get the largest connected component
print(g.vcount())
K = list(set(inf).intersection(g.vs["name"]))
g = gv.parallel_dijkstra_undirected(g, sorted(K))
Du = g.vs["Dv"]
Vu = g.vs["V"]

f = open('Dv-1.txt', 'w')
f.write('{')
for item in Du:
    f.write("%s " % item)
    f.write(",")
f.write("0")
f.write('}')
f.close()

print(Vu.count('id:twitter.com:100293263'))

# lista = {}
# for v in range(g.vcount()):
#     lista[g.vs[v]["name"]] = g.vs[g.vs[v]["V"]]["name"]
#
# results = gv.groups(lista)
