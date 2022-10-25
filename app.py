import tkinter as tk
import webbrowser
import numpy as np
import matplotlib.pyplot as plt
from config import *
from tkinter.messagebox import showinfo, showerror
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from compartment import reset_comp


def rk4(t0, compartments) -> None:
    s, e, i, r = compartments
    h = (DAYS-t0)/DAYS
    for t in np.linspace(t0, DAYS, DAYS):
        k1, k2, k3, k4 = [], [], [], []
        for comp in (s, e, i, r):  # calls the f function for each object
            k1.append(h * comp.f(t, s.pop, e.pop, i.pop, r.pop))
        for comp in (s, e, i, r):
            k2.append(h * comp.f(t + h / 2., s.pop + k1[0] / 2., e.pop + k1[1] / 2., 
                                 i.pop + k1[2] / 2., r.pop + k1[3] / 2.))
        for comp in (s, e, i, r):
            k3.append(h * comp.f(t + h / 2., s.pop + k2[0] / 2., e.pop + k2[1] / 2., 
                                 i.pop + k2[2] / 2., r.pop + k2[3] / 2.))
        for comp in (s, e, i, r):
            k4.append(h * comp.f(t + h, s.pop + k3[0], e.pop + k3[1], 
                                 i.pop + k3[2], r.pop + k3[3]))
        for k, comp in enumerate((s, e, i, r)):
            comp.pop += (1. / 6) * (k1[k] + 2 * k2[k] + 2 * k3[k] + k4[k])
            comp.plot_list.append(comp.pop / POPULATION)


def open_url() -> None:
    print(f'Opening github repository...')
    webbrowser.open_new_tab('https://github.com/xbandrade/seir-model-rk4')


def info() -> None:
    print(f'Showing info...')
    text = ['SEIR Model solved by fourth order Runge-Kutta Method (RK4)',
            'Parameters:',
            'β - Transmission rate',
            'γ - Recovery/discharge rate',
            'μ - Natural death rate',
            'α - Probability to become infectious after being exposed',
            'ε - Death by disease rate',
            ]
    showinfo(title='Info', message='\n'.join(text))


class Toolbar(NavigationToolbar2Tk):
    """Override set_message to hide coordinates"""
    def set_message(self, s) -> None:
        pass


class App(tk.Tk):
    def __init__(self) -> None:
        super().__init__()
        self.title('SEIR Model')
        self.geometry('1000x600')
        self.resizable(False, False) 
        self.config(background='#d8dcd6')
        self.protocol("WM_DELETE_WINDOW", self.on_exit)

    def on_exit(self) -> None:
        # if askyesno("Exit", "Do you want to quit the application?"):
        self.quit()
        self.destroy()


