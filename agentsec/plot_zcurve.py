"""Z(α) 曲线：攻击强度（静态→自适应轮次）vs 累计 ASR，D1-D4。"""
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

x = ['Static', 'Round 1', 'Round 2', 'Round 3']
data = {
    'D1 refusal (L0)':  ([0.000, 0.000, 0.000, 0.000], '#d62728', 'behavioral'),
    'D2 keyword (L1)':  ([0.200, 0.200, 0.467, 0.467], '#ff7f0e', 'surface rule'),
    'D3 confirm (L2)':  ([0.000, 0.000, 0.000, 0.000], '#2ca02c', 'authorization'),
    'D4 sandbox (L3)':  ([0.067, 0.067, 0.167, 0.200], '#1f77b4', 'confinement'),
}

fig, ax = plt.subplots(figsize=(8.5, 5.2))
for name, (ys, color, prov) in data.items():
    ax.plot(x, ys, marker='o', linewidth=2.2, color=color,
            label=f'{name}  [{prov}]')
    for xi, yi in zip(x, ys):
        ax.annotate(f'{yi:.3f}', (xi, yi), textcoords='offset points',
                    xytext=(0, 9), ha='center', fontsize=8.5, color=color)

ax.set_ylabel('Cumulative ASR  Z(α)', fontsize=11)
ax.set_ylim(-0.02, 0.55)
ax.set_title('Zero stability under escalating adaptive attacks (v3, real effects, n=30/point)', fontsize=11)
ax.legend(fontsize=8.5, loc='upper left')
ax.grid(alpha=0.3)
plt.tight_layout()
out = 'jade/zcurve_v3.png'
plt.savefig(out, dpi=150)
print('saved:', out)
