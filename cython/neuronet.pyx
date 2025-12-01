# distutils: language = c++

from neuronet cimport GrafoDisperso
from libcpp.string cimport string
from libcpp.vector cimport vector
from libcpp.utility cimport pair

cdef class NeuroNet:
    cdef GrafoDisperso* c_grafo  # Pointer to C++ instance

    def __cinit__(self):
        self.c_grafo = new GrafoDisperso()

    def __dealloc__(self):
        del self.c_grafo

    def load_data(self, str filename):
        """Loads data from a file into the CSR structure."""
        cdef string c_filename = filename.encode('utf-8')
        self.c_grafo.cargarDatos(c_filename)

    def bfs(self, int start_node, int max_depth):
        """Runs BFS and returns a list of edges (u, v)."""
        print(f"[Cython] Solicitud recibida: BFS desde Nodo {start_node}, Profundidad {max_depth}.")
        cdef vector[pair[int, int]] result = self.c_grafo.bfs(start_node, max_depth)
        print("[Cython] Retornando lista de adyacencia local a Python.")
        return result  # Cython automatically converts vector<pair> to list of tuples

    def get_max_degree_node(self):
        """Returns the node ID with the highest out-degree."""
        return self.c_grafo.obtenerNodoMayorGrado()

    def get_neighbors(self, int node):
        """Returns neighbors of a node."""
        return self.c_grafo.getVecinos(node)

    def get_num_nodes(self):
        return self.c_grafo.getNumNodos()

    def get_num_edges(self):
        return self.c_grafo.getNumAristas()
