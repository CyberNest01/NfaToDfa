import matplotlib.pyplot as plt
from main import NfaToDfa
import networkx as nx
import numpy as np


DATA = NfaToDfa().main()


def my_draw_networkx_edge_labels(
    G,
    pos,
    edge_labels=None,
    label_pos=0.5,
    font_size=10,
    font_color="k",
    font_family="sans-serif",
    font_weight="normal",
    alpha=None,
    bbox=None,
    horizontalalignment="center",
    verticalalignment="center",
    ax=None,
    rotate=True,
    clip_on=True,
    rad=0
):

    if ax is None:
        ax = plt.gca()
    if edge_labels is None:
        labels = {(u, v): d for u, v, d in G.edges(data=True)}
    else:
        labels = edge_labels
    text_items = {}
    for (n1, n2), label in labels.items():
        (x1, y1) = pos[n1]
        (x2, y2) = pos[n2]
        (x, y) = (
            x1 * label_pos + x2 * (1.0 - label_pos),
            y1 * label_pos + y2 * (1.0 - label_pos),
        )
        pos_1 = ax.transData.transform(np.array(pos[n1]))
        pos_2 = ax.transData.transform(np.array(pos[n2]))
        linear_mid = 0.5*pos_1 + 0.5*pos_2
        d_pos = pos_2 - pos_1
        rotation_matrix = np.array([(0,1), (-1,0)])
        ctrl_1 = linear_mid + rad*rotation_matrix@d_pos
        ctrl_mid_1 = 0.5*pos_1 + 0.5*ctrl_1
        ctrl_mid_2 = 0.5*pos_2 + 0.5*ctrl_1
        bezier_mid = 0.5*ctrl_mid_1 + 0.5*ctrl_mid_2
        (x, y) = ax.transData.inverted().transform(bezier_mid)

        if rotate:
            # in degrees
            angle = np.arctan2(y2 - y1, x2 - x1) / (2.0 * np.pi) * 360
            # make label orientation "right-side-up"
            if angle > 90:
                angle -= 180
            if angle < -90:
                angle += 180
            # transform data coordinate angle to screen coordinate angle
            xy = np.array((x, y))
            trans_angle = ax.transData.transform_angles(
                np.array((angle,)), xy.reshape((1, 2))
            )[0]
        else:
            trans_angle = 0.0
        # use default box of white with white border
        if bbox is None:
            bbox = dict(boxstyle="round", ec=(1.0, 1.0, 1.0), fc=(1.0, 1.0, 1.0))
        if not isinstance(label, str):
            label = str(label)  # this makes "1" and 1 labeled the same

        t = ax.text(
            x,
            y,
            label,
            size=font_size,
            color=font_color,
            family=font_family,
            weight=font_weight,
            alpha=alpha,
            horizontalalignment=horizontalalignment,
            verticalalignment=verticalalignment,
            rotation=trans_angle,
            transform=ax.transData,
            bbox=bbox,
            zorder=1,
            clip_on=clip_on,
        )
        text_items[(n1, n2)] = t

    ax.tick_params(
        axis="both",
        which="both",
        bottom=False,
        left=False,
        labelbottom=False,
        labelleft=False,
    )

    return text_items


def create_graph() -> None:
    G = nx.DiGraph()
    edge_list = create_list_for_graph()
    # edge_list = [(1, 2, {'w': 'hosein'}), (2, 1, {'w': 'mmd'}), (2, 3, {'w': 'B'}), (3, 1, {'w': 'C'}),
    #              (3, 4, {'w': 'D1'}), (4, 3, {'w': 'D2'}), (1, 5, {'w': 'E1'}), (5, 1, {'w': 'E2'}),
    #              (3, 5, {'w': 'ali'}), (5, 4, {'w': 'G'}), (4, 4, {'w': 'hosein'}), ('1,2', 1, {'w': 'hosein'})]
    G.add_edges_from(edge_list)
    pos = nx.spring_layout(G, seed=5)
    fig, ax = plt.subplots()
    nx.draw_networkx_nodes(G, pos, ax=ax)
    nx.draw_networkx_labels(G, pos, ax=ax)
    curved_edges = [edge for edge in G.edges() if reversed(edge) in G.edges()]
    straight_edges = list(set(G.edges()) - set(curved_edges))
    nx.draw_networkx_edges(G, pos, ax=ax, edgelist=straight_edges)
    arc_rad = 0.25
    nx.draw_networkx_edges(G, pos, ax=ax, edgelist=curved_edges, connectionstyle=f'arc3, rad = {arc_rad}')
    edge_weights = nx.get_edge_attributes(G, 'w')
    curved_edge_labels = {edge: edge_weights[edge] for edge in curved_edges}
    straight_edge_labels = {edge: edge_weights[edge] for edge in straight_edges}
    my_draw_networkx_edge_labels(G, pos, ax=ax, edge_labels=curved_edge_labels, rotate=False, rad=arc_rad)
    nx.draw_networkx_edge_labels(G, pos, ax=ax, edge_labels=straight_edge_labels, rotate=False)
    options = {"edgecolors": "tab:gray", "node_size": 800, "alpha": 0.4}
    nx.draw_networkx_nodes(G, pos, nodelist=create_list_status_dfa(), node_color="tab:green", **options)
    plt.show()


def create_list_for_graph() -> list:
    edge_list = []
    value = []
    item = []
    for dfa in DATA[0]:
        if dfa.item(0) == '_____main_____':
            continue
        if [dfa.item(0), dfa.item(1), dfa.item(2)] in item:
            continue
        value.append(dfa.item(2))
        for i in DATA[0]:
            if i.item(0) == dfa.item(0) and i.item(1) == dfa.item(1) and i.item(2) != dfa.item(2):
                value.append(i.item(2))
                item.append([i.item(0), i.item(1), i.item(2)])
        value = list(set(value))
        value.sort()
        value = f'{",".join(str(e) for e in value)}'
        edge_list.append((dfa.item(0), dfa.item(1), {'w': value}))
        value = []
    return edge_list


def create_list_status_dfa() -> list:
    status = []
    for data in DATA[1]:
        if data.item(0) == '_____main_____':
            continue
        if data.item(1) == 'True':
            status.append(data.item(0))
    return status


if __name__ == '__main__':
    create_graph()




