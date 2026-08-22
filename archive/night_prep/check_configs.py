"""Check adaptive CONFIGS keys and c1a script defaults."""
import re, sys
sys.stdout.reconfigure(encoding='utf-8')

src = open('agentsec/adaptive_attack.py', encoding='utf-8').read()
m = re.search(r'CONFIGS\s*=\s*\{(.*?)\n\}', src, re.S)
if m:
    keys = re.findall(r'"([A-Z0-9]+)"\s*:', m.group(1))
    print('CONFIGS keys:', keys)
else:
    print('CONFIGS not found; first 50 lines:')
    print(src[:2000])
