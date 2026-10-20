import matplotlib.pyplot as plt
import numpy as np
from matplotlib.widgets import Button, TextBox

from src.physics.integrator import integrator
from src.physics.scenarios import G
from src.physics.state import Stone

MODEL_LABELS = {"viscous": "F ~ v", "head_on": "F ~ v²"}
T_MAX = 1000.0
FPS = 30

LIMITS = {
    "v₀": (0.0, False, 340.0, " м/с"),
    "α": (0.0, False, 90.0, "°"),
    "m": (0.001, True, 1000.0, " кг"),
    "k": (0.0, True, 100.0, ""),
}

MAX_DRAG_RATE = {"viscous": 10.0, "head_on": 50.0}


def drag_rate(v0, mass, k, model):
    rate = k / mass
    if model == "head_on" and k > 0:
        rate = max(rate * v0, np.sqrt(k * G / mass))
    return rate


def check_range(name, value):
    low, low_included, high, unit = LIMITS[name]
    if (value >= low if low_included else value > low) and value <= high:
        return
    left = "[" if low_included else "("
    raise ValueError(f"{name} должно быть в {left}{low:g}, {high:g}]{unit}")


def simulate(v0, angle_deg, mass, k, model, rtol, atol):
    a = np.radians(angle_deg)
    stone = Stone(mass, np.zeros(2), v0 * np.array([np.cos(a), np.sin(a)]))
    t, y = integrator(model, k, G, stone, (0.0, T_MAX), rtol=rtol, atol=atol)
    return t, y[0], y[1]


