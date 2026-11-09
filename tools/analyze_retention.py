#!/usr/bin/env python3
"""Descriptive retention-cliff ranking from an uploaded CSV; no causal claims."""
import argparse
import csv
import statistics
from pathlib import Path
import sys

def seconds(raw):
    value=str(raw).strip();parts=value.split(':')
    if len(parts)==1:return float(value.rstrip('s'))
    result=0.0
    for part in parts: result=result*60+float(part)
    return result

def analyze(path,n=5):
    with Path(path).open(encoding='utf-8-sig',newline='') as f: rows=list(csv.DictReader(f))
    if not rows: raise ValueError('Empty CSV')
    cols={x.lower().strip():x for x in rows[0].keys()}
    tcol=next((cols[x] for x in ['time','time_s','seconds','timestamp','elapsed_time'] if x in cols),None)
    rcol=next((cols[x] for x in ['retention','retention_percent','audience_retention','relative_retention','value'] if x in cols),None)
    if not tcol or not rcol: raise ValueError('Requires time/seconds and retention/retention_percent columns')
    vals=sorted([(seconds(row[tcol]),float(str(row[rcol]).strip().rstrip('%'))) for row in rows],key=lambda x:x[0])
    if any(b<=a for (a,_),(b,__) in zip(vals,vals[1:])): raise ValueError('Repeated/unsorted time samples')
    if max(y for _,y in vals)<=1.5: vals=[(t,r*100) for t,r in vals]
    deltas=[{'start_s':a,'end_s':b,'percentage_point_change':round(y-x,3),'change_per_second':round((y-x)/(b-a),3)} for (a,x),(b,y) in zip(vals,vals[1:])]
    deltas.sort(key=lambda x:x['change_per_second'])
    initial=vals[0][1]; last=vals[-1][1]
    print(f'Samples: {len(vals)} | starts at {initial:.2f}% | ends at {last:.2f}% | interval median: {statistics.median([b-a for (a,_),(b,__) in zip(vals,vals[1:])]):.2f}s')
    print('Largest negative slopes (descriptive only; intervals may differ):')
    for x in deltas[:n]: print(f"{x['start_s']:.1f}–{x['end_s']:.1f}s: {x['percentage_point_change']:+.2f} pp ({x['change_per_second']:+.3f} pp/s)")
    print('Interpretation requires the corresponding scene/transcript, sample size and traffic-source context; no causes inferred.')

def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('csv');p.add_argument('--top',type=int,default=5)
    a=p.parse_args()
    try: analyze(a.csv,a.top);return 0
    except (OSError,ValueError,KeyError) as e: print(f'ERROR: {e}',file=sys.stderr);return 1
if __name__=='__main__': raise SystemExit(main())
