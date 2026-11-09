import test from 'node:test';
import assert from 'node:assert/strict';
import {processPose,timelinePose,STAGE_COUNT,STAGE_SECONDS} from './model.mjs';
import {validateProcess} from './validate.mjs';

test('all schematic stages preserve rendered channel continuity',()=>assert(validateProcess()));
test('the former abrupt RNA disappearance is detected',()=>{
  assert.throws(()=>validateProcess((stage,p)=>{
    const pose=processPose(stage,p);
    return stage===3?{...pose,rna:0}:pose;
  }),/rna opacity at stage boundary/);
});
test('fading RNA stays at translation site while cargo moves',()=>{
  const start=processPose(2,1).point;
  const middle=processPose(3,.1);
  assert.deepEqual(middle.rnaPoint,start);
  assert(middle.rna>0&&middle.rna<.35);
  assert.notDeepEqual(middle.point,start);
});
test('timeline seeks are deterministic and bounded',()=>{
  const end=STAGE_COUNT*STAGE_SECONDS;
  for(const seconds of [0,.1,3.2,7.8,12,19,end]) {
    const expected=timelinePose(seconds);
    timelinePose(end);timelinePose(0);
    assert.deepEqual(timelinePose(seconds),expected);
  }
  assert.deepEqual(timelinePose(-100),timelinePose(0));
  assert.deepEqual(timelinePose(end+100),timelinePose(end));
});
