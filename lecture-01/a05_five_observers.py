"""№5 «П'ять спостерігачів» — випуск 1.2, блок 3.3 «Потяг поруч». Пріоритет 1.

Глядач бачить: склянка чаю на столику у вагоні. «Камера» по черзі від'їжджає:
ви за столиком → провідник у коридорі → дідусь на пероні → центр Землі → Сонце.
Угорі щоразу — хто дивиться і яка для нього швидкість склянки (стрілка — зеленим,
спостерігач — акцентом). Наприкінці — п'ять відповідей поруч.

Синхрон: «Ви за столиком… нуль» → «Провідник… один метр за секунду. І, до речі, назад» →
«Дідусь на пероні… двадцять» → «центр Землі… приблизно триста» → «Сонце… тридцять
кілометрів за секунду» → «П'ять відповідей».

Числа — з calc_1.py: V_CONDUCTOR = 1 м/с, V_TRAIN = 20 м/с, V_ROT_KYIV ≈ 296 м/с
(у кадрі «≈300», як у сценарії), V_ORBIT_EARTH = 29,78 км/с (у кадрі «≈30 км/с»).
На пероні час сповільнено (SLOW_PLATFORM) — підпис у кутку; від Землі й далі
розміри умовні — «масштаб умовний».
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "style"))
sys.path.insert(0, str(Path(__file__).resolve().parent))
from feynman_style import *  # noqa: E402,F403
from calc_1 import V_CONDUCTOR, V_TRAIN, V_ROT_KYIV, V_ORBIT_EARTH, KYIV_LAT  # noqa: E402

# ── Числа в кадрі (округлення — як звучить у сценарії) ──────────────────────
NUM_ROT = int(round(V_ROT_KYIV, -2))            # 296 → 300
NUM_SUN_KM = int(round(V_ORBIT_EARTH / 1000))    # 29,78 → 30
LABELS = [
    ("ви за столиком", "0 м/с"),
    ("провідник", f"{V_CONDUCTOR:.0f} м/с"),
    ("дідусь на пероні", f"{V_TRAIN:.0f} м/с"),
    ("центр Землі", f"≈{NUM_ROT} м/с"),
    ("Сонце", f"≈{NUM_SUN_KM} км/с"),
]
SUMMARY = ["0", f"{V_CONDUCTOR:.0f}", f"{V_TRAIN:.0f}", f"≈{NUM_ROT}",
           f"≈{NUM_SUN_KM * 1000:,}".replace(",", " ")]

# ── Масштаби кадру ──────────────────────────────────────────────────────────
SCALE1 = 2.0                 # од/м у вагоні
SCALE2 = 0.8                 # од/м на пероні
SLOW_PLATFORM = 8            # на пероні час сповільнено ×8
G1 = np.array([1.8, -0.6, 0])   # склянка в кадрі «вагон»
G2 = np.array([-4.0, 0.3, 0])   # склянка на початку кадру «перон»
T_WALK = 4.4                 # с, провідник іде (реальний час: 1 м/с)
T_PLATFORM = 4.0             # с кадру «перон»
V2_SCREEN = V_TRAIN * SCALE2 / SLOW_PLATFORM     # 2 од/с у кадрі

E_C, E_R = np.array([0.0, -0.6, 0]), 2.2         # Земля
TILT = np.radians(20)        # Земля трохи «згори»: північний полюс нахилено до нас
LAT = np.radians(KYIV_LAT)
S_C, ORBIT_R = np.array([-1.6, -0.6, 0]), 3.0     # Сонце й орбіта

LIMB = 6                     # товщина ліній фігурок
WAGON_FILL = interpolate_color(ManimColor(BG), ManimColor(C_NEG), 0.22)
WALL_DARK = interpolate_color(ManimColor(BG), ManimColor(MUTED_TEXT), 0.3)
TEA = interpolate_color(ManimColor(BG), ManimColor(C_X), 0.7)
EARTH_FILL = interpolate_color(ManimColor(BG), ManimColor(C_WAVE), 0.3)


def P(x, y, origin=G1, s=SCALE1):
    """Світові метри (відносно дна склянки) → точка кадру."""
    return origin + s * np.array([x, y, 0.0])


def limb(a, b, color):
    return Line(a, b, color=color, stroke_width=LIMB).set_cap_style(CapStyleType.ROUND)


def seated_person(color):
    hip, knee, foot = P(0.78, -0.27), P(0.38, -0.24), P(0.40, -0.75)
    sh, elbow, hand = P(0.80, 0.30), P(0.58, 0.07), P(0.30, 0.04)
    head = Circle(radius=0.1 * SCALE1, color=color, fill_color=color, fill_opacity=1,
                  stroke_width=0).move_to(P(0.79, 0.46))
    return VGroup(limb(hip, sh, color), limb(hip, knee, color), limb(knee, foot, color),
                  limb(sh, elbow, color), limb(elbow, hand, color), head)


def walker(x, phase, color, cap=True, scale=SCALE1, origin=G1):
    """Людина, що йде праворуч; ноги/руки гойдаються з фазою кроку."""
    def p(dx, dy):
        return P(x + dx, dy, origin, scale)
    th = 0.45 * np.sin(phase)
    hip, sh = p(0, 0.13), p(0.02, 0.66)
    leg = 0.88
    f1 = p(leg * np.sin(th), 0.13 - leg * np.cos(th))
    f2 = p(-leg * np.sin(th), 0.13 - leg * np.cos(th))
    arm = 0.62
    h1 = p(0.02 - arm * np.sin(th), 0.66 - arm * np.cos(th))
    h2 = p(0.02 + arm * np.sin(th), 0.66 - arm * np.cos(th))
    head = Circle(radius=0.11 * scale, color=color, fill_color=color, fill_opacity=1,
                  stroke_width=0).move_to(p(0.03, 0.85))
    g = VGroup(limb(hip, sh, color), limb(hip, f1, color), limb(hip, f2, color),
               limb(sh, h1, color), limb(sh, h2, color), head)
    if cap:  # кашкет провідника
        g.add(Polygon(p(-0.09, 0.93), p(0.15, 0.93), p(0.2, 0.9), p(0.15, 1.01), p(-0.08, 1.01),
                      color=color, fill_color=color, fill_opacity=1, stroke_width=0))
    return g


def grandpa(color, origin, scale):
    """Дідусь із ціпком, стоїть на пероні (ноги на висоті платформи −0,95 м)."""
    def p(dx, dy):
        return origin + scale * np.array([dx, dy, 0.0])
    feet_y = -0.95
    hip, sh = p(0, feet_y + 0.86), p(0.06, feet_y + 1.38)
    head = Circle(radius=0.11 * scale, color=color, fill_color=color, fill_opacity=1,
                  stroke_width=0).move_to(p(0.11, feet_y + 1.56))
    return VGroup(limb(hip, sh, color), limb(hip, p(-0.14, feet_y), color), limb(hip, p(0.14, feet_y), color),
                  limb(sh, p(0.38, feet_y + 0.86), color), limb(p(0.38, feet_y + 0.86), p(0.42, feet_y), color),
                  head)


def wagon(x0, x1, origin=G1, s=SCALE1, interior=False):
    """Вагон-розріз між x0 і x1 (м): корпус, вікна, підлога, візки."""
    def p(x, y):
        return P(x, y, origin, s)
    g = VGroup()
    body = Polygon(p(x0, -1.05), p(x1, -1.05), p(x1, 1.4), p(x1 - 0.6, 1.62), p(x0 + 0.6, 1.62), p(x0, 1.4),
                   fill_color=WAGON_FILL, fill_opacity=1, stroke_color=FG, stroke_width=SW_BODY)
    g.add(body)
    g.add(Line(p(x0, -0.75), p(x1, -0.75), color=MUTED_TEXT, stroke_width=SW_AXIS))   # підлога
    xs = np.arange(x0 + 1.6, x1 - 1.0, 2.3)
    for xw in xs:
        if interior and abs(xw) < 1.2:
            continue
        g.add(Rectangle(width=1.3 * s, height=0.75 * s, color=MUTED_TEXT, stroke_width=SW_AXIS,
                        fill_color=WALL_DARK, fill_opacity=1).move_to(p(xw, 0.55)))
    for xb in (x0 + 2.5, x1 - 2.5):
        for dx in (-1.1, 1.1):
            g.add(Circle(radius=0.46 * s, color=FG, stroke_width=SW_AXIS, fill_color=BG,
                         fill_opacity=1).move_to(p(xb + dx, -1.51)))
    return g


def swap(old, new):
    """Старий напис іде, потім з'являється новий — без накладання."""
    return AnimationGroup(FadeOut(old, shift=UP * 0.2), FadeIn(new, shift=UP * 0.2), lag_ratio=1.0)


