"""深入分析 TF：tool_filter 输出 vs 实际工具名匹配，确认工具过滤逻辑。"""
import json, os, glob
from collections import Counter, defaultdict

BANKING_TOOLS = ['get_iban', 'send_money', 'schedule_transaction', 'update_scheduled_transaction',
                 'get_balance', 'get_most_recent_transactions', 'get_scheduled_transactions',
                 'read_file', 'get_user_info', 'update_password', 'update_user_info']

base = r'logs\ad_TF\TF-deepseek\banking'
files = glob.glob(os.path.join(base, 'user_task_*', '*', '*.json'))

# 统计每个任务的 tool_filter 输出
by_task = defaultdict(list)
for f in files:
    with open(f, encoding='utf-8') as fh:
        d = json.load(fh)
    task = d['user_task_id']
    # tool_filter 输出是第 4 条消息（index 3）
    msgs = d.get('messages', [])
    tf_output = None
    for m in msgs:
        if m.get('role') == 'assistant' and m.get('tool_calls') is None:
            content = m.get('content', '')
            if isinstance(content, list):
                content = ' '.join(c.get('content', '') for c in content if isinstance(c, dict))
            tf_output = content
            break
    by_task[task].append((d['injection_task_id'], d['attack_type'], tf_output, d['utility']))

# 对每个任务，看 tool_filter 输出的工具名是否匹配实际工具
for task in sorted(by_task):
    outputs = set()
    for _, _, out, _ in by_task[task]:
        if out:
            outputs.add(out)
    print(f'\n=== {task} ===')
    for out in sorted(outputs):
        # 检查输出中的词是否匹配工具名
        matched = [t for t in BANKING_TOOLS if t in out]
        print(f'  TF输出: "{out}" -> 匹配工具: {matched}')
