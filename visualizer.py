from __future__ import annotations

import math
import random
from dataclasses import dataclass
from typing import Sequence

import matplotlib.colors as mcolors
import matplotlib.patches as patches
import matplotlib.pyplot as plt

random.seed(8252026)

ColorLike = str | tuple[float, ...] | list[float]


def _normalize_color(color: ColorLike | None, default: ColorLike | None = None) -> tuple[float, ...]:
    """Accept hex strings or RGB(A) tuples/lists and normalize to an RGBA tuple."""
    if color is None:
        color = default
    if color is None:
        return (0.92, 0.92, 0.92, 1.0)
    if isinstance(color, str):
        return mcolors.to_rgba(color)

    if isinstance(color, Sequence) and not isinstance(color, (str, bytes)):
        values = list(color)
        if len(values) not in (3, 4):
            raise ValueError(f"Expected RGB or RGBA values, got {len(values)} values")
        if any(isinstance(value, str) for value in values):
            raise ValueError("RGB colors must be numeric tuples/lists")

        normalized: list[float] = []
        for index, value in enumerate(values):
            numeric = float(value)
            if index < 3 and numeric > 1.0:
                numeric = numeric / 255.0
            normalized.append(max(0.0, min(1.0, numeric)))

        if len(normalized) == 3:
            normalized.append(1.0)
        return tuple(normalized)

    raise TypeError(f"Unsupported color type: {type(color)!r}")


def _blend_color(color_a: ColorLike | None, color_b: ColorLike | None, ratio: float = 0.5) -> tuple[float, ...]:
    """Blend two colors and return an RGBA tuple."""
    a = _normalize_color(color_a, (0.0, 0.0, 0.0))
    b = _normalize_color(color_b, (1.0, 1.0, 1.0))
    t = max(0.0, min(1.0, ratio))
    blended = tuple((1 - t) * a[index] + t * b[index] for index in range(4))
    return tuple(max(0.0, min(1.0, value)) for value in blended)


@dataclass
class Connection:
    source: "Node"
    target: "Node"
    name: str = ""
    weight: float = 1.0
    color: tuple[float, ...] | None = None


class Node:
    def __init__(self, layer: "Layer", name: str = "Unnamed Node", color: ColorLike | None = None):
        self.layer = layer
        self.name = name
        self.color = _normalize_color(color, (0.95, 0.95, 0.95))
        self.x = 0.0
        self.y = 0.0
        self.width = layer.visualizer.node_width
        self.height = layer.visualizer.node_height
        self.connections: list[Connection] = []

    @property
    def center(self) -> tuple[float, float]:
        return (self.x + self.width / 2, self.y + self.height / 2)

    def connect_to(self, node: "Node", name: str = "", weight: float = 1.0, color: ColorLike | None = None) -> Connection:
        connection = Connection(source=self, target=node, name=name, weight=weight, color=_normalize_color(color))
        self.connections.append(connection)
        self.layer.visualizer.connections.append(connection)
        return connection


class Layer:
    def __init__(self, visualizer: "LayerVisualizer", name: str = "Unnamed Layer", color: ColorLike | None = None):
        self.visualizer = visualizer
        self.name = name
        if color is None:
            palette_color = visualizer.palette(len(visualizer.layers) % visualizer.palette.N)
            color = (palette_color[0], palette_color[1], palette_color[2])
        self.color = _normalize_color(color)
        self.nodes: list[Node] = []
        self.x = 0.0
        self.y = 0.0
        self.width = visualizer.layer_width
        self.height = visualizer.layer_min_height

    def add_node(self, name: str = "Unnamed Node", color: ColorLike | None = None) -> Node:
        if color is None:
            color = _blend_color(self.color, (1.0, 1.0, 1.0), 0.7)
        node = Node(layer=self, name=name, color=color)
        self.nodes.append(node)
        return node

    def get_node(self, name: str) -> Node:
        for node in self.nodes:
            if node.name == name:
                return node
        raise ValueError(f"Node by name {name} does not exist in layer {self.name}")


