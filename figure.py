import matplotlib.pyplot as plt
from data_from_df import get_max_power_in_KM

class Figure():
    def __init__(self):
        self.figsize = (8,5)
        self.figure =plt.Figure(figsize=self.figsize, dpi=100)
        self.marg = 0.15
        self.axe_rect = [self.marg, self.marg, 1-1.8*self.marg, 1-1.8*self.marg]
        self.ax = self.figure.add_axes(self.axe_rect)


    def update_figure(self, df):
        self.ax.remove()
        self.ax = self.figure.add_axes(self.axe_rect)
        self.ax.plot(df['engine_rot_speed'], df['torque_on_wheel'], c='blue', lw=1, label="torque_on_wheel", marker='s')
        self.ax.plot(df['engine_rot_speed'], df['power_in_KM'], c='red', lw=1, label="power[KM]", marker='d')
        self.ax.set_xlabel("engine_rot_speed", fontsize=14)
        self.ax.legend(loc='center left', bbox_to_anchor=(1, 0.5), fontsize=6)
        self.ax.text(0.1, 1.1, self.get_max_power_text(df), color='red', fontsize=20, zorder=1, transform=self.ax.transAxes)
        self.ax.grid(linestyle="--", linewidth=0.5, color='.25', zorder=-10)

    def save_figure(self, filename):
        self.figure.savefig(filename)

    def add_moto_name_to_figure(self, motoname):
        self.ax.text(0.5, 1.1, motoname, color='green', fontsize=20, zorder=1, transform=self.ax.transAxes)

    def is_figure_empty(self):
        return len(self.figure.get_axes()) ==  0

    def get_max_power_text(self, df):
        max_power_in_KM = round(get_max_power_in_KM(df),1)
        return 'Pwr=' + str(max_power_in_KM) + 'KM'
