import tkinter as tk
from tkinter import messagebox

class Graph:
    def __init__(self, graph, heuristicNodeList, startNode):
        self.graph = graph
        self.H = heuristicNodeList
        self.start = startNode
        self.parent = {}
        self.status = {}
        self.solutionGraph = {}

    def applyAOStar(self):
        self.aoStar(self.start, False)

    def getNeighbors(self, v):
        return self.graph.get(v, '')

    def getStatus(self, v):
        return self.status.get(v, 0)

    def setStatus(self, v, val):
        self.status[v] = val

    def getHeuristicNodeValue(self, n):
        return self.H.get(n, 0)

    def setHeuristicNodeValue(self, n, value):
        self.H[n] = value

    def printSolution(self):
        return f"SOLUTION GRAPH: {self.solutionGraph}"

    def computeMinimumCostChildNodes(self, v):
        minimumCost = float('inf')
        costToChildNodeListDict = {}
        for nodeInfoTupleList in self.getNeighbors(v):
            cost = 0
            nodeList = []
            for c, weight in nodeInfoTupleList:
                cost += self.getHeuristicNodeValue(c) + weight
                nodeList.append(c)
            if cost < minimumCost:
                minimumCost = cost
                costToChildNodeListDict[minimumCost] = nodeList
        return minimumCost, costToChildNodeListDict.get(minimumCost, [])

    def aoStar(self, v, backTracking):
        if self.getStatus(v) >= 0:
            minimumCost, childNodeList = self.computeMinimumCostChildNodes(v)
            self.setHeuristicNodeValue(v, minimumCost)
            self.setStatus(v, len(childNodeList))
            solved = all(self.getStatus(childNode) == -1 for childNode in childNodeList)
            if solved:
                self.setStatus(v, -1)
                self.solutionGraph[v] = childNodeList
            if v != self.start:
                self.aoStar(self.parent[v], True)
            if not backTracking:
                for childNode in childNodeList:
                    self.setStatus(childNode, 0)
                    self.aoStar(childNode, False)

class GraphApp:
    def __init__(self, root):
        self.root = root
        self.root.title("AO* Algorithm GUI")
        
        self.label = tk.Label(root, text="Click 'Run AO* Algorithm' to start.")
        self.label.pack(pady=10)

        self.run_button = tk.Button(root, text="Run AO* Algorithm", command=self.run_ao_star)
        self.run_button.pack(pady=5)

        self.result_text = tk.Text(root, height=15, width=50)
        self.result_text.pack(pady=10)

        self.setup_graph()

    def setup_graph(self):
        self.h1 = {'A': 1, 'B': 6, 'C': 2, 'D': 12, 'E': 2, 'F': 1, 'G': 5, 'H': 7, 'I': 7, 'J': 1}
        self.graph1 = {
            'A': [[('B', 1), ('C', 1)], [('D', 1)]],
            'B': [[('G', 1)], [('H', 1)]],
            'C': [[('J', 1)]],
            'D': [[('E', 1), ('F', 1)]],
            'G': [[('I', 1)]]
        }
        self.G1 = Graph(self.graph1, self.h1, 'A')

    def run_ao_star(self):
        self.G1.applyAOStar()
        solution = self.G1.printSolution()
        self.result_text.delete(1.0, tk.END)
        self.result_text.insert(tk.END, solution)

if __name__ == "__main__":
    root = tk.Tk()
    app = GraphApp(root)
    root.mainloop()
