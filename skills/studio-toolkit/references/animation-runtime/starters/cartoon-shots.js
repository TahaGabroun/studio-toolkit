// Original Studio Toolkit visual calibration. No spoken/physical claim.
import * as THREE from 'three';
import {makeHuman} from './human.js';
import {cam,place} from './anim.js';
export const DURATION=4;
export const CAPTIONS=[];
export const FADES=[];
function shot({makeStage}) {
  const scene=makeStage({shadowSize:4});
  const person=makeHuman('vest'); scene.add(person.root); person.root.position.x=-.15;
  const ball=new THREE.Mesh(new THREE.SphereGeometry(.18,32,24),new THREE.MeshStandardMaterial({color:0xffb347,roughness:.4}));
  ball.castShadow=true; scene.add(ball);
  const camera=cam(38);
  return {scene,camera,update(t) {
    person.setPose({pelvis:[0,0,0],spine:[0,-.08,0],chest:[0,.1,0],neck:[0,.18,0],head:[0,.1,0],lSh:[.2,0,.2],rSh:[-.8,0,-.25],rEl:[-.5,0,0],lHip:[0,0,.05],rHip:[0,0,-.05]});
    person.setMouth(.12);
    ball.position.set(.5,.2+.45*Math.abs(Math.sin(Math.PI*t/2)),.2);
    place(camera,[.25+Math.sin(t*.5)*.08,1.25,4.6],[0,1,0]);
    return {bloom:.15,dof:{focus:4.6,aperture:0,maxblur:0}};
  }};
}
export const SHOTS=[{start:0,end:DURATION,build:shot}];