class LayerVisualizer:
    def __init__(self):
        self.layers: list[Layer] = []
        self.connections: list[Connection] = []

        self.layer_width = 3.8
        self.layer_horizontal_spacing = 2.8
        self.layer_padding_y = 0.8
        self.layer_min_height = 3.0
        self.node_width = 3.0
        self.node_height = 1.0
        self.node_vertical_spacing = 0.55

        self.fig, self.ax = plt.subplots(figsize=(12, 7))
        self.palette = plt.cm.Set2

    def add_layer(self, name: str = "Unnamed Layer", color: ColorLike | None = None) -> Layer:
        layer = Layer(self, name=name, color=color)
        self.layers.append(layer)
        return layer

    def _layout(self) -> None:
        for layer_index, layer in enumerate(self.layers):
            layer.x = layer_index * (self.layer_width + self.layer_horizontal_spacing)

            node_block_height = 0.0
            if layer.nodes:
                node_block_height = len(layer.nodes) * self.node_height + (len(layer.nodes) - 1) * self.node_vertical_spacing

            layer.height = max(self.layer_min_height, node_block_height + 2 * self.layer_padding_y)
            layer.y = -layer.height / 2

            node_start_y = -node_block_height / 2
            for node_index, node in enumerate(layer.nodes):
                node.x = layer.x + (layer.width - node.width) / 2
                node.y = node_start_y + node_index * (self.node_height + self.node_vertical_spacing)

    def _draw_layers(self) -> None:
        for layer in self.layers:
            layer_box = patches.FancyBboxPatch(
                (layer.x, layer.y),
                layer.width,
                layer.height,
                boxstyle="round,pad=0.04,rounding_size=0.12",
                linewidth=2,
                edgecolor=layer.color,
                facecolor=_blend_color(layer.color, (1.0, 1.0, 1.0), 0.88),
                alpha=0.95,
                zorder=1,
            )
            self.ax.add_patch(layer_box)
            self.ax.annotate(
                layer.name,
                (layer.x + layer.width / 2, layer.y + layer.height + 0.25),
                ha="center",
                va="bottom",
                fontsize=11,
                fontweight="bold",
                color=layer.color,
                zorder=6,
            )

    def _draw_nodes(self) -> None:
        for layer in self.layers:
            for node in layer.nodes:
                node_box = patches.FancyBboxPatch(
                    (node.x, node.y),
                    node.width,
                    node.height,
                    boxstyle="round,pad=0.02,rounding_size=0.08",
                    linewidth=1.2,
                    edgecolor=_blend_color(node.color, (0.0, 0.0, 0.0), 0.25),
                    facecolor=node.color,
                    zorder=3,
                )
                self.ax.add_patch(node_box)
                self.ax.annotate(
                    node.name,
                    node.center,
                    ha="center",
                    va="center",
                    fontsize=9,
                    zorder=5,
                )

    def _draw_connections(self) -> None:
        grouped_connections: dict[tuple[int, int], list[Connection]] = {}
        for connection in self.connections:
            key = (id(connection.source), id(connection.target))
            grouped_connections.setdefault(key, []).append(connection)

        for group in grouped_connections.values():
            lane_count = len(group)
            for lane_index, connection in enumerate(group):
                src_x, src_y = connection.source.center
                dst_x, dst_y = connection.target.center

                src_x = src_x + connection.source.width / 2
                dst_x = dst_x - connection.target.width / 2

                dx = dst_x - src_x
                dy = dst_y - src_y
                length = math.hypot(dx, dy) or 1.0
                perp_x = -dy / length
                perp_y = dx / length

                lane_offset = (lane_index - (lane_count - 1) / 2) * 0.18
                start_x = src_x + perp_x * lane_offset
                start_y = src_y + perp_y * lane_offset
                end_x = dst_x + perp_x * lane_offset
                end_y = dst_y + perp_y * lane_offset
                curve_radius = lane_offset * 0.18

                line_width = max(0.8, min(4.0, abs(connection.weight) * 1.2))
                line_color = connection.color or _blend_color(connection.source.layer.color, connection.target.layer.color, 0.5)

                arrow = patches.FancyArrowPatch(
                    (start_x, start_y),
                    (end_x, end_y),
                    arrowstyle="-|>",
                    mutation_scale=12,
                    linewidth=line_width,
                    color=line_color,
                    alpha=0.88,
                    connectionstyle=f"arc3,rad={curve_radius:.2f}",
                    zorder=2,
                )
                self.ax.add_patch(arrow)

                if connection.name:
                    mid_x = (start_x + end_x) / 2
                    mid_y = (start_y + end_y) / 2 + 0.15
                    self.ax.annotate(
                        f"{connection.name} ({connection.weight:.2f})",
                        (mid_x, mid_y),
                        fontsize=7,
                        color=line_color,
                        ha="center",
                        va="bottom",
                        zorder=7,
                    )

    def draw(self) -> None:
        self._layout()
        self.ax.clear()

        self._draw_layers()
        self._draw_connections()
        self._draw_nodes()

        if self.layers:
            min_x = self.layers[0].x - 1.0
            max_x = self.layers[-1].x + self.layers[-1].width + 1.0
            max_h = max(layer.height for layer in self.layers)
            y_margin = max(1.2, max_h * 0.12)
            self.ax.set_xlim(min_x, max_x)
            self.ax.set_ylim(-(max_h / 2 + y_margin), max_h / 2 + y_margin + 1.0)

        self.ax.set_aspect("equal", adjustable="box")
        self.ax.axis("off")

    def show(self) -> None:
        self.draw()
        plt.tight_layout()
        plt.show()


if __name__ == "__main__":
    vis = LayerVisualizer()

    layer1 = vis.add_layer("Input", (90, 130, 220))
    i1 = layer1.add_node("x1", (220, 230, 245))
    i2 = layer1.add_node("x2", (220, 230, 245))
    i3 = layer1.add_node("x3", (220, 230, 245))

    layer2 = vis.add_layer("Hidden A", (140, 90, 180))
    h1 = layer2.add_node("h1", (240, 220, 250))
    h2 = layer2.add_node("h2", (240, 220, 250))
    h3 = layer2.add_node("h3", (240, 220, 250))

    layer3 = vis.add_layer("Hidden B", (90, 170, 95))
    b1 = layer3.add_node("b1", (230, 245, 230))
    b2 = layer3.add_node("b2", (230, 245, 230))

    layer4 = vis.add_layer("Output", (220, 110, 70))
    o1 = layer4.add_node("y", (250, 235, 220))

    for src in [i1, i2, i3]:
        for dst in [h1, h2, h3]:
            src.connect_to(dst, "w", random.uniform(0.5, 2.0), (230, 80, 90))

    for src in [h1, h2, h3]:
        for dst in [b1, b2]:
            src.connect_to(dst, "v", random.uniform(0.6, 1.8), (90, 120, 200))

    b1.connect_to(o1, "o1", 1.4, (220, 140, 70))
    b2.connect_to(o1, "o2", 0.9, (140, 180, 220))

    vis.show()
