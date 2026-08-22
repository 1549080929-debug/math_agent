"""查看 indirect trace 的多轮细节。"""
import json

for f in ['traces/ND_indirect_M0.json', 'traces/V_indirect_M0.json']:
    d = json.load(open(f, encoding='utf-8'))
    print('=' * 70)
    print(f)
    print('  mcp_desc:', d['mcp_tool_description'][:80])
    for r in d['rounds']:
        print(f'  round{r["round"]}: proposal={r.get("proposal")}')
        raw = repr(r.get('llm_raw_output', ''))
        print(f'    llm_raw={raw[:220]}')
        print(f'    tool_call={r.get("tool_call")}')
        print(f'    defense={r.get("defense")} decision={r.get("decision")}')
