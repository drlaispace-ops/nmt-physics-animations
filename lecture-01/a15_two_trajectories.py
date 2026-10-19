"""№15 «Дві траєкторії» — випуск 1.3, блок 4.4. Пріоритет 1.

Глядач бачить ту саму подію двома очима, синхронно і в одному масштабі:
- згори — з перону: м'яч летить параболою 20,4 м завдовжки і 1,28 м заввишки (майже пряма),
  а рука пасажира весь час під ним і ловить його;
- знизу — з вагона: м'яч іде вертикально вгору на 1,28 м і повертається в нерухому руку.
Наприкінці титр «Одна подія. Два описи. Обидва правильні.»

Синхрон: «Тепер уявіть цю картинку очима дідуся з перону…» → «Одна подія. Два описи».
Масштаб справжній (той самий для обох панелей і обох осей); час сповільнено ×4.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "style"))
sys.path.insert(0, str(Path(__file__).resolve().parent))
from feynman_style import *  # noqa: E402,F403
from calc_1 import G, V_TRAIN, V0_BALL, T_FLIGHT, H_BALL, L_BALL, SLOWMO_15, ua_tex  # noqa: E402

M_TO_U = 11.2 / L_BALL            # 20,4 м займають 11,2 одиниці кадру; той самий масштаб усюди
X0 = -5.6                         # старт м'яча по горизонталі
Y_TOP, Y_BOT = 0.75, -2.05        # рівень руки в панелях «перон» і «вагон»
R_BALL = 0.1


def height(t):
    return V0_BALL * t - G * t * t / 2


def platform_view(t):
    return np.array([X0 + V_TRAIN * t * M_TO_U, Y_TOP + height(t) * M_TO_U, 0])


def wagon_view(t):
    return np.array([0.0, Y_BOT + height(t) * M_TO_U, 0])


def hand(at):
    return RoundedRectangle(width=0.42, height=0.14, corner_radius=0.06,
                            stroke_color=C_X, stroke_width=SW_AXIS, fill_color=C_X,
                            fill_opacity=0.5).move_to(at + DOWN * (R_BALL + 0.08))


class A15_TwoTrajectories(Scene):
    def construct(self):
        row_tag(self, "№15")
        lab_top = L("з перону").move_to(np.array([X0 + 0.9, Y_TOP + 1.35, 0]))
        lab_bot = L("з вагона").move_to(np.array([-1.6, Y_BOT + 0.95, 0]))

        t = ValueTracker(0.0)
        ball_p = Dot(platform_view(0), radius=R_BALL, color=FG)
        ball_w = Dot(wagon_view(0), radius=R_BALL, color=FG)
        hand_p = hand(platform_view(0))
        hand_w = hand(wagon_view(0))
        ball_p.add_updater(lambda m: m.move_to(platform_view(t.get_value())))
        ball_w.add_updater(lambda m: m.move_to(wagon_view(t.get_value())))
        hand_p.add_updater(lambda m: m.move_to(
            np.array([X0 + V_TRAIN * t.get_value() * M_TO_U, Y_TOP, 0]) + DOWN * (R_BALL + 0.08)))
        trail_p = TracedPath(ball_p.get_center, stroke_color=ACCENT, stroke_width=SW_CURVE)
        trail_w = TracedPath(ball_w.get_center, stroke_color=ACCENT, stroke_width=SW_CURVE)
        note = scale_note(self, f"справжній масштаб · час сповільнено ×{SLOWMO_15}")

        self.add_subcaption("Та сама подія — очима людини на пероні і очима пасажира.", duration=4)
        self.play(FadeIn(lab_top), FadeIn(lab_bot), FadeIn(ball_p), FadeIn(ball_w),
                  FadeIn(hand_p), FadeIn(hand_w), run_time=1.2)
        self.wait(1.3)

        self.add(trail_p, trail_w)
        self.add_subcaption("Вагон іде 20 м/с. М'яч підкинули на 5 м/с угору.", duration=T_FLIGHT * SLOWMO_15 + 0.5)
        self.play(t.animate.set_value(T_FLIGHT), run_time=T_FLIGHT * SLOWMO_15, rate_func=linear)
        for m in (ball_p, ball_w, hand_p, trail_p, trail_w):
            m.clear_updaters()
        self.wait(0.8)

        # Розміри — щоб пропорції було видно числами
        start = np.array([X0, Y_TOP, 0])
        end = np.array([X0 + L_BALL * M_TO_U, Y_TOP, 0])
        apex_p = platform_view(T_FLIGHT / 2)
        l_brace = BraceBetweenPoints(start, end, direction=DOWN, color=MUTED_TEXT).shift(DOWN * 0.22)
        l_lab = M(rf"{ua_tex(L_BALL, 1)}\ \text{{м}}", SIZE_MATH_MIN).next_to(l_brace, DOWN, buff=0.1)
        h_brace_p = BraceBetweenPoints(apex_p, np.array([apex_p[0], Y_TOP, 0]), direction=RIGHT,
                                       color=MUTED_TEXT).shift(RIGHT * 0.15)
        h_lab_p = M(rf"{ua_tex(H_BALL)}\ \text{{м}}", SIZE_MATH_MIN).next_to(h_brace_p, RIGHT, buff=0.1)
        apex_w = wagon_view(T_FLIGHT / 2)
        h_brace_w = BraceBetweenPoints(apex_w, np.array([0, Y_BOT, 0]), direction=RIGHT,
                                       color=MUTED_TEXT).shift(RIGHT * 0.25)
        h_lab_w = M(rf"{ua_tex(H_BALL)}\ \text{{м}}", SIZE_MATH_MIN).next_to(h_brace_w, RIGHT, buff=0.1)
        self.add_subcaption("Двадцять метрів уперед — і метр двадцять угору. Майже пряма.", duration=5)
        self.play(GrowFromCenter(l_brace), FadeIn(l_lab), run_time=0.8)
        self.play(GrowFromCenter(h_brace_p), FadeIn(h_lab_p), run_time=0.8)
        self.wait(1.6)
        self.add_subcaption("А з вагона — вертикальний відрізок. Угору й назад.", duration=4)
        self.play(GrowFromCenter(h_brace_w), FadeIn(h_lab_w), run_time=0.8)
        self.wait(2.5)

        # Повтор — щоб побачити синхронність ще раз
        for m in (ball_p, ball_w, hand_p):
            m.clear_updaters()
        t.set_value(0)
        ball_p.add_updater(lambda m: m.move_to(platform_view(t.get_value())))
        ball_w.add_updater(lambda m: m.move_to(wagon_view(t.get_value())))
        hand_p.add_updater(lambda m: m.move_to(
            np.array([X0 + V_TRAIN * t.get_value() * M_TO_U, Y_TOP, 0]) + DOWN * (R_BALL + 0.08)))
        self.play(t.animate.set_value(T_FLIGHT), run_time=T_FLIGHT * SLOWMO_15, rate_func=linear)
        for m in (ball_p, ball_w, hand_p):
            m.clear_updaters()

        # Титр зі сценарію
        title = VGroup(T("Одна подія. Два описи.", 40), T("Обидва правильні.", 40, color=ACCENT)).arrange(RIGHT, buff=0.3)
        title.to_edge(UP, buff=0.5)
        self.add_subcaption("Одна подія. Два описи. Обидва правильні.", duration=5)
        self.play(FadeIn(title, shift=DOWN * 0.2), run_time=1)
        self.wait(4)
