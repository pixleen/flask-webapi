# Utility function to convert Neo4j Node objects to a Python dictionary

def node_to_dict(node):
    """Convert a Neo4j Node to a Python dictionary."""
    return {key: value for key, value in node.items()}

def node_to_dict_2(node):
    return dict(node)