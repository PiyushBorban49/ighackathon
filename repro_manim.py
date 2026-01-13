from manim import *

class ExplanationScene(Scene):
    def construct(self):
        # Title
        title = Text("Photosynthesis", font_size=50).to_edge(UP)
        self.play(Write(title))
        self.wait(1)

        # Central plant/leaf representation
        leaf = Rectangle(width=4, height=2.5, color=GREEN_B, fill_opacity=0.8).center()
        leaf_label = Text("Plant Leaf", font_size=24, color=WHITE).move_to(leaf.center())
        self.play(Create(leaf), FadeIn(leaf_label))
        self.wait(0.5)

        # Inputs
        # Sunlight
        sun = Circle(radius=0.6, color=YELLOW, fill_opacity=1).next_to(leaf, UP * 2.5)
        sun_text = Text("Sunlight", font_size=28).next_to(sun, UP)
        arrow_sun = Arrow(sun.get_bottom(), leaf.get_top() + DOWN * 0.5, buff=0.1, color=YELLOW)
        self.play(FadeIn(sun), Write(sun_text), Create(arrow_sun))
        self.wait(0.5)

        # Water
        water_text = Text("Water (H2O)", font_size=28).next_to(leaf, LEFT * 3)
        arrow_water = Arrow(water_text.get_right(), leaf.get_left() + RIGHT * 0.5, buff=0.1, color=BLUE)
        self.play(FadeIn(water_text), Create(arrow_water))
        self.wait(0.5)

        # Carbon Dioxide
        co2_text = Text("Carbon Dioxide (CO2)", font_size=28).next_to(leaf, RIGHT * 3)
        arrow_co2 = Arrow(co2_text.get_left(), leaf.get_right() + LEFT * 0.5, buff=0.1, color=GRAY)
        self.play(FadeIn(co2_text), Create(arrow_co2))
        self.wait(1)

        # Process animation
        process_text = Text("Process!", font_size=32, color=ORANGE).move_to(leaf.center()).scale(0.1)
        self.play(
            FadeOut(arrow_sun), FadeOut(arrow_water), FadeOut(arrow_co2),
            FadeOut(sun), FadeOut(sun_text), FadeOut(water_text), FadeOut(co2_text),
            Transform(leaf_label, process_text.move_to(leaf.center())), 
            run_time=1
        )
        self.wait(0.5)

        # Outputs
        # Sugar/Food
        sugar_text = Text("Sugar (Food)", font_size=28, color=BROWN).next_to(leaf, DOWN * 2.5 + LEFT * 2)
        arrow_sugar = Arrow(leaf.get_bottom() + LEFT * 0.8, sugar_text.get_top(), buff=0.1, color=BROWN)
        self.play(FadeIn(sugar_text), Create(arrow_sugar))
        self.wait(0.5)

        # Oxygen
        oxygen_text = Text("Oxygen (O2)", font_size=28, color=LIGHT_GRAY).next_to(leaf, DOWN * 2.5 + RIGHT * 2)
        arrow_oxygen = Arrow(leaf.get_bottom() + RIGHT * 0.8, oxygen_text.get_top(), buff=0.1, color=LIGHT_GRAY)
        self.play(FadeIn(oxygen_text), Create(arrow_oxygen))
        self.wait(2)

        # Fade out everything
        self.play(FadeOut(self.mobjects))
