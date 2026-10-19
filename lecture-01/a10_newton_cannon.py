"""№10 «Ньютонова гармата» — випуск 1.2, блок 3.5 (МКС і орбіта). Пріоритет 2.

Глядач бачить: Земля в масштабі, на вершині (завищеної) гори — гармата. Ядра летять
горизонтально з дедалі більшою швидкістю: 4, 6, 7, 7,5 км/с — кожне падає дедалі далі;
при 7,9 км/с ядро облітає всю Землю й повертається до гармати: орбіта = падіння,
яке весь час промахується.

Фізика: траєкторії — чисельне інтегрування закону всесвітнього тяжіння (GM = g·R²,
без повітря), solve_ivp. Гору завищено (0,2 R Землі ≈ 1270 км, як у Ньютона), тому швидкості задано
як частку f колової швидкості на вершині: f = v / 7,9 км/с. Форма траєкторії залежить
лише від f, тож підписи «4 … 7,9 км/с» відповідають справжній картині біля поверхні.
Падіння: 21°, 43°, 74°, 145° дуги — і повний оберт.
Час прискорено ×800 однаково для всіх ядер (оберт — 6660 с → 8,3 с ролика).

Синхрон: «станція весь час падає… вісім кілометрів за секунду, — що поверхня Землі
відходить униз» → ядра; «[ГРАФІКА] Ньютонова гармата» → вся анімація;
«щоб навчитися літати, треба кинутися в землю — і промахнутися» → орбіта.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "style"))
sys.path.insert(0, str(Path(__file__).resolve().parent))
from feynman_style import *  # noqa: E402,F403
from calc_1 import G, EARTH_R, V_FIRST_COSMIC, ua  # noqa: E402
from scipy.integrate import solve_ivp  # noqa: E402

# ── Розрахунки для цієї сцени (calc_1 не змінюємо) ──────────────────────────
GM = G * EARTH_R ** 2            # м³/с², з g і R Землі (як у сценарії)
EPS_MOUNTAIN = 0.20              # висота гори в радіусах Землі — завищено (≈1270 км)
R_LAUNCH = EARTH_R * (1 + EPS_MOUNTAIN)
V1_KMS = V_FIRST_COSMIC / 1000   # 7,9 км/с
SPEEDS_KMS = (4.0, 6.0, 7.0, 7.5, V1_KMS)
TIME_X = 800                     # час прискорено ×800


def period(r0=R_LAUNCH):
    return 2 * np.pi * np.sqrt(r0 ** 3 / GM)


def trajectory(f, r0=R_LAUNCH, n=700):
    """Горизонтальний постріл з висоти r0 зі швидкістю f·v_колова(r0).

    Повертає (t, xy): час, с, і координати, м (центр Землі в нулі, старт (0, r0), рух на схід = праворуч).
    Інтегрування зупиняється на поверхні Землі або після одного оберту.
    """
    v0 = f * np.sqrt(GM / r0)

    def rhs(_, s):
        x, y, vx, vy = s
        r3 = (x * x + y * y) ** 1.5
        return [vx, vy, -GM * x / r3, -GM * y / r3]

    def hit(_, s):
        return np.hypot(s[0], s[1]) - EARTH_R
    hit.terminal, hit.direction = True, -1

    sol = solve_ivp(rhs, (0, period(r0)), [0.0, r0, v0, 0.0], events=hit,
                    rtol=1e-10, atol=1e-3, dense_output=True, max_step=10)
    t = np.linspace(0, sol.t[-1], n)
    return t, sol.sol(t)[:2].T


def kms(v):
    """4 км/с, 7,5 км/с — без зайвого «,0»."""
    return str(int(round(v))) if abs(v - round(v)) < 1e-9 else ua(v, 1)


class Cannon:
    """Земля + гора + гармата в екранних координатах; спільне для №10 і №19."""

    def __init__(self, center, radius):
        self.c = np.array(center, dtype=float)
        self.k = radius / EARTH_R          # одиниць екрана на метр

    def p(self, xy):
        return self.c + np.array([xy[0], xy[1], 0.0]) * self.k

    def earth(self):
        return Circle(radius=EARTH_R * self.k, stroke_color=C_WAVE, stroke_width=SW_BODY,
                      fill_color=C_WAVE, fill_opacity=0.15).move_to(self.c)

    def mountain(self):
        half = np.radians(10)
        base = [self.p(EARTH_R * np.array([s * np.sin(half), np.cos(half)])) for s in (-1, 1)]
        peak = self.p([0, R_LAUNCH])
        return Polygon(base[0], peak, base[1], stroke_color=FG, stroke_width=SW_AXIS,
                       fill_color=FG, fill_opacity=0.3)

    def gun(self):
        peak = self.p([0, R_LAUNCH])
        return Rectangle(width=0.34, height=0.12, stroke_width=0, fill_color=FG,
                         fill_opacity=1).move_to(peak + RIGHT * 0.1 + UP * 0.03)

    def path(self, xy, color=C_X):
        return VMobject(color=color, stroke_width=SW_CURVE).set_points_smoothly(
            [self.p(q) for q in xy[:: max(1, len(xy) // 160)]] + [self.p(xy[-1])])


def notes(scene, time_x):
    """Два підписи в правому нижньому куті: масштаб і час."""
    s = scale_note(scene)
    t = L(f"час прискорено ×{time_x}").next_to(s, UP, buff=0.12, aligned_edge=RIGHT)
    scene.add(t)
    return VGroup(s, t)


EARTH_C = LEFT * 2.0 + DOWN * 0.6
EARTH_SR = 2.35                   # радіус Землі на екрані
TEXT_X = 1.5                      # лівий край тексту праворуч


class A10_NewtonCannon(Scene):
    def construct(self):
        row_tag(self, "№10")
        notes(self, TIME_X)
        cn = Cannon(EARTH_C, EARTH_SR)
        earth, hill, gun = cn.earth(), cn.mountain(), cn.gun()
        peak = cn.p([0, R_LAUNCH])

        self.add_subcaption("Гармата на вершині гори.", duration=2.6)
        self.play(FadeIn(earth), run_time=1.0)
        self.play(FadeIn(hill, shift=UP * 0.1), FadeIn(gun), run_time=0.8)
        self.wait(0.8)

        captions = [
            "Повільно — ядро падає поруч.",
            "Швидше — падає далі.",
            "Ще швидше — ще далі.",
            "Земля «відходить» униз з-під ядра.",
        ]
        read = None
        trails = []
        for i, v in enumerate(SPEEDS_KMS):
            t, xy = trajectory(v / V1_KMS)   # для 7,9 км/с f = 1 — рівно колова швидкість
            orbit = i == len(SPEEDS_KMS) - 1
            new_read = T(f"v = {kms(v)} км/с", color=C_V).move_to([TEXT_X, 2.6, 0], aligned_edge=LEFT)
            arrow = vec(peak + RIGHT * 0.3, peak + RIGHT * (0.3 + 0.16 * v), C_V)
            arrow.shift(UP * 0.22)
            fly = t[-1] / TIME_X
            if orbit:  # 0,6 с стрілка + політ + 2 с паузи
                self.add_subcaption("7,9 км/с — ядро падає і весь час промахується.", duration=6)
                self.add_subcaption("Це орбіта.", duration=0.6 + fly + 2.0 - 6, offset=6)
            else:      # 0,6 с стрілка + політ + 0,5 с притухання
                self.add_subcaption(captions[i], duration=0.6 + fly + 0.5)
            anims = [GrowArrow(arrow)]
            anims.append(FadeIn(new_read) if read is None else ReplacementTransform(read, new_read))
            self.play(*anims, run_time=0.6)
            read = new_read

            tt = ValueTracker(0.0)   # справжній час польоту, с

            def pos(tt=tt, t=t, xy=xy):
                tc = tt.get_value()
                return cn.p([np.interp(tc, t, xy[:, 0]), np.interp(tc, t, xy[:, 1])])

            ball = always_redraw(lambda pos=pos: Dot(pos(), radius=0.075, color=FG))

            def trail(tt=tt, t=t, xy=xy, pos=pos):
                k = int(np.searchsorted(t, tt.get_value()))
                pts = [cn.p(q) for q in xy[:k]] + [pos()]
                if len(pts) < 2:
                    return VMobject()
                return VMobject(color=C_X, stroke_width=SW_CURVE).set_points_as_corners(pts)

            tr = always_redraw(trail)
            self.add(tr, ball)
            if orbit:
                key = T("падає і промахується", color=ACCENT).move_to([TEXT_X, 0.4, 0], aligned_edge=LEFT)
                self.play(tt.animate.set_value(t[-1] / 2), FadeOut(arrow), run_time=fly / 2, rate_func=linear)
                # ключові слова з'являються за 1 с, ядро летить далі з тим самим прискоренням часу
                self.play(tt.animate.set_value(t[-1] / 2 + TIME_X * 1.0), FadeIn(key),
                          run_time=1.0, rate_func=linear)
                self.play(tt.animate.set_value(t[-1]), run_time=fly / 2 - 1.0, rate_func=linear)
                tr.clear_updaters()
                ball.clear_updaters()
                self.wait(2.0)
            else:
                self.play(tt.animate.set_value(t[-1]), FadeOut(arrow), run_time=fly, rate_func=linear)
                tr.clear_updaters()
                ball.clear_updaters()
                hit = Circle(radius=0.1, color=C_X, stroke_width=SW_BODY).move_to(ball.get_center())
                self.remove(ball)
                self.add(hit)
                self.play(tr.animate.set_stroke(opacity=0.75), hit.animate.set_stroke(opacity=0.75),
                          run_time=0.5)
                trails.append(tr)
