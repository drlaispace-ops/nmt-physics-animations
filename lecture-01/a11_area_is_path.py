"""№11 «Площа = шлях» — випуск 1.3, блок 4.1. Пріоритет 1.

Глядач бачить: графік v(t) для v = 10 м/с; прямокутник під ним від 0 до 4 с заповнюється,
а число шляху росте синхронно до 40 м. Висновок: шлях = площа під графіком v(t).

Синхрон: «Який шлях воно пройде за чотири секунди?» → «Площу прямокутника» →
«s = площа під графіком v(t)». Осі з реальними числами — масштаб справжній, підпис не потрібен.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "style"))
sys.path.insert(0, str(Path(__file__).resolve().parent))
from feynman_style import *  # noqa: E402,F403
from feynman_style import _backed  # noqa: E402
from calc_1 import V_CONST, T_CONST  # noqa: E402

AXIS_NUM = 40      # цифри на осях (формульний шрифт дрібніший за текст)
AXIS_LABEL = 48    # «t, с», «v, м/с»
RIGHT_COL = RIGHT * 4.35   # центр правої колонки


class A11_AreaIsPath(Scene):
    def construct(self):
        row_tag(self, "№11")
        ax = Axes(
            x_range=[0, 5.4, 1], y_range=[0, 13, 5], x_length=7.0, y_length=5.0,
            tips=True, axis_config={"color": FG, "stroke_width": SW_AXIS, "tick_size": 0.1},
        ).to_corner(DL, buff=0.8).shift(UP * 0.4)
        for axis, nums in ((ax.x_axis, range(1, 6)), (ax.y_axis, (5, 10))):
            _backed(axis.add_numbers(x_values=list(nums), font_size=AXIS_NUM, color=FG))
        t_lab = MP("t", r",\ \text{с}", size=AXIS_LABEL).next_to(ax.x_axis.get_end(), RIGHT, buff=0.2)
        v_lab = MP("v", r",\ \text{м/с}", size=AXIS_LABEL).next_to(ax.y_axis.get_end(), RIGHT, buff=0.25)

        self.add_subcaption("Тіло їде з постійною швидкістю — 10 м/с.", duration=4)
        self.play(Create(ax), FadeIn(t_lab), FadeIn(v_lab), run_time=2)
        line = Line(ax.c2p(0, V_CONST), ax.c2p(5.2, V_CONST), color=C_V, stroke_width=SW_CURVE)
        self.play(Create(line), run_time=1.5)
        self.wait(0.8)

        # Пауза-питання: шлях за 4 с?
        mark = DashedLine(ax.c2p(T_CONST, 0), ax.c2p(T_CONST, V_CONST), color=FG, stroke_width=SW_AXIS)
        q = MP("t", r"=\,4\ \text{с}", size=SIZE_MATH).move_to(ax.c2p(T_CONST / 2, V_CONST * 0.45))
        self.add_subcaption("Який шлях за чотири секунди?", duration=3)
        self.play(Create(mark), FadeIn(q), run_time=0.8)
        self.wait(2.2)
        self.play(FadeOut(q), run_time=0.4)

        # Прямокутник заповнюється синхронно з лічильником шляху s = v·t
        t = ValueTracker(0.0)
        rect = always_redraw(lambda: Polygon(
            ax.c2p(0, 0), ax.c2p(t.get_value(), 0),
            ax.c2p(t.get_value(), V_CONST), ax.c2p(0, V_CONST),
            stroke_width=0, fill_color=C_V, fill_opacity=0.35,
        ))
        anchor = RIGHT_COL + UP * 2.4

        def counter():
            s = MP("s", "=", size=64)
            s[0].set_color(C_V)
            num = _backed(DecimalNumber(V_CONST * t.get_value(), num_decimal_places=0, font_size=64, color=FG))
            unit = M(r"\text{м}", 64)
            return VGroup(s, num, unit).arrange(RIGHT, buff=0.22, aligned_edge=DOWN).move_to(anchor)

        number = always_redraw(counter)
        self.add(rect)
        self.add_subcaption("Десять на чотири — сорок метрів.", duration=4)
        self.play(FadeIn(number), run_time=0.5)
        self.play(t.animate.set_value(T_CONST), run_time=3, rate_func=linear)
        self.wait(1)

        # Площа прямокутника = висота × основа
        area = M(r"10 \cdot 4 = 40", SIZE_MATH).move_to(ax.c2p(T_CONST / 2, V_CONST / 2))
        self.add_subcaption("Це площа прямокутника: висота на основу.", duration=4)
        self.play(Write(area), run_time=1.2)
        self.wait(2.8)

        # Висновок — у два рядки в правій колонці, під лічильником
        row1 = VGroup(MP("s", "=", size=SIZE_MATH), T("площа під", SIZE_BODY)).arrange(RIGHT, buff=0.25)
        row1[0][0].set_color(C_V)
        row2 = VGroup(T("графіком", SIZE_BODY), M("v(t)", SIZE_MATH)).arrange(RIGHT, buff=0.25)
        rule = VGroup(row1, row2).arrange(DOWN, buff=0.3, aligned_edge=LEFT).move_to(RIGHT_COL + DOWN * 0.1)
        box = SurroundingRectangle(rule, color=ACCENT, buff=0.3, stroke_width=SW_BODY)
        self.add_subcaption("Шлях — це завжди площа під графіком швидкості.", duration=5)
        self.play(FadeIn(rule, shift=DOWN * 0.2), run_time=1)
        self.play(Create(box), run_time=0.7)
        self.wait(3.5)
