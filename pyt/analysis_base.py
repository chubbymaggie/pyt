"""Thos module contains a base class for the analysis component used in PyT."""

class AnalysisBase(object):
    """Base class for fixed point analyses."""

    annotated_cfg_nodes = dict()
    
    def __init__(self, cfg, visitor):
        """Annotate visitor if not None and save visitor."""
        if visitor:
            self.annotate_cfg(cfg, visitor)
        self.visitor = visitor

    def annotate_cfg(self, cfg, visitor):
        """Add the visitor to the cfg nodes."""
        for node in cfg.nodes:
            if node.ast_node:
                _visitor = visitor()
                _visitor.visit(node.ast_node)
                self.annotated_cfg_nodes[node] = _visitor.result


        
    
