#include "GrafoDisperso.h"
#include <algorithm>
#include <chrono> // Added for std::chrono
#include <chrono>
#include <fstream>
#include <iostream>
#include <limits>
#include <queue>
#include <sstream>

GrafoDisperso::GrafoDisperso() : numNodos(0), numAristas(0) {
  std::cout << "[C++ Core] Inicializando GrafoDisperso..." << std::endl;
}

GrafoDisperso::~GrafoDisperso() {}

void GrafoDisperso::cargarDatos(const std::string &archivo) {
  std::cout << "[C++ Core] Cargando dataset '" << archivo << "'..."
            << std::endl;

  std::ifstream infile(archivo);
  if (!infile.is_open()) {
    std::cerr << "Error al abrir el archivo: " << archivo << std::endl;
    return;
  }

  // Pass 1: Determine max node ID and count degrees
  int max_id = 0;
  int edges_count = 0;
  std::string line;

  // We need to store degrees temporarily.
  // Since we don't know max_id yet, we might need a dynamic approach or just a
  // map? But map is slow. Let's assume a reasonable initial size or resize
  // dynamically. Actually, for a massive graph, we might want to just scan for
  // max_id first? Or we can use a vector and resize if we see a larger ID.
  std::vector<int> degrees;
  degrees.reserve(1000000); // Reserve for 1M nodes

  while (std::getline(infile, line)) {
    if (line.empty() || line[0] == '#')
      continue;
    std::stringstream ss(line);
    int u, v;
    if (ss >> u >> v) {
      if (u > max_id)
        max_id = u;
      if (v > max_id)
        max_id = v;

      if (u >= degrees.size()) {
        degrees.resize(u + 10000, 0); // Grow in chunks
      }
      degrees[u]++;
      edges_count++;
    }
  }

  // Resize degrees to actual max_id + 1
  if (max_id >= degrees.size()) {
    degrees.resize(max_id + 1, 0);
  } else {
    // Optional: shrink to fit, but not strictly necessary
  }

  numNodos = max_id + 1;
  numAristas = edges_count;

  // Build row_ptr
  row_ptr.resize(numNodos + 2, 0);
  row_ptr[0] = 0;
  for (int i = 0; i < numNodos; ++i) {
    row_ptr[i + 1] = row_ptr[i] + degrees[i];
  }

  // Allocate col_indices
  col_indices.resize(numAristas);
  // values.resize(numAristas, 1); // Not strictly needed for logic, but for CSR
  // completeness

  // Pass 2: Fill col_indices
  // We need to reset file stream
  infile.clear();
  infile.seekg(0, std::ios::beg);

  // We need a tracker for current insertion position for each row
  std::vector<int> current_pos = row_ptr; // Copy starting positions

  while (std::getline(infile, line)) {
    if (line.empty() || line[0] == '#')
      continue;
    std::stringstream ss(line);
    int u, v;
    if (ss >> u >> v) {
      int pos = current_pos[u];
      col_indices[pos] = v;
      current_pos[u]++;
    }
  }

  infile.close();
  std::cout << "[C++ Core] Carga completa. Nodos: " << numNodos
            << " | Aristas: " << numAristas << std::endl;
  // Estimate memory: 3 vectors of ints.
  // row_ptr: numNodos+2, col_indices: numAristas, values: numAristas (if used,
  // currently empty but let's assume overhead) Actually values is empty in my
  // code, but let's estimate based on what we have.
  long long mem_bytes = (numNodos + 2) * sizeof(int) + numAristas * sizeof(int);
  double mem_mb = mem_bytes / (1024.0 * 1024.0);
  std::cout << "[C++ Core] Estructura CSR construida. Memoria estimada: "
            << mem_mb << " MB." << std::endl;
}

std::vector<std::pair<int, int>> GrafoDisperso::bfs(int nodoInicio,
                                                    int profundidadMax) {
  std::cout << "[C++ Core] Ejecutando BFS nativo..." << std::endl;
  auto start_time = std::chrono::high_resolution_clock::now();

  std::vector<std::pair<int, int>> result_edges;
  if (nodoInicio < 0 || nodoInicio >= numNodos)
    return result_edges;

  std::vector<int> dist(numNodos, -1);
  std::queue<int> q;

  dist[nodoInicio] = 0;
  q.push(nodoInicio);

  while (!q.empty()) {
    int u = q.front();
    q.pop();

    if (dist[u] >= profundidadMax)
      continue;

    int start = row_ptr[u];
    int end = row_ptr[u + 1];

    for (int i = start; i < end; ++i) {
      int v = col_indices[i];
      // We record the edge even if v is visited, to show connections?
      // Usually BFS tree only records edges to unvisited nodes.
      // But for visualization "subgraph", we might want all edges between
      // visited nodes? The prompt says "retorna la lista de nodos visitados y
      // sus aristas." Let's return edges that are part of the BFS traversal
      // (discovery edges).

      if (dist[v] == -1) {
        dist[v] = dist[u] + 1;
        q.push(v);
        result_edges.push_back({u, v});
      } else {
        // If v is already visited and within depth, we might want to show this
        // edge too? For a "star" graph visualization, usually we just want the
        // tree. Let's stick to the tree edges for clarity, or maybe edges where
        // dist[v] == dist[u] + 1? Let's just return discovery edges for now.
      }
    }
  }
  auto end_time = std::chrono::high_resolution_clock::now();
  std::chrono::duration<double, std::milli> elapsed = end_time - start_time;

  // Count unique nodes found? Or just edges?
  // The log says "Nodos encontrados".
  // We can count non -1 in dist?
  int nodes_found = 0;
  for (int d : dist) {
    if (d != -1)
      nodes_found++;
  }

  std::cout << "[C++ Core] Nodos encontrados: " << nodes_found
            << ". Tiempo ejecución: " << elapsed.count() << "ms." << std::endl;
  return result_edges;
}

int GrafoDisperso::obtenerNodoMayorGrado() {
  int max_degree = -1;
  int max_node = -1;

  for (int i = 0; i < numNodos; ++i) {
    int degree = row_ptr[i + 1] - row_ptr[i];
    if (degree > max_degree) {
      max_degree = degree;
      max_node = i;
    }
  }
  return max_node;
}

std::vector<int> GrafoDisperso::getVecinos(int nodo) {
  std::vector<int> vecinos;
  if (nodo < 0 || nodo >= numNodos)
    return vecinos;

  int start = row_ptr[nodo];
  int end = row_ptr[nodo + 1];

  for (int i = start; i < end; ++i) {
    vecinos.push_back(col_indices[i]);
  }
  return vecinos;
}

int GrafoDisperso::getNumNodos() { return numNodos; }

int GrafoDisperso::getNumAristas() { return numAristas; }
