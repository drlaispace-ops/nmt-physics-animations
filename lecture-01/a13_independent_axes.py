"""№13 «Незалежність осей» — випуск 1.3, блок 4.3. Пріоритет 1. Також план Б для досліду Е3.

Глядач бачить: з висоти 1 м одна кулька падає вертикально, друга одночасно летить
убік зі швидкістю 4,5 м/с. Обидві торкаються підлоги одночасно (через 0,45 с, друга — за 2 м).
Повтор зі стробоскопом: у кожен момент обидві кульки на одній висоті (пунктири рівня),
а горизонтальна швидкість другої не змінюється.

Синхрон: «Будь-який рух можна розкласти на два незалежні рухи…» → «X ⊥ Y — не спілкуються» →
«по X: v = const». Масштаб справжній (1 м : 2,03 м); час сповільнено ×8.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "style"))
sys.path.insert(0, str(Path(__file__).resolve().parent))
from feynman_style import *  # noqa: E402,F403
from calc_1 import G, H_DROP, VX_LAUNCH, T_DROP, X_LAUNCH, SLOWMO_13, ua  # noqa: E402

M_TO_U = 3.5                      # одиниць кадру на метр (той самий для обох осей — масштаб справжній)
ORIGIN = LEFT * 3.9 + DOWN * 1.8  # точка на підлозі під місцем старту
N_STROBE = 6                      # кадри стробоскопа
A_X = -0.12                       # кульки в пристрої стоять поруч, а не в одній точці


def pos(x_m, y_m):
    return ORIGIN + RIGHT * x_m * M_TO_U + UP * y_m * M_TO_U


def ball_a(t):   # просто падає
    return pos(A_X, H_DROP - G * t * t / 2)


def ball_b(t):   # летить убік з vx = 4,5 м/с
    return pos(VX_LAUNCH * t, H_DROP - G * t * t / 2)


class A13_IndependentAxes(Scene):
    def construct(self):
        row_tag(self, "№13")
        floor = Line(pos(-0.45, 0), pos(2.5, 0), color=FG, stroke_width=SW_BODY)
        r = 0.13
        stand = Line(pos(-0.4, H_DROP) + DOWN * r, pos(0.03, H_DROP) + DOWN * r,
                     color=MUTED_TEXT, stroke_width=SW_CURVE)   # виступ пристрою пуску
        a = Dot(ball_a(0), radius=r, color=FG)
        b = Dot(ball_b(0), radius=r, color=FG)
        h_brace = BraceBetweenPoints(pos(-0.32, 0), pos(-0.32, H_DROP), direction=LEFT, color=MUTED_TEXT)
        h_lab = M(r"1\ \text{м}", SIZE_MATH_MIN).next_to(h_brace, LEFT, buff=0.15)
        slow = scale_note(self, f"справжній масштаб · час сповільнено ×{SLOWMO_13}")

        self.add_subcaption("Одна кулька падає, друга летить убік — одночасно.", duration=4)
        self.play(Create(floor), Create(stand), FadeIn(a), FadeIn(b), GrowFromCenter(h_brace), FadeIn(h_lab), run_time=1.5)
        self.wait(1)

        # Перший пуск — повільно, зі слідами траєкторій
        t = ValueTracker(0.0)
        a.add_updater(lambda m: m.move_to(ball_a(t.get_value())))
        b.add_updater(lambda m: m.move_to(ball_b(t.get_value())))
        trail_b = TracedPath(b.get_center, stroke_color=MUTED_TEXT, stroke_width=SW_AXIS, dissipating_time=None)
        trail_a = TracedPath(a.get_center, stroke_color=MUTED_TEXT, stroke_width=SW_AXIS, dissipating_time=None)
        self.add(trail_a, trail_b)
        self.play(t.animate.set_value(T_DROP), run_time=T_DROP * SLOWMO_13, rate_func=linear)
        a.clear_updaters()
        b.clear_updaters()
        trail_a.clear_updaters()   # інакше слід запише повернення кульок на старт
        trail_b.clear_updaters()
        flash_a = Circle(radius=0.3, color=ACCENT, stroke_width=SW_BODY).move_to(a)
        flash_b = Circle(radius=0.3, color=ACCENT, stroke_width=SW_BODY).move_to(b)
        same = T("одночасно", SIZE_TITLE, color=ACCENT).move_to(pos(1.0, H_DROP * 0.62))
        self.add_subcaption("Одночасно. Знову одночасно.", duration=3)
        self.play(Create(flash_a), Create(flash_b), FadeIn(same, scale=1.1), run_time=0.6)
        self.wait(1.6)
        x_brace = BraceBetweenPoints(pos(0, 0), pos(X_LAUNCH, 0), direction=DOWN, color=MUTED_TEXT)
        x_lab = M(r"\approx 2\ \text{м}", SIZE_MATH_MIN).next_to(x_brace, DOWN, buff=0.12)
        self.play(FadeOut(flash_a), FadeOut(flash_b), FadeOut(same), GrowFromCenter(x_brace), FadeIn(x_lab), run_time=0.8)
        self.wait(1)

        # Повтор зі стробоскопом: однакова висота в кожен момент
        self.play(a.animate.move_to(ball_a(0)), b.animate.move_to(ball_b(0)), run_time=0.8)
        axes_note = MP("X", r"\perp", "Y", size=SIZE_MATH).to_corner(UR, buff=1.0).shift(LEFT * 0.6)
        axes_txt = T("не спілкуються", SIZE_BODY).next_to(axes_note, DOWN, buff=0.25)
        self.add_subcaption("Сила тяжіння тягне тільки вниз. Їй байдуже, що діється вбік.", duration=6)
        self.play(FadeIn(axes_note), FadeIn(axes_txt), run_time=0.8)

        ghosts = VGroup()
        for k in range(1, N_STROBE + 1):
            tk = T_DROP * k / N_STROBE
            ga = Dot(ball_a(tk), radius=r, color=FG, fill_opacity=0.7)
            gb = Dot(ball_b(tk), radius=r, color=FG, fill_opacity=0.7)
            level = DashedLine(ball_a(tk) + LEFT * 0.25, ball_b(tk) + RIGHT * 0.25,
                               color=ACCENT, stroke_width=SW_AXIS, dash_length=0.12)
            vx = vec(ball_b(tk), ball_b(tk) + RIGHT * 0.75, C_V)
            ghosts.add(VGroup(level, ga, gb, vx))
            self.play(FadeIn(ga), FadeIn(gb), Create(level), GrowArrow(vx), run_time=0.55)
        self.wait(1.2)

        vconst = MP(r"\text{по } X:", r"\ v = \text{const}", size=SIZE_MATH).next_to(axes_txt, DOWN, buff=0.6)
        vconst[1].set_color(C_V)
        self.add_subcaption("По горизонталі нічого не діє — швидкість не змінюється.", duration=5)
        self.play(FadeIn(vconst, shift=DOWN * 0.2), run_time=0.8)
        self.wait(4)
