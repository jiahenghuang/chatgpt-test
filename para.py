#coding:utf-8
import openai
from openai.embeddings_utils import get_embedding, cosine_similarity

openai.api_key = "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"

class Paragraph_Merge():
    '''
    对自然段进行合并
    '''
    def __init__(self):
        pass

    def calc_sim(self, text_a, text_b):
        embedding_a = get_embedding(text_a)
        embedding_b = get_embedding(text_b)
        sim = cosine_similarity(embedding_a, embedding_b)
        return sim

    def get_score(self, sim_a, sim_b, sim_c):
        return sim_a + sim_c - 2 * sim_b

    def get_distance(self, sims):
        result = []
        if len(sims) == 0:
            return None
        if len(sims) == 1:
            return None
        if len(sims) == 2:
            return sims[1] - sims[0]
        else:
            for sim_a, sim_b, sim_c in zip(sims,sims[1:],sims[2:]):
                score = self.get_score(sim_a,sim_b,sim_c)
                result.append(score)
        return result

    def merge_para(self, d):
        result = []
        if len(d) == 1:
            if d[0] > threshold:
                return [[all_paragraphs[0]], [all_paragraphs[1]]]
            else:
                return [all_paragraphs]
        if len(d) > 1:
            start=0
            for i, item in enumerate(d):
                if item > threshold:
                    tmp = all_paragraphs[start:i+1]        
                    result.append(tmp)
                    start = i+1
            result.append(all_paragraphs[start:])
        return result

    def main(self, all_paragraphs, threshold):
        sims = []
        for a,b in zip(all_paragraphs, all_paragraphs[1:]):
            sim = self.calc_sim(a, b)
            sims.append(sim)
        d = self.get_distance(sims)
        print(d)
        result = self.merge_para(d)
        return result


if __name__=='__main__':
    threshold=-0.02
    all_paragraphs = ["应用一个二分类器来识别边界。就像前面提到的例子，我们可以采用一个基于正负标签数据的二分类器来决定是否需要对给定的两个段落进行切分。",
                      "或者使用序列分类器。我们也可以使用像 HMM 或者 RNN 这类序列模型进行分类。这种情况下，我们在分段时会考虑一些上下文信息，从而在分段时得到一个全局最优的决策结果。",
                      "我们还可以潜在地包含分类的章节类型 (section type)，例如：Introduction, Conclusion 等。假如我们使用维基百科或者科学文章，我们知道其中每个章节都有特定的主题/功能，我们可以原问题转换为一个多任务问题：我们不仅对语篇文本进行分段，并且我们还需要给出每个分段所对应的章节",
                      "我们还可以集成一些更宽泛的特征，包括：分布语义学语篇标记（discourse markers），例如：等。语篇标记在这里要更加重要一些，因为它们通常对于语篇分段前后的差异具有放大效应。",
                      "现在，我们将讨论第二个主要任务：语篇解析（Discourse Parsing），其目标是将 语篇单元 (discourse units) 组织成层级结构中的故事线，例如：某段文本是否是对另一段文本的解释。"]
    pm = Paragraph_Merge()
    result = pm.main(all_paragraphs, threshold)
    print(result)