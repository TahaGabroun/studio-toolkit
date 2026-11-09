import assert from 'node:assert/strict';
import {processPose, STAGE_COUNT} from './model.mjs';

// This checks a schematic presentation contract, not biological geometry.
export const visibleChannels = pose => ({
  rna: pose.rna,
  chain: pose.chain,
  cargo: pose.cargo * pose.fold,
  carrier: pose.carrier,
  neck: pose.stage === 3 ? pose.carrier * (1-pose.carrier) * 3.6 : 0,
  fusion: pose.stage === 7 ? Math.sin(pose.fusion*Math.PI) : 0,
});
export function validateProcess(poseAt = processPose) {
  for(let stage=0;stage<STAGE_COUNT;stage++) {
    for(let frame=0;frame<=120;frame++) {
      const pose=poseAt(stage,frame/120);
      assert(pose.point.every(Number.isFinite), 'finite cargo position');
      if(pose.rnaPoint)assert(pose.rnaPoint.every(Number.isFinite), 'finite RNA position');
      for(const value of Object.values(visibleChannels(pose))) {
        assert(Number.isFinite(value)&&value>=-1e-12&&value<=1+1e-12, 'opacity is bounded');
      }
      if(stage<2)assert.equal(visibleChannels(pose).cargo,0,'no protein in RNA-only stages');
    }
  }
  for(let stage=0;stage<STAGE_COUNT-1;stage++) {
    const a=poseAt(stage,1),b=poseAt(stage+1,0);
    assert(Math.hypot(...a.point.map((x,i)=>x-b.point[i]))<1e-8,'position at stage boundary');
    const ca=visibleChannels(a),cb=visibleChannels(b);
    for(const key of Object.keys(ca))assert(Math.abs(ca[key]-cb[key])<1e-8,`${key} opacity at stage boundary ${stage}`);
    if(ca.rna>1e-8) {
      const pa=a.rnaPoint||a.point,pb=b.rnaPoint||b.point;
      assert(Math.hypot(...pa.map((x,i)=>x-pb[i]))<1e-8,'RNA position at stage boundary');
    }
  }
  return true;
}
