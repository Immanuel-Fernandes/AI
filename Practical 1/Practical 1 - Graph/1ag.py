import tkinter as tk

def create_image_case(canvas, x, case, image_references):
    images = {
        0: ("00.png", x / 2, 100),
        1: ("01.png", x / 4, 200),
        2: ("02.png", x * 3 / 4, 200),
        3: ("03.png", x / 8, 300),
        4: ("04.png", x * 3 / 8, 300),
        5: ("05.png", x * 5 / 8, 300),
        6: ("06.png", x * 7 / 8, 300),
        7: ("07.png", x / 2, 400)
    }
    if case in images:
        file, x_pos, y_pos = images[case]
        img = tk.PhotoImage(file=file)
        canvas.create_image(x_pos, y_pos, anchor=tk.CENTER, image=img)
        image_references.append(img)
        return img

def update_status_label(status_label, iteration, traversal_order, visited, goal_node, goal_reached):
    status_text = (
        f"Iteration: {iteration}\n"
        f"Traversal Order: {traversal_order}\n"
        f"Visited Array: {visited}\n"
        f"Goal {'Reached' if goal_reached else 'Unsuccessful'}"
    )
    status_label.config(text=status_text)

def dfs_step(adjList, stack, visited, traversal_order, canvas, delay, status_label, image_references, goal_node):
    if stack:
        current_node = stack.pop()
        
        traversal_order.append(current_node)
        goal_reached = (current_node == goal_node)
        update_status_label(status_label, len(traversal_order), traversal_order, visited, goal_node, goal_reached)

        create_image_case(canvas, 720, current_node, image_references)

        if goal_reached:
            return

        for neighbor in reversed(adjList[current_node]):
            if not visited[neighbor]:
                visited[neighbor] = True
                stack.append(neighbor)
                
        canvas.after(delay, dfs_step, adjList, stack, visited, traversal_order, canvas, delay, status_label, image_references, goal_node)
    else:
        # No more nodes to explore, display unsuccessful message
        update_status_label(status_label, len(traversal_order), traversal_order, visited, goal_node, False)

def main():
    adjList = [
        [1, 2],     # Node 0: connected to nodes 1 and 2
        [3, 4],     # Node 1: connected to nodes 3 and 4
        [5, 6],     # Node 2: connected to nodes 5 and 6
        [],         # Node 3: no connections
        [7],        # Node 4: connected to node 7
        [7],        # Node 5: connected to node 7
        [],         # Node 6: no connections
        []          # Node 7: no connections
    ]

    start_node = 0
    goal_node = 7
    
    root = tk.Tk()
    root.title("DFS Visualization")
    x = cw = 720
    ch = 700
    root.geometry(f"{cw}x{ch}")
    canvas = tk.Canvas(root, width=cw, height=ch - 100, bg='light green')
    canvas.pack()
    status_label = tk.Label(root, text="", justify=tk.LEFT)
    status_label.pack()

    title = tk.PhotoImage(file="DFS.png")
    canvas.create_image(364, 23, image=title)
    canvas.create_line(cw / 2, 100 + 20, cw / 4, 200 - 20, fill="black")  
    canvas.create_line(cw / 2, 100 + 20, cw * 3 / 4, 200 - 20, fill="black")  
    canvas.create_line(cw / 4, 200 + 20, cw / 8, 300 - 20, fill="black")  
    canvas.create_line(cw / 4, 200 + 20, cw * 3 / 8, 300 - 20, fill="black")  
    canvas.create_line(cw * 3 / 4, 200 + 20, cw * 5 / 8, 300 - 20, fill="black")  
    canvas.create_line(cw * 3 / 4, 200 + 20, cw * 7 / 8, 300 - 20, fill="black")
    canvas.create_line(cw * 3 / 8, 300 - 20, x / 2, 400, fill="black")
    canvas.create_line(cw * 5 / 8, 300 - 20, x / 2, 400, fill="black")

    img0 = tk.PhotoImage(file="0.png")
    img1 = tk.PhotoImage(file="1.png")
    img2 = tk.PhotoImage(file="2.png")
    img3 = tk.PhotoImage(file="3.png")
    img4 = tk.PhotoImage(file="4.png")
    img5 = tk.PhotoImage(file="5.png")
    img6 = tk.PhotoImage(file="6.png")
    img7 = tk.PhotoImage(file="7.png")
    image_references = [img0, img1, img2, img3, img4, img5, img6, img7]
    canvas.create_image(x / 2, 100, anchor=tk.CENTER, image=img0)
    canvas.create_image(x / 4, 200, anchor=tk.CENTER, image=img1)
    canvas.create_image(x * 3 / 4, 200, anchor=tk.CENTER, image=img2)
    canvas.create_image(x / 8, 300, anchor=tk.CENTER, image=img3)
    canvas.create_image(x * 3 / 8, 300, anchor=tk.CENTER, image=img4)
    canvas.create_image(x * 5 / 8, 300, anchor=tk.CENTER, image=img5)
    canvas.create_image(x * 7 / 8, 300, anchor=tk.CENTER, image=img6)
    canvas.create_image(x / 2, 400, anchor=tk.CENTER, image=img7)

    stack = []
    visited = [False] * len(adjList)
    traversal_order = []
    visited[start_node] = True
    stack.append(start_node)
    delay = 1000  # Delay in milliseconds (1 second)
    canvas.after(delay, dfs_step, adjList, stack, visited, traversal_order, canvas, delay, status_label, image_references, goal_node)
    root.mainloop()

if __name__ == "__main__":
    main()
