En esta carpeta encontramos la implementacion usada para dar solucion a los problemas de grafos con espectros de colores TSC y CSC.
Veremos a continuacion, una breve explicacion de cada fichero.


graph2.py
-----------
En este fichero se implementa la clase para representar los grafos.

graph_coloring.py
-----------
En este fichero se implementa una clase abstracta para los problemas TSC y CSC, que cuenta con
algunos metodos y campos necesarios.

secuencial_gc.py
-----------
En este fichero se implementa una clase abstracta para los algoritmos de coloracion secuencial
en grafos.

bfs.py
-----------
En este fichero se implementa una solucion a TSC y CSC mediante un algoritmo de coloracion secuencial
basado en BFS.

degree_bfs.py
-----------
En este fichero se implementa una solucion a TSC y CSC mediante un algoritmo de coloracion secuencial
basado en BFS con una cola con prioridad sobre los grados de los vertices.

dsatur.py
-----------
En este fichero se implementa una solucion a TSC y CSC mediante un algoritmo de coloracion secuencial
basado en DSATUR.

randomc.py
-----------
En este fichero se implementa una solucion a TSC y CSC mediante un algoritmo de coloracion secuencial
aleatorio.

swo.py
-----------
En este fichero se implementa una solucion a TSC y CSC mediante un algoritmo de coloracion secuencial
basado en el algoritmo de optimizacion SWO.

vertex_merge.py
-----------
En este fichero se implementa una solucion a TSC y CSC mediante un algoritmo de coloracion secuencial
que toma el par de vertices no adyacentes de mayor grado en cada paso.

simple_search.py
-----------
En este fichero se implementa un algoritmo de optimizacion para mejorar una solucion de TSC obtenida en
un computo previo.

improved_methods.py
-----------
En este fichero se implementa la combinacion de cada algoritmo de coloracion secuencial con el algoritmo
de optimizacion Busqueda Simple.

csc_binarysearch.py
-----------
En este fichero se implementa un metodo para hallar la solucion de CSC mediante una Busqueda Binaria en
las soluciones de TSC.

dimacs.py
-----------
En este fichero se implementa un metodo para crear grafos a partir de ficheros que cumplan la representacion
DIMACS.

gcd.py
-----------
En este fichero se implementa un metodo para hallar el maximo comun divisor de una lista de numeros no enteros.

iterative_quicksort.py
-----------
Implementacion iterativa de QuickSort.

tester.py
-----------
En este fichero se implementan las herramientas para experimentar con los problemas TSC y CSC, asi como calcular
las estadisticas de los resultados.

weight_functions.py
-----------
En este fichero se implementan las funciones usadas para general la matriz de interferencias entre los colores.
