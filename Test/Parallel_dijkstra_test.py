import igraph as ig
import Logic.Utils.graph_variables as gv

g = ig.Graph()
g.add_vertices(["a", "b", "c", "d", "e", "f"])
g.add_edges([("a", "b"), ("b", "c"), ("c", "d"), ("d", "a"), ("e", "f")])
g.es["weight"] = [1, 2, 3, 2.5, 4]

g = (g.decompose(maxcompno=1)[0])
g = gv.parallel_dijkstra_undirected(g, ["a", "c"])
Du = g.vs["Dv"]
Vu = g.vs["V"]

nodes = g.vs["name"]
ids = {}
for i in range(g.vcount()):
    ids[nodes[i]] = i

print(Vu.count(ids["a"]))
