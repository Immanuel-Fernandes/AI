import tkinter as tk
import math

def distance(x1, y1, x2, y2): 
    dist = math.pow(x2-x1, 2) + math.pow(y2-y1, 2) 
    return dist 

def sumOfDistances(x1, y1, points): 
    return sum(distance(x1, y1, px[0], px[1]) for px in points)

def newDistance(x1, y1, points): 
    d1temp = sumOfDistances(x1, y1, points) 
    return [x1, y1, d1temp]

def newPoints(minimum, candidates): 
    for candidate in candidates:
        if candidate[2] == minimum:
            return [candidate[0], candidate[1]]
    return None

class DistanceMinimizerApp:
    def __init__(self, master):
        self.master = master
        self.master.title("Distance Minimizer")
        
        self.increment = 0.1
        self.startingPoint = [1, 1]
        self.points = [[1, 5], [6, 4], [5, 2], [2, 1]]
        
        self.minDistance = sumOfDistances(self.startingPoint[0], self.startingPoint[1], self.points)
        self.flag = True
        
        self.label = tk.Label(master, text=f"Current Point: {self.startingPoint}")
        self.label.pack()

        self.start_button = tk.Button(master, text="Start Minimizing", command=self.start_minimizing)
        self.start_button.pack()

    def start_minimizing(self):
        i = 1
        while self.flag:
            d1 = newDistance(self.startingPoint[0] + self.increment, self.startingPoint[1], self.points)
            d2 = newDistance(self.startingPoint[0] - self.increment, self.startingPoint[1], self.points)
            d3 = newDistance(self.startingPoint[0], self.startingPoint[1] + self.increment, self.points)
            d4 = newDistance(self.startingPoint[0], self.startingPoint[1] - self.increment, self.points)

            minimum = min(d1[2], d2[2], d3[2], d4[2])
            candidates = [d1, d2, d3, d4]

            if minimum < self.minDistance:
                self.startingPoint = newPoints(minimum, candidates)
                self.minDistance = minimum

                self.label.config(text=f"Iteration {i}: Current Point: {self.startingPoint}")
                self.master.update()  
            else:
                break  


if __name__ == "__main__":
    root = tk.Tk()
    app = DistanceMinimizerApp(root)
    root.mainloop()
