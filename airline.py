from tkinter import *
from tkinter.ttk import *
import tkinter.messagebox

from collections import deque, namedtuple

if __name__ == "__main__":
    # infity = default distance for nodes
    inf = float('inf')
    Edge = namedtuple('Edge', 'start, end, cost')

    def make_edge(start, end, cost=1):
        return Edge(start, end, cost)

    class Graph:
        def __init__(self, edges):
            # let's check that the data is right
            wrong_edges = [i for i in edges if len(i) not in [2, 3]]
            if wrong_edges:
                raise ValueError('Wrong edges data: {}'.format(wrong_edges))

            self.edges = [make_edge(*edge) for edge in edges]

        @property
        def vertices(self):
            return set(
                sum(
                    ([edge.start, edge.end] for edge in self.edges), []
                )
            )

        def get_node_pairs(self, n1, n2, both_ends=True):
            if both_ends:
                node_pairs = [[n1, n2], [n2, n1]]
            else:
                node_pairs = [[n1, n2]]
            return node_pairs

        def remove_edge(self, n1, n2, both_ends=True):
            node_pairs = self.get_node_pairs(n1, n2, both_ends)
            edges = self.edges[:]
            for edge in edges:
                if [edge.start, edge.end] in node_pairs:
                    self.edges.remove(edge)

        def add_edge(self, n1, n2, cost=1, both_ends=True):
            node_pairs = self.get_node_pairs(n1, n2, both_ends)
            for edge in self.edges:
                if [edge.start, edge.end] in node_pairs:
                    return ValueError('Edge {} {} already exists'.format(n1, n2))

            self.edges.append(Edge(start=n1, end=n2, cost=cost))
            if both_ends:
                self.edges.append(Edge(start=n2, end=n1, cost=cost))

        @property
        def neighbours(self):
            neighbours = {vertex: set() for vertex in self.vertices}
            for edge in self.edges:
                neighbours[edge.start].add((edge.end, edge.cost))

            return neighbours

        def dijkstra(self, source, dest):
            assert source in self.vertices, 'Such source node doesn\'t exist'
            distances = {vertex: inf for vertex in self.vertices}
            previous_vertices = {
                vertex: None for vertex in self.vertices
            }
            distances[source] = 0
            vertices = self.vertices.copy()

            while vertices:
                current_vertex = min(
                    vertices, key=lambda vertex: distances[vertex])
                vertices.remove(current_vertex)
                if distances[current_vertex] == inf:
                    break
                for neighbour, cost in self.neighbours[current_vertex]:
                    alternative_route = distances[current_vertex] + cost
                    if alternative_route < distances[neighbour]:
                        distances[neighbour] = alternative_route
                        previous_vertices[neighbour] = current_vertex
            path, current_vertex = deque(), dest
            while previous_vertices[current_vertex] is not None:
                path.appendleft(current_vertex)
                current_vertex = previous_vertices[current_vertex]
            if path:
                path.appendleft(current_vertex)
            return path
    # Adding path to find shortest one

    def add_path():
        start_point = start_point_text.get()
        end_point = end_point_text.get()
    # Getting edges data

    def get_data():
        start_edge = start_text.get()
        end_edge = end_text.get()
        pondere = pondere_text.get()
        print("Start Edge", start_edge)
        print("End Edge", end_edge)
        print("Pondere", pondere)
        list_edge = (start_edge, end_edge, pondere)
        edge_pondere.append(list_edge)
        listbox.insert(END, list_edge)
        start_entry.delete(first=0, last=100)
        end_entry.delete(first=0, last=100)
        pondere_entry.delete(first=0, last=100)

    def calculate():
        start_point = start_point_text.get()
        end_point = end_point_text.get()
        test_graph = Graph(edge_pondere)
        deque_result = test_graph.dijkstra(start_point, end_point)
        graph_result = []
        while deque_result:
            graph_result.append(deque_result[0])
            deque_result.popleft()
        graph_result = "➜".join(repr(data) for data in graph_result)
        edge_pondere_result = ",".join(repr(e) for e in edge_pondere)
        output = "Edges Added are : %s \n The path is : %s" % (
            edge_pondere_result, graph_result)
        tkinter.messagebox.showinfo(
            "Airline Scheduler Calculation", output)
        print(test_graph.dijkstra(start_point, end_point))

    def clear():
        listbox.delete(0, END)
        edge_pondere.clear()
        start_point_entry.delete(first=0, last=100)
        end_point_entry.delete(first=0, last=100)
        start_entry.delete(first=0, last=100)
        end_entry.delete(first=0, last=100)
        pondere_entry.delete(first=0, last=100)
        print("paths cleared")
        output = "Data Cleared"
        tkinter.messagebox.showinfo(
            "Airline Scheduler Clear", output)

    def show_paths():
        if len(edge_pondere) == 0:
            print(len(edge_pondere))
            output = "No Paths added yet"
        else:
            output = edge_pondere
        tkinter.messagebox.showinfo(
            "Airline Scheduler Paths", output)

    def delete_one_list_elem():
        delete_id = int(delete_element.get()-1)
        edge_pondere.pop(delete_id)
        listbox.delete(delete_id, delete_id)

    edge_pondere = []
    # Create Window Object
    root = Tk()

    # Content
    # Start Point
    start_label = tkinter.Label(root, text="Start Graph Point", bg='white')
    start_point_text = StringVar()
    start_point_entry = Entry(textvariable=start_point_text, width=19)
    # End point
    end_label = tkinter.Label(root, text="End Graph Point", bg='white')
    end_point_text = StringVar()
    end_point_entry = Entry(textvariable=end_point_text, width=19)
    add_path_button = tkinter.Button(text="Add Route", command=add_path, fg="white",
                                     bg="#009900", font=14, borderwidth=0, width=12, height=1)
    show_paths_button = tkinter.Button(text="Show Paths", command=show_paths,
                                       fg="white", bg="#a6a6a6", font=14, borderwidth=0, width=12, height=1)
    # Edge add
    start_path_label = tkinter.Label(
        root, text="Start Edge", bg='white')
    start_text = StringVar()
    start_entry = Entry(textvariable=start_text, width=19)
    end_path_label = tkinter.Label(
        root, text="End Edge", bg='white')
    end_text = StringVar()
    end_entry = Entry(textvariable=end_text, width=19)
    pondere_text = DoubleVar()
    pondere_entry = Entry(textvariable=pondere_text, width=19)
    pondere_entry.delete(first=0, last=100)
    pondere_path_label = tkinter.Label(
        root, text="Ponderea", bg='white')
    add_button = tkinter.Button(
        text="Add Path", command=get_data, fg="white", bg="#009900", font=14, borderwidth=0, width=12, height=1)
    # Execute and Clear buttons
    calculate_button = tkinter.Button(
        text="Calculate", command=calculate, fg="white", bg="#009900", font=14, borderwidth=0, width=12, height=1)
    clear_button = tkinter.Button(
        text="Clear", command=clear, fg="white", bg="#e60000", font=14, borderwidth=0, width=12, height=1)
    listbox = tkinter.Listbox(
        root, bd=0.5, relief="solid", highlightthickness=0, justify='center')
    delete_element_label = tkinter.Label(
        root, text="Delete Edge(id)", bg='white')
    delete_element = DoubleVar()
    delete_element_entry = Entry(textvariable=delete_element, width=19)
    delete_element_entry.delete(first=0, last=100)
    clear_list = tkinter.Button(
        text="Clear List Element", command=delete_one_list_elem, fg="white", bg="#e60000", font=14, borderwidth=0, width=15, height=1)

    # style&positioning
    # Route Style
    start_label.place(relx=.3, rely=.1, anchor="c")
    start_point_entry.place(relx=.3, rely=.15, anchor="c")
    end_label.place(relx=.3, rely=.2, anchor="c")
    end_point_entry.place(relx=.3, rely=.25, anchor="c")
    add_path_button.place(relx=.3, rely=.35, anchor="c")
    show_paths_button.place(relx=.3, rely=.45, anchor="c")
    # Path Style
    start_path_label.place(relx=.7, rely=.1, anchor="c")
    start_entry.place(relx=.7, rely=.15, anchor="c")
    end_path_label.place(relx=.7, rely=.2, anchor="c")
    end_entry.place(relx=.7, rely=.25, anchor="c")
    pondere_path_label.place(relx=.7, rely=.3, anchor="c")
    pondere_entry.place(relx=.7, rely=.35, anchor="c")
    add_button.place(relx=.7, rely=.45, anchor="c")
    # button style
    calculate_button.place(relx=.5, rely=.65, anchor="c")
    clear_button.place(relx=.5, rely=.75, anchor="c")
    listbox.place(relx=.5, rely=.23, anchor="c")
    delete_element_label.place(relx=.5, rely=.4, anchor="c")
    delete_element_entry.place(relx=.5, rely=.45, anchor="c")
    clear_list.place(relx=.5, rely=.55, anchor="c")
    # root parameters
    style = Style()
    root.configure(background='white')
    style.configure('TButton', font=(12),
                    borderwidth='2', foreground='gray', background='gray')
    root.title('Airline Scheduler')
    root.wm_iconbitmap('icon.ico')
    root.geometry('900x600')
    root.mainloop()
