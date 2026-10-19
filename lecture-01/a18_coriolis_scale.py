"""№18 «Масштаб Коріоліса» — випуск 1.3, врізка «Міф про зливу». Пріоритет 3.

Глядач бачить: раковину 40 см на весь кадр і масштабну лінійку «10 см». Камера плавно
віддаляється (експоненційний зум, 6,2 порядку): раковина зникає, лінійка проходить
1 м → 1 км → 100 км; кілька секунд кадр майже порожній — і лише наприкінці з-за краю
«в'їжджає» циклон 1000 км. Раковина й циклон увесь час в одному масштабі
(«справжній масштаб»). Фінал: кільце «раковина тут» — у кадрі 1080p вона займає
≈0,0003 пікселя; 1000 км / 40 см = 2,5·10⁶.

Фізика/геометрія: усі розміри множаться на той самий масштаб s (одиниць кадру на метр);
s спадає від 8 до 5,2·10⁻⁶. Раковина закручена за годинниковою, циклон (Північна півкуля) —
проти: напрямок у раковині вирішують інші чинники. Без обертання в часі — підпис про час не потрібен.

Синхрон: «Уся штука в масштабі… потрібні тисячі кілометрів» → зум;
«Циклон — так. Ваша раковина діаметром сорок сантиметрів… — ні» → фінальний кадр.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "style"))
sys.path.insert(0, str(Path(__file__).resolve().parent))
from feynman_style import *  # noqa: E402,F403
from calc_1 import CYCLONE_D, SINK_D, SCALE_RATIO_18, ua  # noqa: E402

# ── Розрахунки для цієї сцени (calc_1 не змінюємо) ──────────────────────────
P = np.array([-4.4, -0.1, 0])     # центр раковини на екрані (нерухомий під час зуму)
S0 = 3.2 / SINK_D                 # одиниць кадру на метр на старті: раковина 3,2 одиниці
CYC_SD = 5.2                      # діаметр циклону на екрані наприкінці
S1 = CYC_SD / CYCLONE_D           # одиниць на метр наприкінці
Z1 = np.log10(S0 / S1)            # 6,19 порядку зуму
CYC_X = 2.2                       # де опиниться центр циклону
DX = (CYC_X - P[0]) / S1          # м: від раковини до центру циклону (≈1300 км)
SINK_PX = SINK_D * S1 * 1080 / 8  # ширина раковини в пікселях кадру 1080p наприкінці (≈0,0003)
UNITS = {-1: "10 см", 0: "1 м", 1: "10 м", 2: "100 м", 3: "1 км", 4: "10 км", 5: "100 км", 6: "1000 км"}
BAR = np.array([-6.3, 2.75, 0])   # лівий кінець масштабної лінійки


def tex_sci(x, nd=1):
    exp = int(np.floor(np.log10(abs(x))))
    mant = ua(x / 10 ** exp, nd).replace(",", "{,}")
    return rf"{mant}\cdot 10^{{{exp}}}"


def spiral(arms, r0, b, sign, color, opacity, width):
    """Логарифмічні спіралі r = r0·e^(bθ) до r = 1; sign = +1 проти годинникової, −1 — за."""
    g = VGroup()
    th_max = np.log(1 / r0) / b
    th = np.linspace(0, th_max, 120)
    r = r0 * np.exp(b * th)
    for j in range(arms):
        a = 2 * np.pi * j / arms + sign * th
        g.add(VMobject(stroke_color=color, stroke_width=width, stroke_opacity=opacity)
              .set_points_smoothly(np.c_[r * np.cos(a), r * np.sin(a), 0 * r]))
    return g


def sink_template():
    """Раковина одиничного радіуса: чаша, злив, вода закручена за годинниковою."""
    bowl = Circle(radius=1, stroke_color=FG, stroke_width=SW_BODY, fill_color=C_WAVE, fill_opacity=0.22)
    swirl = spiral(3, 0.1, 0.5, -1, C_WAVE, 1.0, SW_CURVE).scale(0.85, about_point=ORIGIN)
    drain = Circle(radius=0.08, stroke_color=FG, stroke_width=SW_AXIS, fill_color=FG, fill_opacity=0.6)
    return VGroup(bowl, swirl, drain)


def cyclone_template():
    """Циклон одиничного радіуса: хмарні рукави проти годинникової (Північна півкуля) і око."""
    mass = Circle(radius=1, stroke_width=0, fill_color=FG, fill_opacity=0.07)
    arms = spiral(5, 0.07, 0.32, +1, FG, 0.8, SW_CURVE)
    eye = Circle(radius=0.06, stroke_color=FG, stroke_width=SW_AXIS)
    return VGroup(mass, arms, eye)


SINK, CYCLONE = sink_template(), cyclone_template()


class A18_CoriolisScale(Scene):
    def construct(self):
        row_tag(self, "№18")
        scale_note(self, "справжній масштаб")
        z = ValueTracker(0.0)

        def s():
            return S0 * 10 ** (-z.get_value())

        def world():
            g = VGroup()
            r_sink = SINK_D / 2 * s()
            if r_sink > 0.004:
                g.add(SINK.copy().scale(r_sink, about_point=ORIGIN).shift(P))
            r_cyc = CYCLONE_D / 2 * s()
            cx = P[0] + DX * s()
            if r_cyc < 80 and cx - r_cyc < 7.4:
                g.add(CYCLONE.copy().scale(r_cyc, about_point=ORIGIN).move_to([cx, P[1], 0]))
            return g

        def scale_bar():
            k = int(np.ceil(np.log10(0.35 / s())))
            length = 10.0 ** k * s()
            end = BAR + RIGHT * length
            bar = VGroup(Line(BAR, end, color=FG, stroke_width=SW_BODY),
                         Line(BAR + DOWN * 0.12, BAR + UP * 0.12, color=FG, stroke_width=SW_BODY),
                         Line(end + DOWN * 0.12, end + UP * 0.12, color=FG, stroke_width=SW_BODY))
            lab = T(UNITS.get(k, ""), 32).next_to(BAR, UP, buff=0.22, aligned_edge=LEFT)
            return VGroup(bar, lab)

        def marker():
            """Кільце довкола раковини, щойно вона стає меншою за саме кільце."""
            r_sink = SINK_D / 2 * s()
            op = float(np.clip((0.6 - r_sink) / 0.3, 0, 1))
            return DashedVMobject(Circle(radius=0.32, color=ACCENT, stroke_width=SW_BODY),
                                  num_dashes=14).move_to(P).set_stroke(opacity=op)

        pic = always_redraw(world)
        bar = always_redraw(scale_bar)
        ring = always_redraw(marker)
        title = VGroup(T("раковина"), T(f"{round(SINK_D * 100)} см", color=C_X)).arrange(RIGHT, buff=0.3)
        title.next_to(P + UP * 1.6, UP, buff=0.3)

        self.add_subcaption("Раковина: 40 сантиметрів.", duration=3.2)
        self.play(FadeIn(pic), FadeIn(bar), FadeIn(title), run_time=1.0)
        self.wait(2.2)

        self.add(ring)
        self.add_subcaption("Віддаляємося: метри, кілометри…", duration=4.0)
        self.add_subcaption("…сотні кілометрів.", duration=3.4, offset=4.0)
        self.play(FadeOut(title, run_time=0.8), run_time=0.8)
        self.play(z.animate.set_value(Z1), run_time=6.6, rate_func=smooth)
        for m in (pic, bar, ring):
            m.clear_updaters()

        cyc_lab = VGroup(T("циклон"), T(f"{round(CYCLONE_D / 1000)} км", color=C_X)).arrange(RIGHT, buff=0.3)
        cyc_lab.move_to([CYC_X, 3.05, 0])
        self.add_subcaption("Циклон — тисяча кілометрів.", duration=2.8)
        self.play(FadeIn(cyc_lab), run_time=0.8)
        self.wait(2.0)

        here = T("раковина тут").next_to(ring, UP, buff=0.3)
        px = L(f"≈{ua(SINK_PX, 4)} пікселя").next_to(ring, DOWN, buff=0.3)
        self.add_subcaption("А раковина — тут. Її не видно.", duration=3.4)
        self.play(FadeIn(here), run_time=0.7)
        self.play(FadeIn(px), run_time=0.6)
        self.wait(2.1)

        ratio = M(rf"\frac{{{round(CYCLONE_D / 1000)}\ \text{{км}}}}{{{round(SINK_D * 100)}\ \text{{см}}}}"
                  rf" = {tex_sci(SCALE_RATIO_18)}", 54)
        ratio.move_to([-3.6, -1.95, 0])  # не ближче 5 % до лівого краю
        self.add_subcaption("Різниця — у 2,5 мільйона разів.", duration=4.5)
        self.play(Write(ratio), run_time=1.2)
        self.wait(3.3)
