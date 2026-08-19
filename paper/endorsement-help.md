# 背书（Endorsement）帮助文档

> 生成：2026-08-18 · 用途：首次提交 arXiv cs.AI 需要背书，本文档提供候选人清单（邮箱已从论文首页核实）+ 现成请求信。
> 诚实声明：邮箱全部从论文 PDF 首页提取（2026-08-18 联网核实）；"xu@sdu.edu.cn" 未能确认具体是哪位作者，谨慎使用。

---

## 一、背书是什么（30 秒版）

- 首次提交到 cs.AI（或任何 cs 类目）需要**一个在该类目近一年发过 arXiv 论文的人**为你担保；
- 不是评审——他在 arXiv 邮件里点一下"同意"即可；
- 你只需要他的**邮箱**，arXiv 系统会把请求发给他，你不直接接触他的私人信息。

## 二、候选人清单（按推荐优先级排序）

| 优先级 | 姓名 | 机构 | 相关论文 | 邮箱（已核实） | 为什么合适 |
|---|---|---|---|---|---|
| ⭐1 | **Tanmoy Chakraborty** | IIT Delhi（资深教授，极活跃） | LM² (EMNLP 2024) | tanchak@ee.iitd.ac.in | 大牛+验证代理架构，回复率高；与你论文"分解-验证"直接相关 |
| ⭐2 | **Ehsan Shareghi** | Monash（资深） | VerifiAgent (2025) | ehsan.shareghi@monash.edu | 验证代理方向通讯作者，主题最贴 |
| ⭐3 | **Ming Zhang（张铭）** | 北京大学（资深教授） | Safe (ACL 2025, Lean 4) | mzhang_cs@pku.edu.cn | 中国教授、形式化验证，语言无障碍 |
| 4 | **Ning Miao** | Oxford | SelfCheck (ICLR 2024) | ning.miao@stats.ox.ac.uk | 自验证方向一作 |
| 5 | **Jiuzhou Han** | Monash | VerifiAgent 一作 | jiuzhou.han@monash.edu | 一作，通常愿意帮 |
| 6 | **Yifei Li** | 北京大学 | DiVERSE (ACL 2023) 一作 | liyifei@stu.pku.edu.cn | 逐步验证器一作 |
| 7 | GoV 作者 | 山东大学 | GoV (2025) | xu@sdu.edu.cn | 同名邮箱，未确认具体人，慎用 |

## 三、arXiv 表单里的背书短消息（复制粘贴）

> 在 arXiv 提交走到 Endorsement 步骤时，需要填一句说明（≤ 几行）：

```
Dear colleague,

I am an independent researcher working on verification frameworks for
large language models. My first arXiv submission (cs.AI) proposes
Verification Autonomy Levels (L0-L5), a meta-standard for classifying
LLM verification schemes by their ground-truth anchor. Your work on
[对应论文] is directly relevant. I would be grateful if you could
endorse my submission.

Thank you,
Yajie Yin (1549080929@qq.com)
```

## 四、给候选人的正式邮件（复制粘贴后改 [ ] 内容）

```
Subject: Endorsement request for arXiv cs.AI submission (LLM verification)

Dear Prof./Dr. [姓名],

I am Yajie Yin, an independent researcher working on verification
frameworks for large language models. I am preparing my first arXiv
submission: "Grading the Graders: Verification Autonomy Levels (L0-L5)
for LLM Reasoning", a conceptual paper proposing a six-level taxonomy
for classifying LLM verification schemes by their ground-truth anchor
(LLM self-declaration -> objective truth -> decidable systems).

Your work on [对应论文名] is directly relevant to this line of work:
[一句话连接，例如 "the step-verification architecture you proposed is
exactly the L2 class we analyze"].

Because this is my first submission to cs.AI, arXiv requires an
endorsement from an author with a recent paper in the category. If you
are comfortable, could you endorse me? It is a quick click on a link
arXiv sends you—not a review.

The full draft is available at:
https://github.com/1549080929-debug/math_agent (paper/preprint.pdf)

Thank you for your time and for your contributions to this area.

Best regards,
Yajie Yin
Email: 1549080929@qq.com
```

## 五、操作建议（重要）

1. **一次只发 1–2 位**，别群发轰炸；等 2–3 天没回再换下一位；
2. 每位候选人的邮件**必须个性化**（改掉 [对应论文] 和"一句话连接"），模板套用会被一眼识破；
3. **绝对不要付钱**——arXiv 背书免费，任何收费"代背书"都是骗局（可能封号）；
4. 背书人只需要有近一年 cs.AI/cs.CL 相关论文即可，不需要认识你；
5. 若 7 位都未回应：找任何你有联系的、发过 arXiv 论文的同行/老师/同学（**任何 cs 类目都行，但必须与你要投的类目一致**）；
6. 拿到背书后，在 arXiv 提交流程里填背书人邮箱 → 他点确认 → 你完成提交 → 审核（几小时到 2 天）。

## 六、如果卡在背书这一步（备选路径）

- 先投**不需要背书的类目**再转？→ 不可行：cs 类目都要背书，数学/物理不要但不适合本文；
- 联系 arXiv 客服（help@arxiv.org）说明情况？→ 仅限特殊情形（如你是学生但导师不可用），一般不会特批；
- 最现实的做法：**多发几封**。LLM 验证是热门方向，这类请求该领域的学者经常收到，接受率不低。
