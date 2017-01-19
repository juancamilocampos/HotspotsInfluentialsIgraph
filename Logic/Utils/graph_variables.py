# coding=utf-8
import igraph as ig
import math
import heapq
from collections import defaultdict


def _replace(lista, item_to_replace, replacement_value):
    """
    :Date: 2016-09-18
    :Version: 0.1
    :Author: Juan Camilo Campos - Pontificia Universidad Javeriana Cali
    :Copyright: To be defined
    :Organization: Centro de Excelencia y Apropiación de Big Data y Data Analytics - CAOBA

    This method replaces every occurrence of the item_to_replace by the replacement value

    :param: lista: list of values
    :param: item_to_replace: value to replace.
    :param: replacement_value: replacement value
    :rtype: list
    :return: Returns the new list

    """
    for n, i in enumerate(lista):
        if i == item_to_replace:
            lista[n] = replacement_value

    return lista


def influentials(g):
    """
    :Date: 2016-09-18
    :Version: 0.1
    :Author: Juan Camilo Campos - Pontificia Universidad Javeriana Cali
    :Copyright: To be defined
    :Organization: Centro de Excelencia y Apropiación de Big Data y Data Analytics - CAOBA

    This method evaluates if each node satisfies the requirements to be considered as influential. Then it return the
    list of influentials

    :param: g:  weighted graph (V,E) of retweets where i->j belongs to E if user i retweets user j. V = {v1, ... vn},
     such that v=(name, friends, followers)
    :rtype: list
    :return: Returns the list of influential users
    """
    threshold1 = 1/100.0
    threshold2 = 1/10.0

    nodes = g.vs["name"]

    retweets = [sum([g.es[s]["weight"] for s in g.incident(t, mode="out")]) for t in nodes]
    times_retweeted = [sum([g.es[s]["weight"] for s in g.incident(t, mode="in")]) for t in nodes]

    retweets = _replace(retweets, 0, 1)

    friends = g.vs["friends"]
    followers = g.vs["followers"]

    friends = _replace(friends, 0, 1)

    list_influentials = []

    i = 0
    while i < len(nodes):
        if (followers[i] <= 0) or (times_retweeted[i] <= 0) or (friends[i] <= 0) or (retweets[i] <= 0):
            nodes.pop(i)
            followers.pop(i)
            friends.pop(i)
            times_retweeted.pop(i)
            retweets.pop(i)
        else:
            x = retweets[i] / float(times_retweeted[i])
            y = friends[i] / float(followers[i])

            if (x < threshold1) and (y < threshold2):
                list_influentials = list_influentials + [nodes[i]]

            i += 1

    return list_influentials


def _interest_entrophy(C, Hu):
    """
    :Date: 2016-09-18
    :Version: 0.1
    :Author: Juan Camilo Campos - Pontificia Universidad Javeriana Cali
    :Copyright: To be defined
    :Organization: Centro de Excelencia y Apropiación de Big Data y Data Analytics - CAOBA

    This method computes the entropy of a user's hashtags

    :param: C: Hashtags communities (topics in the hashtags co-occurrence graph).
    :param: Hu: Hashtags used by the user.
    :rtype: float
    :return: Returns value of the entrophy of a user's hashtags
    """

    Cn = C
    T = []

    for h in Hu:
        cdefined = False

        for i in range(0, len(Cn)):
            community = Cn[i]

            if h in community:
                T = T + [i]
                cdefined = True

        if cdefined == False:
            Cn = Cn + [[h]]
            T = T + [len(Cn) - 1]

    Tu = list(set(T))
    nu = float(len(Hu))
    totalu = 0
    for Tk in Tu:
        P = (T.count(Tk)) / nu
        totalu = totalu - P * math.log10(P)

    return totalu


def users_entrophy(C, H):
    """
    :Date: 2016-09-18
    :Version: 0.1
    :Author: Juan Camilo Campos - Pontificia Universidad Javeriana Cali
    :Copyright: To be defined
    :Organization: Centro de Excelencia y Apropiación de Big Data y Data Analytics - CAOBA

    This method computes the entropy of hashtags for all users.

    :param: C: Hashtags communities (topics in the hashtags co-occurence graph).
    :param: Hu: List of Hashtags used by each user.
    :rtype: list of floats
    :return: Returns a list with the values of the entrophy of hashtags for all users.
    """

    graphentrophy = list()

    for Hu in H:
        graphentrophy.append(_interest_entrophy(C, Hu))

    return graphentrophy


