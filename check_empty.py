import json

results = {r["id"]: r for r in json.load(open("data/testset_results.json", encoding="utf-8"))}
for pid in (7, 9, 11):
    r = results[pid]
    print(f"#{pid} ok={r['ok']} fv={r['final_verify']} final_answer={r['final_answer']!r}")
    print(f"   answer前200字: {r['answer'][:200]!r}")
    print()
