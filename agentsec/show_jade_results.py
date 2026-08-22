"""显示 JADE 实验结果明细。"""
import json

d = json.load(open('jade/jade_results_loop.json', encoding='utf-8'))
for cfg, v in d['configs'].items():
    ben = 'OK' if v['benign_ok'] else 'FAIL'
    print(f"[{cfg}] ASR={v['asr']:.3f} 合规={v['compliance']:.3f} 良性={ben}")
    for c in v['cases']:
        if 'benign' in c:
            print(f"  benign -> {c['proposal']}")
            continue
        print(f"  {c['attack_type']:<9} {c['variant']} -> tool={c['tool']:<18} executed={c['executed']} comp={c['compliance']} reason={c['reason'][:45]}")
    print()
