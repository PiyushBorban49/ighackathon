from manim import *


class ExplanationScene(Scene):
    def construct(self):
        # 1. Title and Definition
        title = Text("Undirected Graphs: G = (V, E)", font_size=40, weight=BOLD).to_edge(UP)
        self.play(Write(title))
        self.wait(0.5)

        # 2. Define V (Nodes) and visualize them
        v_title = Text("V = Nodes (Vertices)", font_size=30).shift(LEFT * 4 + UP * 1)
        self.play(Write(v_title))

        # Create 3 nodes
        node_1 = Circle(radius=0.2, color=BLUE, fill_opacity=1).shift(RIGHT * 1)
        node_2 = Circle(radius=0.2, color=BLUE, fill_opacity=1).shift(RIGHT * 3)
        node_3 = Circle(radius=0.2, color=BLUE, fill_opacity=1).shift(RIGHT * 2 + DOWN * 1.5)
        nodes = VGroup(node_1, node_2, node_3)

        self.play(Create(nodes), run_time=1)

        # 3. Define E (Edges) and visualize connections
        e_title = Text("E = Edges (Arcs)", font_size=30).shift(LEFT * 4 + DOWN * 2)
        self.play(Write(e_title))

        # Create edges
        e1 = Line(node_1.get_center(), node_2.get_center(), color=RED)
        e2 = Line(node_1.get_center(), node_3.get_center(), color=RED)
        e3 = Line(node_2.get_center(), node_3.get_center(), color=RED)
        edges = VGroup(e1, e2, e3)

        self.play(Create(edges), run_time=1)

        # 4. Size Parameters
        n_text = Text("n = |V| (Number of Nodes = 3)", font_size=25).to_edge(DR).shift(LEFT * 1.5)
        m_text = Text("m = |E| (Number of Edges = 3)", font_size=25).next_to(n_text, UP, buff=0.5)

        self.play(FadeIn(n_text, shift=UP), FadeIn(m_text, shift=UP))
        self.wait(2)