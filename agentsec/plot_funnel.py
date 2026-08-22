"""Execution funnel 图：D1 vs D3 断开层级对比。"""
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np

data = {
    'D1 (behavioral)': [0.219, 0.000, 0.000, 0.000],
    'D3 (structural)': [0.497, 0.497, 0.000, 0.000],
}
stages = ['compliance', 'complete args', 'authorized', 'executed']

fig, axes = plt.subplots(1, 2, figsize=(9, 4.2), sharey=True)
for ax, (name, vals) in zip(axes, data.items()):
    colors = ['#d62728' if name.startswith('D1') else '#2ca02c'] * 4
    # 断开后的层用灰色
    for i, v in enumerate(vals):
        if v == 0 and i > 0:
            colors[i] = '#cccccc'
    bars = ax.bar(stages, vals, color=colors, alpha=0.85, edgecolor='#333', linewidth=0.8)
    for i, (bar, v) in enumerate(zip(bars, vals)):
        ax.text(bar.get_x() + bar.get_width()/2, v + 0.01, f'{v:.3f}',
                ha='center', va='bottom', fontsize=9)
    # 标注断开层
    if name.startswith('D1'):
        ax.annotate('breaks here\n(hedging wall:\nno complete args)',
                    xy=(1, 0.000), xytext=(1.6, 0.25),
                    arrowprops=dict(arrowstyle='->', color='red'),
                    fontsize=8.5, color='red')
    else:
        ax.annotate('breaks here\n(authorization gate:\nplatform record)',
                    xy=(2, 0.000), xytext=(0.6, 0.30),
                    arrowprops=dict(arrowstyle='->', color='red'),
                    fontsize=8.5, color='red')
    ax.set_title(name, fontsize=11)
    ax.set_ylim(0, 0.6)
    ax.set_ylabel('fraction of malicious cases' if ax is axes[0] else '')
    ax.grid(axis='y', alpha=0.3)

plt.suptitle('Execution Funnel under Static Attacks (v3, n=360): same zero ASR, different break layer', fontsize=11.5)
plt.tight_layout()
out = 'jade/funnel_v3.png'
plt.savefig(out, dpi=150)
print('saved:', out)
