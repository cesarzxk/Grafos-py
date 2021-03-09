

import sys
import heapq

def cmp(x, y):
    return (x > y) - (x < y)

class Edge(object):

    def __init__(self, n, c):
        self.__node = n
        self.__cost = c

  
    def getVertex(self):
        return self.__node

    def getCost(self): 
        return self.__cost

    def setCost(self, c):
        self.__cost = c
    

    def cmpCost(self, other): 
        return -cmp(self.getCost(), other.getCost())


    def __repr__ (self):
        return "<%s, %s>" % (self.__node, self.__cost)

    def __hash__(self):
        return hash((self.__node, self.__cost))

    def __eq__(self, obj):
        if (self is obj):
            return True

        if (obj == None) or (type(obj) != type(self)):
            return False

        return (self.__node == obj.__node)


    def __contains__(self, obj):

class DiGraph(object):


    def __init__(self):
        self.graph = {}

        self.__numEdges = 0


        self.__infinity = sys.maxsize

        self.__pathToNode = None

        self.__dist = None

    def getInfinity(self):
        return self.__infinity
    
    def addEdge(self, src, dst, c=1):
        if ( src == None or dst == None or c <= 0 or src == dst ):
            return False

        # the edge set of src
        eSet = self.graph.get(src)
        e = Edge(dst,c) 
        if eSet == None: 
        
            eSet = set()
            self.__numEdges += 1
        else:
            ed = self.getEdge(src,dst)
            if ( ed != None ):
                ed.setCost(c)
                return True
            else:
                self.__numEdges += 1
        
        eSet.add(e) 

        self.graph[src] = eSet
        if not self.hasVertex(dst):
            self.addVertex(dst)
        
        return True

    
    def addVertex(self, vertex):
        if ( vertex == None or self.hasVertex(vertex) ):
            return False
        self.graph[vertex] = set()
        return True

    def numVertices(self):
        return len(self.graph)


    def vertices(self):
        return self.graph.keys()
    

    def adjacentTo(self,vertex):
        return set() if ( vertex == None or not self.hasVertex(vertex) ) else self.graph.get (vertex)
    

    def hasVertex(self,vertex): 
        return self.graph.get(vertex) != None
    

    def numEdges(self):
        return self.__numEdges
    

    def getEdge(self, src, dst):
        if ( src == None or dst == None or not self.hasVertex(src) or not self.hasVertex(dst) ):
            return None

        eSet = self.graph.get (src)

        for ed in eSet:
            if dst == ed.getVertex():
                return ed
            
        return None


    def hasEdge(self, src, dst):
        return self.getEdge(src,dst) != None
    


    def removeVertex(self, vertex):
        if ( vertex == None or not self.hasVertex(vertex) ):
            return False

        eSet = self.graph.get (vertex) 
        self.__numEdges -= len(eSet)

        for v in self.incomingEdges(vertex):
            eSet = self.graph.get(v)     
            eSet.remove(self.getEdge(v,vertex))
            self.__numEdges -= 1
        
        self.graph.pop(vertex)
        return True 

    def incomingEdges(self, vertex):
        if ( vertex == None or not self.hasVertex(vertex) ):
            return None

        hSet = set()  
        for v in self.vertices():
            if v != vertex:
                if self.hasEdge(v, vertex):
                    hSet.add(v)                       
        
        return hSet


    def __generate_edges(self):
        edges = []
        for vertex in self.graph:
            for neighbour in self.graph[vertex]:
                if (neighbour, vertex) not in edges:
                    edges.append((vertex, neighbour))
        return edges

    def __repr__(self):
        res = "vertices: "
        for k in self.graph:
            res += str(k) + " "
        res += "\nedges: "
        for edge in self.__generate_edges():
            res += str(edge) + " "
        return res


    def Dijkstra(self, source):

        if self.__dist is None:
            self.__dist = {}

        dist = self.__dist

        if ( source == None or not self.hasVertex(source) or not self.adjacentTo(source) ):
            return dist

        visited = {}
        previous = {}
            

        q = []

        for v in self.vertices():           
            dist[v] = self.getInfinity()    
            visited[v] = False              
            previous[v] = None             
                                            
        dist[source] = 0                    
        heapq.heappush(q,source)            

        while q:                            
            u = heapq.heappop(q)            
            if visited[u]:                  
                continue

            visited[u] = True               

            for e in self.adjacentTo(u):
                v = e.getVertex()
                
                alt = dist[u] + self.getEdge(u,v).getCost() 
                if alt < dist[v]:
                    dist[v] = alt           
                    previous[v] = u
                    if not visited[v]:
                        heapq.heappush(q,v) 
                
        self.__pathToNode = previous
        return dist

    def Dijkstra2(self, source, dest):
        sp = []

        if ( dest == None or not self.hasVertex(dest) ):
            return sp

        d = self.Dijkstra(source)
        if ( not d or self.__pathToNode.get(dest) == None ):
            return sp

        v = dest
        while  v != source and v != None:
            sp.insert(0, Edge(v,d.get(v)))
            v = self.__pathToNode.get(v)
        
        if sp:
            sp.insert(0,Edge(source,d.get(source)))

        return sp

def main(argv=None):
    if argv is None:
        argv = sys.argv

    if ( len(argv) > 1 ):
        f = argv[1]
                                                    
    try:
        g = DiGraph()
        g.addVertex ("f")
        g.addEdge ("a", "d")
        g.addEdge ("a", "c")
        g.addEdge ("c", "d")
        g.addEdge ("c", "b")
        g.addEdge ("c", "e")
        g.addEdge ("e", "c")
        print(g.Dijkstra("c"))
        print(g.numEdges())
        print("Dijkstra2 from c to e: %s" % g.Dijkstra2("c", "e"))
        print (g)
        print("incomingEdges of c: %s" % g.incomingEdges ("c"))
        g.removeVertex("c")
        print("Removed vertex c")
        print (g)
    except IOError:
        sys.exit ( "File %s not found." % f )

if __name__=="__main__":
    sys.exit(main())
