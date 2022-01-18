import overpy
from road_network.base_classes import *
from road_network.api_buffer import ApiBuffer

QUERY_FSTR = """  way{}["highway"];
            (._;>;);
            out body; """


def make_query(bbox: BBox) -> dict[int, Node]:
    query = QUERY_FSTR.format(str(bbox))
    api = overpy.Overpass()
    query_res = api.query(query)
    # api_buff = ApiBuffer()
    # api_buff.make_query(query)
    # query_res = api_buff.get_last_query()
    nodes: dict[int, Node] = {}
    node_to_way: dict[int, list[int]] = {}
    for way in query_res.get_ways():
        for node in way.get_nodes():
            node_to_way.setdefault(node.id, list())
            node_to_way[node.id].append(way.id)
    for way in query_res.get_ways():
        cur_path = Path()
        last_node = None
        for i, node in enumerate(way.get_nodes()):
            cur_path.points.append(Point(float(node.lon), float(node.lat)))
            if len(node_to_way[node.id]) > 1 or i == 0 or i == len(way.get_nodes()) - 1:
                cur_node = nodes.setdefault(node.id, Node(node))
                if last_node is not None:
                    last_node.neighbors.append(Edge(cur_node.id, cur_path))
                    cur_node.neighbors.append(Edge(last_node.id, Path(cur_path.points[::-1])))
                    cur_path = Path([cur_node])
                last_node = cur_node
    to_remove = [node_id for node_id, node in nodes.items() if not bbox.is_inside(node)]
    for node_id in to_remove:
        del nodes[node_id]
    return nodes
