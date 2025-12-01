from libcpp.vector cimport vector
from libcpp.utility cimport pair
from libcpp.string cimport string

cdef extern from "../src/GrafoBase.h":
    cdef cppclass GrafoBase:
        pass

cdef extern from "../src/GrafoDisperso.h":
    cdef cppclass GrafoDisperso(GrafoBase):
        GrafoDisperso() except +
        void cargarDatos(string archivo)
        vector[pair[int, int]] bfs(int nodoInicio, int profundidadMax)
        int obtenerNodoMayorGrado()
        vector[int] getVecinos(int nodo)
        int getNumNodos()
        int getNumAristas()
