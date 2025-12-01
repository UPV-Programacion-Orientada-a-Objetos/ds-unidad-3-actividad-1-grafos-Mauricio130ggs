#ifndef GRAFOBASE_H
#define GRAFOBASE_H

#include <string>
#include <vector>
#include <utility>

class GrafoBase {
public:
    virtual ~GrafoBase() {}
    virtual void cargarDatos(const std::string& archivo) = 0;
    virtual std::vector<std::pair<int, int>> bfs(int nodoInicio, int profundidadMax) = 0;
    virtual int obtenerNodoMayorGrado() = 0;
    virtual std::vector<int> getVecinos(int nodo) = 0;
    virtual int getNumNodos() = 0;
    virtual int getNumAristas() = 0;
};

#endif // GRAFOBASE_H
