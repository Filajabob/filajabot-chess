class NodeType:
    @staticmethod
    def get_node_type(score, alpha, beta, turn):
        if alpha < score < beta:
            return NodeType.PVNode

        if turn:
            if score >= beta:
                return NodeType.CutNode
            elif score <= alpha:
                return NodeType.AllNode
        else:
            if score <= alpha:
                return NodeType.CutNode
            elif score >= beta:
                return NodeType.CutNode

    class PVNode:
        """
        PV-nodes (Knuth's Type 1) are nodes that have a score that ends up being inside the window. So if the
        bounds passed are [a,b], with the score returned s, a<s<b. These nodes have all moves searched, and the value
        returned is exact (i.e., not a bound), which propagates up to the root along with a principal variation.
        """

    class CutNode:
        """
        Cut-nodes (Knuth's Type 2), otherwise known as fail-high nodes, are nodes in which a beta-cutoff was
        performed. So with bounds [a,b], s>=b. A minimum of one move at a Cut-node needs to be searched. The score
        returned is a lower bound (might be greater) on the exact score of the node
        """

    class AllNode:
        """
        All-nodes (Knuth's Type 3), otherwise known as fail-low nodes, are nodes in which no move's score exceeded
        alpha. With bounds [a,b], s<=a. Every move at an All-node is searched, and the score returned is an upper
        bound, the exact score might be less.
        """
