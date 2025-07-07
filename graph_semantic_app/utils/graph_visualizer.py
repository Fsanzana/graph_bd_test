from pyvis.network import Network


def visualize_graph(graph_data):
    net = Network(directed=True)
    for node in graph_data.get('nodes', []):
        net.add_node(node['id'], label=node['label'])
    for edge in graph_data.get('edges', []):
        net.add_edge(edge['source'], edge['target'], value=edge.get('weight', 1))
    return net.generate_html()