class MainFrame(tk.Frame):
    def __init__(self, container, compartments) -> None:
        super().__init__(container, background='#d8dcd6')
        self.container = container
        self.compartments = compartments
        self.grid(sticky='snwe')
        self.fig = plt.Figure(figsize=(10, 5))
        self.ax = self.fig.add_subplot
        self.canvas_plot = FigureCanvasTkAgg(self.fig, master=self.container)
        self.entries = []
        self.img = [tk.PhotoImage(file='img/github.png'), tk.PhotoImage(file='img/info.png')]
        self.plot()
        self.entry_box()
        self.update_plot()
        self.buttons()

    def buttons(self) -> None:
        button1 = tk.Button(self, text='Plot')
        button1['command'] = self.update_plot
        button1.grid(row=0, column=10, padx=10, pady=10)
        button2 = tk.Button(self, text='Default Values')
        button2['command'] = self.set_default
        button2.grid(row=0, column=11, padx=10)    
        button3 = tk.Button(self, command=info, image=self.img[1])
        button3.grid(row=0, column=12, padx=10)
        button4 = tk.Button(self, command=open_url, image=self.img[0])
        button4.grid(row=0, column=13, padx=10)

    def set_default(self) -> None:
        v1, v2, v3, v4, v5 = self.entry_box
        v1.set(round(BETA, 7))
        v2.set(round(RECOVERY_RATE, 7))
        v3.set(round(NATURAL_DEATH, 7))
        v4.set(round(EXP_TO_INFECTIOUS, 7))
        v5.set(round(DISEASE_DEATH, 7))

    def new_values(self) -> tuple[str] | None:
        v1, v2, v3, v4, v5 = self.entries
        s, e, i, r = self.compartments
        try:
            x = v1.get(), v2.get(), v3.get(), v4.get(), v5.get()
        except tk.TclError:
            x = None
            showerror('Error', 'Parameters were not filled correctly.')
        else:
            s.beta = e.beta = i.beta = r.beta = float(x[0])
            s.gamma = e.gamma = i.gamma = r.gamma = float(x[1])
            s.mu = e.mu = i.mu = r.mu = float(x[2])
            s.alpha = e.alpha = i.alpha = r.alpha = float(x[3])
            s.epsilon = e.epsilon = i.epsilon = r.epsilon = float(x[4])
        finally:
            return x

    def entry_box(self) -> None:
        vcmd = (self.register(self.validate), '%d', '%i', '%P', '%s', '%S', '%v', '%V', '%W')
        # Beta
        tk.Label(self, text='β', background='#d8dcd6').grid(row=0, column=0)
        v1 = tk.DoubleVar()
        e1 = tk.Entry(self, width=10, textvariable=v1, validate='key', validatecommand=vcmd)
        v1.set(round(BETA, 7))
        e1.grid(row=0, column=1, padx=10)
        # Gamma
        tk.Label(self, text='γ', background='#d8dcd6').grid(row=0, column=2)
        v2 = tk.DoubleVar()
        e2 = tk.Entry(self, width=10, textvariable=v2, validate='key', validatecommand=vcmd)
        v2.set(round(RECOVERY_RATE, 7))
        e2.grid(row=0, column=3, padx=10)
        # Mu
        tk.Label(self, text='μ', background='#d8dcd6').grid(row=0, column=4)
        v3 = tk.DoubleVar()
        e3 = tk.Entry(self, width=10, textvariable=v3, validate='key', validatecommand=vcmd)
        v3.set(round(NATURAL_DEATH, 7))
        e3.grid(row=0, column=5, padx=10)
        # Alpha
        tk.Label(self, text='α', background='#d8dcd6').grid(row=0, column=6)
        v4 = tk.DoubleVar()
        e4 = tk.Entry(self, width=10, textvariable=v4, validate='key', validatecommand=vcmd)
        v4.set(round(EXP_TO_INFECTIOUS, 7))
        e4.grid(row=0, column=7, padx=10)
        # Epsilon
        tk.Label(self, text='ε', background='#d8dcd6').grid(row=0, column=8)
        v5 = tk.DoubleVar()
        e5 = tk.Entry(self, width=10, textvariable=v5, validate='key', validatecommand=vcmd)
        v5.set(round(DISEASE_DEATH, 7))
        e5.grid(row=0, column=9, padx=10)
        self.entries = [v1, v2, v3, v4, v5]

    def validate(self, action, index, value_if_allowed, prior_value, text, validation_type,
                 trigger_type, widget_name) -> bool:
        if action == '1':
            if text in '0123456789.-+e':
                try:
                    if text == '-' and index == '0':
                        return True
                    if len(value_if_allowed) > 10:
                        return False
                    float(value_if_allowed)
                    return True
                except ValueError:
                    return False
            else:
                return False
        return True

    def plot(self) -> None:
        self.canvas_plot.draw()
        toolbar = Toolbar(self.canvas_plot, pack_toolbar=False)
        toolbar.config(background='#d8dcd6')
        toolbar._message_label.config(background='#d8dcd6')
        for button in toolbar.winfo_children():
            button.config(background='#d8dcd6')
        toolbar.update()
        toolbar.grid(row=2, column=0, sticky='nw')
        self.canvas_plot.get_tk_widget().grid(row=1, column=0, sticky='nw')

    def update_plot(self) -> None:
        if not self.new_values():
            return
        s, e, i, r = reset_comp(self.compartments)
        rk4(T_0, self.compartments)
        s_i, e_i, i_i, r_i = s.plot_list, e.plot_list, i.plot_list, r.plot_list
        t = np.linspace(T_0, DAYS, DAYS)
        self.fig.clear()
        self.ax = self.fig.add_subplot(111)
        self.ax.clear()
        self.fig.patch.set_facecolor('xkcd:light gray')
        self.ax.set_facecolor('xkcd:light gray')
        self.ax.set_xlabel('Time (days)')
        self.ax.set_ylabel('Population (%)')
        self.ax.grid(alpha=0.6)
        self.ax.plot(t, s_i, label='Susceptible')
        self.ax.plot(t, e_i, label='Exposed')
        self.ax.plot(t, i_i, label='Infectious')
        self.ax.plot(t, r_i, label='Recovered')
        self.ax.legend(loc=2, bbox_to_anchor=(1, 1), facecolor='#d8dcd6')
        self.ax.set_xlim((0, DAYS))
        self.ax.set_ylim((0, 1.01))
        plt.tight_layout()
        box = self.ax.get_position()
        self.ax.set_position([box.x0, box.y0, box.width * 0.8, box.height])
        self.canvas_plot.draw_idle()