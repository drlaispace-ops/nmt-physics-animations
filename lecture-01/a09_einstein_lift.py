"""№9 «Ліфт Ейнштейна» — випуск 1.2, врізка «Найщасливіша думка в житті Ейнштейна». Пріоритет 2.

Глядач бачить два ліфти поруч. Ліворуч — трос обірвався, ліфт вільно падає в шахті
(поверхи летять угору дедалі швидше, стрілка швидкості росте). Праворуч — ліфт висить
у глибокому космосі серед зір. Усередині обох — ІДЕНТИЧНА картинка: людина ширяє,
м'ячик, чашка й крапля води пливуть рівномірно й прямолінійно. Наприкінці — «=».

Фізика: у системі вільно падаючого ліфта, як і в ліфті далеко від мас, тіла рухаються
рівномірно й прямолінійно (інерціальна система локально). Тому вміст обох ліфтів —
одна функція `inside(t)` (сталі швидкості й обертання), зсунута в центр кожного ліфта.
Падіння шахтою — y = g t²/2 зі справжнім g у масштабі ліфта (2,4 м), час сповільнено ×SLOW.
Приливні відмінності (сценарій їх згадує) тут не показуються — ліфт малий.

Синхрон: «Варіант перший: обірвався трос…» → «Варіант другий: … глибокий космос» →
«Ви не можете відрізнити».
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "style"))
sys.path.insert(0, str(Path(__file__).resolve().parent))
from feynman_style import *  # noqa: E402,F403
from calc_1 import G  # noqa: E402

LIFT_W, LIFT_H = 2.7, 4.2
SHAFT_TOP = 2.65                          # вище — місце для підпису
LIFT_Y = -0.25
LEFT_C = np.array([-3.5, LIFT_Y, 0])
RIGHT_C = np.array([3.5, LIFT_Y, 0])
M_PER_UNIT = 2.4 / LIFT_H                 # кабіна 2,4 м заввишки
SLOW = 6                                  # час сповільнено ×6
G_EFF = G / M_PER_UNIT / SLOW ** 2        # од/с² у кадрі
FLOOR_GAP = 3.0 / M_PER_UNIT              # поверх 3 м
T_RUN = 17.5
T_EQ = 11.8                               # коли з'являється «=»
K_V = 0.4                                 # довжина стрілки швидкості, од на (од/с)
CABLE_DX = 0.65                           # трос кріпиться праворуч від центру даху

CABIN = interpolate_color(ManimColor(BG), ManimColor(MUTED_TEXT), 0.2)
SHAFT = interpolate_color(ManimColor(BG), ManimColor(MUTED_TEXT), 0.55)

# Вміст ліфта: початкове положення, стала швидкість, кутова швидкість (локальні координати)
PERSON = (np.array([-0.3, -0.55, 0]), np.array([0.015, 0.035, 0]), 0.04)
BALL = (np.array([0.85, 0.95, 0]), np.array([0.0, -0.07, 0]))
CUP = (np.array([-0.85, 1.25, 0]), np.array([-0.005, 0.02, 0]), 0.3)
DROP = (np.array([-0.55, 0.85, 0]), np.array([0.05, 0.035, 0]))


def _limb(a, b):
    return Line(a, b, color=FG, stroke_width=7).set_cap_style(CapStyleType.ROUND)


def person(hip, angle):
    pts = {
        "sh": (0, 0.75), "h1": (-0.6, 1.2), "h2": (0.62, 1.05), "e1": (-0.35, 0.95), "e2": (0.4, 0.85),
        "k1": (-0.28, -0.58), "f1": (-0.1, -1.15), "k2": (0.28, -0.52), "f2": (0.45, -1.05),
    }
    P = {k: np.array([x, y, 0.0]) for k, (x, y) in pts.items()}
    o = ORIGIN
    g = VGroup(_limb(o, P["sh"]), _limb(P["sh"], P["e1"]), _limb(P["e1"], P["h1"]),
               _limb(P["sh"], P["e2"]), _limb(P["e2"], P["h2"]),
               _limb(o, P["k1"]), _limb(P["k1"], P["f1"]), _limb(o, P["k2"]), _limb(P["k2"], P["f2"]),
               Circle(radius=0.24, color=FG, fill_color=FG, fill_opacity=1, stroke_width=0).move_to([0.02, 1.05, 0]))
    return g.rotate(angle, about_point=ORIGIN).shift(hip)


def inside(t, center):
    """Однаковий вміст обох ліфтів у момент t: усе рухається рівномірно й прямолінійно."""
    p0, pv, pw = PERSON
    b0, bv = BALL
    c0, cv, cw = CUP
    d0, dv = DROP
    cup = Polygon([-0.17, 0.2, 0], [0.17, 0.2, 0], [0.13, -0.2, 0], [-0.13, -0.2, 0],
                  color=FG, stroke_width=SW_AXIS, fill_color=BG, fill_opacity=1)
    cup.rotate(0.6 + cw * t, about_point=ORIGIN).shift(c0 + cv * t)
    return VGroup(
        person(p0 + pv * t, -0.25 + pw * t),
        Circle(radius=0.22, color=C_X, fill_color=C_X, fill_opacity=1, stroke_width=0).move_to(b0 + bv * t),
        cup,
        Circle(radius=0.13, color=C_WAVE, fill_color=C_WAVE, fill_opacity=1, stroke_width=0).move_to(d0 + dv * t),
    ).shift(center)


def cabin(center, hook=False):
    box = Rectangle(width=LIFT_W, height=LIFT_H, color=FG, stroke_width=SW_BODY, fill_color=CABIN,
                    fill_opacity=1).move_to(center)
    door = Line(center + DOWN * LIFT_H / 2 + UP * 0.05, center + DOWN * LIFT_H / 2 + UP * 2.9,
                color=SHAFT, stroke_width=SW_AXIS)
    lamp = Line(center + UP * (LIFT_H / 2 - 0.12) + LEFT * 0.35, center + UP * (LIFT_H / 2 - 0.12) + RIGHT * 0.35,
                color=C_LIGHT, stroke_width=SW_BODY * 2)
    g = VGroup(box, door, lamp)
    if hook:
        top = center + UP * LIFT_H / 2
        g.add(Circle(radius=0.16, color=FG, stroke_width=SW_AXIS).move_to(top + UP * 0.16))
    return g


def fall(t):
    return 0.5 * G_EFF * t ** 2


def shaft_view(t):
    """Шахта в системі ліфта: стіни й поверхи летять угору на fall(t)."""
    x_l, x_r = LEFT_C[0] - LIFT_W / 2 - 0.25, LEFT_C[0] + LIFT_W / 2 + 0.25
    g = VGroup(Line([x_l, -4.2, 0], [x_l, SHAFT_TOP, 0], color=SHAFT, stroke_width=SW_BODY),
               Line([x_r, -4.2, 0], [x_r, SHAFT_TOP, 0], color=SHAFT, stroke_width=SW_BODY))
    off = fall(t) % FLOOR_GAP
    for j in range(-1, 3):                  # рівно 4 перекриття (незмінна структура)
        y = -3.3 + j * FLOOR_GAP + off
        op = 1.0 if y < SHAFT_TOP - 0.1 else 0.0
        for x0, dx in ((x_l, 0.22), (x_r, -0.22)):
            g.add(Rectangle(width=0.44, height=0.16, color=SHAFT, fill_color=SHAFT, fill_opacity=op,
                            stroke_width=0).move_to([x0 + dx, min(y, SHAFT_TOP), 0]))
    # верхній кінець троса лишився в шахті — відлітає вгору
    brk = LEFT_C[1] + LIFT_H / 2 + 0.55 + fall(t)
    cx = LEFT_C[0] + CABLE_DX
    g.add(Line([cx, min(brk, SHAFT_TOP - 0.01), 0], [cx, SHAFT_TOP, 0], color=FG, stroke_width=SW_AXIS))
    return g


def cable_stub():
    top = LEFT_C + UP * LIFT_H / 2 + RIGHT * CABLE_DX
    end = top + UP * 0.5
    return VGroup(Line(top, end, color=FG, stroke_width=SW_AXIS),
                  *[Line(end, end + 0.18 * np.array([np.sin(a), np.cos(a), 0]), color=FG, stroke_width=SW_AXIS)
                    for a in (-0.6, 0.0, 0.6)])


def stars():
    rng = np.random.default_rng(7)
    g = VGroup()
    while len(g) < 46:
        x, y = rng.uniform(2.0, 6.9), rng.uniform(-3.9, 2.6)
        if abs(x - RIGHT_C[0]) < LIFT_W / 2 + 0.25 and abs(y - RIGHT_C[1]) < LIFT_H / 2 + 0.5:
            continue
        if x > 2.8 and y < -3.1:          # місце підпису «час сповільнено»
            continue
        r = rng.choice([0.025, 0.035, 0.05])
        g.add(Dot([x, y, 0], radius=r, color=FG).set_opacity(rng.uniform(0.5, 1.0)))
    return g


class A09_EinsteinLift(Scene):
    def construct(self):
        row_tag(self, "№9")
        clock = ValueTracker(0.0)
        lab_l = T("трос обірвався", SIZE_BODY).move_to([LEFT_C[0], 3.15, 0])
        lab_r = T("глибокий космос", SIZE_BODY).move_to([RIGHT_C[0], 3.15, 0])
        cab_l, cab_r = cabin(LEFT_C), cabin(RIGHT_C, hook=True)
        stub, sky = cable_stub(), stars()
        shaft = always_redraw(lambda: shaft_view(clock.get_value()))
        in_l = always_redraw(lambda: inside(clock.get_value(), LEFT_C))
        in_r = always_redraw(lambda: inside(clock.get_value(), RIGHT_C))
        v_x = LEFT_C[0] - LIFT_W / 2 - 0.75
        v_top = np.array([v_x, LIFT_Y + 1.4, 0])

        def v_arrow():
            v = G_EFF * clock.get_value()
            if v < 0.1:
                return VGroup(vec(v_top, v_top + DOWN * 0.3, color=C_V).set_opacity(0),
                              M("v", 64, color=C_V).next_to(v_top, LEFT, buff=0.15).set_opacity(0))
            a = vec(v_top, v_top + DOWN * K_V * v, color=C_V)
            return VGroup(a, M("v", 64, color=C_V).next_to(a, LEFT, buff=0.15))

        v_arr = always_redraw(v_arrow)
        note = scale_note(self, f"час сповільнено ×{SLOW}")

        self.add_subcaption("Ліфт без вікон. Ви ширяєте.", duration=4.0)
        first = VGroup(shaft_view(0), inside(0, LEFT_C), inside(0, RIGHT_C))
        self.play(FadeIn(sky), FadeIn(first), FadeIn(cab_l), FadeIn(cab_r), FadeIn(stub),
                  FadeIn(lab_l), FadeIn(lab_r), FadeIn(note), run_time=1.2)
        self.remove(first)
        # порядок шарів: шахта → кабіни → вміст
        self.add(shaft, cab_l, cab_r, stub, in_l, in_r, v_arr)

        def run(t_to, *anims):
            self.play(clock.animate.set_value(t_to), *anims, run_time=t_to - clock.get_value(), rate_func=linear)

        self.add_subcaption("Перший варіант: трос обірвався.", duration=5.0, offset=2.8)
        self.add_subcaption("Другий: глибокий космос, гравітації нема.", duration=T_EQ - 7.8, offset=7.8)
        run(T_EQ)
        eq = M("=", 120, color=ACCENT).move_to([0, LIFT_Y + 0.4, 0])
        same = T("не відрізнити", SIZE_BODY).next_to(eq, DOWN, buff=0.35)
        self.add_subcaption("Зсередини — не відрізнити.", duration=T_RUN - T_EQ)
        run(T_EQ + 1.0, FadeIn(eq, scale=0.6), FadeIn(same, shift=UP * 0.15))
        run(T_RUN)
