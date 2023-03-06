from HarvestText.harvesttext.harvesttext import HarvestText

def merge(text, num_paras=3):
    ht0 = HarvestText()
    predicted_paras = ht0.cut_paragraphs(text, num_paras=int(num_paras))
    corpus = []
    for i,para in enumerate(predicted_paras):
        result = "段落%d:\n%s" % (i+1,para)
        corpus.append(result)
    return "\n\n".join(corpus)
