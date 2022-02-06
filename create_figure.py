import matplotlib.pyplot as plt
from data_from_df import get_max_power_in_KM

class Figure():
    def __init__(self):
        self.figsize = (6,5)
        self.figure =plt.Figure(figsize=self.figsize, dpi=100)
        self.marg = 0.15
        
    def create_figure(self, df):
        self.figure =plt.Figure(figsize=self.figsize, dpi=100)
        ax = self.figure.add_axes([self.marg, self.marg, 1-1.8*self.marg, 1-1.8*self.marg])
        ax.plot(df['engine_rot_speed'], df['torque_on_wheel'], c='blue', lw=1, label="torque_on_wheel", marker='s')
        ax.plot(df['engine_rot_speed'], df['power_in_KM'], c='red', lw=1, label="power[KM]", marker='d')
        ax.set_xlabel("engine_rot_speed", fontsize=14)
        ax.legend(loc='center left', bbox_to_anchor=(1, 0.5), fontsize=6)
        ax.text(0.5, 1.1, self.get_max_power_text(df), color='red', fontsize=20, zorder=1, transform=ax.transAxes)
        ax.grid(linestyle="--", linewidth=0.5, color='.25', zorder=-10)

    def save_figure(self, filename):
        self.figure.savefig(filename)
    
    def is_figure_empty(self):
        return len(self.figure.get_axes()) ==  0
    
    def get_max_power_text(self, df):
        max_power_in_KM = get_max_power_in_KM(df)
        return 'Pwr=' + str(max_power_in_KM) + 'KM'