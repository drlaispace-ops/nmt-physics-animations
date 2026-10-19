"""№7 «Каюта Галілея» — випуск 1.2, блок 3.4 «Корабель Галілея» (Dialogo, 1632). Пріоритет 1.

Глядач бачить: каюту під палубою — метелики літають на всі боки, рибки плавають
в акваріумі, з підвішеного відра краплі падають у посудину. У ілюмінаторі — порт.
Потім корабель пливе рівно (у ілюмінаторі пропливає берег, угорі — стрілка швидкості),
а все в каюті відбувається ТОЧНІСІНЬКО так само.

Вимога ТЗ: «другий кадр має бути фізично тим самим». Усе, що в каюті, рахує одна
функція `cabin_life(t)` від часу петлі t ∈ [0, T_LOOP); обидва стани — це той самий
виклик `cabin_loop()` з тією самою тривалістю, різниться лише ілюмінатор і напис.
Усі рухи в каюті періодичні з періодом T_LOOP, тож монтаж може зациклити кожну половину.

Фізика крапель: справжнє g = 9,8 м/с² у масштабі каюти (M_PER_UNIT), час реальний,
тому підпис про час не потрібен. Схема якісна — «масштаб умовний» не потрібен.

Межа половин: 1,2 с (вхід) + T_LOOP = 15,2 с.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "style"))
sys.path.insert(0, str(Path(__file__).resolve().parent))
from feynman_style import *  # noqa: E402,F403
from calc_1 import G  # noqa: E402

T_LOOP = 14.0                # с, період усього життя каюти
T_INTRO = 1.2

# ── Каюта (кадр) ────────────────────────────────────────────────────────────
CAB = (-6.0, 6.0, -3.1, 2.5)               # x0, x1, y0, y1
M_PER_UNIT = 2.4 / (CAB[3] - CAB[2])       # висота каюти 2,4 м
G_U = G / M_PER_UNIT                       # g в од/с²

PORT_C, PORT_R = np.array([-4.1, 0.85, 0]), 1.25
BUCKET_X, SPOUT_Y = 0.3, 1.05
BASIN_TOP, WATER_Y = -2.1, -2.3
H_FALL = SPOUT_Y - WATER_Y
T_FALL = np.sqrt(2 * H_FALL / G_U)         # ≈0,58 с
DRIP = 1.0                                 # с між краплями (T_LOOP кратне DRIP)
SPLASH = 0.35

BOWL_C, BOWL_R = np.array([3.9, -0.55, 0]), 1.3
WATER_TOP = BOWL_C[1] + 0.55 * BOWL_R

# Метелики: центр, амплітуди, цілі частоти (оборотів за петлю), фази — замкнені криві
BUTTERFLIES = [
    (np.array([-0.8, 1.0, 0]), 1.6, 0.5, 1, 2, 0.0, 0.3),
    (np.array([1.3, 0.2, 0]), 1.2, 0.7, 2, 3, 1.3, 2.0),
    (np.array([-1.9, -0.9, 0]), 1.1, 0.5, 1, 3, 2.4, 0.9),
]
FLAP_HZ = 4                                # помахів за секунду (ціле → періодично)
# Рибки: центр, амплітуда, частота (разів за петлю), фаза, розмір
FISH = [
    (BOWL_C + np.array([0, 0.0, 0]), 0.55, 2, 0.0, 1.45),
    (BOWL_C + np.array([0, -0.55, 0]), 0.45, 3, 2.0, 1.15),
]

WOOD = interpolate_color(ManimColor(BG), ManimColor(C_X), 0.16)
WOOD_LINE = interpolate_color(ManimColor(BG), ManimColor(C_X), 0.32)
WATER = interpolate_color(ManimColor(BG), ManimColor(C_WAVE), 0.45)
SKY = interpolate_color(ManimColor(BG), ManimColor(C_WAVE), 0.22)
SEA = interpolate_color(ManimColor(BG), ManimColor(C_WAVE), 0.5)
LAND = interpolate_color(ManimColor(BG), ManimColor(MUTED_TEXT), 0.4)
STONE = interpolate_color(ManimColor(BG), ManimColor(MUTED_TEXT), 0.45)

V_COAST, V_WAVES = 0.32, 1.1               # од/с у ілюмінаторі, коли корабель пливе


def _w(phase):
    return 2 * PI * phase


def _empty():
    return Polygon(ORIGIN, RIGHT * 1e-3, UP * 1e-3, fill_opacity=0, stroke_width=0)


# ── Життя каюти: одна функція часу петлі ───────────────────────────────────
def butterfly(c, flap, color=C_LIGHT, s=1.7):
    k = 0.3 + 0.7 * abs(np.cos(flap))      # помах: крила стискаються по горизонталі
    g = VGroup()
    for side in (-1, 1):
        up = Ellipse(width=0.34 * s * k, height=0.26 * s, color=color, fill_color=color, fill_opacity=0.95,
                     stroke_width=0).rotate(side * 0.5).move_to(c + np.array([side * 0.17 * s * k, 0.08 * s, 0]))
        lo = Ellipse(width=0.22 * s * k, height=0.17 * s, color=color, fill_color=color, fill_opacity=0.95,
                     stroke_width=0).rotate(-side * 0.5).move_to(c + np.array([side * 0.12 * s * k, -0.1 * s, 0]))
        g.add(up, lo)
    g.add(Ellipse(width=0.07 * s, height=0.32 * s, color=BG, fill_color=BG, fill_opacity=1, stroke_width=0).move_to(c))
    return g


def fish(c, facing, size, color=C_X):
    """facing ∈ [−1, 1]: знак — куди дивиться, модуль — «поворот» (стискання)."""
    sx = np.sign(facing) * max(abs(facing), 0.15)
    body = Ellipse(width=0.55 * size, height=0.3 * size, color=color, fill_color=color, fill_opacity=1, stroke_width=0)
    tail = Polygon([-0.25 * size, 0, 0], [-0.45 * size, 0.15 * size, 0], [-0.45 * size, -0.15 * size, 0],
                   color=color, fill_color=color, fill_opacity=1, stroke_width=0)
    eye = Dot([0.15 * size, 0.04 * size, 0], radius=0.035 * size, color=BG)
    g = VGroup(tail, body, eye)
    g.stretch(sx, 0, about_point=ORIGIN)
    return g.shift(c)


def cabin_life(t):
    """Усе, що рухається в каюті, у момент t петлі. Незмінна структура для always_redraw."""
    t = t % T_LOOP
    g = VGroup()
    # краплі: відпускаються щосекунди, падають з прискоренням g
    tau = (t - 0.3) % DRIP
    if tau < T_FALL:
        y = SPOUT_Y - 0.5 * G_U * tau ** 2
        g.add(Ellipse(width=0.18, height=0.28, color=C_WAVE, fill_color=C_WAVE, fill_opacity=1,
                      stroke_width=0).move_to([BUCKET_X, y - 0.14, 0]))
    else:
        g.add(_empty())
    if T_FALL <= tau < T_FALL + SPLASH:
        a = (tau - T_FALL) / SPLASH
        g.add(Ellipse(width=0.25 + 0.9 * a, height=0.08 + 0.14 * a, color=C_WAVE,
                      stroke_width=SW_AXIS, stroke_opacity=1 - a).move_to([BUCKET_X, WATER_Y, 0]))
    else:
        g.add(_empty())
    # рибки
    for c, amp, k, ph, size in FISH:
        th = _w(k * t / T_LOOP) + ph
        pos = c + np.array([amp * np.sin(th), 0.07 * np.sin(_w(5 * t / T_LOOP) + ph), 0])
        g.add(fish(pos, np.cos(th), size))
    # метелики
    for c, ax, ay, n, m, px, py in BUTTERFLIES:
        pos = c + np.array([ax * np.sin(_w(n * t / T_LOOP) + px), ay * np.sin(_w(m * t / T_LOOP) + py), 0])
        g.add(butterfly(pos, PI * FLAP_HZ * t + px))
    return g


def cabin_static():
    x0, x1, y0, y1 = CAB
    room = RoundedRectangle(width=x1 - x0, height=y1 - y0, corner_radius=0.3, fill_color=WOOD, fill_opacity=1,
                            stroke_color=FG, stroke_width=SW_BODY).move_to([(x0 + x1) / 2, (y0 + y1) / 2, 0])
    planks = VGroup(*[Line([x0 + 0.15, y, 0], [x1 - 0.15, y, 0], color=WOOD_LINE, stroke_width=SW_AXIS)
                      for y in np.arange(y0 + 0.6, y1 - 0.2, 0.6)])
    beams = VGroup(*[Line([x, y1 - 0.02, 0], [x, y1 - 0.35, 0], color=WOOD_LINE, stroke_width=SW_BODY * 2)
                     for x in np.arange(x0 + 1.0, x1, 2.0)])
    # відро на мотузці
    rope = Line([BUCKET_X, y1, 0], [BUCKET_X, 1.95, 0], color=FG, stroke_width=SW_AXIS)
    bucket = Polygon([BUCKET_X - 0.6, 1.95, 0], [BUCKET_X + 0.6, 1.95, 0], [BUCKET_X + 0.42, 1.2, 0],
                     [BUCKET_X - 0.42, 1.2, 0], color=FG, stroke_width=SW_AXIS, fill_color=STONE, fill_opacity=1)
    spout = Line([BUCKET_X, 1.2, 0], [BUCKET_X, SPOUT_Y, 0], color=FG, stroke_width=SW_BODY)
    # посудина на підлозі
    basin = Polygon([BUCKET_X - 0.85, BASIN_TOP, 0], [BUCKET_X + 0.85, BASIN_TOP, 0], [BUCKET_X + 0.62, y0 + 0.05, 0],
                    [BUCKET_X - 0.62, y0 + 0.05, 0], color=FG, stroke_width=SW_AXIS, fill_color=STONE, fill_opacity=1)
    basin_w = Polygon([BUCKET_X - 0.79, WATER_Y, 0], [BUCKET_X + 0.79, WATER_Y, 0], [BUCKET_X + 0.63, y0 + 0.1, 0],
                      [BUCKET_X - 0.63, y0 + 0.1, 0], stroke_width=0, fill_color=WATER, fill_opacity=1)
    # акваріум на столику
    leg_top = BOWL_C[1] - BOWL_R
    table = VGroup(
        Rectangle(width=3.0, height=0.12, color=FG, stroke_width=SW_AXIS, fill_color=WOOD_LINE,
                  fill_opacity=1).move_to([BOWL_C[0], leg_top - 0.06, 0]),
        Line([BOWL_C[0] - 1.2, leg_top - 0.12, 0], [BOWL_C[0] - 1.2, y0 + 0.02, 0], color=FG, stroke_width=SW_BODY),
        Line([BOWL_C[0] + 1.2, leg_top - 0.12, 0], [BOWL_C[0] + 1.2, y0 + 0.02, 0], color=FG, stroke_width=SW_BODY),
    )
    disc = Circle(radius=BOWL_R).move_to(BOWL_C)
    below = Rectangle(width=3 * BOWL_R, height=2 * BOWL_R).move_to([BOWL_C[0], WATER_TOP - BOWL_R, 0])
    water = Intersection(disc, below, stroke_width=0, fill_color=WATER, fill_opacity=1)
    bowl = Arc(radius=BOWL_R, start_angle=PI / 2 + 0.55, angle=2 * PI - 1.1, color=FG,
               stroke_width=SW_BODY).move_arc_center_to(BOWL_C)
    return VGroup(room, planks, beams, rope, bucket, spout, basin, basin_w, table, water), bowl


# ── Ілюмінатор ─────────────────────────────────────────────────────────────
# Вид у ілюмінаторі будується в одиничному колі R0 з центром у початку координат,
# потім масштабується до PORT_R і ставиться в PORT_C.
R0 = 0.95


def _place(g):
    return g.scale(PORT_R / R0, about_point=ORIGIN).shift(PORT_C)


def _clip(m):
    disc = Circle(radius=R0 - 0.02)
    out = Intersection(m, disc, fill_color=m.get_fill_color(), fill_opacity=m.get_fill_opacity(), stroke_width=0)
    return out if len(out.points) else _empty()


def _p(x, y):
    return np.array([x, y, 0.0])


def porthole_base():
    disc = Circle(radius=R0, fill_color=SKY, fill_opacity=1, stroke_width=0)
    sea = _clip(Rectangle(width=3, height=1.2, fill_color=SEA, fill_opacity=1).move_to(DOWN * 0.75))
    return _place(VGroup(disc, sea))


def porthole_frame():
    r = PORT_R + 0.1
    return VGroup(Circle(radius=r, color=FG, stroke_width=SW_BODY * 2).move_to(PORT_C),
                  *[Dot(PORT_C + r * np.array([np.cos(a), np.sin(a), 0]), radius=0.06, color=BG)
                    for a in np.linspace(0, 2 * PI, 8, endpoint=False)])


def port_view():
    """Порт: причальна стінка, тумба, будиночок, вежа — нерухомі."""
    quay = _clip(Rectangle(width=3, height=0.6, fill_color=STONE, fill_opacity=1).move_to(DOWN * 0.45))
    house = _clip(Polygon(_p(-0.7, -0.15), _p(-0.05, -0.15), _p(-0.05, 0.4), _p(-0.37, 0.7), _p(-0.7, 0.4),
                          fill_color=WOOD_LINE, fill_opacity=1))
    tower = _clip(Rectangle(width=0.3, height=1.2, fill_color=STONE, fill_opacity=1).move_to(_p(0.45, 0.3)))
    bollard = _clip(RoundedRectangle(width=0.16, height=0.22, corner_radius=0.05, fill_color=FG,
                                     fill_opacity=1).move_to(_p(0.15, -0.05)))
    return _place(VGroup(quay, house, tower, bollard))


def _hills(x):
    return 0.12 + 0.1 * np.sin(1.7 * x) + 0.06 * np.sin(4.1 * x + 1.0)


def sea_view(t, op=1.0):
    """Корабель пливе праворуч: далекий берег і хвилі пливуть ліворуч. op — непрозорість."""
    g = VGroup()
    off = V_COAST * t
    xs = np.linspace(-1.2, 1.2, 40)
    pts = [_p(x, -0.3 + _hills(x + off)) for x in xs] + [_p(1.2, -0.32), _p(-1.2, -0.32)]
    g.add(_clip(Polygon(*pts, fill_color=LAND, fill_opacity=1, stroke_width=0)))
    lx = 1.4 - (off % 3.6)                                  # маяк на березі
    yb = -0.3 + _hills(lx + off) - 0.05
    g.add(_clip(Polygon(_p(lx - 0.07, yb), _p(lx + 0.07, yb), _p(lx + 0.04, 0.3), _p(lx - 0.04, 0.3),
                        fill_color=FG, fill_opacity=1)))
    for row, (yy, sp) in enumerate([(-0.45, V_WAVES * 0.6), (-0.7, V_WAVES)]):   # ближчі хвилі — швидші
        half = np.sqrt(max(R0 ** 2 - yy ** 2, 0)) - 0.15
        for j in range(5):
            x = ((j * 0.55 + row * 0.27 - sp * t) % 2.75) - 1.375
            fade = float(np.clip((half - abs(x)) / 0.25, 0, 1))
            g.add(Ellipse(width=0.3, height=0.07, fill_color=FG, fill_opacity=0.8 * fade, stroke_width=0)
                  .move_to(_p(x, yy)))
    for m in g:
        m.set_fill(opacity=op * m.get_fill_opacity())
    return _place(g)


class A07_GalileoCabin(Scene):
    def cabin_loop(self, clock, *anims_at_start):
        """Одна петля життя каюти. Викликається двічі — порт і плавба — однаково."""
        t0 = clock.get_value()
        if anims_at_start:
            self.play(clock.animate.set_value(t0 + 0.8), *anims_at_start, run_time=0.8, rate_func=linear)
        self.play(clock.animate.set_value(t0 + T_LOOP), run_time=t0 + T_LOOP - clock.get_value(), rate_func=linear)

    def construct(self):
        row_tag(self, "№7")
        clock = ValueTracker(0.0)
        cabin, bowl = cabin_static()
        life = always_redraw(lambda: cabin_life(clock.get_value()))
        base, frame = porthole_base(), porthole_frame()
        port = port_view()
        h1 = T("Корабель у порту", SIZE_TITLE).move_to(UP * 3.15)

        # вхід: перший кадр петлі, час стоїть
        self.add_subcaption("Каюта. Корабель стоїть у порту.", duration=T_INTRO + 2.8)
        first = cabin_life(0.0)
        self.play(FadeIn(cabin), FadeIn(base), FadeIn(port), FadeIn(frame), FadeIn(h1),
                  FadeIn(first), FadeIn(bowl), run_time=T_INTRO)
        self.remove(first)
        self.add(life, bowl)

        # ПЕТЛЯ 1 — у порту
        self.add_subcaption("Метелики, рибки, краплі.", duration=4.0, offset=2.8)
        self.add_subcaption("Краплі падають прямо в посудину.", duration=6.0, offset=6.8)
        self.cabin_loop(clock)

        # ПЕТЛЯ 2 — пливе рівно. Каюта — той самий виклик; міняється лише ілюмінатор і напис
        sail_clock, sea_op = ValueTracker(0.0), ValueTracker(0.0)
        sea = always_redraw(lambda: sea_view(sail_clock.get_value(), sea_op.get_value()))
        sail_clock.add_updater(lambda m, dt: m.increment_value(dt))
        arrow = vec(ORIGIN, RIGHT * 1.3, color=C_V)
        h2 = VGroup(T("Корабель пливе рівно", SIZE_TITLE), arrow, M("v", 64, color=C_V)).arrange(RIGHT, buff=0.3)
        h2.move_to(UP * 3.15)
        self.add(sail_clock)
        self.add(sea)
        self.bring_to_front(frame, life, bowl)
        self.add_subcaption("Корабель пливе — рівно, без хитавиці.", duration=4.0)
        self.add_subcaption("А в каюті — нічого не змінилося.", duration=T_LOOP - 4.0, offset=4.0)
        self.cabin_loop(clock, FadeOut(port), sea_op.animate.set_value(1.0),
                        AnimationGroup(FadeOut(h1, shift=UP * 0.2), FadeIn(h2, shift=UP * 0.2), lag_ratio=1.0))
