from bokeh.io import curdoc
from bokeh.models import ColumnDataSource, Slider
from bokeh.plotting import figure
from bokeh.layouts import row, column, gridplot, layout
import numpy as np

# Funkcja opisująca model SIR
def sir_model(y, beta, gamma):
    S, I, R = y
    return np.array([
        -beta * S * I,  # Zmiana liczby podatnych
        beta * S * I - gamma * I,  # Zmiana liczby zakażonych
        gamma * I  # Zmiana liczby ozdrowieńców
    ])

# Funkcja do rozwiązywania układu równań różniczkowych metodą Eulera
def rozwiazanie_sir(parametry_poczatkowe, beta, gamma, time_steps, dt):
    S, I, R = parametry_poczatkowe
    results = np.zeros((time_steps, 3))
    results[0] = [S, I, R]

    for t in range(1, time_steps):
        results[t] = results[t - 1] + sir_model(results[t - 1], beta, gamma) * dt

    return results

# Parametry początkowe
S0, I0, R0 = 0.98, 0.02, 0.0
parametry_poczatkowe = (S0, I0, R0)
T = 200  # Całkowity czas symulacji
dt = 0.1  # Długość kroku czasowego
time_steps = int(T / dt)
czas = np.linspace(0, T, time_steps)

# Początkowe wartości beta i gamma
beta = 0.5
gamma = 0.01

# Rozwiązanie początkowe
results = rozwiazanie_sir(parametry_poczatkowe, beta, gamma, time_steps, dt)

# Dane do wykresu
source = ColumnDataSource(data={
    'czas': czas[::10],
    'S': results[::10, 0],
    'I': results[::10, 1],
    'R': results[::10, 2]
})

# Tworzenie wykresu
plot = figure(title="Model SIR", x_axis_label="Czas", y_axis_label="Udział populacji", 
              width=800, height=400)
plot.scatter('czas', 'S', source=source, legend_label="Podatni (S)", line_width=2, color="blue")
plot.line('czas', 'I', source=source, legend_label="Zakażeni (I)", line_width=2, color="pink")
plot.line('czas', 'R', source=source, legend_label="Ozdrowieńcy (R)", line_width=2, color="green")
plot.legend.location = "right"
plot.grid.grid_line_dash = [6, 4]
plot.toolbar.logo = None
plot.toolbar.autohide = True
# Slider do zmiany beta i gamma
beta_slider = Slider(start=0.1, end=1.0, value=beta, step=0.01, title="Beta")
gamma_slider = Slider(start=0.01, end=0.5, value=gamma, step=0.01, title="Gamma",)

# Callback do aktualizacji danych
def update_data(attr, old, new):
    beta_val = beta_slider.value
    gamma_val = gamma_slider.value

    updated_results = rozwiazanie_sir(parametry_poczatkowe, beta_val, gamma_val, time_steps, dt)

    source.data = {
        'czas': czas[::10],
        'S': updated_results[::10, 0],
        'I': updated_results[::10, 1],
        'R': updated_results[::10, 2]
    }

# Połączenie sliderów z funkcją aktualizującą
beta_slider.on_change('value', update_data)
gamma_slider.on_change('value', update_data)

# Layout aplikacji
layout = column( row(plot,beta_slider, gamma_slider))
curdoc().add_root(layout)
