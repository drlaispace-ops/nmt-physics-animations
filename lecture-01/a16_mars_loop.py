"""№16 «Петля Марса» — випуск 1.2, врізка «Марс, який їде задом наперед». Пріоритет 2.

Частина 1 (≈13 с) — небо з Землі: Марс повзе відносно зірок, зупиняється, кілька тижнів
їде назад, знову зупиняється й рушає далі — петля ретроградного руху.
Частина 2 (≈19 с) — той самий відрізок часу згори: спершу з центром у Землі (Марс
описує петлю навколо нас), потім початок координат «пересідає» на Сонце — петля
розплітається в дугу кола; Земля по внутрішній орбіті просто обганяє Марс.

Розрахунок (не на око): колові орбіти, Земля 1 а. о. / 1 рік, Марс 1,524 а. о. / 1,881 року,
нахил орбіти Марса 1,85°. Вузол обрано так, щоб протистояння (t = 0) припало на найбільшу
північну широту Марса (аргумент широти 90°) — тоді на небі виходить петля, а не зиґзаґ.
Небо: геоцентрична екліптична довгота λ і широта β в однаковому масштабі по обох осях
(схід ліворуч, як на небі обличчям на південь). Вікно — ±110 діб від протистояння.
Спрощення: орбіти колові (без ексцентриситетів), розміри планет і Сонця умовні.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "style"))
from feynman_style import *  # noqa: E402,F403

# ── Орбіти ──────────────────────────────────────────────────────────────────
YEAR = 365.25
A_MARS, T_MARS = 1.524, 1.881              # а. о., роки
INC = np.radians(1.85)
U_OPP = np.radians(90.0)                   # аргумент широти Марса в протистоянні
NODE = -U_OPP                              # довгота висхідного вузла (протистояння на λ = 0)
D_WIN = 110                                # діб в обидва боки від протистояння
DAYS = np.linspace(-D_WIN, D_WIN, 2201)


def helio(days):
    """Геліоцентричні екліптичні координати Землі й Марса (а. о.)."""
    t = np.atleast_1d(days) / YEAR
    th_e = 2 * PI * t
    E = np.stack([np.cos(th_e), np.sin(th_e), 0 * t], -1)
    u = 2 * PI * t / T_MARS + U_OPP        # аргумент широти
    M = A_MARS * np.stack([np.cos(NODE) * np.cos(u) - np.sin(NODE) * np.sin(u) * np.cos(INC),
                           np.sin(NODE) * np.cos(u) + np.cos(NODE) * np.sin(u) * np.cos(INC),
                           np.sin(u) * np.sin(INC)], -1)
    return E, M


E_ALL, M_ALL = helio(DAYS)
D_ALL = M_ALL - E_ALL
LAM = np.degrees(np.unwrap(np.arctan2(D_ALL[:, 1], D_ALL[:, 0])))
BETA = np.degrees(np.arctan2(D_ALL[:, 2], np.hypot(D_ALL[:, 0], D_ALL[:, 1])))
_dl = np.gradient(LAM, DAYS)
STATIONS = DAYS[np.where(np.diff(np.sign(_dl)))[0]]          # ≈ −36 і +36 діб

# ── Небо (частина 1) ───────────────────────────────────────────────────────
K_SKY = 0.36                               # од/градус по обох осях — пропорції справжні
SKY_Y0 = 0.1
BETA_C = 0.5 * (BETA.min() + BETA.max())


def sky_xy(i):
    return np.array([-K_SKY * LAM[i], SKY_Y0 + K_SKY * (BETA[i] - BETA_C), 0.0])


SKY_PTS = np.array([sky_xy(i) for i in range(len(DAYS))])

# ── Згори (частина 2) ──────────────────────────────────────────────────────
AU = 1.9                                   # од/а. о.
O_TOP = np.array([0.0, -0.65, 0])
ROT = np.array([[0, -1, 0], [1, 0, 0], [0, 0, 1.0]])   # протистояння дивиться вгору


def top_xy(p, origin):
    q = (p - origin)
    q = q * np.array([1, 1, 0])
    return O_TOP + AU * (q @ ROT.T)


T_SKY, T_TOP = 11.0, 6.0                   # с на весь відрізок ±110 діб


def weeks_note(seconds):
    w = int(round(2 * D_WIN / seconds / 7))
    word = "тиждень" if w == 1 else ("тижні" if 2 <= w <= 4 else "тижнів")
    return f"1 с ≈ {w} {word}"


def idx(day):
    return int(np.clip(np.searchsorted(DAYS, day), 0, len(DAYS) - 1))


def polyline(pts, color, width=SW_CURVE):
    m = VMobject(stroke_color=color, stroke_width=width)
    if len(pts) < 2:
        pts = [pts[0], pts[0] + RIGHT * 1e-3] if len(pts) else [ORIGIN, RIGHT * 1e-3]
        m.set_points_as_corners(pts).set_stroke(opacity=0)
        return m
    return m.set_points_as_corners(pts)


def body(color, r):
    return Circle(radius=r, color=color, fill_color=color, fill_opacity=1, stroke_width=0)


class A16_MarsLoop(Scene):
    def construct(self):
        row_tag(self, "№16")
        day = ValueTracker(-D_WIN)

        # ── Частина 1: небо з Землі ────────────────────────────────────────
        rng = np.random.default_rng(16)
        stars = VGroup()
        while len(stars) < 70:
            x, y = rng.uniform(-6.9, 6.9), rng.uniform(-3.9, 2.7)
            if (x > 2.5 and y < -3.1) or (abs(x) < 2.6 and y > 2.6):
                continue
            stars.add(Dot([x, y, 0], radius=rng.choice([0.025, 0.035, 0.05]), color=FG)
                      .set_opacity(rng.uniform(0.45, 1.0)))
        head1 = T("Небо з Землі", SIZE_TITLE).move_to(UP * 3.15)
        trail1 = always_redraw(lambda: polyline(SKY_PTS[: idx(day.get_value()) + 1], C_X))
        mars1 = always_redraw(lambda: body(C_X, 0.13).move_to(SKY_PTS[idx(day.get_value())]))
        note1 = scale_note(self, weeks_note(T_SKY))
        note1.set_opacity(0)

        self.add_subcaption("Марс місяцями повзе відносно зірок.", duration=4.0)
        m0 = body(C_X, 0.13).move_to(SKY_PTS[0])
        self.play(FadeIn(stars), FadeIn(head1), FadeIn(m0), note1.animate.set_opacity(1), run_time=1.0)
        self.remove(m0)
        self.add(trail1, mars1)
        self.wait(0.3)

        s1, s2 = STATIONS
        t_of = lambda d: T_SKY * (d + D_WIN) / (2 * D_WIN)   # noqa: E731  с від початку руху
        i_top = idx(0)
        back = T("назад", SIZE_BODY, ACCENT).next_to(SKY_PTS[i_top], UP, buff=0.4)
        self.add_subcaption("Зупиняється — і кілька тижнів їде назад.", duration=t_of(s2) - t_of(s1) + 1.0,
                            offset=t_of(s1) - 0.5)
        self.add_subcaption("Знову зупинка — і далі, куди їхав.", duration=T_SKY - t_of(s2) + 1.0,
                            offset=t_of(s2) + 0.5)
        def go(d_to, *anims):
            self.play(day.animate.set_value(d_to), *anims, run_time=t_of(d_to) - t_of(day.get_value()),
                      rate_func=linear)

        dd = 2 * D_WIN / T_SKY            # діб за секунду
        go(s1)
        go(s1 + 0.8 * dd, FadeIn(back))
        go(s2)
        go(s2 + 1.0 * dd, FadeOut(back))
        go(D_WIN)
        self.wait(1.5)

        # ── Частина 2: згори, центр — Земля ────────────────────────────────
        org = ValueTracker(1.0)          # 1 — початок координат у Землі, 0 — у Сонці
        day2 = ValueTracker(-D_WIN)

        def origin_at(i):
            return org.get_value() * E_ALL[i]

        def mars_trail():
            i = idx(day2.get_value())
            s = org.get_value()
            pts = [top_xy(M_ALL[j], s * E_ALL[j]) for j in range(0, i + 1, 4)]
            return polyline(pts, C_X)

        def earth_trail():
            i = idx(day2.get_value())
            s = org.get_value()
            pts = [top_xy(E_ALL[j], s * E_ALL[j]) for j in range(0, i + 1, 4)]
            return polyline(pts, C_WAVE).set_stroke(opacity=min(1.0, 4 * (1 - s)))

        def planets():
            i = idx(day2.get_value())
            o = origin_at(i)
            pe, pm, ps = top_xy(E_ALL[i], o), top_xy(M_ALL[i], o), top_xy(np.zeros(3), o)
            return VGroup(
                body(C_LIGHT, 0.3).move_to(ps), body(C_WAVE, 0.15).move_to(pe), body(C_X, 0.13).move_to(pm),
                T("Сонце", 32).next_to(ps, DOWN, buff=0.2),
                T("Земля", 32).next_to(pe, DOWN, buff=0.2),
                T("Марс", 32).next_to(pm, RIGHT, buff=0.2),
            )

        # заголовок ліворуч угорі — щоб промінь зору на Марс не перетинав його
        head2 = T("Згори: центр — Земля", SIZE_TITLE).move_to(UP * 3.15).align_to([-6.3, 0, 0], LEFT)
        head3 = T("Згори: центр — Сонце", SIZE_TITLE).move_to(UP * 3.15).align_to([-6.3, 0, 0], LEFT)
        tr_m, tr_e, pl = always_redraw(mars_trail), always_redraw(earth_trail), always_redraw(planets)
        note2 = L(weeks_note(T_TOP)).to_corner(DR, buff=0.4)
        first = planets()
        self.add_subcaption("Той самий рух згори. Центр — Земля.", duration=T_TOP + 1.5)
        self.play(FadeOut(VGroup(stars, trail1, mars1)), FadeOut(head1, shift=UP * 0.2), FadeOut(note1),
                  run_time=0.7)
        self.play(FadeIn(first), FadeIn(head2, shift=UP * 0.2), FadeIn(note2), run_time=0.7)
        self.remove(first)
        self.add(tr_e, tr_m, pl)
        self.play(day2.animate.set_value(D_WIN), run_time=T_TOP, rate_func=linear)
        self.wait(0.8)

        # ── «Пересідаємо» на Сонце: петля розплітається ───────────────────
        orbits = VGroup(*[DashedVMobject(Circle(radius=AU * r, color=MUTED_TEXT, stroke_width=SW_AXIS)
                                         .move_to(O_TOP), num_dashes=n) for r, n in ((1, 50), (A_MARS, 70))])
        self.add_subcaption("Переносимо початок координат на Сонце.", duration=3.5)
        self.play(org.animate.set_value(0.0), AnimationGroup(FadeOut(head2, shift=UP * 0.2),
                                                             FadeIn(head3, shift=UP * 0.2), lag_ratio=1.0),
                  run_time=3.0, rate_func=smooth)
        self.play(FadeIn(orbits), run_time=0.6)
        self.wait(0.9)

        # ── Повтор у системі Сонця: Земля обганяє Марс ──────────────────────
        def sight():
            i = idx(day2.get_value())
            pe, pm = top_xy(E_ALL[i], 0 * E_ALL[i]), top_xy(M_ALL[i], 0 * E_ALL[i])
            u = (pm - pe) / np.linalg.norm(pm - pe)
            return DashedLine(pe, pm + 0.9 * u, color=FG, stroke_width=SW_AXIS, dash_length=0.12)

        day2.set_value(-D_WIN)
        line = always_redraw(sight)
        self.add(line)
        self.bring_to_front(pl)
        self.add_subcaption("Петлі немає: Земля просто обганяє Марс.", duration=T_TOP + 2.0)
        self.play(day2.animate.set_value(D_WIN), run_time=T_TOP, rate_func=linear)
        self.wait(2.0)