def parallel_dijkstra_undirected(g, k):
    nbors = {}
    graph = g
    nodes = graph.vs["name"]
    for v in nodes:
        nbors[v] = [nodes[s] for s in graph.neighbors(v)]

    ids = {}
    for i in range(graph.vcount()):
        ids[nodes[i]] = i

    graph.vs["Dv"] = [1000]*graph.vcount()
    graph.vs["V"] = [0]*graph.vcount()
    graph.vs["visit"] = [0]*graph.vcount()

    Q = []
    for ki in k:
        node = ids[ki]
        graph.vs[node]["Dv"] = 0
        graph.vs[node]["V"] = ki
        heapq.heappush(Q, (0, ki))

    # Node Expansion: First find the lowest value and check not visited node
    while len(Q) != 0:
        v = heapq.heappop(Q)
        graph.vs[ids[v[1]]]["visit"] = 1  # Mark the node as visited

        # Visit all the neighbors of the node to be expanded
        for nbr in nbors[v[1]]:
            if graph.vs[ids[nbr]]["visit"] == 0:
                delta = graph.vs[ids[v[1]]]["Dv"] + graph.es[graph.get_eid(nbr, v[1])]["weight"]

                node = ids[nbr]
                if graph.vs[node]["Dv"] == 1000:
                    graph.vs[node]["Dv"] = delta
                    graph.vs[node]["V"] = graph.vs[ids[v[1]]]["V"]
                    heapq.heappush(Q, (delta, nbr))

                if (graph.vs[node]["Dv"] < 1000) and (delta < graph.vs[node]["Dv"]):
                    graph.vs[node]["V"] = graph.vs[ids[v[1]]]["V"]
                    graph.vs[node]["Dv"] = delta
    return graph


def groups(many_to_one):
    one_to_many = defaultdict(list)
    for v, k in many_to_one.items():
        one_to_many[k].append(v)
    return dict(one_to_many)


def graph_hotspots(dict_voronoi, K, g, max_distance):
    """
    :Date: 2016-09-18
    :Version: 0.1
    :Author: Juan Camilo Campos - Pontificia Universidad Javeriana Cali
    :Copyright: To be defined
    :Organization: Centro de Excelencia y Apropiación de Big Data y Data Analytics - CAOBA

    This method establishes the existence of hotspots in a Graph. Furthermore, if there are hotspots, then it returns which are the hotspots

    :param: dict_voronoi: dictionary with the information about the voronoi segmentation
    :param: K: breaking nodes (sometimes the influentials)
    :param: g: unweighted and undirected graph
    :param: max_distance: maximum distance between breaking point to be considered as a part of the same hotspots
    :rtype: list [hotspotboolean,c,final_hotspots]
    :return: hotspotboolean: It is True if there are hotspots in the graph
    :return: c: The percentage of crimes or influentials when there is the 30% of the network in the accumulative distribution
    :return: final_hotspots: If there are hotspots, it contains the hotspots
    """
    cell_sizes = list()
    for k in K:
        cell_sizes.append([k, len(dict_voronoi[k])])

    cell_sizes = sorted(cell_sizes, key=lambda t: t[1])

    nnodes = g.vcount()
    nodes_distribution = [0]
    influentials_distribution = list()
    ncells = len(K)
    c = 0
    for i in range(ncells):
        nodes_distribution.append(nodes_distribution[-1] + cell_sizes[i][1])
        [x, y] = [1.0 * (i + 1) / ncells, 1.0 * nodes_distribution[-1] / nnodes]
        influentials_distribution.append([x, y])
        if y <= 0.3:
            c = x
            px = i

    # If more than the 70% of influentials are contained in the 30% of the network, then there are hostposts and
    # it stars to calculate them.

    if c >= 0.70:
        # Hk is the set of the breaking nodes which build the "small" voronoi cells.
        Hk = list()
        for i in range(px):
            Hk.append(cell_sizes[i][0])

        weights_distribution = list()
        wei = g.es["weight"]
        print(Hk[0])
        for i in range(len(Hk)-1):
            for j in range(i+1, len(Hk)):
                weights_distribution.append(g.shortest_paths_dijkstra(Hk[i], Hk[j], weights=wei)[0][0])

        # final_hotspots = _hotspots_breaking_nodes(dict_voronoi, Hk, g, maxdistance)
        # return [True, c, final_hotspots]
        return [True, c, weights_distribution]

    else:
        return [False, 0, {}]