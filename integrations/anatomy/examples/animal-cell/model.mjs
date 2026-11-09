export const STAGE_SECONDS=3.2;
export const STAGE_COUNT=8;
export const lerp=(a,b,t)=>a+(b-a)*t;
export const smooth=t=>{t=Math.max(0,Math.min(1,t));return t*t*(3-2*t);};
export const blendPoint=(a,b,t)=>a.map((x,i)=>lerp(x,b[i],t));
export function bezier(a,b,c,d,t){const u=1-t;return a.map((x,i)=>u*u*u*x+3*u*u*t*b[i]+3*u*t*t*c[i]+t*t*t*d[i]);}
export function processPose(index,progress){
 const p=smooth(progress),rnaOrigin=[-54,-31,54],pore=[-9,-14,48],ribosome=[-72,17,34],er=[-69,25,31],cis=[46,-26,24],trans=[83,-7,35],dock=[120,73,6],outside=[150,108,12];
 const common={stage:index,progress:p,carrier:0,fold:0,fusion:0,rna:0,chain:0,cargo:0,point:er};
 if(index===0)return {...common,point:rnaOrigin,rna:p};
 if(index===1)return {...common,point:blendPoint(rnaOrigin,pore,p),rna:1};
 if(index===2)return {...common,point:blendPoint(pore,ribosome,smooth(Math.min(1,p/.35))),rna:1-p*.65,chain:smooth(Math.max(0,(p-.3)/.7))};
 if(index===3)return {...common,point:blendPoint(ribosome,er,smooth(Math.min(1,p/.35))),rna:.35*(1-smooth(Math.min(1,p/.3))),rnaPoint:ribosome,chain:1-p,fold:p,cargo:1,carrier:smooth(Math.max(0,(p-.42)/.58))};
 if(index===4)return {...common,point:bezier(er,[-47,52,30],[18,48,27],cis,p),carrier:1,cargo:1,fold:1};
 if(index===5)return {...common,point:blendPoint(cis,trans,p),cargo:1,fold:1,carrier:1-smooth(Math.min(1,p/.25))+smooth(Math.max(0,(p-.65)/.35))};
 if(index===6)return {...common,point:bezier(trans,[106,23,34],[120,55,17],dock,p),cargo:1,fold:1,carrier:1};
 return {...common,point:blendPoint(dock,outside,smooth(Math.max(0,(p-.4)/.6))),cargo:1,fold:1,carrier:1-smooth(Math.min(1,p/.6)),fusion:p};
}
export function timelinePose(seconds){const time=Math.max(0,Math.min(STAGE_COUNT*STAGE_SECONDS,seconds));const stage=Math.min(STAGE_COUNT-1,Math.floor(time/STAGE_SECONDS));return processPose(stage,stage===STAGE_COUNT-1&&time===STAGE_COUNT*STAGE_SECONDS?1:(time-stage*STAGE_SECONDS)/STAGE_SECONDS);}
