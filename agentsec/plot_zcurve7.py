"""8 点 Z(α) 曲线（7 轮）。"""
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

x = ['Static', 'R1', 'R2', 'R3', 'R4', 'R5', 'R6', 'R7']
data = {
    'D1 refusal (L0)':  ([0.000, 0.000, 0.000, 0.000, 0.000, 0.000, 0.000, 0.000], '#d62728', 'behavioral plateau'),
    'D2 keyword (L1)':  ([0.200, 0.233, 0.467, 0.500, 0.700, 0.733, 0.800, 0.833], '#ff7f0e', 'collapse'),
    'D3 confirm (L2)':  ([0.000, 0.000, 0.000, 0.000, 0.000, 0.000, 0.000, 0.000], '#2ca02c', 'structural plateau'),
    'D4 sandbox (L3)':  ([0.067, 0.067, 0.300, 0.300, 0.300, 0.300, 0.300, 0.300], '#1f77b4', 'erosion'),
}

fig, ax = plt.subplots(figsize=(9.5, 5.5))
for name, (ys, color, morph) in data.items():
    ax.plot(x, ys, marker='o', linewidth=2.2, color=color,
            label=f'{name}  [{morph}]')
    for xi, yi in zip(x, ys):
        ax.annotate(f'{yi:.2f}', (xi, yi), textcoords='offset points',
                    xytext=(0, 8), ha='center', fontsize=7.5, color=color)

ax.set_ylabel('Cumulative ASR  Z(α)', fontsize=11)
ax.set_ylim(-0.02, 0.92)
ax.set_title('Zero stability under 7-round adaptive escalation (v3, real effects, n=30/point)', fontsize=11)
ax.legend(fontsize=8.5, loc='upper left')
ax.grid(alpha=0.3)
plt.tight_layout()
out = 'jade/zcurve7_v3.png'
plt.savefig(out, dpi=150)
print('saved:', out)
