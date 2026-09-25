# 检索增强生成：面向知识密集型自然语言处理任务

> **文献**：Lewis 等，*Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks*，NeurIPS 2020，arXiv:2005.11401v4
> **原始资料**：[PDF](../../raw/papers/lewis2020-rag-knowledge-intensive-nlp-v4.pdf) · [来源登记卡](../../raw/papers/lewis2020-rag-knowledge-intensive-nlp-v4.md) · [arXiv 官方页面](https://arxiv.org/abs/2005.11401)

## 一、研究背景与核心科学问题

### 1. 广泛背景

预训练语言模型能够把事实知识编码进参数，但难以直接扩展、修订或解释其知识来源。在知识密集型任务中，仅依赖参数记忆可能导致知识更新困难、证据不可追溯和事实性不足。

### 2. 具体问题

本文研究如何把**参数化记忆**与可读、可替换的**非参数化记忆**组合到一个通用生成模型中，使同一架构能够处理开放域问答、抽象问答、问题生成和事实核验等任务。非参数化记忆由 Wikipedia 文本块构成，参数化记忆由预训练序列到序列模型承担。研究对象、任务和数据范围均在文献的实验部分定义，而非对所有知识任务作无条件外推。

### 3. 核心科学问题

在不为每个任务设计独立检索与抽取流水线的条件下，检索器和生成器能否通过端到端微调协同工作，从外部文本记忆中获得更好的准确性、事实性、特异性和可更新性？

## 二、研究设计

研究者构建 Retrieval-Augmented Generation（RAG）模型，将 DPR 风格的密集检索器与 BART-large 生成器组合，并把检索到的文档视为潜变量进行边缘化。实验覆盖四类开放域问答、抽象问答、Jeopardy 问题生成和 FEVER 事实核验；同时设置 BART、DPR、REALM、T5 等参数化或检索式基线，并开展冻结检索器、BM25 检索、检索数量和索引热替换实验。

## 三、数据与样本来源

### 1. 外部知识库

- 来源：2018年12月 Wikipedia dump。
- 处理：每篇文章切分为互不重叠的 100 词文本块。
- 规模：约 2100 万个文档块。
- 索引：使用文档编码器生成向量，并用 FAISS 的近似最大内积搜索建立索引。

### 2. 任务数据

| 任务                |     训练集 |    开发集 |      测试集 | 任务形式       |
| ----------------- | ------: | -----: | -------: | ---------- |
| Natural Questions |  79,169 |  8,758 |    3,611 | 开放域问答      |
| TriviaQA          |  78,786 |  8,838 |   11,314 | 开放域问答      |
| WebQuestions      |   3,418 |    362 |    2,033 | 开放域问答      |
| CuratedTrec       |     635 |    134 |      635 | 开放域问答      |
| Jeopardy 问题生成     |  97,392 | 13,714 |   26,849 | 知识密集型生成    |
| MS-MARCO          | 153,726 | 12,468 | 101,093* | 抽象问答       |
| FEVER 三分类         | 145,450 | 10,000 |   10,000 | 支持/反驳/信息不足 |
| FEVER 二分类         |  96,966 |  6,666 |    6,666 | 支持/反驳      |

`*` 文献注明 MS-MARCO 测试集包含隐藏子集。以上规模来自 Table 7（`doc:23e3249/tier:standard/page:19`）。

## 四、方法与技术

### 1. 检索器

检索器采用 DPR 双编码器。查询编码器将输入 (x) 映射为 (mathbf q(x))，文档编码器将文档 (z) 映射为 (mathbf d(z))，并依据内积计算检索分布：

\[
p_\eta(z\mid x)\propto\exp\big(\mathbf d(z)^\top\mathbf q(x)\big)。
\]

文档编码器和文档索引预先建立并在训练中保持固定；查询编码器参与微调。检索阶段默认取前 (K) 个文档，训练中比较 (K=5) 和 (K=10)，测试时依据开发集选择检索数量。

### 2. 生成器

生成器采用 4 亿参数规模的 BART-large。输入文本 (x) 与检索文档 (z) 被拼接后输入序列到序列生成器，输出目标序列 (y)。

### 3. 两种 RAG 形式

- **RAG-Sequence**：同一检索文档负责整个输出序列，先计算每个文档条件下的序列概率，再对文档进行边缘化。
- **RAG-Token**：每个输出 token 都可以依据不同检索文档生成，再对 token 级文档分布进行边缘化。

两种模型都把文档视为潜变量，用前 (K) 个候选文档近似完整边缘化；RAG-Token 更容易组合多个文档的信息，RAG-Sequence 则保留整段输出由同一文档解释的结构假设（`doc:23e3249/tier:standard/page:2`）。

### 4. 训练与解码

训练目标是输入—输出样本的负对数似然，并使用 Adam 进行随机梯度下降。RAG-Token 可以直接使用标准 beam decoder；RAG-Sequence 为每个文档分别进行 beam search，再通过 Thorough Decoding 或 Fast Decoding 近似整句概率。

### 5. 工具与实验平台

文献使用 Fairseq 训练，并在 8 张 32GB NVIDIA V100 GPU 上进行分布式训练；推理可在单 GPU 上运行。FAISS 索引向量存储在 CPU 内存中，完整 Wikipedia 索引约需 100GB CPU 内存，压缩后可降至约 36GB。论文后续还提供了 Hugging Face Transformers 实现（`doc:23e3249/tier:standard/page:17`）。

## 五、分析流程

1. 下载并固定 2018 年 12 月 Wikipedia 原始知识库。
2. 将文章切分为 100 词文档块，使用 DPR 文档编码器生成向量并建立 FAISS 索引。
3. 对每个任务的输入 (x) 使用查询编码器检索前 (K) 个候选文档。
4. 将 (x) 与各候选文档拼接，输入 BART-large 生成目标序列或类别 token。
5. 以潜变量边缘化方式聚合不同文档的生成概率，并端到端微调查询编码器与生成器。
6. 在问答、生成和事实核验任务上与基线比较，再通过冻结检索器、BM25、检索数量变化和索引热替换拆解性能来源。
7. 使用自动指标、人工成对评价和定性生成案例交叉检查准确性、事实性、特异性、多样性与知识更新能力。

## 六、核心发现

1. RAG-Sequence 在四个开放域问答任务上取得文中报告的最佳或并列最佳结果：Natural Questions 44.5 EM、TriviaQA 56.8/68.0 EM、WebQuestions 45.2、CuratedTrec 52.2（Table 1）。
2. 检索增强不只适用于抽取式问答：在 MS-MARCO 抽象问答中，RAG-Sequence 相对 BART 的 BLEU-1 和 Rouge-L 均提高 2.6 个百分点。
3. 在 Jeopardy 问题生成中，RAG-Token 的 Q-BLEU-1 为 22.2，高于 BART 的 19.7；人工评价中 RAG 被认为更具事实性的比例为 42.7%，BART 为 7.1%。
4. 检索器与生成器存在互补关系：检索文档可提供事实约束和生成线索，参数化记忆仍可补全文档中未直接出现的内容。Natural Questions 中，即使正确答案不在任一检索文档内，RAG 仍报告 11.8% 的准确率，而抽取式模型在该情形下为 0%。
5. 非参数记忆可以热替换：使用 2016 年索引回答 2016 年世界领导人问题的准确率为 70%，使用 2018 年索引回答 2018 年问题为 68%；索引与问题年份错配时准确率降至 12% 和 4%。这支持了“更新外部索引即可更新部分世界知识”的结论。

## 七、实验结果

### 1. 主结果

| 模型 | NQ EM | TQA EM（标准/ Wiki） | WQ | CT | Jeopardy Q-BLEU-1 | MS-MARCO Rouge-L / BLEU-1 | FEVER 三分类 | FEVER 二分类 |
| --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| BART | - | - | - | - | 19.7 | 38.2 / 41.6 | 64.0 | 81.1 |
| RAG-Token | 44.1 | 55.2 / 66.1 | 45.5 | 50.0 | 22.2 | 40.1 / 41.5 | 72.5 | 89.5 |
| RAG-Sequence | 44.5 | 56.8 / 68.0 | 45.2 | 52.2 | 21.4 | 40.8 / 44.2 | 72.5 | 89.5 |

表中数值来自 Table 1 和 Table 2（`doc:23e3249/tier:standard/page:6`）。不同任务的指标不可直接横向合并为单一总分；表中仅在原论文定义的任务内比较。

### 2. 消融与检索分析

- 可学习检索优于冻结检索：论文报告学习检索在所有任务上改善结果；例如 NQ 上 RAG-Token 从冻结检索的 37.8 提升到 43.5，RAG-Sequence 从 41.2 提升到 44.0。
- BM25 并非所有任务都占优：FEVER 的实体密集型声明更适合词面重叠，而开放域问答更依赖可微密集检索。
- 生成多样性：在三元组比例指标上，MS-MARCO 中 BART 为 70.7%、RAG-Token 为 77.8%、RAG-Sequence 为 83.5%；Jeopardy 问题生成中分别为 32.4%、46.8% 和 53.8%（Table 5）。
- 检索数量：RAG-Sequence 的 NQ 表现随测试时检索文档增加而单调改善；RAG-Token 在 10 个文档附近达到峰值，更多检索会改变 Rouge-L 与 BLEU-1 的权衡（Figure 3）。

### 3. 资源与规模

论文报告模型总规模约为 626M 参数，非参数索引包含 2100 万个 728 维向量。该记忆库不是可训练参数，但带来显著 CPU 内存和索引管理成本。

## 八、Figure 与 Table 索引

| 编号 | 标题 | 核心内容 | MinerU 定位 |
| --- | --- | --- | --- |
| Figure 1 | Overview of our approach | 展示查询编码器、文档索引、生成器和对潜在文档的边缘化流程 | `doc:23e3249/tier:standard/page:2/block:1` |
| Figure 2 | RAG-Token document posterior | 以 Hemingway 的 Jeopardy 生成示例展示不同 token 对不同文档的后验偏好 | `doc:23e3249/tier:standard/page:7/block:3` |
| Figure 3 | NQ performance / retrieval recall / MS-MARCO metrics | 展示检索数量对 NQ、检索召回和 MS-MARCO 指标的影响 | `doc:23e3249/tier:standard/page:8/block:10`–`block:12` |
| Figure 4 | Annotation interface for human evaluation of factuality | 展示事实性人工评价界面与随机化评价设计 | `doc:23e3249/tier:standard/page:17/block:5` |
| Table 1 | Open-Domain QA Test Scores | 比较闭卷、开放书和 RAG 模型在四个开放域问答任务上的 EM | `doc:23e3249/tier:standard/page:6` |
| Table 2 | Generation and classification Test Scores | 比较 Jeopardy、MS-MARCO 和 FEVER 的生成/分类结果 | `doc:23e3249/tier:standard/page:6` |
| Table 3 | Examples from generation tasks | 给出 MS-MARCO 和 Jeopardy 的生成案例，比较事实性与特异性 | `doc:23e3249/tier:standard/page:7` |
| Table 4 | Human assessments for the Jeopardy Question Generation Task | 汇总事实性与特异性的人工成对评价 | `doc:23e3249/tier:standard/page:8` |
| Table 5 | Ratio of distinct to total tri-grams | 比较不同模型在两类生成任务中的多样性 | `doc:23e3249/tier:standard/page:8` |
| Table 6 | Ablations on the dev set | 比较 BM25、冻结检索和可学习检索的影响 | `doc:23e3249/tier:standard/page:8` |
| Table 7 | Number of instances in the datasets used | 列出八类任务的训练、开发和测试集规模 | `doc:23e3249/tier:standard/page:19` |

## 九、Introduction 与 Discussion 结构映射

### Introduction：倒三角

1. **广泛背景**：参数化语言模型具有事实记忆，但存在知识修订、来源解释和事实性问题。
2. **具体领域**：将范围收敛到知识密集型 NLP，覆盖问答、生成和事实核验，并用 Wikipedia 作为可读的外部知识库。
3. **中心论点**：将预训练检索器、非参数文档索引和预训练生成器端到端组合，可以在多个知识密集型任务上取得竞争力，同时保留外部记忆可替换的更新路径。

### Discussion：正三角

1. **重申论点**：RAG 通过参数化记忆与非参数化记忆的协同，实现了统一的检索增强生成框架。
2. **综合观点**：主结果证明任务收益，消融证明检索学习的作用，人工评价和生成案例补充事实性/特异性证据，索引热替换实验支持知识更新论点。
3. **扩展背景**：该方法为可解释、可更新的知识型生成系统提供了路线，但 Wikipedia 的偏差与过时性、检索坍缩、索引内存成本和 FEVER 证据抽取缺口限制了结论的适用边界。

## 十、Discussion 论证框架

- **自证**：用主结果、冻结检索/BM25 消融、检索数量曲线和索引热替换构成内部证据链，分别回答“是否有效”“是否由可学习检索带来”“资源规模如何影响结果”“知识是否可更新”。
- **旁征**：与 BART、DPR、REALM、T5 等同领域基线比较，说明 RAG 在生成灵活性、检索利用和开放域问答之间的相对位置。
- **博引**：当前页面只整理本文已引用的对比证据，未声称完成后续文献的系统复核。后续可围绕检索增强生成的事实性、知识更新、偏差和检索坍缩补充独立文献，并明确区分不同数据集、模型规模和评估协议。

## 十一、局限性与不确定性

1. 主要知识库是 2018 年 12 月 Wikipedia，不能直接代表当前世界知识；热替换实验只证明了本文设置下的索引更新现象。
2. Wikipedia 可能包含事实错误、偏差和覆盖缺口，检索增强不等于事实保证。
3. 论文报告了部分任务中的 retrieval collapse：检索器可能对不同输入返回相同文档，生成器随后忽略外部文档并退化为类似 BART 的行为。
4. FEVER 实验主要处理标签分类，未直接完成因使用不同 Wikipedia dump 而变得困难的证据句抽取任务。
5. 训练和索引的硬件、内存与数据规模较大；小型设备或私有数据集不能直接复现实验资源条件。
6. 文中数值依赖特定数据切分、检索数量、解码策略和基线实现，不能将单项指标外推为所有生成任务的普遍改进。

## 十二、与当前 Second Brain 的关联

- RAG 的“原始文档 → 检索 → 编译答案”结构与本库的 `raw/` → `wiki/` 编译路径同构，可作为外部知识接入和来源追溯的概念参照。
- 论文明确展示了非参数记忆可替换、可读、可更新的优点，这支持将原始资料保持不变、把结论编译到 Wiki 的工作区约定。
- 本页的 MinerU locator 使每个关键结论可以回到 PDF 页/块；后续新增文献时应复用同一证据粒度，而不是只保留无定位的摘要。
- 可验证的下一步是：选取本库中的一组公开资料，比较“仅参数化总结”和“先检索原始资料再总结”的来源覆盖率与事实核对率；该实验尚未在本页执行。

## 参考文献

1. Lewis, P. et al. *Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks*. NeurIPS 2020. arXiv:2005.11401v4. [arXiv](https://arxiv.org/abs/2005.11401).
