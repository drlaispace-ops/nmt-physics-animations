"""№14 «Повітряна куля над Києвом» — випуск 1.3, врізка «Міф, який вбиває незалежність рухів». Пріоритет 3.

Глядач бачить: Землю згори, з Північного полюса (ортографічна проєкція: точка на широті φ —
на відстані R·cos φ від центру). Київ і Лісабон на своїх довготах, над Києвом — куля.
(1) Міф: куля «висить» нерухомо, Земля обертається під нею; за ≈2,6 год під довготу кулі
приходить Лісабон — «не працює». (2) Насправді куля вже летить разом із Києвом ≈300 м/с,
Земля обертається разом із нею — куля весь час над Києвом.

Фізика: кут повороту — 39,66° різниці довгот Київ → Лісабон; час — calc_1.HOURS_KYIV_LISBON
(зоряна доба). Швидкість — calc_1.V_ROT_KYIV ≈ 296 м/с, у кадрі «≈300 м/с», як у сценарії.
Час прискорено ×2000 (2,6 год → 4,7 с). Куля — значок (у масштабі Землі її не видно).

Синхрон: «зависніть, зачекайте кілька годин — і Земля сама прокрутиться» → міф;
«Три години — і ти в Португалії» → годинник ≈2,6 год (див. питання в звіті);
«Не працює» → закреслення; «Куля… уже летить… разом із Києвом» → друга частина.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "style"))
sys.path.insert(0, str(Path(__file__).resolve().parent))
from feynman_style import *  # noqa: E402,F403
from calc_1 import KYIV_LAT, KYIV_LON, LISBON_LON, V_ROT_KYIV, HOURS_KYIV_LISBON, ua  # noqa: E402

# ── Розрахунки для цієї сцени (calc_1 не змінюємо) ──────────────────────────
LISBON_LAT = 38.72                       # °, широта Лісабона
TURN = KYIV_LON - LISBON_LON             # 39,66° — на стільки має повернутися Земля
TIME_X = 2000                            # час прискорено ×2000
RUN = HOURS_KYIV_LISBON * 3600 / TIME_X  # 4,7 с ролика
V_SHOWN = int(round(V_ROT_KYIV, -2))     # 296 м/с → «≈300 м/с», як у сценарії

D = LEFT * 2.4 + DOWN * 0.25             # центр диска (Північний полюс)
RD = 2.9                                 # радіус диска = екватор
COL_X = 1.3                              # лівий край тексту праворуч


def spot(lat, lon, rot):
    """Екранна точка (широта, довгота) при повороті Землі на rot° (проти годинникової — на схід)."""
    a = np.radians(90 + (lon - KYIV_LON) + rot)
    return D + RD * np.cos(np.radians(lat)) * np.array([np.cos(a), np.sin(a), 0])


def earth_face(rot, kyiv_side=DOWN):
    """Меридіани через 30° і дві точки-міста; усе крутиться разом із Землею."""
    g = VGroup()
    for k in range(12):
        a = np.radians(90 + 30 * k + rot)
        g.add(Line(D, D + RD * np.array([np.cos(a), np.sin(a), 0]), color=FG,
                   stroke_width=SW_GRID, stroke_opacity=0.3))
    kyiv, lis = spot(KYIV_LAT, KYIV_LON, rot), spot(LISBON_LAT, LISBON_LON, rot)
    g.add(Dot(kyiv, radius=0.09, color=FG), Dot(lis, radius=0.09, color=FG))
    g.add(T("Київ").next_to(kyiv, kyiv_side, buff=0.3))
    g.add(T("Лісабон").next_to(lis, RIGHT, buff=0.2))
    return g


def balloon(pos, side=UL):
    """Куля-значок; підпис угорі ліворуч (міф: Київ іде вниз ліворуч, згори приходить Лісабон) або згори (друга частина: ліворуч стрілка v)."""
    ring = Circle(radius=0.22, stroke_color=ACCENT, stroke_width=SW_BODY,
                  fill_color=ACCENT, fill_opacity=0.3).move_to(pos)
    return VGroup(ring, T("куля").next_to(ring, side, buff=0.15))


class A14_BalloonKyiv(Scene):
    def construct(self):
        row_tag(self, "№14")
        scale_note(self, f"час прискорено ×{TIME_X}")
        rot = ValueTracker(0.0)

        disk = Circle(radius=RD, stroke_color=C_WAVE, stroke_width=SW_BODY,
                      fill_color=C_WAVE, fill_opacity=0.12).move_to(D)
        pole = Dot(D, radius=0.06, color=FG)
        spin = Arc(radius=RD + 0.3, start_angle=np.radians(-70), angle=np.radians(45),
                   arc_center=D, color=FG, stroke_width=SW_AXIS).add_tip(tip_length=0.2, tip_width=0.2)
        face = always_redraw(lambda: earth_face(rot.get_value()))
        start = spot(KYIV_LAT, KYIV_LON, 0)
        ball0 = balloon(start)
        view = L("вигляд з Північного полюса").move_to([COL_X, 2.6, 0], aligned_edge=LEFT)

        self.add_subcaption("Куля над Києвом. Земля — згори, з полюса.", duration=3.2)
        self.play(FadeIn(disk), FadeIn(pole), FadeIn(face), Create(spin), FadeIn(view), run_time=1.2)
        self.play(FadeIn(ball0, scale=0.6), run_time=0.6)
        self.wait(1.4)

        # ── Міф: куля нерухома, Земля крутиться під нею ──────────────────────
        myth = T("Земля прокрутиться\nпід кулею?").move_to([COL_X, 2.2, 0], aligned_edge=LEFT)
        line = DashedLine(D, D + (start - D) / np.linalg.norm(start - D) * RD, color=ACCENT,
                          stroke_width=SW_AXIS, dash_length=0.14)
        clock = always_redraw(lambda: T(
            f"t = {ua(HOURS_KYIV_LISBON * rot.get_value() / TURN, 1)} год", color=C_TIME)
            .move_to([COL_X, 0.6, 0], aligned_edge=LEFT))
        self.add_subcaption("Міф: зависни — і Земля прокрутиться під тобою.", duration=2.5)
        self.play(FadeOut(view), FadeIn(myth), Create(line), run_time=0.9)
        self.play(FadeIn(clock), run_time=0.4)
        self.wait(1.2)
        self.add_subcaption("До довготи Лісабона — ≈2,6 години.", duration=RUN + 1.2)
        self.play(rot.animate.set_value(TURN), run_time=RUN, rate_func=linear)
        clock.clear_updaters()
        approx = T(f"≈{ua(HOURS_KYIV_LISBON, 1)} год", color=C_TIME).move_to(clock, aligned_edge=LEFT)
        self.play(ReplacementTransform(clock, approx), run_time=0.5)
        self.wait(0.7)

        strike = Line(myth.get_left() + LEFT * 0.1, myth.get_right() + RIGHT * 0.1, color=FG,
                      stroke_width=SW_BODY)
        nope = T("не працює").next_to(myth, DOWN, buff=0.35, aligned_edge=LEFT)
        self.add_subcaption("Не працює.", duration=2.4)
        self.play(Create(strike), FadeIn(nope), run_time=0.7)
        self.wait(1.7)

        # ── Повертаємо Землю у вихідне положення (перебивка) ──────────────────
        face.clear_updaters()
        self.play(FadeOut(VGroup(myth, strike, nope, line, approx, face, ball0)), run_time=0.6)
        rot.set_value(0.0)
        face = always_redraw(lambda: earth_face(rot.get_value(), DR))
        ball = always_redraw(lambda: balloon(spot(KYIV_LAT, KYIV_LON, rot.get_value()), UP))

        def v_arrow():
            k = spot(KYIV_LAT, KYIV_LON, rot.get_value())
            a = np.radians(90 + rot.get_value())
            tang = np.array([-np.sin(a), np.cos(a), 0])
            return vec(k + tang * 0.3, k + tang * 1.5, C_V)

        speed = always_redraw(v_arrow)
        truth = T("куля летить\nразом із Києвом").move_to([COL_X, 2.2, 0], aligned_edge=LEFT)
        v_lab = T(f"v ≈ {V_SHOWN} м/с", color=C_V).move_to([COL_X, 0.9, 0], aligned_edge=LEFT)
        clock2 = always_redraw(lambda: T(
            f"t = {ua(HOURS_KYIV_LISBON * rot.get_value() / TURN, 1)} год", color=C_TIME)
            .move_to([COL_X, -0.1, 0], aligned_edge=LEFT))
        self.add_subcaption("Насправді куля вже летить разом із Києвом.", duration=2.7)
        self.play(FadeIn(face), FadeIn(ball), FadeIn(truth), FadeIn(clock2), run_time=0.7)
        self.play(FadeIn(speed), FadeIn(v_lab), run_time=0.6)
        self.wait(1.4)
        self.add_subcaption("≈300 м/с — Земля крутиться разом із нею.", duration=RUN + 2.5)
        self.play(rot.animate.set_value(TURN), run_time=RUN, rate_func=linear)
        for m in (face, ball, speed, clock2):
            m.clear_updaters()
        self.wait(2.5)
