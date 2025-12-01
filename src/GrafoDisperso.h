#ifndef GRAFODISPERSO_H
#define GRAFODISPERSO_H

#include "GrafoBase.h"
#include <iostream>
#include <string>
#include <vector>

class GrafoDisperso : public GrafoBase {
private:
  int numNodos;
  int numAristas;

  // CSR format
  // values is implicit (all 1 for unweighted), but we can store it if needed.
  // For this problem, adjacency is binary, so we might just need col_indices
  // and row_ptr. However, the prompt mentions "values, indices de columnas,
  // punteros de fila". We will include values to strictly follow CSR
  // definition, though they will be 1.
  std::vector<int> values;
  std::vector<int> col_indices;
  std::vector<int> row_ptr;

public:
  GrafoDisperso();
  ~GrafoDisperso();

  void cargarDatos(const std::string &archivo) override;
  std::vector<std::pair<int, int>> bfs(int nodoInicio,
                                       int profundidadMax) override;
  int obtenerNodoMayorGrado() override;
  std::vector<int> getVecinos(int nodo) override;
  int getNumNodos() override;
  int getNumAristas() override;
};

#endif // GRAFODISPERSO_H
