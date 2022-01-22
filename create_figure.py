import matplotlib.pyplot as plt

class Figure():
    def __init__(self):
        self.figure =plt.Figure(figsize=(9,8), dpi=100)
    
    def create_figure(self, df):
        marg = 0.15
        ax = self.figure.add_axes([marg, marg, 1-1.8*marg, 1-1.8*marg])
        ax.plot(df['engine_rot_speed'], df['torque_on_wheel'], c='blue', lw=2.5, label="torque_on_wheel", zorder=10)
        ax.plot(df['engine_rot_speed'], df['power_in_KM'], c='red', lw=2.5, label="power[KM]", zorder=10)
        ax.set_xlabel("engine_rot_speed", fontsize=14)
        ax.legend(loc='center left', bbox_to_anchor=(1, 0.5), fontsize=6)
        ax.grid(linestyle="--", linewidth=0.5, color='.25', zorder=-10)

    def save_figure(self, filename):
        self.figure.savefig(filename)
    
    def is_figure_empty(self):
        return len(self.figure.get_axes()) ==  0