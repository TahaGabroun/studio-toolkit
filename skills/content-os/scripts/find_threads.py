#!/usr/bin/env python3
"""Local TF-IDF related-insight groups; no hosted embedding/model calls."""
import argparse,json
from pathlib import Path
def groups(insights,threshold=.25):
    from sklearn.feature_extraction.text import TfidfVectorizer
    from sklearn.metrics.pairwise import cosine_similarity
    texts=[x.get('insight',{}).get('insight_text','') if isinstance(x.get('insight'),dict) else x.get('text','') for x in insights]
    if len(texts)<2:return []
    matrix=TfidfVectorizer(ngram_range=(1,2)).fit_transform(texts);sim=cosine_similarity(matrix);seen=set();out=[]
    for i in range(len(texts)):
        if i in seen:continue
        cluster={i};pending=[i]
        while pending:
            node=pending.pop()
            for j in range(len(texts)):
                if j not in cluster and sim[node,j]>=threshold:cluster.add(j);pending.append(j)
        seen.update(cluster)
        if len(cluster)>1:out.append({'indices':sorted(cluster),'texts':[texts[k] for k in sorted(cluster)],'status':'lexical candidates; editorial review required'})
    return out
if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('insights',type=Path);p.add_argument('output',type=Path);p.add_argument('--threshold',type=float,default=.25);a=p.parse_args()
    try:a.output.write_text(json.dumps(groups(json.loads(a.insights.read_text()),a.threshold),ensure_ascii=False,indent=2)+'\n')
    except ImportError:raise SystemExit('Optional local grouping needs scikit-learn; install it in a venv, or group insights with the agent.')
