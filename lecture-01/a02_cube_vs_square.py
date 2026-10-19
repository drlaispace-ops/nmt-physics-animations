"""№2 «Куб проти квадрата» — випуск 1.1, блок 2.2. Пріоритет 1.

Глядач бачить: кулю радіуса r; поруч — «вага ~ r³» і «опір ~ r²» (опір — від площі перерізу,
яку підсвічено еліпсом-перерізом). Куля плавно росте до 2r, і множники ростуть синхронно
з радіусом: вага ×1 → ×8, опір ×1 → ×4. Висновок: вага на одиницю площі опору ×2 —
великому легше ігнорувати повітря.

Синхрон: «Візьмемо кулю… об'єм росте як радіус у кубі» → «вага ~ r³»;
«…площа росте як радіус у квадраті» → «опір ~ r²»; «Збільшуємо кулю вдвічі» → ріст;
«Вага виграла вдвічі» → ×2; «…легше ігнорувати повітря» → ключові слова.
Без чисел на осях і без спотворених пропорцій — підпис «масштаб умовний» не потрібен.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "style"))
sys.path.insert(0, str(Path(__file__).resolve().parent))
from feynman_style import *  # noqa: E402,F403
from calc_1 import R_SCALE, VOLUME_FACTOR, AREA_FACTOR, WEIGHT_PER_AREA, ua  # noqa: E402

CENTER = LEFT * 3.4 + UP * 0.45   # центр кулі
R0 = 1.0                          # радіус малої кулі на екрані; велика — R0·R_SCALE
ROW_X = 0.2                       # лівий край стовпчика формул
NUM_X = 4.3                       # лівий край множників
ROWS_Y = (1.75, 0.3, -1.2)       # вага, опір, вага/опір
FORMULA = 60                      # формули рядків: CM-шрифт дрібніший за DejaVu, тому 60


def factor(v):
    """×8 для цілих, ×3,4 — у русі (десяткова кома)."""
    return f"×{round(v)}" if abs(v - round(v)) < 1e-6 else f"×{ua(v, 1)}"


def ball(k):
    r = R0 * k
    body = Circle(radius=r, stroke_color=FG, stroke_width=SW_BODY,
                  fill_color=FG, fill_opacity=0.1).move_to(CENTER)
    return body


def section(k):
    """Переріз, який «бачить» повітря: еліпс по екватору кулі."""
    r = R0 * k
    disk = Ellipse(width=2 * r, height=0.34 * r, stroke_width=0,
                   fill_color=FG, fill_opacity=0.28).move_to(CENTER)
    rim = DashedVMobject(
        Ellipse(width=2 * r, height=0.34 * r, color=FG, stroke_width=SW_AXIS),
        num_dashes=28,
    ).move_to(CENTER)
    return VGroup(disk, rim)


class A02_CubeVsSquare(Scene):
    def construct(self):
        row_tag(self, "№2")
        k = ValueTracker(1.0)

        body = always_redraw(lambda: ball(k.get_value()))
        rad = always_redraw(lambda: Line(
            CENTER, CENTER + UP * R0 * k.get_value(), color=C_X, stroke_width=SW_BODY))
        r_lab = M("r", SIZE_MATH_MIN, color=C_X)
        r_lab.add_updater(lambda m: m.next_to(rad, RIGHT, buff=0.15))

        self.add_subcaption("Куля радіуса r.", duration=2.5)
        self.play(FadeIn(body), Create(rad), run_time=1.2)
        r_lab.update()
        self.play(FadeIn(r_lab), run_time=0.5)
        self.wait(0.8)

        # Вага ~ об'єм ~ r³
        w_row = MP(r"\text{вага}", r"\sim", r"r^{3}", size=FORMULA)
        w_row[2].set_color(C_X)
        w_row.move_to([ROW_X, ROWS_Y[0], 0], aligned_edge=LEFT)
        self.add_subcaption("Вага — як об'єм: росте як r³.", duration=4)
        self.play(Write(w_row), run_time=1.3)
        self.wait(2.7)

        # Опір ~ площа перерізу ~ r²
        sec = always_redraw(lambda: section(k.get_value()))
        d_row = MP(r"\text{опір}", r"\sim", r"r^{2}", size=FORMULA)
        d_row[2].set_color(C_X)
        d_row.move_to([ROW_X, ROWS_Y[1], 0], aligned_edge=LEFT)
        self.add_subcaption("Опір — як площа перерізу: r².", duration=4.5)
        self.play(FadeIn(sec), run_time=1.0)
        self.play(Write(d_row), run_time=1.3)
        self.wait(2.2)

        # Радіус ×2 — множники ростуть синхронно з радіусом
        def readout(power, y):
            mob = always_redraw(lambda: T(factor(k.get_value() ** power), SIZE_MATH)
                                .move_to([NUM_X, y, 0], aligned_edge=LEFT))
            return mob

        w_num = readout(3, ROWS_Y[0])
        d_num = readout(2, ROWS_Y[1])
        self.add_subcaption("Радіус удвічі: вага ×8, опір ×4.", duration=5)
        self.play(FadeIn(w_num), FadeIn(d_num), run_time=0.6)
        self.play(k.animate.set_value(R_SCALE), run_time=3.2, rate_func=smooth)
        r2 = M("2r", SIZE_MATH_MIN, color=C_X).next_to(rad, RIGHT, buff=0.15)
        r_lab.clear_updaters()
        self.play(ReplacementTransform(r_lab, r2), run_time=0.5)
        self.wait(0.7)

        # Множники фіксуються з calc_1 (не з трекера), щоб числа в кадрі були точні
        for mob in (w_num, d_num, body, rad, sec):
            mob.clear_updaters()
        w_fix = T(f"×{VOLUME_FACTOR}", SIZE_MATH).move_to([NUM_X, ROWS_Y[0], 0], aligned_edge=LEFT)
        d_fix = T(f"×{AREA_FACTOR}", SIZE_MATH).move_to([NUM_X, ROWS_Y[1], 0], aligned_edge=LEFT)
        self.remove(w_num, d_num)
        self.add(w_fix, d_fix)

        # Вага на одиницю площі опору ×2
        ratio = MP(r"\text{вага}\,/\,\text{опір}", size=FORMULA)
        ratio.move_to([ROW_X, ROWS_Y[2] - 0.1, 0], aligned_edge=LEFT)
        r_num = T(f"×{WEIGHT_PER_AREA}", SIZE_MATH, color=ACCENT)
        r_num.move_to([NUM_X, ratio.get_center()[1], 0], aligned_edge=LEFT)
        rule = Line([ROW_X, ROWS_Y[2] + 0.75, 0], [NUM_X + 1.3, ROWS_Y[2] + 0.75, 0],
                    color=FG, stroke_width=SW_AXIS)
        box = SurroundingRectangle(r_num, color=ACCENT, buff=0.2, stroke_width=SW_BODY)
        self.add_subcaption("Вага виграла вдвічі.", duration=3.5)
        self.play(Create(rule), FadeIn(ratio), run_time=0.8)
        self.play(FadeIn(r_num, scale=1.3), Create(box), run_time=0.9)
        self.wait(1.8)

        # Висновок під кулею
        moral = T("легше ігнорувати повітря", SIZE_BODY)
        moral.move_to([CENTER[0], -2.35, 0])
        self.add_subcaption("Великому легше ігнорувати повітря.", duration=4.5)
        self.play(FadeIn(moral, shift=UP * 0.2), run_time=1.0)
        self.wait(3.5)
