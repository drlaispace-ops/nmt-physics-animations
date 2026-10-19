"""№8 «Візочок Фейнмана» — випуск 1.2, врізка «Хлопчик, візочок і куля». Пріоритет 1.

Глядач бачить ту саму подію двічі:
(а) камера їде разом із візком: хлопчик різко тягне — м'ячик «котиться назад» до задньої
    стінки; різко зупиняє — м'ячик «котиться вперед»;
(б) камера стоїть на землі: м'ячик майже стоїть (пунктир — де він був), а задня стінка
    візка під'їжджає до нього; після зупинки візка м'ячик просто їде далі.

Фізика (рахується, не малюється на око): візок — рушання з прискоренням A_PULL до V_CART,
рівномірно, гальмування A_BRAKE. М'ячик котиться без проковзування по дну візка: суцільна
куля на прискореній підлозі має прискорення відносно землі (2/7)·a візка, відносно візка —
(5/7)·a назад. Удари об стінки — непружні (м'ячик зупиняється відносно візка).
Тому «майже стоїть», як і в сценарії. Обидва кадри — один і той самий розрахунок,
різниться лише система відліку камери.

Синхрон: (а) «різко тягне — котиться назад… різко зупиняє — котиться вперед»;
(б) «а тепер подивись збоку… задня стінка під'їжджає до нього».
Схема якісна (без чисел і осей) — підпис про масштаб не потрібен.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "style"))
from feynman_style import *  # noqa: E402,F403

# ── Розрахунок руху (одиниці кадру, с) ──────────────────────────────────────
A_PULL, T_PULL = 0.5, 2.0          # рушання
V_CART = A_PULL * T_PULL           # 1 од/с
T_BRAKE, A_BRAKE = 4.6, 1.0        # коли й як різко гальмує
T_MOTION = 11.2
K_ROLL = 2 / 7                     # суцільна куля без проковзування: a_кулі = 2/7 · a_візка

HALF_IN = 2.4                      # півдовжина дна візка (всередині)
R_BALL = 0.5
X_FREE = HALF_IN - R_BALL          # межа руху центру кулі відносно візка
WALL_H = 1.3
R_WHEEL = 0.48
GROUND_Y = -1.5
FLOOR_Y = GROUND_Y + 2 * R_WHEEL + 0.18      # верх дна візка
BALL_Y = FLOOR_Y + R_BALL


def cart_acc(t):
    if 0 <= t < T_PULL:
        return A_PULL
    if T_BRAKE <= t < T_BRAKE + V_CART / A_BRAKE:
        return -A_BRAKE
    return 0.0


def simulate(dt=1 / 1000):
    """Візок і куля в системі землі; повертає таблицю t, x_візка, v_візка, x_кулі_відн, v_кулі_відн."""
    n = int(T_MOTION / dt) + 1
    out = np.zeros((n, 5))
    xc = vc = 0.0
    xr = vr = 0.0          # куля відносно візка
    for i in range(n):
        t = i * dt
        out[i] = t, xc, vc, xr, vr
        a = cart_acc(t)
        at_back, at_front = xr <= -X_FREE + 1e-9, xr >= X_FREE - 1e-9
        if (at_back and a >= 0) or (at_front and a <= 0):
            ar = 0.0       # стінка тримає кулю — їде разом із візком
            vr = 0.0
        else:
            ar = (K_ROLL - 1) * a      # відносне прискорення = −5/7 · a
        vc += a * dt
        xc += vc * dt
        vr += ar * dt
        xr += vr * dt
        if xr < -X_FREE:   # непружний удар об задню стінку
            xr, vr = -X_FREE, 0.0
        if xr > X_FREE:    # … об передню
            xr, vr = X_FREE, 0.0
    return out


TABLE = simulate()


def state(t):
    t = float(np.clip(t, 0, T_MOTION))
    return [np.interp(t, TABLE[:, 0], TABLE[:, k]) for k in range(1, 5)]


T_HIT_BACK = TABLE[np.argmax(TABLE[:, 3] <= -X_FREE + 1e-6), 0]     # ≈3,2 с
T_HIT_FRONT = TABLE[np.argmax(TABLE[:, 3] >= X_FREE - 1e-6), 0]     # ≈9,8 с

K_ARROW = 1.4                      # довжина стрілки на 1 од/с
CART_FILL = interpolate_color(ManimColor(BG), ManimColor(C_X), 0.35)
BOY = FG


def _limb(a, b):
    return Line(a, b, color=BOY, stroke_width=7).set_cap_style(CapStyleType.ROUND)


def boy(x_hand, stride_phase):
    """Хлопчик іде праворуч, рука відведена назад — тримає мотузку візка."""
    hip = np.array([x_hand + 0.85, GROUND_Y + 1.12, 0])
    sh = hip + np.array([0.14, 0.9, 0])
    th = 0.42 * np.sin(stride_phase)
    leg = 1.12
    f1 = hip + leg * np.array([np.sin(th), -np.cos(th), 0])
    f2 = hip + leg * np.array([-np.sin(th), -np.cos(th), 0])
    hand = np.array([x_hand, GROUND_Y + 1.0, 0])
    elbow = (sh + hand) / 2 + np.array([0.1, -0.12, 0])
    arm2 = sh + 0.7 * np.array([np.sin(-th) + 0.3, -np.cos(th), 0])
    head = Circle(radius=0.36, color=BOY, fill_color=BOY, fill_opacity=1, stroke_width=0).move_to(sh + UP * 0.5)
    return VGroup(_limb(hip, sh), _limb(hip, f1), _limb(hip, f2), _limb(sh, elbow), _limb(elbow, hand),
                  _limb(sh, arm2), head)


def velocity_arrow(start, v):
    if abs(v) < 0.05:
        return vec(start, start + RIGHT * 0.3, color=C_V).set_opacity(0)
    return vec(start, start + RIGHT * K_ARROW * v, color=C_V)


def picture(t, ground_frame, x0, show_cart_arrow=False, marker_x=None):
    """Кадр у момент t. ground_frame=False — камера їде з візком (візок стоїть у x0)."""
    xc, vc, xr, vr = state(t)
    cx = x0 + (xc if ground_frame else 0.0)          # центр візка на екрані
    shift_ground = 0.0 if ground_frame else -xc       # як зміщується земля в кадрі
    g = VGroup()
    # земля: лінія + камінці (рівно 18 штук — незмінна структура)
    g.add(Line([-7.6, GROUND_Y, 0], [7.6, GROUND_Y, 0], color=FG, stroke_width=SW_AXIS))
    span, n = 15.3, 18
    for j in range(n):
        x = ((j * span / n + shift_ground) % span) - span / 2
        g.add(Line([x, GROUND_Y - 0.12, 0], [x - 0.25, GROUND_Y - 0.4, 0], color=MUTED_TEXT, stroke_width=SW_AXIS))
    # пунктир «де був м'ячик» (лише з землі)
    if marker_x is not None:
        g.add(DashedLine([marker_x, GROUND_Y, 0], [marker_x, FLOOR_Y + WALL_H + 0.9, 0], color=ACCENT,
                         stroke_width=SW_AXIS, dash_length=0.12))
    # візок
    x_l, x_r = cx - HALF_IN, cx + HALF_IN
    body = VGroup(
        Polygon([x_l - 0.12, FLOOR_Y - 0.18, 0], [x_r + 0.12, FLOOR_Y - 0.18, 0], [x_r + 0.12, FLOOR_Y + WALL_H, 0],
                [x_r, FLOOR_Y + WALL_H, 0], [x_r, FLOOR_Y, 0], [x_l, FLOOR_Y, 0], [x_l, FLOOR_Y + WALL_H, 0],
                [x_l - 0.12, FLOOR_Y + WALL_H, 0], fill_color=CART_FILL, fill_opacity=1, stroke_color=FG,
                stroke_width=SW_BODY),
    )
    g.add(body)
    ang = -xc / R_WHEEL                                 # колеса котяться по землі
    for wx in (x_l + 0.8, x_r - 0.8):
        c = np.array([wx, GROUND_Y + R_WHEEL, 0])
        wheel = VGroup(Circle(radius=R_WHEEL, color=FG, stroke_width=SW_BODY, fill_color=BG, fill_opacity=1).move_to(c),
                       Line(c + LEFT * R_WHEEL, c + RIGHT * R_WHEEL, color=FG, stroke_width=SW_AXIS),
                       Line(c + DOWN * R_WHEEL, c + UP * R_WHEEL, color=FG, stroke_width=SW_AXIS))
        wheel[1:].rotate(ang, about_point=c)
        g.add(wheel)
    # м'ячик: котиться по дну без проковзування → кут = −(шлях відносно візка)/r
    bc = np.array([cx + xr, BALL_Y, 0])
    ball = VGroup(Circle(radius=R_BALL, color=ACCENT, fill_color=ACCENT, fill_opacity=1, stroke_width=0).move_to(bc),
                  Line(bc + LEFT * R_BALL * 0.85, bc + RIGHT * R_BALL * 0.85, color=BG, stroke_width=SW_BODY + 2))
    ball[1].rotate(-xr / R_BALL, about_point=bc)
    g.add(ball)
    # хлопчик і мотузка
    hand_x = x_r + 1.5
    stride = 2 * PI * xc / 1.5
    rope_a = np.array([x_r + 0.12, FLOOR_Y + WALL_H * 0.7, 0])
    g.add(Line(rope_a, [hand_x, GROUND_Y + 1.0, 0], color=FG, stroke_width=SW_AXIS))
    g.add(boy(hand_x, stride))
    # стрілки швидкості: м'ячика (у системі камери) і візка (лише з землі)
    v_ball_screen = vr + (vc if ground_frame else 0.0)
    g.add(velocity_arrow(bc + UP * (R_BALL + 0.35), v_ball_screen))
    if show_cart_arrow:
        g.add(velocity_arrow(np.array([cx + 0.4, FLOOR_Y + WALL_H + 0.45, 0]), vc))
    return g


X_A = -1.5       # (а) візок стоїть у кадрі тут
X_B = -3.5       # (б) візок рушає звідси


class A08_FeynmanWagon(Scene):
    def construct(self):
        row_tag(self, "№8")
        clock = ValueTracker(0.0)

        def run(t_to, *anims):
            self.play(clock.animate.set_value(t_to), *anims, run_time=t_to - clock.get_value(), rate_func=linear)

        # ── (а) камера їде з візком ─────────────────────────────────────────
        h_a = T("Камера їде разом із візком", SIZE_TITLE).move_to(UP * 3.15)
        pic_a = always_redraw(lambda: picture(clock.get_value(), False, X_A))
        first = picture(0.0, False, X_A)
        self.add_subcaption("Хлопчик різко тягне візок.", duration=2.5)
        self.play(FadeIn(first), FadeIn(h_a), run_time=1.0)
        self.remove(first)
        self.add(pic_a)
        self.wait(0.5)
        self.add_subcaption("М'ячик котиться назад!", duration=T_BRAKE - 1.0, offset=1.0)
        self.add_subcaption("Різко зупинив — котиться вперед.", duration=T_MOTION - T_BRAKE + 1.0,
                            offset=T_BRAKE)
        run(T_MOTION)
        self.wait(1.0)

        # ── (б) камера стоїть на землі ─────────────────────────────────────
        clock.set_value(0.0)
        h_b = T("Камера стоїть на землі", SIZE_TITLE).move_to(UP * 3.15)
        pic_b = always_redraw(lambda: picture(clock.get_value(), True, X_B, show_cart_arrow=True, marker_x=X_B))
        first_b = picture(0.0, True, X_B, show_cart_arrow=True, marker_x=X_B)
        self.remove(pic_a)
        last_a = picture(T_MOTION, False, X_A)
        self.add(last_a)
        self.add_subcaption("А тепер — збоку, з землі.", duration=2.0)
        self.play(FadeOut(last_a), FadeOut(h_a, shift=UP * 0.2), run_time=0.7)
        self.play(FadeIn(first_b), FadeIn(h_b, shift=UP * 0.2), run_time=0.8)
        self.remove(first_b)
        self.add(pic_b)
        self.wait(0.5)
        self.add_subcaption("М'ячик майже стоїть — стінка під'їжджає.", duration=T_BRAKE)
        self.add_subcaption("Візок зупинився — м'ячик котиться далі.", duration=T_MOTION - T_BRAKE + 2.0,
                            offset=T_BRAKE)
        run(T_MOTION)
        self.wait(2.0)
