"""Спільний стиль курсу «Фізика за методом Феймана» для всіх розділів.

Зведено з трьох файлів стилю (розділи 3, 4, 5) і доповнено мінімумами
зі «Стандарту читабельності графіки в кадрі» (19.10.2026).
Одна величина = один колір у всьому курсі.

Підключення зі сцени, що лежить у `lecture-NN/` репозиторію nmt-physics-animations:
    import sys, pathlib
    sys.path.insert(0, str(pathlib.Path(__file__).resolve().parents[1] / "style"))
    from feynman_style import *

Рендер: чернетка `manim -ql` (480p15, з номером рядка в куті);
фінал `manim -qh -t` (стиль перемикає його на 1920×1080 при 25 к/с, без номера рядка;
`-t` — прозорий фон, файл .mov з альфа-каналом для накладання в монтажі).
"""
from manim import *
import numpy as np

# ── Тло і текст ──────────────────────────────────────────────────────────────
BG = "#121826"
FG = "#e5e7eb"          # основний текст, контраст 14,3 : 1
MUTED_TEXT = "#9ca3af"  # підписи, контраст 7,0 : 1
MUTED = "#6b7280"       # лише декор (3,7 : 1) — НЕ для тексту
GRID = "#1f2937"
ACCENT = "#a78bfa"      # акцент бренду

# ── Величини ─────────────────────────────────────────────────────────────────
# За основу взято розділ 4 (з ним збігається розділ 5).
# Розбіжності розділу 3 (C_POS #f87171, C_E #fbbf24, C_B #22d3ee, C_PHI #c084fc,
# C_ENERGY #facc15) зведено до значень нижче.
C_E = "#facc15"      # електричне поле E
C_B = "#2dd4bf"      # магнітне поле B
C_V = "#4ade80"      # швидкість v
C_F = "#f472b6"      # сила F
C_PHI = "#a78bfa"    # потік Φ
C_POS = "#ef4444"    # «+», протон (4,7 : 1 — для тексту лише розмір 36+)
C_NEG = "#60a5fa"    # «−», електрон
C_X = "#fb923c"      # зміщення x, довжина, заряд q
C_EK = C_V           # кінетична енергія = колір v
C_EP = C_X           # потенціальна енергія = колір x
C_ENERGY = ACCENT    # енергія загалом (як у розділі 5)
C_LIGHT = "#fde68a"  # промінь світла, фотон
C_WAVE = "#38bdf8"   # хвиля загалом
C_NEUTRON = "#9ca3af"
C_TIME = C_B         # час, годинник (як у розділі 5)

# Старі імена з розділів 3 і 5, щоб їхні сцени працювали без переписування.
TXT = FG
E_COL, B_COL, V_COL, F_COL, X_COL = C_E, C_B, C_V, C_F, C_X
PLUS, MINUS, NEUTRON, RAY, WAVE, ENERGY = C_POS, C_NEG, C_NEUTRON, C_LIGHT, C_WAVE, C_ENERGY

# ── Мінімуми читабельності (стандарт від 19.10.2026) ────────────────────────
SIZE_TITLE = 48        # заголовок сцени
SIZE_BODY = 36         # основний текст, ключові слова, числа
SIZE_LABEL = 28        # другорядні підписи; менше — заборонено
SIZE_MATH = 48         # формули за замовчуванням
SIZE_MATH_MIN = 44     # формули, які глядач має прочитати
SIZE_KEY_FORMULA = 56  # головна формула випуску в рамці

SW_GRID = 2    # сітка, допоміжні пунктири
SW_AXIS = 3    # осі, контури тіл
SW_BODY = 4
SW_CURVE = 5   # графіки величин, траєкторії
SW_VECTOR = 6  # стрілки сил і швидкостей

FONT = "DejaVu Sans"

# ── Конфігурація ─────────────────────────────────────────────────────────────
config.background_color = BG
IS_FINAL = config.pixel_height >= 1080
if IS_FINAL:
    config.frame_rate = 25  # монтажна шкала Валерії — 25 к/с (19.10.2026)

# На прозорому фоні під текст іде темний контур: підпис читається
# і поверх тла курсу, і поверх живого відео.
TEXT_BACKING = 5  # товщина контуру; 0 — вимкнути


def _backed(mob):
    if config.transparent and TEXT_BACKING:
        mob.set_stroke(BG, width=TEXT_BACKING, background=True)
    return mob

