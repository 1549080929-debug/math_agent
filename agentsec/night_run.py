"""夜间实验 master（2026-08-22，无人值守）：A→B→C 顺序执行。

A: c1a_bounded.py（C1 另一半，DeepSeek）--strong --exploit
   -> results/night_bounded.jsonl
B: adaptive_attack.py D1,D3 × 10 轮（DeepSeek）--tag night2（新 tag 避开 resume 坑）
   -> results/adaptive_night2_D1.json / adaptive_night2_D3.json
C: c1a_experiment_v2.py（C1a 第二受害者 Llama 3.1 8B，本地 Ollama）--strong --exploit
   -> results/night_c1a_llama.jsonl

每步 stdout/stderr -> night_logs/exp{X}.log；全部结束写 night_logs/SUMMARY.txt。
明早的独立聚合/审计在新会话做（本脚本只执行 + 留 trace）。
"""
import datetime
import io
import os
import subprocess
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))
os.chdir(HERE)
os.makedirs('results', exist_ok=True)
os.makedirs('night_logs', exist_ok=True)

PY = sys.executable
LLAMA_ENV = {
    'VICTIM_BASE_URL': 'http://localhost:11434/v1',
    'VICTIM_API_KEY': 'ollama',
    'VICTIM_MODEL': 'llama3.1:8b',
}


def run(name, cmd, env_extra=None):
    env = dict(os.environ)
    if env_extra:
        env.update(env_extra)
    log = os.path.join('night_logs', f'{name}.log')
    t0 = time.time()
    ok = False
    with io.open(log, 'w', encoding='utf-8') as f:
        f.write(f'== {name} start {datetime.datetime.now()} ==\n')
        f.flush()
        try:
            r = subprocess.run(cmd, stdout=f, stderr=subprocess.STDOUT, env=env,
                               encoding='utf-8', errors='replace')
            ok = r.returncode == 0
            f.write(f'== exit {r.returncode} after {(time.time()-t0)/60:.1f} min ==\n')
        except Exception as e:
            f.write(f'== EXCEPTION {e!r} ==\n')
    print(f'[night] {name}: {"OK" if ok else "FAIL"} ({(time.time()-t0)/60:.1f} min)')
    return ok


if __name__ == '__main__':
    results = []
    results.append(('A_bounded', run('expA_bounded', [PY, 'c1a_bounded.py', '--strong', '--exploit',
                                                      '--out', 'results/night_bounded.jsonl'])))
    results.append(('B_adaptive_D1D3_10r', run('expB_adaptive', [PY, 'adaptive_attack.py', '--configs', 'D1,D3',
                                                                 '--rounds', '10', '--tag', 'night2'])))
    results.append(('C_c1a_llama', run('expC_c1a_llama', [PY, 'c1a_experiment_v2.py', '--strong', '--exploit',
                                                          '--out', 'results/night_c1a_llama.jsonl'], LLAMA_ENV)))

    with io.open('night_logs/SUMMARY.txt', 'w', encoding='utf-8') as f:
        f.write(f'night run finished {datetime.datetime.now()}\n')
        for name, ok in results:
            f.write(f'{name}: {"OK" if ok else "FAIL"}\n')
        f.write('--- 明早审计流程 ---\n')
        f.write('1. 独立聚合（勿用实验脚本内部逻辑）：\n')
        f.write('   - bounded: results/night_bounded.jsonl -> 按组算 ASR (specs.is_asr_success)\n')
        f.write('   - adaptive: results/adaptive_night2_D1.json / D3 -> 每轮累计 ASR (Z(alpha))\n')
        f.write('   - c1a_llama: results/night_c1a_llama.jsonl -> ASR/benign 与 DeepSeek 版对比\n')
        f.write('2. trace 级抽检：从 jsonl 抽查 success 判定与 trace 一致\n')
        f.write('3. 对照预测卡核对（docs/27 纪律：声明 vs 结果）\n')
    print('[night] ALL DONE. See night_logs/SUMMARY.txt')
