"""№4 «Два потяги» — випуск 1.2, блок 3.3 «Потяг поруч». Пріоритет 1.

Глядач бачить: вид із вікна нашого вагона; за вікном упритул стоїть сусідній потяг
(вікна, люди). Потяг поповз — хто рушив, незрозуміло. Потім у вікно входить
нерухомий стовп між коліями — він пливе разом із сусіднім потягом, отже, і стовп,
і сусід стоять, а їдемо ми.

Синхрон: «І раптом — поповзло» → «Ви не знаєте, хто поїхав» → «шукаєте очима щось
третє… Стовп» → «питання зникло». Схема якісна (без чисел), «масштаб умовний» не потрібен.

Фізика: у системі відліку нашого вагона все, що стоїть на землі (сусідній потяг, стовп),
зміщується у вікні на −x(t), де x(t) — наш шлях: рушання з місця з прискоренням A
до швидкості V, далі рівномірно. Стовп і сусідній потяг мають однакове зміщення —
бо обидва нерухомі відносно землі (вид збоку, ортогональна проєкція).
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "style"))
from feynman_style import *  # noqa: E402,F403

# ── Кінематика (умовні одиниці кадру) ───────────────────────────────────────
T_START = 2.5       # с, наш потяг рушає
A = 0.10            # од/с², рушання «повзе»
V = 0.80            # од/с, далі рівномірно
T_ACC = V / A       # 8 с розгону
T_POLE = 10.5       # с, стовп торкається правого краю вікна
T_END = 20.0


def travel(t):
    """Наш шлях x(t) від станції: розгін з місця, далі рівномірно."""
    tau = max(0.0, t - T_START)
    if tau <= T_ACC:
        return 0.5 * A * tau ** 2
    return 0.5 * A * T_ACC ** 2 + V * (tau - T_ACC)


# ── Геометрія вікна ─────────────────────────────────────────────────────────
WIN_C = np.array([0.0, 0.4, 0.0])
WIN_W, WIN_H = 9.6, 4.0
BOX = (WIN_C[0] - WIN_W / 2, WIN_C[0] + WIN_W / 2, WIN_C[1] - WIN_H / 2, WIN_C[1] + WIN_H / 2)

# Сусідній вагон (світові координати; екран = світ − наш шлях)
WAGON_L, GAP = 13.0, 0.6
N_WAGONS = 3
X_FIRST = -9.0                    # лівий край першого вагона
PANE_Y, PANE_H, PANE_W = 0.75, 1.5, 1.7
PANE_DX = [1.4, 4.0, 6.6, 9.2, 11.8]
PEOPLE = {(0, 1), (0, 3), (1, 0), (1, 2), (1, 4), (2, 1), (2, 2)}  # (вагон, вікно) з людьми

POLE_W = 0.34
X_POLE = BOX[1] + POLE_W / 2 + travel(T_POLE)   # стовп торкається краю вікна в T_POLE

BODY = interpolate_color(ManimColor(BG), ManimColor(C_NEG), 0.42)
GLASS = interpolate_color(ManimColor(BG), ManimColor(GRID), 0.5)
BELLOWS = ManimColor(GRID)
FRAME = interpolate_color(ManimColor(BG), ManimColor(MUTED_TEXT), 0.45)


def _clip_rect(x0, x1, y0, y1, box=BOX, **style):
    cx0, cx1 = max(x0, box[0]), min(x1, box[1])
    cy0, cy1 = max(y0, box[2]), min(y1, box[3])
    if cx1 - cx0 < 1e-3 or cy1 - cy0 < 1e-3:
        return None
    return Polygon([cx0, cy0, 0], [cx1, cy0, 0], [cx1, cy1, 0], [cx0, cy1, 0], **style)


def _clip_circle(c, r, box=BOX, **style):
    if c[0] + r <= box[0] or c[0] - r >= box[1]:
        return None
    circ = Circle(radius=r, **style).move_to(c)
    if c[0] - r >= box[0] and c[0] + r <= box[1]:
        return circ
    rect = Polygon([box[0], box[2], 0], [box[1], box[2], 0], [box[1], box[3], 0], [box[0], box[3], 0])
    return Intersection(circ, rect, **style)


def window_view(shift, op=1.0):
    """Що видно у вікні, коли наш вагон проїхав `shift` від станції (op — непрозорість)."""
    g = VGroup()

    def add(m):
        # Незмінна структура групи (порожнє місце — невидима заглушка), щоб become()
        # в always_redraw зіставляв частини одну з одною й не плутав їхні стилі.
        if m is None:
            m = Polygon(ORIGIN, RIGHT * 1e-3, UP * 1e-3, fill_opacity=0, stroke_width=0)
        else:
            m.set_fill(opacity=op * m.get_fill_opacity()).set_stroke(opacity=op)
        g.add(m)

    for k in range(N_WAGONS):
        x0 = X_FIRST + k * (WAGON_L + GAP) - shift
        add(_clip_rect(x0, x0 + WAGON_L, -3, 3, fill_color=BODY, fill_opacity=1, stroke_width=0))
        add(_clip_rect(x0, x0 + WAGON_L, -1.05, -0.8, fill_color=MUTED_TEXT, fill_opacity=1, stroke_width=0))
        # гармошка між вагонами
        gx = x0 + WAGON_L
        add(_clip_rect(gx, gx + GAP, -3, 3, fill_color=BELLOWS, fill_opacity=1, stroke_width=0))
        for j in range(1, 4):
            xr = gx + j * GAP / 4
            add(_clip_rect(xr - 0.025, xr + 0.025, -3, 3, fill_color=FRAME, fill_opacity=1, stroke_width=0))
        for i, dx in enumerate(PANE_DX):
            px = x0 + dx
            pane = (px - PANE_W / 2, px + PANE_W / 2, PANE_Y - PANE_H / 2, PANE_Y + PANE_H / 2)
            add(_clip_rect(*pane, fill_color=GLASS, fill_opacity=1,
                           stroke_color=MUTED_TEXT, stroke_width=SW_AXIS))
            if (k, i) in PEOPLE:
                hx = px + (0.25 if (i + k) % 2 else -0.2)
                inner = (max(pane[0], BOX[0]), min(pane[1], BOX[1]), pane[2], pane[3])
                add(_clip_rect(hx - 0.42, hx + 0.42, pane[2], pane[2] + 0.55, box=inner,
                               fill_color=MUTED_TEXT, fill_opacity=1, stroke_width=0))
                add(_clip_circle(np.array([hx, pane[2] + 0.85, 0]), 0.26, box=inner,
                                 fill_color=MUTED_TEXT, fill_opacity=1, stroke_width=0))
    # нерухомий стовп між коліями (ближче до нас — малюється поверх)
    px = X_POLE - shift
    add(_clip_rect(px - POLE_W / 2, px + POLE_W / 2, -3, 3, fill_color=ACCENT, fill_opacity=1, stroke_width=0))
    for yb in (-1.4, -0.3):
        add(_clip_rect(px - POLE_W / 2 - 0.06, px + POLE_W / 2 + 0.06, yb, yb + 0.14,
                       fill_color=ACCENT, fill_opacity=1, stroke_width=0))
    return g


class A04_TwoTrains(Scene):
    def construct(self):
        row_tag(self, "№4")
        clock = ValueTracker(0.0)

        fade = ValueTracker(0.0)
        view = always_redraw(lambda: window_view(travel(clock.get_value()), fade.get_value()))
        outer = RoundedRectangle(width=WIN_W + 0.8, height=WIN_H + 0.8, corner_radius=0.55).move_to(WIN_C)
        inner = RoundedRectangle(width=WIN_W, height=WIN_H, corner_radius=0.3).move_to(WIN_C)
        frame = Difference(outer, inner, fill_color=FRAME, fill_opacity=1, stroke_color=FG, stroke_width=SW_AXIS)
        sill = RoundedRectangle(width=WIN_W + 1.6, height=0.32, corner_radius=0.08,
                                fill_color=FRAME, fill_opacity=1, stroke_color=FG, stroke_width=SW_AXIS)
        sill.next_to(outer, DOWN, buff=-0.12)

        def run(t_to, *anims):
            self.play(clock.animate.set_value(t_to), *anims, run_time=t_to - clock.get_value(), rate_func=linear)

        # 0 — поруч стоїть інший потяг
        self.add_subcaption("Поруч стоїть інший потяг.", duration=T_START)
        self.add(view)
        run(1.2, fade.animate.set_value(1.0), FadeIn(frame), FadeIn(sill))
        run(T_START)

        # 1 — поповзло: хто рушив?
        self.add_subcaption("І раптом — поповзло.", duration=2.5)
        run(T_START + 2.5)
        ask = T("Хто рушив?", SIZE_TITLE).move_to(UP * 3.25)
        self.add_subcaption("Хто поїхав — ми чи вони?", duration=T_POLE - clock.get_value())
        run(clock.get_value() + 1.0, FadeIn(ask, shift=DOWN * 0.15))
        run(T_POLE)

        # 2 — у вікно входить нерухомий стовп
        pole_lab = T("стовп", SIZE_BODY, ACCENT)
        pole_lab.add_updater(lambda m: m.move_to(
            [X_POLE - travel(clock.get_value()) + POLE_W / 2 + 0.2 + m.width / 2, 1.95, 0]))
        self.add_subcaption("Шукаємо щось нерухоме. Стовп!", duration=4.5)
        run(T_POLE + 1.8)
        self.add(pole_lab)
        run(T_POLE + 2.6, FadeIn(pole_lab))
        run(T_POLE + 4.5)

        # 3 — відповідь: стовп пливе разом із сусідом → стоять обидва, їдемо ми
        verdict = T("Стовп стоїть — їдемо ми", SIZE_TITLE).move_to(UP * 3.25)
        verdict[-2:].set_color(C_V)
        y_arr = sill.get_bottom()[1] - 0.45
        arrow = vec([-1.3, y_arr, 0], [1.3, y_arr, 0], color=C_V)
        v_lab = M("v", 64, color=C_V).next_to(arrow, RIGHT, buff=0.2)
        self.add_subcaption("Стовп стоїть — отже, їдемо ми.", duration=T_END - clock.get_value())
        run(clock.get_value() + 1.2, FadeOut(ask, shift=UP * 0.15), FadeIn(verdict, shift=DOWN * 0.15))
        run(clock.get_value() + 1.0, GrowArrow(arrow), FadeIn(v_lab))
        run(T_END)
