"""№19 «Місяць, що падає» — випуск 1.3, блок 5.5 (місток до випуску 1.4 «Рух по колу»). Пріоритет 2.

Глядач бачить: коротко — Ньютонова гармата (ті самі траєкторії, що в №10: два падіння
й орбіта). Камера віддаляється: Земля меншає, і ззовні «в'їжджає» орбіта Місяця —
у справжньому співвідношенні відстаней (60,3 радіуса Землі). Місяць рухається по орбіті,
а «привид» — по дотичній, як летів би без тяжіння; відрізок між ними — це падіння.
Далі числа задачі 16: за хвилину Місяць «падає» на 4,9 м — як яблуко за секунду;
a ≈ 2,7·10⁻³ м/с²; g/a ≈ 3600 проти (R/R_З)² ≈ 3640 — зійшлися (пауза 3 с для монтажу).

Фізика: відстані — справжні (MOON_R / EARTH_R); Землю й Місяць збільшено ×6, гору — як у №10,
тому «масштаб умовний». Рух Місяця: 45° орбіти = 3,4 доби за 3,9 с — час прискорено ×75 000.
Відрізок «привид → Місяць» — точна різниця положень на дотичній і на колі (≈ a t²/2).

Синхрон: «А що, як він падає?» → старт; «Місяць летить убік так швидко, що ніяк не долетить»
→ гармата і орбіта; «Узяв відстань… період… порівняв із прискоренням яблука» → числа;
«І цифри зійшлися» → 3600 / 3640, пауза.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "style"))
sys.path.insert(0, str(Path(__file__).resolve().parent))
from feynman_style import *  # noqa: E402,F403
from calc_1 import (EARTH_R, MOON_R, MOON_T, A_MOON, G_OVER_A_MOON, DIST_RATIO_SQ,  # noqa: E402
                    MOON_FALL_PER_MINUTE, APPLE_FALL_1S, ua)
from a10_newton_cannon import Cannon, trajectory, R_LAUNCH, V1_KMS  # noqa: E402

# ── Розрахунки для цієї сцени (calc_1 не змінюємо) ──────────────────────────
MOON_EARTH_R = 1737e3 / EARTH_R          # радіус Місяця в радіусах Землі (0,273)
ORBIT_RATIO = MOON_R / EARTH_R           # 60,3
BODY_X = 6                               # Землю й Місяць у кадрі збільшено ×6
ARC = np.radians(45)                     # Місяць проходить 45° орбіти
ARC_T = MOON_T * ARC / (2 * np.pi)       # = 294 840 с ≈ 3,4 доби
TIME_X = 75_000                          # час прискорено ×75 000 → 3,9 с ролика
OMEGA = 2 * np.pi / MOON_T

E = LEFT * 3.4 + DOWN * 0.3              # центр Землі на екрані
EARTH_SR0 = 1.9                          # радіус Землі на першому плані (гармата)
ORBIT_SR = 2.9                           # радіус орбіти Місяця після віддалення
Z_END = ORBIT_SR / (ORBIT_RATIO * EARTH_SR0)
EARTH_SR1 = EARTH_SR0 * Z_END * BODY_X   # Земля після віддалення (×5)
MOON_SR = EARTH_SR0 * Z_END * MOON_EARTH_R * BODY_X
TH0 = np.radians(-20)                    # звідки Місяць починає рух
COL_X = 0.8                              # лівий край стовпчика чисел


def moon_pos(t):
    th = TH0 + OMEGA * t
    return E + ORBIT_SR * np.array([np.cos(th), np.sin(th), 0])


def ghost_pos(t):
    """Де був би Місяць без тяжіння: рух по дотичній з тією самою швидкістю."""
    u = np.array([np.cos(TH0), np.sin(TH0), 0])
    tang = np.array([-np.sin(TH0), np.cos(TH0), 0])
    return E + ORBIT_SR * (u + OMEGA * t * tang)


def tex_sci(x, nd=1):
    """2{,}7\\cdot 10^{-3} — для M()."""
    exp = int(np.floor(np.log10(abs(x))))
    mant = ua(x / 10 ** exp, nd).replace(",", "{,}")
    return rf"{mant}\cdot 10^{{{exp}}}"


class A19_FallingMoon(Scene):
    def construct(self):
        row_tag(self, "№19")
        note = scale_note(self)

        # ── 1. Ньютонова гармата (як у №10): два падіння й орбіта ──────────────
        cn = Cannon(E, EARTH_SR0)
        hill, gun = cn.mountain(), cn.gun()
        paths = VGroup(*[cn.path(trajectory(v / V1_KMS)[1]) for v in (6.0, 7.5, V1_KMS)])
        cannon = VGroup(hill, gun, paths)
        earth0 = cn.earth()

        self.add_subcaption("А що, як він падає?", duration=1.6)
        self.add_subcaption("Ядро летить убік так швидко, що промахується.", duration=2.6, offset=1.6)
        self.play(FadeIn(earth0), FadeIn(hill), FadeIn(gun), run_time=0.8)
        self.play(Create(paths[0]), run_time=0.7)
        self.play(Create(paths[1]), run_time=0.9)
        self.play(Create(paths[2]), run_time=1.4)
        self.wait(0.4)

        # ── 2. Віддалення: Земля меншає, ззовні в'їжджає орбіта Місяця ─────────
        lz = ValueTracker(0.0)

        def world(with_moon=True):
            z = np.exp(lz.get_value())
            g = VGroup()
            er = max(EARTH_SR0 * z, EARTH_SR1)
            g.add(Circle(radius=er, stroke_color=C_WAVE, stroke_width=SW_BODY,
                         fill_color=C_WAVE, fill_opacity=0.15).move_to(E))
            fade = float(np.clip((z - 0.1) / 0.3, 0, 1))
            if fade > 0:
                c = cannon.copy().scale(z, about_point=E)
                for sm in c.family_members_with_points():
                    sm.set_stroke(opacity=sm.get_stroke_opacity() * fade)
                    sm.set_fill(opacity=sm.get_fill_opacity() * fade)
                g.add(c)
            r_orb = ORBIT_RATIO * EARTH_SR0 * z
            if r_orb < 25:
                g.add(DashedVMobject(Circle(radius=r_orb, color=FG, stroke_width=SW_AXIS,
                                            stroke_opacity=0.85), num_dashes=96).move_to(E))
            if with_moon and r_orb < 12:
                g.add(Circle(radius=MOON_SR, stroke_width=0, fill_color=FG, fill_opacity=1)
                      .move_to(E + r_orb * np.array([np.cos(TH0), np.sin(TH0), 0])))
            return g

        self.remove(earth0, hill, gun, *paths)
        zoom = always_redraw(world)
        self.add(zoom)
        self.add_subcaption("Відходимо далі — до Місяця.", duration=3.4)
        self.play(lz.animate.set_value(np.log(Z_END)), run_time=3.0, rate_func=smooth)
        zoom.clear_updaters()
        self.remove(zoom)
        base = world(with_moon=False)
        self.add(base)
        earth_lab = L("Земля", 32).next_to(E, DOWN, buff=0.35)
        self.play(FadeIn(earth_lab), run_time=0.4)

        # ── 3. Місяць і «привид» на дотичній: різниця = падіння ───────────────
        tm = ValueTracker(0.0)   # справжній час, с
        tangent = DashedLine(ghost_pos(0), ghost_pos(ARC_T * 1.4), color=FG,
                             stroke_width=SW_AXIS, dash_length=0.12).set_stroke(opacity=0.9)
        straight = L("без тяжіння").next_to(ghost_pos(ARC_T * 1.4), RIGHT, buff=0.15)
        moon = always_redraw(lambda: Circle(radius=MOON_SR, stroke_width=0, fill_color=FG,
                                            fill_opacity=1).move_to(moon_pos(tm.get_value())))
        ghost = always_redraw(lambda: Circle(radius=MOON_SR, color=FG, stroke_width=SW_AXIS)
                              .set_stroke(opacity=0.8).move_to(ghost_pos(tm.get_value())))

        def fall_seg():
            a, b = ghost_pos(tm.get_value()), moon_pos(tm.get_value())
            if np.linalg.norm(a - b) < 0.03:
                return VMobject()
            return Line(a, b, color=C_X, stroke_width=SW_BODY)

        seg = always_redraw(fall_seg)
        moon_lab = L("Місяць", 32).next_to(moon_pos(0), LEFT, buff=0.2)
        self.add(moon, seg)
        self.play(Create(tangent), FadeIn(straight), FadeIn(moon_lab), run_time=0.9)
        self.add(ghost)
        t_note = L(f"час прискорено ×{TIME_X:,}".replace(",", " ")).next_to(
            note, UP, buff=0.12, aligned_edge=RIGHT)
        self.add(t_note)
        self.add_subcaption("Без тяжіння Місяць летів би прямо.", duration=2.0)
        self.add_subcaption("Відставання від прямої — і є падіння.", duration=3.0, offset=2.0)
        self.play(tm.animate.set_value(ARC_T), FadeOut(moon_lab),
                  run_time=ARC_T / TIME_X, rate_func=linear)
        for m in (moon, ghost, seg):
            m.clear_updaters()
        fall_lab = T("падає", color=C_X).next_to(seg, RIGHT, buff=0.25).shift(DOWN * 0.12)
        self.play(FadeIn(fall_lab), run_time=0.5)
        self.wait(0.6)

        # ── 4. Хвилина Місяця = секунда яблука ────────────────────────────────
        moon_row = VGroup(T("Місяць за 1 хв:"), T(f"{ua(MOON_FALL_PER_MINUTE, 1)} м", color=C_X))
        apple_row = VGroup(T("яблуко за 1 с:"), T(f"{ua(APPLE_FALL_1S, 1)} м", color=C_X))
        for row, y in ((moon_row, 2.75), (apple_row, 1.9)):
            row[0].move_to([COL_X, y, 0], aligned_edge=LEFT)
            row[1].move_to([COL_X + 3.75, y, 0], aligned_edge=LEFT)
        self.add_subcaption("За хвилину Місяць «падає» на 4,9 м — як яблуко за секунду.", duration=4.4)
        self.play(FadeOut(straight), FadeIn(moon_row, shift=LEFT * 0.2), run_time=0.9)
        self.play(FadeIn(apple_row, shift=LEFT * 0.2), run_time=0.9)
        self.wait(2.6)

        # ── 5. Ньютонів розрахунок: g/a ≈ 3600 і (R/R_З)² ≈ 3640 ─────────────
        r_line = Line(E, moon.get_center(), color=C_X, stroke_width=SW_BODY)
        r_lab = M("R", SIZE_MATH_MIN, color=C_X).next_to(r_line.get_center(), UP, buff=0.15)
        a_row = M(rf"a \approx {tex_sci(A_MOON)}\ \text{{м/с}}^2", 52)
        a_row.move_to([COL_X, 2.4, 0], aligned_edge=LEFT)
        g_row = MP(r"\frac{g}{a}", r"\approx", f"{round(G_OVER_A_MOON, -2):.0f}", size=SIZE_MATH)
        d_row = MP(r"\left(\frac{R}{R_\text{З}}\right)^{2}", r"\approx", f"{round(DIST_RATIO_SQ, -1):.0f}",
                   size=SIZE_MATH)
        d_row[0][1].set_color(C_X)  # R — та сама довжина, що й відрізок на рисунку
        eq_x = COL_X + 2.45                       # «≈» одне під одним
        g_row.move_to([0, 0.85, 0]).shift(RIGHT * (eq_x - g_row[1].get_center()[0]))
        d_row.move_to([0, -0.65, 0]).shift(RIGHT * (eq_x - d_row[1].get_center()[0]))
        self.add_subcaption("Ньютон порахував прискорення Місяця.", duration=3.0)
        self.play(FadeOut(moon_row), FadeOut(apple_row), FadeOut(fall_lab), run_time=0.5)
        self.play(Create(r_line), FadeIn(r_lab), Write(a_row), run_time=1.2)
        self.wait(1.3)
        self.add_subcaption("У 3600 разів слабше за g — і відстань у 60 разів більша.", duration=4.0)
        self.play(Write(g_row), run_time=1.0)
        self.wait(0.6)
        self.play(Write(d_row), run_time=1.0)
        self.wait(1.4)
        box = SurroundingRectangle(VGroup(g_row, d_row), color=ACCENT, buff=0.25, stroke_width=SW_BODY)
        ok = T("зійшлися", color=ACCENT).next_to(box, DOWN, buff=0.3)
        self.add_subcaption("Цифри зійшлися.", duration=4.0)
        self.play(Create(box), FadeIn(ok), run_time=0.8)
        self.wait(3.2)  # пауза після 3600 і 3640 — не вирізати (задача 16, монтаж)
