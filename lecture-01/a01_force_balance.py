"""№1 «Баланс сил» — випуск 1.1, блок 2.2. Пріоритет 2.

Глядач бачить: тіло падає (камера летить разом із ним — повз пролітають смуги повітря).
Стрілка тяжіння стала; стрілка опору росте як v² і зрівнюється з тяжінням. Праворуч
графік v(t) за формулою v = v_t·th(g t / v_t) з calc_1.v_skydiver: крива підходить до 55 м/с,
прискорення a = g·(1 − v²/v_t²) спадає до нуля. Час прискорено ×2 (вісь t — справжні секунди).

Синхрон: «Тіло починає падати. Швидкість — нуль, опір — нуль» → старт;
«Швидкість росте — опір росте… ще швидше, бо квадрат» → розгін;
«опір… точно зрівняється з силою тяжіння» → стрілки рівні;
«Сумарна сила — нуль. Прискорення — нуль… усталеною швидкістю» → фінал.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "style"))
sys.path.insert(0, str(Path(__file__).resolve().parent))
from feynman_style import *  # noqa: E402,F403
from calc_1 import G, V_TERM, T_95, v_skydiver, ua  # noqa: E402

# ── Розрахунки для цієї сцени (calc_1 не змінюємо) ──────────────────────────
TIME_X = 2.0            # час прискорено ×2: 1 с ролика = 2 с падіння
T_SHOW = 20.0           # с падіння на графіку; v(20 с) = 54,9 м/с, a ≈ 0,03 м/с²
T_HOLD = 7.0            # с ролика після виходу на усталену швидкість


def accel(t):
    """a = g·(1 − v²/v_t²) — те саме, що похідна v_skydiver."""
    return G * (1 - (v_skydiver(t) / V_TERM) ** 2)


def fallen(t):
    """Пройдений шлях y(t) = v_t²/g · ln ch(g t / v_t), м — для руху смуг повітря."""
    return V_TERM ** 2 / G * np.log(np.cosh(G * t / V_TERM))


BODY = LEFT * 3.9 + UP * 0.5
BODY_R = 0.42
LEN_G = 1.75            # довжина стрілки тяжіння; опір = LEN_G·(v/v_t)²
STREAK_K = 0.035        # одиниць екрана на метр падіння (смуги — декор, без чисел)


class A01_ForceBalance(Scene):
    def construct(self):
        row_tag(self, "№1")
        scale_note(self, f"час прискорено ×{round(TIME_X)}")
        tr = ValueTracker(0.0)   # справжній час падіння, с

        # Смуги повітря ліворуч від тіла: рухаються вгору зі швидкістю ∝ v
        cols = [-6.25, -5.7, -5.15, -0.95]
        span, y_lo = 6.6, -3.1
        rng = np.random.default_rng(7)
        seeds = [(x, rng.uniform(0, span)) for x in cols for _ in range(5)]

        def streaks():
            off = fallen(tr.get_value()) * STREAK_K
            g = VGroup()
            for x, y0 in seeds:
                y = y_lo + (y0 + off) % span
                g.add(Line([x, y, 0], [x, y + 0.6, 0], color=FG, stroke_width=SW_AXIS,
                           stroke_opacity=0.4))
            return g

        air = always_redraw(streaks)
        body = Circle(radius=BODY_R, stroke_color=FG, stroke_width=SW_BODY,
                      fill_color=FG, fill_opacity=0.15).move_to(BODY)
        grav = vec(BODY, BODY + DOWN * LEN_G, C_F)
        g_lab = T("тяжіння").next_to(grav, RIGHT, buff=0.3).shift(DOWN * 0.35)

        def drag_len():
            return LEN_G * (v_skydiver(tr.get_value()) / V_TERM) ** 2

        drag = always_redraw(lambda: vec(BODY, BODY + UP * drag_len(), C_F)
                             if drag_len() > 0.06 else VGroup())

        def drag_label():
            lab = T("опір").next_to(BODY + UP * drag_len(), RIGHT, buff=0.3).shift(DOWN * 0.35)
            return lab.set_opacity(float(np.clip((drag_len() - 0.5) / 0.4, 0, 1)))

        d_lab = always_redraw(drag_label)

        # Графік v(t), вісь t — справжні секунди
        ax = Axes(
            x_range=[0, T_SHOW, 5], y_range=[0, 70, 20], x_length=5.4, y_length=4.6,
            tips=True, axis_config={"color": FG, "stroke_width": SW_AXIS, "tick_size": 0.08},
        )
        ax.shift(RIGHT * 0.7 + DOWN * 2.1 - ax.c2p(0, 0))
        t_lab = L("t, с", 32).next_to(ax.x_axis.get_end(), DOWN, buff=0.2)
        v_lab = L("v, м/с", 32).next_to(ax.y_axis.get_end(), LEFT, buff=0.2)
        ticks = VGroup(*[L(str(n), 32).next_to(ax.c2p(n, 0), DOWN, buff=0.18) for n in (5, 10, 15)],
                       *[L(str(n), 32).next_to(ax.c2p(0, n), LEFT, buff=0.18) for n in (20, 40)])
        term = DashedLine(ax.c2p(0, V_TERM), ax.c2p(T_SHOW, V_TERM), color=C_V,
                          stroke_width=SW_AXIS, dash_length=0.15)
        term_lab = T(f"{round(V_TERM)}", 32, color=C_V).next_to(ax.c2p(0, V_TERM), LEFT, buff=0.18)

        def curve():
            tc = min(tr.get_value(), T_SHOW)
            if tc < 0.05:
                return VGroup()
            ts = np.linspace(0, tc, 90)
            return VMobject(color=C_V, stroke_width=SW_CURVE).set_points_as_corners(
                [ax.c2p(t, v_skydiver(t)) for t in ts])

        graph = always_redraw(curve)
        dot = always_redraw(lambda: Dot(ax.c2p(min(tr.get_value(), T_SHOW),
                                              v_skydiver(min(tr.get_value(), T_SHOW))),
                                        radius=0.08, color=C_V))
        v_read = always_redraw(lambda: T(f"v = {round(v_skydiver(tr.get_value()))} м/с",
                                         color=C_V).move_to([0.7, 3.15, 0], aligned_edge=LEFT))
        a_read = always_redraw(lambda: T(f"a = {ua(accel(tr.get_value()), 1)} м/с²")
                               .move_to([3.9, 3.15, 0], aligned_edge=LEFT))

        self.add_subcaption("Старт: швидкість нуль — опору нема.", duration=3)
        self.add(air)
        self.play(FadeIn(body), GrowArrow(grav), FadeIn(g_lab),
                  Create(ax), FadeIn(t_lab), FadeIn(v_lab), FadeIn(ticks), run_time=1.6)
        self.play(FadeIn(v_read), FadeIn(a_read), Create(term), FadeIn(term_lab), run_time=0.8)
        self.add(drag, d_lab, graph, dot)
        self.wait(0.6)

        # Розгін: справжній час іде вдвічі швидше за ролик
        tr.add_updater(lambda m, dt: m.increment_value(TIME_X * dt))
        self.add(tr)
        fall = T_SHOW / TIME_X
        self.add_subcaption("Швидкість росте — опір росте.", duration=3.5)
        self.add_subcaption("Опір росте як квадрат швидкості.", duration=3.3, offset=3.5)
        self.add_subcaption("Опір зрівнявся з тяжінням.", duration=3.2, offset=6.8)
        self.wait(fall)

        # Усталена швидкість: сума сил нуль, a ≈ 0, тіло летить далі рівномірно
        a_read.clear_updaters()
        a_zero = T("a ≈ 0").move_to([3.9, 3.15, 0], aligned_edge=LEFT)
        box = SurroundingRectangle(a_zero, color=ACCENT, buff=0.15, stroke_width=SW_BODY)
        steady = T("усталена швидкість").next_to(ax.c2p(T_SHOW, V_TERM), UP, buff=0.2,
                                                  aligned_edge=RIGHT)
        self.add_subcaption("Сума сил нуль — прискорення нуль.", duration=3.5)
        self.play(ReplacementTransform(a_read, a_zero), Create(box), run_time=1.0)
        self.wait(2.5)
        self.add_subcaption("Швидкість стала — усталена.", duration=T_HOLD - 3.5)
        self.play(FadeIn(steady, shift=UP * 0.15), run_time=0.8)
        self.wait(T_HOLD - 3.5 - 0.8)
