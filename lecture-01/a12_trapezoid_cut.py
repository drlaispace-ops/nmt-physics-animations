"""№12 «Розріз трапеції» — випуск 1.3, блок 4.1. Пріоритет 1, найважливіша анімація лекції.

Глядач бачить: під похилим графіком v(t) — трапеція; горизонтальний розріз на рівні v₀
ділить її на прямокутник і трикутник; трикутник відсувається, фігури підписуються,
і формула s = v₀t + at²/2 збирається з двох площ.

Синхрон: «Трапеція. Незручно. Але дивіться, що я зроблю» → «Складаємо дві площі» → пауза 3 с.
Графік якісний (без чисел на осях), тому підпис «масштаб умовний» не потрібен.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "style"))
from feynman_style import *  # noqa: E402,F403

# Геометрія графіка (умовні одиниці, бо графік без чисел): v(t) = V0 + A·t на [0, T_END].
V0, A, T_END = 2.0, 0.75, 4.4
LIFT = UP * 0.7 + RIGHT * 0.3     # куди відсувається трикутник після розрізу
MATH_LABEL = SIZE_MATH_MIN        # курсивні літери формул дрібніші за текст, тому 44


class A12_TrapezoidCut(Scene):
    def construct(self):
        row_tag(self, "№12")
        ax = Axes(
            x_range=[0, 5.0, 1], y_range=[0, 6.4, 1], x_length=7.2, y_length=5.6,
            tips=True, axis_config={"color": FG, "stroke_width": SW_AXIS, "include_ticks": False},
        ).to_corner(DL, buff=0.75).shift(UP * 0.25)
        t_lab = M("t", MATH_LABEL).next_to(ax.x_axis.get_end(), DOWN, buff=0.2)
        v_lab = M("v", MATH_LABEL).next_to(ax.y_axis.get_end(), LEFT, buff=0.2)

        self.add_subcaption("Тіло розганяється рівномірно.", duration=4.5)
        self.play(Create(ax), FadeIn(t_lab), FadeIn(v_lab), run_time=2)

        v_end = V0 + A * T_END
        line = Line(ax.c2p(0, V0), ax.c2p(T_END, v_end), color=C_V, stroke_width=SW_CURVE)
        v0_lab = M("v_0", MATH_LABEL, color=C_V).next_to(ax.c2p(0, V0), LEFT, buff=0.2)
        self.play(Create(line), FadeIn(v0_lab), run_time=2.5)

        slope = T("a = нахил", SIZE_BODY).next_to(line.point_from_proportion(0.5), UP, buff=0.45).shift(LEFT * 0.6)
        self.add_subcaption("Нахил графіка — це прискорення.", duration=3)
        self.play(FadeIn(slope, shift=UP * 0.2), run_time=1)
        self.wait(2)

        # Трапеція = площа під графіком
        p0, p1 = ax.c2p(0, 0), ax.c2p(T_END, 0)
        q0, q1 = ax.c2p(0, V0), ax.c2p(T_END, V0)
        top = ax.c2p(T_END, v_end)
        trap = Polygon(p0, p1, top, q0, stroke_width=0, fill_color=C_V, fill_opacity=0.3)
        ask = MP("s", "=", "\\,?", size=SIZE_MATH).move_to(ax.c2p(T_END / 2, V0 * 0.55 + 0.6))
        self.add_subcaption("Шлях — площа під графіком. Фігура — трапеція.", duration=4)
        self.play(FadeOut(slope), FadeIn(trap), run_time=1.5)
        self.play(FadeIn(ask), run_time=0.8)
        self.wait(1.7)

        # Розріз на рівні v0
        cut = DashedLine(q0, q1, color=FG, stroke_width=SW_BODY, dash_length=0.2)
        self.add_subcaption("Розрізаю на прямокутник і трикутник.", duration=3.5)
        self.play(FadeOut(ask), Create(cut), run_time=1.5)

        rect = Polygon(p0, p1, q1, q0, stroke_color=C_V, stroke_width=SW_BODY,
                       fill_color=C_V, fill_opacity=0.3)
        tri = Polygon(q0, q1, top, stroke_color=ACCENT, stroke_width=SW_BODY,
                      fill_color=ACCENT, fill_opacity=0.35)
        self.remove(trap)
        self.add(rect, tri)
        self.play(FadeOut(cut), FadeOut(line), run_time=0.6)
        self.play(tri.animate.shift(LIFT), run_time=1.5)
        self.wait(0.6)

        # Прямокутник: висота v0, основа t, площа v0·t
        r_brace = BraceBetweenPoints(p0, p1, direction=DOWN, color=FG).shift(DOWN * 0.08)
        r_base = M("t", MATH_LABEL).next_to(r_brace, DOWN, buff=0.12)
        r_area = M("v_0 t", SIZE_MATH, color=C_V).move_to(rect)
        self.add_subcaption("Прямокутник: висота v₀, основа t. Площа v₀t.", duration=4.5)
        self.play(FadeOut(t_lab), GrowFromCenter(r_brace), FadeIn(r_base), run_time=0.8)
        self.play(Write(r_area), run_time=1.2)
        self.wait(2.2)

        # Трикутник: висота at, площа ½·t·at = at²/2
        b_right, t_right = q1 + LIFT, top + LIFT
        h_brace = BraceBetweenPoints(t_right, b_right, direction=RIGHT, color=ACCENT)
        h_lab = M("at", MATH_LABEL, color=ACCENT).next_to(h_brace, RIGHT, buff=0.15)
        self.add_subcaption("Висота трикутника — at: на стільки виросла швидкість.", duration=4.5)
        self.play(GrowFromCenter(h_brace), FadeIn(h_lab), run_time=1.2)
        self.wait(1.8)

        centroid = (q0 + q1 + top) / 3 + LIFT + RIGHT * 0.55 + DOWN * 0.15
        t_area = M(r"\tfrac{1}{2}\, t \cdot at", SIZE_MATH, color=ACCENT).move_to(centroid)
        self.add_subcaption("Площа трикутника — половина основи на висоту.", duration=4)
        self.play(Write(t_area), run_time=1.2)
        t_area2 = M(r"\frac{a t^2}{2}", SIZE_MATH, color=ACCENT).move_to(centroid)
        self.play(TransformMatchingShapes(t_area, t_area2), run_time=1.2)
        self.wait(1.4)

        # Формула збирається з двох площ; фігури притухають — акцент на формулі
        formula = MP("s", "=", "v_0 t", "+", r"\frac{a t^2}{2}", size=72)
        formula[2].set_color(C_V)
        formula[4].set_color(ACCENT)
        formula.to_corner(UR, buff=0.9).shift(DOWN * 0.3)
        box = SurroundingRectangle(formula, color=FG, buff=0.35, stroke_width=SW_BODY)
        shapes = VGroup(rect, tri, r_brace, h_brace)
        labels = VGroup(r_base, h_lab, v0_lab, v_lab)
        self.add_subcaption("Складаємо дві площі.", duration=6.5)
        self.play(
            ReplacementTransform(r_area, formula[2]),
            ReplacementTransform(t_area2, formula[4]),
            FadeIn(formula[0]), FadeIn(formula[1]), FadeIn(formula[3]),
            shapes.animate.set_opacity(0.35), labels.animate.set_opacity(0.45),
            run_time=2,
        )
        self.play(Create(box), run_time=0.8)
        self.wait(3.5)  # [ПАУЗА 3] — не вирізати
