""" Python Class
    Clase que da solucion a CSC hallando el menor k que
    cumpla con el t fijado en el problema. Este k se encuentra
    mediante una Busqueda Binaria desde 1 hasta |V|, tomando el
    menor valor que satisfaga el umbral t. Para saber si
    con un determinado k se puede satisfacer un umbral t, usaremos
    algun metodo de TSC. Dicho metodo no estara implementado en esta
    clase, por lo que esta sera solo una clase abstracta que
    brinda una solucion a CSC si se le proporciona una de TSC.
"""

from graph_coloring import SpectrumGraphColoring


class CSCBinarySearch(SpectrumGraphColoring):

    def ChromaticSpectrumColoring(self, t):
        """Determina el menor k que satisface con el umbral t
        mediante una Busqueda Binaria entre 1 y |V|.

        Args:
            t (float): Umbral de interferencia permitido.

        Returns:
            int, dict: Numero cromatico de t-interferencia, coloracion
                del grafo que cumple las restricciones.
        """            
        n_vertices = len(self.vertices())
        c = {v:None for v in range(0, n_vertices)}
        k = n_vertices
        L = 1
        R = n_vertices
        while L <= R:
            k0 = (L + R)//2
            t0, c0 = self.ThresholdSpectrumColoring(k0)
            if t0 <= t:
                c = c0
                k = k0
                R = k0 - 1
            else:
                L = k0 + 1
        return k, c