def header(i):
    name, num = LABELS[i]
    h = VGroup(T(name + ":", SIZE_BODY), T(num, SIZE_TITLE, C_V)).arrange(RIGHT, buff=0.3, aligned_edge=DOWN)
    return h.move_to(UP * 3.15)


class A05_FiveObservers(Scene):
    def construct(self):
        row_tag(self, "№5")

        # ── Рівень 1: вагон зсередини ───────────────────────────────────────
        ours = wagon(-9.0, 16.0, interior=True)
        ahead, behind = wagon(16.8, 41.8), wagon(-34.8, -9.8)
        window = Rectangle(width=1.5 * SCALE1, height=0.8 * SCALE1, color=MUTED_TEXT, stroke_width=SW_AXIS,
                           fill_color=WALL_DARK, fill_opacity=1).move_to(P(0.0, 0.55))
        table = VGroup(
            Rectangle(width=0.75 * SCALE1, height=0.05 * SCALE1, color=FG, stroke_width=SW_AXIS,
                      fill_color=WALL_DARK, fill_opacity=1).move_to(P(0, -0.025)),
            Line(P(0, -0.05), P(0, -0.75), color=FG, stroke_width=SW_BODY),
        )
        seat = VGroup(
            Rectangle(width=0.6 * SCALE1, height=0.08 * SCALE1, color=FG, stroke_width=SW_AXIS,
                      fill_color=WALL_DARK, fill_opacity=1).move_to(P(0.78, -0.33)),
            Rectangle(width=0.08 * SCALE1, height=0.8 * SCALE1, color=FG, stroke_width=SW_AXIS,
                      fill_color=WALL_DARK, fill_opacity=1).move_to(P(1.1, 0.07)),
            Line(P(0.78, -0.37), P(0.78, -0.75), color=FG, stroke_width=SW_AXIS),
        )
        glass = Polygon(P(-0.04, 0), P(0.04, 0), P(0.055, 0.18), P(-0.055, 0.18),
                        color=FG, stroke_width=SW_AXIS, fill_color=TEA, fill_opacity=1)
        you = seated_person(ACCENT)
        ring = Circle(radius=0.5, color=FG, stroke_width=SW_AXIS).move_to(glass.get_center())
        for m in (table, glass, ring):   # столик і склянка завжди попереду провідника
            m.set_z_index(1)
        train = VGroup(behind, ahead, ours, window, seat, table, you, glass, ring)

        h = header(0)
        self.add_subcaption("Ви за столиком: склянка стоїть.", duration=5.0)
        self.play(FadeIn(train), FadeIn(h), run_time=1.2)
        self.wait(3.8)

        # ── Рівень 1б: провідник іде назустріч, 1 м/с ──────────────────────
        x_end = -1.3                                    # м, зупиняється перед столиком
        x_start = x_end - V_CONDUCTOR * T_WALK
        walk = ValueTracker(0.0)

        def conductor_now():
            t = walk.get_value()
            x = x_start + V_CONDUCTOR * t
            return walker(x, 2 * PI * x / 1.4, ACCENT)   # крок 1,4 м на повний цикл

        cond = always_redraw(conductor_now)
        top = ring.get_top()
        a_cond = vec(top + UP * 0.15, top + UP * 0.15 + LEFT * 1.6, color=C_V)
        h1 = header(1)
        self.add_subcaption("Провідник іде назустріч: 1 м/с — і назад.", duration=T_WALK + 0.4)
        self.add(cond)
        self.play(walk.animate.set_value(1.0), swap(h, h1),
                  you.animate.set_color(MUTED_TEXT), run_time=1.0, rate_func=linear)
        self.play(walk.animate.set_value(1.8), GrowArrow(a_cond), run_time=0.8, rate_func=linear)
        self.play(walk.animate.set_value(T_WALK), run_time=T_WALK - 1.8, rate_func=linear)
        self.remove(cond)
        cond_static = conductor_now()
        train.add(cond_static)
        self.wait(0.4)

        # ── Рівень 2: від'їжджаємо — перон, дідусь, потяг летить ───────────
        k = SCALE2 / SCALE1
        self.add_subcaption(f"Дідусь на пероні: склянка летить {V_TRAIN:.0f} м/с.", duration=2.2 + T_PLATFORM)
        self.play(FadeOut(a_cond), cond_static.animate.set_color(MUTED_TEXT), run_time=0.5)
        self.play(train.animate.scale(k, about_point=G1).shift(G2 - G1), run_time=2.2)

        ground_y = G2 + SCALE2 * np.array([0, -0.95, 0])
        face = 1.1 * SCALE2                                   # висота платформи над рейками
        platform = Polygon(
            [-7.6, ground_y[1], 0], [7.6, ground_y[1], 0], [7.6, ground_y[1] - face, 0], [-7.6, ground_y[1] - face, 0],
            fill_color=WALL_DARK, fill_opacity=1, stroke_width=0)
        edge = Line([-7.6, ground_y[1], 0], [7.6, ground_y[1], 0], color=FG, stroke_width=SW_BODY)
        old_man = grandpa(ACCENT, np.array([0.0, G2[1], 0]), SCALE2)
        a_train = vec(ring.get_top() + UP * 0.15, ring.get_top() + UP * 0.15 + RIGHT * 1.6, color=C_V)
        mover = VGroup(train, a_train)
        h2 = header(2)
        note = scale_note(self, f"час сповільнено ×{SLOW_PLATFORM}")
        note.set_opacity(0)
        drive = ValueTracker(0.0)
        x_ref = [0.0]

        def drive_upd(m):
            d = drive.get_value()
            m.shift(RIGHT * (d - x_ref[0]))
            x_ref[0] = d

        mover.add_updater(drive_upd)
        self.add(mover, platform, edge, old_man)
        t_in = 0.8
        self.play(drive.animate.set_value(V2_SCREEN * t_in), FadeIn(platform), FadeIn(edge), FadeIn(old_man),
                  GrowArrow(a_train), swap(h1, h2),
                  note.animate.set_opacity(1), run_time=t_in, rate_func=linear)
        self.play(drive.animate.set_value(V2_SCREEN * T_PLATFORM), run_time=T_PLATFORM - t_in, rate_func=linear)
        mover.remove_updater(drive_upd)

        # ── Рівень 3: Земля, центр Землі ────────────────────────────────────
        kyiv = E_C + E_R * np.array([0, np.sin(LAT - TILT), 0])
        disc = Circle(radius=E_R, color=C_WAVE, stroke_width=SW_BODY, fill_color=EARTH_FILL, fill_opacity=1).move_to(E_C)
        axis_top = E_C + UP * (E_R * np.cos(TILT) + 0.6)
        axis = VGroup(Line(E_C + UP * E_R * np.cos(TILT), axis_top, color=FG, stroke_width=SW_AXIS),
                      Line(E_C + DOWN * E_R * np.cos(TILT), E_C + DOWN * (E_R * np.cos(TILT) + 0.6),
                           color=FG, stroke_width=SW_AXIS))

        def lat_arc(phi, color, sw):
            a, b = E_R * np.cos(phi), E_R * np.cos(phi) * np.sin(TILT)
            yc = E_R * np.sin(phi) * np.cos(TILT)
            return ParametricFunction(lambda u: E_C + np.array([a * np.cos(u), yc - b * np.sin(u), 0]),
                                      t_range=[0, PI], color=color, stroke_width=sw)

        equator = lat_arc(0.0, MUTED_TEXT, SW_AXIS)
        parallel = lat_arc(LAT, FG, SW_AXIS)
        centre = Dot(E_C, radius=0.12, color=ACCENT)
        k_dot = Dot(kyiv, radius=0.1, color=FG)
        k_ring = Circle(radius=0.22, color=FG, stroke_width=SW_AXIS).move_to(kyiv)
        a_rot = vec(kyiv + RIGHT * 0.22, kyiv + RIGHT * 2.2, color=C_V)
        earth = VGroup(axis, disc, equator, parallel, centre, k_dot, k_ring)
        earth.save_state()
        earth.scale(7, about_point=kyiv).set_opacity(0)
        world2 = VGroup(mover, platform, edge, old_man)
        h3 = header(3)
        note2 = L("масштаб умовний").to_corner(DR, buff=0.4)
        self.add_subcaption(f"Центр Землі: ще й обертання, ≈{NUM_ROT} м/с.", duration=6.0)
        self.play(AnimationGroup(
                      world2.animate.scale(0.04, about_point=ring.get_center()).move_to(kyiv).set_opacity(0),
                      Restore(earth), lag_ratio=0.4),
                  swap(h2, h3), FadeOut(note), FadeIn(note2), run_time=2.4)
        self.remove(world2)
        self.play(GrowArrow(a_rot), run_time=0.8)
        self.wait(3.0)

        # ── Рівень 4: Сонце ────────────────────────────────────────────────
        e_pos = S_C + RIGHT * ORBIT_R
        sun = Circle(radius=0.6, color=C_LIGHT, stroke_width=SW_BODY, fill_color=C_LIGHT, fill_opacity=1).move_to(S_C)
        s_ring = Circle(radius=0.85, color=ACCENT, stroke_width=SW_BODY).move_to(S_C)
        orbit = DashedVMobject(Circle(radius=ORBIT_R, color=MUTED_TEXT, stroke_width=SW_AXIS).move_to(S_C),
                               num_dashes=60)
        e_dot = Circle(radius=0.2, color=C_WAVE, stroke_width=SW_AXIS, fill_color=EARTH_FILL, fill_opacity=1).move_to(e_pos)
        a_orb = vec(e_pos + UP * 0.3, e_pos + UP * 2.4, color=C_V)
        solar = VGroup(orbit, sun, s_ring, e_dot)
        solar.save_state()
        solar.scale(8, about_point=e_pos).set_opacity(0)
        h4 = header(4)
        earth_all = VGroup(earth, a_rot)
        self.add_subcaption(f"Сонце: вся конструкція мчить ≈{NUM_SUN_KM} км/с.", duration=6.0)
        self.play(AnimationGroup(
                      earth_all.animate.scale(0.2 / E_R, about_point=E_C).move_to(e_pos).set_opacity(0),
                      Restore(solar), lag_ratio=0.4),
                  swap(h3, h4), run_time=2.4)
        self.remove(earth_all)
        self.play(GrowArrow(a_orb), run_time=0.8)
        self.wait(3.0)

        # ── Підсумок: п'ять відповідей ─────────────────────────────────────
        nums = VGroup(*[T(s, 56, C_V) for s in SUMMARY]).arrange(RIGHT, buff=0.75)
        unit = T("м/с", SIZE_TITLE)
        row = VGroup(nums, unit).arrange(RIGHT, buff=0.45, aligned_edge=DOWN).move_to(UP * 0.4)
        self.add_subcaption("П'ять спостерігачів — п'ять відповідей.", duration=5.5)
        self.play(FadeOut(VGroup(solar, a_orb)), FadeOut(h4), run_time=1.0)
        self.play(LaggedStart(*[FadeIn(n, shift=UP * 0.2) for n in nums], lag_ratio=0.35),
                  FadeIn(unit), run_time=2.0)
        self.wait(2.5)
