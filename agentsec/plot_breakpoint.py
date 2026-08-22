"""初步 breakpoint 图：D1-D4 单防御 × 攻击强度（静态/自适应）ASR。"""
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

# v3 口径数据（重跑后）
defenses = [
    ('D1 refusal (L0)',      'behavioral', 0.000, 0.000, '#d62728'),
    ('D2 keyword (L1)',      'surface rule', 0.200, 0.467, '#ff7f0e'),
    ('D3 confirmation (L2)', 'authorization', 0.000, 0.000, '#2ca02c'),
    ('D4 sandbox (L3)',      'confinement', 0.067, 0.200, '#1f77b4'),
]

x = ['Static', 'Adaptive (3 rounds)']
fig, ax = plt.subplots(figsize=(8, 5))
for name, prov, s, a, color in defenses:
    ax.plot(x, [s, a], marker='o', linewidth=2, color=color, label=f'{name}  [{prov}]')

ax.set_ylabel('ASR (attack success rate)', fontsize=11)
ax.set_ylim(-0.02, 0.55)
ax.set_title('Single-defense zero breakpoints under escalating attacks (v3, real effects, n=360/30)', fontsize=11)
ax.legend(fontsize=8.5, loc='upper left')
ax.grid(alpha=0.3)
for name, prov, s, a, color in defenses:
    ax.annotate(f'{s:.3f}', (x[0], s), textcoords='offset points', xytext=(0, 8), ha='center', fontsize=9, color=color)
    ax.annotate(f'{a:.3f}', (x[1], a), textcoords='offset points', xytext=(0, 8), ha='center', fontsize=9, color=color)

plt.tight_layout()
out = 'jade/breakpoint_v3.png'
plt.savefig(out, dpi=150)
print('saved:', out)
