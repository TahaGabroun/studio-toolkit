(() => {
 const root=document.getElementById('anatomy-cell');
 if(!root)return;
 const {structures,journey,projection:P,targets,width:W,height:H,why}=CELL_SCENE;
 const choice=root.querySelector('[data-choice]'),heading=root.querySelector('[data-heading]'),detail=root.querySelector('[data-detail]'),role=root.querySelector('[data-role]'),whyText=root.querySelector('[data-why]');
 const prev=root.querySelector('[data-prev]'),next=root.querySelector('[data-next]'),play=root.querySelector('[data-play]'),focus=root.querySelector('[data-focus]'),readout=root.querySelector('[data-readout]'),counter=root.querySelector('[data-counter]');
 const svg=root.querySelector('.iso-svg'),camera=root.querySelector('[data-camera]'),process=root.querySelector('[data-process]');
 const rna=root.querySelector('[data-rna]'),chain=root.querySelector('[data-chain]'),cargo=root.querySelector('[data-cargo]'),carrier=root.querySelector('[data-carrier]'),neck=root.querySelector('[data-neck]'),fusion=root.querySelector('[data-fusion]'),fusionMask=root.querySelector('[data-fusion-mask]');
 const still=matchMedia('(prefers-reduced-motion: reduce)');
 let mode='structures',index=0,seconds=0,playing=false,hasStarted=false,visible=true,last=0,frame=0,focused=false,view={x:0,y:0,s:1},targetView={...view};
 const list=()=>mode==='structures'?structures:journey;
 const coordinates=p=>iso(p,P);
 function chooseCamera(){
  const e=list()[index],id=mode==='structures'?e.id:e.org;
  if(!focused){targetView={x:0,y:0,s:1};return;}
  const p=coordinates(targets[id]),scale=id==='cytosol'?1.15:id==='ser'||id==='rer'?2.4:3.1;
  targetView={x:W/2-p[0]*scale,y:H/2-p[1]*scale,s:scale};
 }
 function drawCamera(dt=1){
  const t=still.matches?1:1-Math.exp(-dt/.2);
  for(const key of ['x','y','s'])view[key]+=(targetView[key]-view[key])*t;
  camera.setAttribute('transform','translate('+view.x.toFixed(2)+' '+view.y.toFixed(2)+') scale('+view.s.toFixed(4)+')');
 }
 function update(){
  const e=list()[index],id=mode==='structures'?e.id:e.org;
  root.querySelectorAll('[data-org]').forEach(el=>el.classList.toggle('is-active',el.dataset.org===id));
  heading.textContent=e.name;detail.textContent=e.detail;role.textContent=e.location;whyText.textContent=mode==='structures'?why[id]:why.journey[index];
  root.querySelector('[data-why-heading]').textContent=mode==='structures'?'How structure helps':'What changes';
  counter.textContent=(mode==='structures'?'Structure ':'Stage ')+(index+1)+' / '+list().length;
  choice.value=String(index);prev.disabled=index===0;next.disabled=index===list().length-1;
  play.hidden=mode!=='journey';play.disabled=still.matches;play.textContent=playing?'Pause sequence':'Play sequence';
  process.hidden=mode!=='journey';
  if(mode==='journey')process.removeAttribute('hidden');else process.setAttribute('hidden','');
  root.querySelector('[data-choice-label]').textContent=mode==='structures'?'Explore a structure':'Follow the sequence';
  focus.textContent=focused?'Whole cell':'Focus selected';focus.setAttribute('aria-pressed',String(focused));
  readout.textContent=mode==='structures'?'Selected · '+e.name:e.location;
  root.dataset.mode=mode;root.dataset.selected=id;root.dataset.stage=String(index);root.dataset.playing=String(playing);
  chooseCamera();
 }
 function drawProcess(){
  if(mode!=='journey')return;
  const pose=CELL_MODEL.timelinePose(seconds),p=coordinates(pose.point);
  const place='translate('+p[0].toFixed(2)+' '+p[1].toFixed(2)+')';
  for(const el of [rna,chain,cargo,carrier,neck])el.setAttribute('transform',place);
  // RNA stays at the translation site while emphasis transfers to the folded protein.
  if(pose.rnaPoint){const q=coordinates(pose.rnaPoint);rna.setAttribute('transform','translate('+q[0].toFixed(2)+' '+q[1].toFixed(2)+')');}
  const rn=pose.rna;
  rna.setAttribute('opacity',String(rn));rna.setAttribute('d','M-12 -8 Q-9 -15 -6 -8 T0 -8 T6 -8 T12 -8');
  chain.setAttribute('opacity',String(pose.chain));
  const points=Array.from({length:30},(_,i)=>{const t=i/29;return [-5+24*t*pose.chain,2+3*Math.sin(t*3*Math.PI*pose.chain)];});
  chain.setAttribute('d',pathOf(points));
  cargo.setAttribute('opacity',String(pose.cargo*pose.fold));
  cargo.setAttribute('d','M-4 -3 Q1 -7 5 -2 Q8 2 3 5 Q-2 7 -5 2 Q-7 -1 -4 -3 Z');
  const radius=9.3*Math.max(.001,pose.carrier);
  carrier.setAttribute('d','M'+radius+' 0 A'+radius+' '+radius+' 0 1 1 '+(-radius)+' 0 A'+radius+' '+radius+' 0 1 1 '+radius+' 0Z');
  carrier.setAttribute('opacity',String(pose.carrier));
  neck.setAttribute('opacity',pose.stage===3?String(pose.carrier*(1-pose.carrier)*3.6):'0');
  neck.setAttribute('d','M-13 10 Q-9 10 '+(-radius*.55)+' '+(radius*.835)+' M13 10 Q9 10 '+(radius*.55)+' '+(radius*.835));
  const fuse=pose.stage===7?pose.fusion:0,fp=coordinates([129,74,0]);
  const theta=Math.atan2(74/128,129/160),tangent=axisVector(P,[-160*Math.sin(theta),128*Math.cos(theta),0]),angle=Math.atan2(-tangent[1],-tangent[0])*180/Math.PI;
  fusion.setAttribute('transform','translate('+fp[0]+' '+fp[1]+') rotate('+angle+')');
  fusionMask.setAttribute('transform','translate('+fp[0]+' '+fp[1]+') rotate('+angle+')');
  fusion.setAttribute('opacity',String(Math.sin(fuse*Math.PI)));
  fusionMask.setAttribute('opacity',String(Math.sin(fuse*Math.PI)));
  fusion.setAttribute('d','M-15 0 Q-9 0 -9 -6 C-9 -20 9 -20 9 -6 Q9 0 15 0 M-15 2 Q-7 2 -7 -5 C-7 -17 7 -17 7 -5 Q7 2 15 2');
  fusionMask.setAttribute('d','M-15 -5H15V5H-15Z');
 }
 function tick(time){
  if(!visible||document.hidden){frame=0;last=0;return;}
  const elapsed=last?Math.max(0,(time-last)/1000):0;last=time;
  const dt=Math.min(.05,elapsed); // Clamp camera easing, not the process clock.
  if(playing&&!still.matches){
   seconds=Math.min(CELL_MODEL.STAGE_SECONDS*CELL_MODEL.STAGE_COUNT,seconds+elapsed);
   const stage=CELL_MODEL.timelinePose(seconds).stage;
   if(stage!==index){index=stage;update();}
   if(seconds>=CELL_MODEL.STAGE_SECONDS*CELL_MODEL.STAGE_COUNT){playing=false;update();}
  }
  drawProcess();drawCamera(dt||.02);
  const moving=Math.abs(view.x-targetView.x)+Math.abs(view.y-targetView.y)+Math.abs(view.s-targetView.s)>.025;
  if(playing||moving)frame=requestAnimationFrame(tick);else {frame=0;last=0;}
 }
 function render(){drawProcess();if(still.matches)drawCamera();if(!frame&&visible&&!document.hidden)frame=requestAnimationFrame(tick);}
 function select(n){index=n;playing=false;hasStarted=false;seconds=n*CELL_MODEL.STAGE_SECONDS+CELL_MODEL.STAGE_SECONDS*.75;update();render();}
 function switchMode(value){
  mode=value;index=0;playing=false;hasStarted=false;seconds=mode==='journey'?CELL_MODEL.STAGE_SECONDS*.75:0;
  root.querySelectorAll('[data-mode]').forEach(el=>el.setAttribute('aria-pressed',String(el.dataset.mode===mode)));
  choice.replaceChildren(...list().map((e,i)=>{const o=document.createElement('option');o.value=String(i);o.textContent=e.name;return o;}));
  update();render();
 }
 root.querySelectorAll('[data-mode]').forEach(el=>el.addEventListener('click',()=>switchMode(el.dataset.mode)));
 choice.addEventListener('change',()=>select(Number(choice.value)));
 prev.addEventListener('click',()=>{if(index>0)select(index-1);});next.addEventListener('click',()=>{if(index<list().length-1)select(index+1);});
 play.addEventListener('click',()=>{
  if(still.matches)return;
  if(!playing&&seconds>=CELL_MODEL.STAGE_SECONDS*CELL_MODEL.STAGE_COUNT){seconds=0;index=0;hasStarted=false;}
  if(!playing&&index===0&&!hasStarted)seconds=0;
  playing=!playing;if(playing)hasStarted=true;update();render();
 });
 focus.addEventListener('click',()=>{focused=!focused;update();render();});
 root.querySelector('[data-theme-toggle]').addEventListener('click',e=>{
  const dark=document.body.dataset.theme!=='dark';document.body.dataset.theme=dark?'dark':'light';e.currentTarget.textContent=dark?'Light theme':'Dark theme';
 });
 root.querySelectorAll('[data-org]').forEach(el=>el.addEventListener('click',event=>{event.stopPropagation();if(mode!=='structures')switchMode('structures');select(structures.findIndex(e=>e.id===el.dataset.org));}));
 new IntersectionObserver(entries=>{visible=entries[entries.length-1].isIntersecting;if(visible)render();else{cancelAnimationFrame(frame);frame=0;last=0;}}).observe(svg);
 document.addEventListener('visibilitychange',()=>{if(document.hidden){cancelAnimationFrame(frame);frame=0;last=0;}else render();});
 still.addEventListener('change',()=>{playing=false;update();render();});
 update();render();
})();
