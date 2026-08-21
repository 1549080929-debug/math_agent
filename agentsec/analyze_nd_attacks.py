"""检查 ND 的 ignore_previous 和 injecagent 攻击族是否真正生效。"""
import json, glob, os

base = r'logs\ad_ND\ND-deepseek\banking'
for atk in ['ignore_previous', 'injecagent', 'system_message']:
    files = glob.glob(os.path.join(base, 'user_task_*', atk, '*.json'))
    print(f'=== {atk} (n={len(files)}) ===')
    for f in files[:3]:
        with open(f, encoding='utf-8') as fh:
            d = json.load(fh)
        print(f'  {d["user_task_id"]}/{d["injection_task_id"]} sec={d["security"]}')
        print('  injections:', json.dumps(d.get('injections'), ensure_ascii=False)[:200])
        # 打印最后几条消息
        for m in d.get('messages', [])[-3:]:
            role = m.get('role')
            content = m.get('content')
            if isinstance(content, list):
                content = ' '.join(c.get('content', '') for c in content if isinstance(c, dict))
            tc = m.get('tool_calls')
            print(f'    [{role}] tc={tc is not None} | {str(content)[:120]}')
    print()
