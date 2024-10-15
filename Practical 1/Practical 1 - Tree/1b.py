import tkinter as tk
from collections import deque

def create_image_case(canvas, x, case, image_references):
    images = {
        0: ("00.png", x / 2, 100),
        1: ("01.png", x / 4, 200),
        2: ("02.png", x * 3 / 4, 200),
        3: ("03.png", x / 8, 300),
        4: ("04.png", x * 3 / 8, 300),
        5: ("05.png", x * 5 / 8, 300),
        6: ("06.png", x * 7 / 8, 300)
    }
    if case in images:
        file, x_pos, y_pos = images[case]
        img = tk.PhotoImage(file=file)
        canvas.create_image(x_pos, y_pos,  image=img)
        image_references.append(img)
        return img

def update_status_label(status_label, iteration, traversal_order, visited):
    status_text = (
        f"Iteration: {iteration}\n"
        f"Traversal Order: {traversal_order}\n"
        f"Visited Array: {visited}"
    )
    status_label.config(text=status_text)

def bfs_step(adjList, queue, visited, traversal_order, canvas, delay, status_label, image_references):
    if queue:
        currentNode = queue.popleft()
        traversal_order.append(currentNode)
        update_status_label(status_label, len(traversal_order), traversal_order, visited)

        case = currentNode
        create_image_case(canvas, 720, case, image_references)

        for neighbor in adjList[currentNode]:
            if not visited[neighbor]:
                visited[neighbor] = True
                queue.append(neighbor)
        
        canvas.after(delay, bfs_step, adjList, queue, visited, traversal_order, canvas, delay, status_label, image_references)
    else:
        for i in range(len(adjList)):
            if not visited[i]:
                visited[i] = True
                queue.append(i)
                canvas.after(delay, bfs_step, adjList, queue, visited, traversal_order, canvas, delay, status_label, image_references)
                break

def main():
    # adjList = [
    #     [1, 2],     # Node 0: connected to nodes 1 and 2
    #     [3, 4],     # Node 1: connected to nodes 3 and 4
    #     [5, 6],     # Node 2: connected to nodes 5 and 6
    #     [],         # Node 3: no connections
    #     [],         # Node 4: no connections
    #     [],         # Node 5: no connections
    #     []          # Node 6: no connections
    # ]

    adjList = [ [1, 2], [3, 4], [5, 6], [], [], [], [] ]

    startNode = 0  # Change the start node here
    root = tk.Tk()
    root.title("BFS")
    x = cw = 720
    ch = 500
    root.geometry(f"{cw}x{ch}")
    canvas = tk.Canvas(root, width=cw, height=ch - 100)
    canvas.pack()
    status_label = tk.Label(root, text="", justify=tk.CENTER)
    status_label.pack()

    title = tk.PhotoImage(file="BFS.png")
    canvas.create_image(364, 23, image=title)
    canvas.create_line(cw / 2, 100 + 20, cw / 4, 200 - 20)
    canvas.create_line(cw / 2, 100 + 20, cw * 3 / 4, 200 - 20)
    canvas.create_line(cw / 4, 200 + 20, cw / 8, 300 - 20)
    canvas.create_line(cw / 4, 200 + 20, cw * 3 / 8, 300 - 20)
    canvas.create_line(cw * 3 / 4, 200 + 20, cw * 5 / 8, 300 - 20)
    canvas.create_line(cw * 3 / 4, 200 + 20, cw * 7 / 8, 300 - 20)
    img0 = tk.PhotoImage(file="0.png")
    node0 = canvas.create_image(x / 2, 100, image=img0)
    img1 = tk.PhotoImage(file="1.png")
    node1 = canvas.create_image(x / 4, 200, image=img1)
    img2 = tk.PhotoImage(file="2.png")
    node2 = canvas.create_image(x * 3 / 4, 200, image=img2)
    img3 = tk.PhotoImage(file="3.png")
    node3 = canvas.create_image(x / 8, 300, image=img3)
    img4 = tk.PhotoImage(file="4.png")
    node4 = canvas.create_image(x * 3 / 8, 300, image=img4)
    img5 = tk.PhotoImage(file="5.png")
    node5 = canvas.create_image(x * 5 / 8, 300, image=img5)
    img6 = tk.PhotoImage(file="6.png")
    node6 = canvas.create_image(x * 7 / 8, 300, image=img6)
    queue = deque()
    visited = [False] * len(adjList)
    traversal_order = []
    image_references = []
    visited[startNode] = True
    queue.append(startNode)
    delay = 1000  # Delay in milliseconds (1 second)
    canvas.after(delay, bfs_step, adjList, queue, visited, traversal_order, canvas, delay, status_label, image_references)
    root.mainloop()

if __name__ == "__main__":
    main()