class StoneViewer:
    def __init__(self, v0, angle, mass, k, model, rtol, atol):
        self.model = model
        self.tolerances = (rtol, atol)

        self.t = None
        self.x = None
        self.y = None
        self.t_now = 0.0

        self.playing = False

        self.fig = plt.figure(figsize=(8, 5))
        self._build_plot()
        self._build_controls(v0, angle, mass, k)

        self.timer = self.fig.canvas.new_timer(interval=1000 // FPS)
        self.timer.add_callback(self._tick)
        self.timer.start()

        self._reset()

    def _build_plot(self):
        ax = self.ax = self.fig.add_axes([0.08, 0.24, 0.88, 0.7])

        ax.set_xlabel("x, м")
        ax.set_ylabel("y, м")

        ax.grid(alpha=0.3)

        (self.path,) = ax.plot([], [], color="tab:blue", lw=2)

        (self.stone,) = ax.plot([], [], "o", color="dimgray", ms=8, zorder=5)

        self.error = ax.text(
            0.02, 0.97, "", color="red", va="top", transform=ax.transAxes
        )

    def _build_controls(self, v0, angle, mass, k):
        fig = self.fig

        def box(x, width, label, value):
            return TextBox(fig.add_axes([x, 0.04, width, 0.07]), label, f"{value:g}")

        self.box_v0 = box(0.13, 0.07, "v₀, м/с", v0)
        self.box_angle = box(0.26, 0.07, "α, °", angle)
        self.box_mass = box(0.41, 0.07, "m, кг", mass)
        self.box_k = box(0.52, 0.1, "k", k)

        self.boxes = (self.box_v0, self.box_angle, self.box_mass, self.box_k)

        self.btn_model = Button(
            fig.add_axes([0.65, 0.04, 0.1, 0.07]), MODEL_LABELS[self.model]
        )

        self.btn_model.on_clicked(lambda _: self._toggle_model())
        self.btn_play = Button(fig.add_axes([0.85, 0.04, 0.044, 0.07]), "▶")
        self.btn_play.on_clicked(lambda _: self._on_play())
        self.btn_reset = Button(fig.add_axes([0.916, 0.04, 0.044, 0.07]), "■")
        self.btn_reset.on_clicked(lambda _: self._reset())

    def _set_inputs_enabled(self, enabled):
        for box in self.boxes:
            box.stop_typing()
            box.set_active(enabled)
            box.ax.set_facecolor("white" if enabled else "0.85")
            box.text_disp.set_color("black" if enabled else "0.5")

        self.btn_model.set_active(enabled)
        self.btn_model.label.set_color("black" if enabled else "0.5")

    def _toggle_model(self):
        self.model = "head_on" if self.model == "viscous" else "viscous"
        self.btn_model.label.set_text(MODEL_LABELS[self.model])
        self.fig.canvas.draw_idle()

    def _reset(self):
        self.t = self.x = self.y = None
        self.playing = False
        self.btn_play.label.set_text("▶")
        self.path.set_data([], [])
        self.stone.set_data([], [])

        if self.ax.get_legend():
            self.ax.get_legend().remove()

        self._set_inputs_enabled(True)
        self.fig.canvas.draw_idle()

    def _read_params(self):
        values = []

        for name, box in zip(("v₀", "α", "m", "k"), self.boxes):
            try:
                values.append(float(box.text.replace(",", ".")))
            except ValueError:
                raise ValueError(f"{name}: не число")

        for name, value in zip(LIMITS, values):
            check_range(name, value)

        v0, angle, mass, k = values

        max_rate = MAX_DRAG_RATE[self.model]
        if drag_rate(v0, mass, k, self.model) > max_rate:
            raise ValueError(
                "сопротивление слишком сильное для такой массы и скорости\n"
                f"(торможение быстрее {1000 / max_rate:g} мс): уменьшите k или v₀, "
                "увеличьте m"
            )

        return v0, angle, mass, k

    def _start(self):
        try:
            v0, angle, mass, k = self._read_params()

            t, x, y = (
                np.asarray(a, dtype=float)
                for a in simulate(v0, angle, mass, k, self.model, *self.tolerances)
            )
        except Exception as e:
            self.error.set_text(f"Ошибка: {e}")
            self.fig.canvas.draw_idle()
            return

        self.error.set_text("")

        self.t, self.x, self.y = t, x, y
        self.t_now = t[0]

        self._set_inputs_enabled(False)
        self.path.set_label(
            f"v₀ = {v0:g} м/с, α = {angle:g}°, m = {mass:g} кг, "
            f"k = {k:g}, {MODEL_LABELS[self.model]}"
        )
        self.ax.legend(loc="upper right", fontsize=9)
        self._rescale()
        self._set_playing(True)
        self._draw_frame()

    def _rescale(self):
        x0, x1 = min(0.0, self.x.min()), max(self.x.max(), 1.0)
        y0, y1 = min(0.0, self.y.min()), max(self.y.max(), 1.0)
        self.ax.set_xlim(x0 - 0.02 * (x1 - x0), x1 + 0.05 * (x1 - x0))
        self.ax.set_ylim(y0 - 0.02 * (y1 - y0), y1 + 0.2 * (y1 - y0))

    def _set_playing(self, playing):
        self.playing = playing
        self.btn_play.label.set_text("||" if playing else "▶")
        self.fig.canvas.draw_idle()

    def _on_play(self):
        if self.t is None:
            self._start()
        elif self.playing:
            self._set_playing(False)
        elif self.t_now < self.t[-1]:
            self._set_playing(True)

    def _tick(self):
        if not self.playing:
            return
        self.t_now = min(self.t_now + 1 / FPS, self.t[-1])
        if self.t_now >= self.t[-1]:
            self._set_playing(False)
        self._draw_frame()

    def _draw_frame(self):
        i = np.searchsorted(self.t, self.t_now, side="right")
        x_now = np.interp(self.t_now, self.t, self.x)
        y_now = np.interp(self.t_now, self.t, self.y)
        self.path.set_data(np.append(self.x[:i], x_now), np.append(self.y[:i], y_now))
        self.stone.set_data([x_now], [y_now])
        self.fig.canvas.draw_idle()


def run(**params):
    viewer = StoneViewer(**params)
    plt.show()
    return viewer