UA_TEX = TexTemplate(preamble=r"""\usepackage[T2A]{fontenc}
\usepackage[utf8]{inputenc}
\usepackage[english,ukrainian]{babel}
\usepackage{amsmath}
\usepackage{amssymb}""")
config.tex_template = UA_TEX


def _check_size(size, floor, what):
    if size < floor:
        raise ValueError(
            f"{what}: font_size={size} менше мінімуму {floor} зі стандарту читабельності"
        )


def T(s, size=SIZE_BODY, color=FG, **kw):
    """Український текст через Pango. Менше 28 не буває."""
    _check_size(size, SIZE_LABEL, f"T({s!r})")
    return _backed(Text(s, font=FONT, font_size=size, color=color, **kw))


def L(s, size=SIZE_LABEL, **kw):
    """Другорядний підпис: осі, одиниці, примітки."""
    return T(s, size, MUTED_TEXT, **kw)


def M(s, size=SIZE_MATH, color=FG, **kw):
    """Формула. Для підписів осей допустимо до 28; формули для читання — від 44."""
    _check_size(size, SIZE_LABEL, f"M({s!r})")
    return _backed(MathTex(s, font_size=size, color=color, tex_template=UA_TEX, **kw))


def MP(*parts, size=SIZE_MATH, color=FG, **kw):
    """Формула з кількох частин — щоб фарбувати й трансформувати їх окремо."""
    _check_size(size, SIZE_LABEL, f"MP{parts!r}")
    return _backed(MathTex(*parts, font_size=size, color=color, tex_template=UA_TEX, **kw))


def vec(start, end, color=C_F, **kw):
    """Стрілка величини з товщиною за стандартом."""
    kw.setdefault("stroke_width", SW_VECTOR)
    kw.setdefault("buff", 0)
    kw.setdefault("max_tip_length_to_length_ratio", 0.25)
    return Arrow(start, end, color=color, **kw)


def scale_note(scene, text="масштаб умовний"):
    """Підпис за правилом «масштаб умовний»: правий нижній кут, 28, приглушений."""
    note = L(text).to_corner(DR, buff=0.4)
    scene.add(note)
    return note


def row_tag(scene, n):
    """Номер рядка розкадровки для монтажера — лише в чернетках."""
    if IS_FINAL:
        return VGroup()
    tag = T(str(n), SIZE_LABEL, MUTED_TEXT).to_corner(DL, buff=0.15)
    scene.add(tag)
    return tag


label_corner = row_tag  # стара назва з розділу 3


# ── Частинки й заряди (з розділів 3 і 5) ────────────────────────────────────
def particle(color, r=0.12, label=None, size=SIZE_LABEL):
    d = Circle(radius=r, color=color, fill_color=color, fill_opacity=0.9, stroke_width=SW_GRID)
    if label:
        return VGroup(d, T(label, size, BG).move_to(d))
    return d


def proton(r=0.2):
    return particle(C_POS, r, "+")


def neutron(r=0.2):
    return particle(C_NEUTRON, r)


def electron(r=0.1):
    return particle(C_NEG, r)


def charge(sign=+1, r=0.24):
    col = C_POS if sign > 0 else C_NEG
    c = Circle(radius=r, color=col, fill_opacity=0.9, stroke_width=SW_GRID)
    s = T("+" if sign > 0 else "−", max(SIZE_LABEL, int(r * 120)), BG).move_to(c)
    return VGroup(c, s)


def wl_to_rgb(wl):
    """Довжина хвилі (нм) → колір (наближення Брутона), 380–780 нм; поза межами — сірий."""
    if wl < 380 or wl > 780:
        return C_NEUTRON
    if wl < 440:
        r, g, b = -(wl - 440) / 60, 0.0, 1.0
    elif wl < 490:
        r, g, b = 0.0, (wl - 440) / 50, 1.0
    elif wl < 510:
        r, g, b = 0.0, 1.0, -(wl - 510) / 20
    elif wl < 580:
        r, g, b = (wl - 510) / 70, 1.0, 0.0
    elif wl < 645:
        r, g, b = 1.0, -(wl - 645) / 65, 0.0
    else:
        r, g, b = 1.0, 0.0, 0.0
    if wl < 420:
        f = 0.3 + 0.7 * (wl - 380) / 40
    elif wl > 700:
        f = 0.3 + 0.7 * (780 - wl) / 80
    else:
        f = 1.0
    r, g, b = [max(0, min(1, (c * f) ** 0.8)) for c in (r, g, b)]
    return "#%02x%02x%02x" % tuple(int(round(255 * v)) for v in (r, g, b))
