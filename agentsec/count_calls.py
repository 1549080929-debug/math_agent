"""核算总 LLM 调用量：从结果文件 + REPORT 记录统计。"""
import json
import glob
import os

results_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'results')
print('=== 静态实验（results/*.json 实际 cases 数） ===')
static_total = 0
for f in sorted(glob.glob(os.path.join(results_dir, '*.json'))):
    name = os.path.basename(f)
    if 'agentdojo' in name or 'adaptive' in name or 'pairlite' in name or 'benign' in name:
        continue
    try:
        d = json.load(open(f, encoding='utf-8'))
        n = len(d.get('results', []))
        static_total += n
        print(f'  {name}: {n} cases')
    except Exception as e:
        print(f'  {name}: ERR {e}')

print(f'静态（非良性）合计: {static_total}')

print('\n=== 良性（results/*_benign.json） ===')
benign_total = 0
for f in sorted(glob.glob(os.path.join(results_dir, '*_benign*.json'))):
    name = os.path.basename(f)
    try:
        d = json.load(open(f, encoding='utf-8'))
        n = len(d.get('results', []))
        benign_total += n
        print(f'  {name}: {n} cases')
    except Exception as e:
        print(f'  {name}: ERR {e}')
print(f'良性合计: {benign_total}')

print('\n=== 自适应/白盒/PAIR（adaptive*.json + pairlite*.json） ===')
misc_total = 0
for f in sorted(glob.glob(os.path.join(results_dir, 'adaptive*.json')) + glob.glob(os.path.join(results_dir, 'pairlite*.json'))):
    name = os.path.basename(f)
    try:
        d = json.load(open(f, encoding='utf-8'))
        n = len(d.get('results', []))
        misc_total += n
        print(f'  {name}: {n} cases')
    except Exception:
        # 可能不是 cases 结构
        print(f'  {name}: (非标准结构，跳过计数)')
print(f'自适应/PAIR 合计: {misc_total}')

print('\n=== JADE 实验（jade/*.json） ===')
jade_total = 0
for f in sorted(glob.glob(os.path.join(results_dir, '..', 'jade', '*.json'))):
    name = os.path.basename(f)
    if 'results' not in name:
        continue
    try:
        d = json.load(open(f, encoding='utf-8'))
        # jade_mcp_results: configs -> each has cases
        if 'configs' in d:
            n = sum(len(v.get('cases', [])) for v in d['configs'].values())
        else:
            n = 0
        jade_total += n
        print(f'  {name}: ~{n} cases')
    except Exception as e:
        print(f'  {name}: ERR {e}')
print(f'JADE 合计（非良性）: {jade_total}')

print('\n=== 汇总（近似，每 case 约 1 次 LLM 调用；indirect/自适应有额外轮次） ===')
print(f'静态+良性: {static_total + benign_total}')
print(f'全部（不含 AgentDojo）: {static_total + benign_total + misc_total + jade_total}')
print('AgentDojo: 144 对 × 6 配置 × 每对 ~2-3 次调用 ≈ 1700-2600（估计）')
