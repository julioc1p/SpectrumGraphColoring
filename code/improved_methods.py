from code.graph2 import Graph
from code.secuencial_gc import SecuencialGraphColoring
# soluciones base
from code.dsatur import DSATURGraphColoring
from code.bfs import BFSGraphColoring
from code.degree_bfs import DegreeBFSGraphColoring
from code.vertex_merge import VertexMergeGraphColoring
from code.swo import SWOGraphColoring
# algoritmos de optimizacion
from code.simple_search import SimpleSearch


class DSATURPlusSS(DSATURGraphColoring, SimpleSearch):

    def _update_values(self, vertex, color, semi_coloring, aupdate=False, update_color=False):
        super()._update_values(vertex, color, semi_coloring, True, update_color)

    def ThresholdSpectrumColoring(self, k):
        _, coloring = super().ThresholdSpectrumColoring(k)
        return self.simple_search(coloring, self._spectrum[:k])

class BFSPlusSS(BFSGraphColoring, SimpleSearch):
    
    def _update_values(self, vertex, color, semi_coloring, aupdate=False, update_color=False):
        super()._update_values(vertex, color, semi_coloring, True, update_color)

    def ThresholdSpectrumColoring(self, k):
        _, coloring = super().ThresholdSpectrumColoring(k)
        return self.simple_search(coloring, self._spectrum[:k])

class DBFSPlusSS(DegreeBFSGraphColoring, SimpleSearch):

    def _update_values(self, vertex, color, semi_coloring, aupdate=False, update_color=False):
        super()._update_values(vertex, color, semi_coloring, True, update_color)

    def ThresholdSpectrumColoring(self, k):
        _, coloring = super().ThresholdSpectrumColoring(k)
        return self.simple_search(coloring, self._spectrum[:k])

class VMPlusSS(VertexMergeGraphColoring, SimpleSearch):

    def _update_values(self, vertex, color, semi_coloring, aupdate=False, update_color=False):
        super()._update_values(vertex, color, semi_coloring, True, update_color)

    def ThresholdSpectrumColoring(self, k):
        _, coloring = super().ThresholdSpectrumColoring(k)
        return self.simple_search(coloring, self._spectrum[:k])

class SWOPlusSS(SWOGraphColoring, SimpleSearch):

    def _update_values(self, vertex, color, semi_coloring, aupdate=False, update_color=False):
        super()._update_values(vertex, color, semi_coloring, True, update_color)

    def ThresholdSpectrumColoring(self, k):
        _, coloring = super().ThresholdSpectrumColoring(k)
        return self.simple_search(coloring, self._spectrum[:k])