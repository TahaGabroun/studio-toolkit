import * as k from '../../kit/iso-kit.mjs';
import * as G from '../../kit/lathe.mjs';
import * as T from '../../kit/tube.mjs';

// All lengths are illustration units. Organelle counts, sizes and positions
// are schematic. No kinetic or physical measurement is implied.
const W=880, H=650;
const P=k.fitProjection([[-160,-128,-106],[160,128,0],[-160,128,0],[160,-128,0],[-42,-26,83]],W,H,{pad:30,azimuth:48,elevation:33});
const at=p=>k.iso(p,P), path=(pts,close=false)=>k.pathOf(pts.map(at),close);
const S=(s,extra={})=>k.solidSvg(s,{tone:'mid',crease:'faint',...extra});
const L=(d,tone='lo')=>k.lineSvg(d,{tone});
const ball=(p,r,extra={})=>S(G.sphereOf(p,r,P,{steps:40}),{crease:'none',...extra});
const ell=(x,y,rx,ry,angle=0,n=88)=>Array.from({length:n},(_,i)=>{
 const t=i/n*Math.PI*2, u=rx*Math.cos(t),v=ry*Math.sin(t);
 return [x+u*Math.cos(angle)-v*Math.sin(angle),y+u*Math.sin(angle)+v*Math.cos(angle)];
});
const ringPath=(ring,z)=>k.onTop(ring,z,P,true);
const org=(id,markup)=>`<g class="org cursor-interaction" data-org="${id}" data-name="${structures.find(x=>x.id===id)?.name||id}">${markup}</g>`;
const structures=[
 {id:'membrane',name:'Plasma membrane',location:'Cell boundary',detail:'A phospholipid bilayer with embedded proteins forms a selective boundary. Channels, pumps and receptors regulate transport and communication.'},
 {id:'cytosol',name:'Cytosol',location:'Between the organelles',detail:'The aqueous interior contains ions, metabolites and proteins. Many reactions, including glycolysis, occur here; cytoplasm includes the cytosol and structures outside the nucleus.'},
 {id:'nucleus',name:'Nucleus',location:'Chromatin inside a double envelope',detail:'DNA and associated proteins form chromatin. A double nuclear envelope separates transcription and RNA processing from cytoplasmic translation; its outer membrane is continuous with the ER.'},
 {id:'nucleolus',name:'Nucleolus',location:'Dense region within the nucleus',detail:'This region has no enclosing membrane. Ribosomal RNA is produced and processed here, and ribosomal subunits are assembled before export to the cytoplasm.'},
 {id:'pores',name:'Nuclear pores',location:'Openings across the nuclear envelope',detail:'Protein complexes span both nuclear membranes. They selectively transport molecules, including processed messenger RNA outwards and many nuclear proteins inwards.'},
 {id:'ribosomes',name:'Ribosomes',location:'Free in the cytosol and on rough ER',detail:'Two subunits made of RNA and proteins translate messenger RNA into polypeptides. Free and ER-bound ribosomes are the same machinery in different locations.'},
 {id:'rer',name:'Rough endoplasmic reticulum',location:'Flattened sacs next to the nuclear envelope',detail:'Ribosomes on its cytosolic surface make many secreted and membrane proteins. New polypeptides enter the ER for folding and early processing; the internal space is its lumen.'},
 {id:'ser',name:'Smooth endoplasmic reticulum',location:'Tubular continuation of the ER',detail:'Interconnected membrane tubules lack attached ribosomes. They support lipid synthesis and calcium storage; detoxification roles depend on the cell type.'},
 {id:'golgi',name:'Golgi apparatus',location:'Stack of curved, flattened cisternae',detail:'Its cis side receives ER-derived cargo. Processing through the stack and sorting at the trans side direct proteins and lipids towards different destinations.'},
 {id:'vesicles',name:'Transport vesicles',location:'Small membrane-enclosed carriers',detail:'Vesicles bud from one membrane and fuse with another. Their membranes keep cargo separate from the cytosol during transport between compartments or to the cell surface.'},
 {id:'mitochondria',name:'Mitochondria',location:'Double membranes with inner folds',detail:'The inner membrane folds into cristae around the matrix. Electron transport and ATP synthase in this membrane support oxidative phosphorylation; mitochondria also contain their own DNA.'},
 {id:'lysosomes',name:'Lysosomes',location:'Membrane-enclosed digestive compartments',detail:'An acidic lumen contains hydrolytic enzymes. Lysosomes degrade material delivered through endocytosis or autophagy and return reusable products to the cell.'},
 {id:'peroxisomes',name:'Peroxisomes',location:'Membrane-enclosed oxidative compartments',detail:'These organelles carry out specialised lipid metabolism, including breakdown of very long-chain fatty acids. Oxidases generate hydrogen peroxide, and catalase helps remove it.'},
 {id:'cytoskeleton',name:'Cytoskeleton and centrosome',location:'Fibres throughout the cytoplasm',detail:'Actin, intermediate filaments and microtubules support shape, movement and transport. The centrosome, shown with two centrioles, organises many microtubules in a typical animal cell.'}
];
const items=[];
const add=(id,center,markup)=>items.push({id,center,markup,depth:k.depthOf(center,P)});
function hull(points) {
 const p=[...points].sort((a,b)=>a[0]-b[0]||a[1]-b[1]);
 const cross=(o,a,b)=>(a[0]-o[0])*(b[1]-o[1])-(a[1]-o[1])*(b[0]-o[0]);
 const lower=[],upper=[];
 for(const a of p){while(lower.length>1&&cross(lower.at(-2),lower.at(-1),a)<=0)lower.pop();lower.push(a);}
 for(const a of p.reverse()){while(upper.length>1&&cross(upper.at(-2),upper.at(-1),a)<=0)upper.pop();upper.push(a);}
 return lower.slice(0,-1).concat(upper.slice(0,-1));
}
function cellBowl() {
 const radius=z=>160*Math.sqrt(Math.max(0,1-(z/104)**2));
 const slope=z=>-160*z/(104*104*Math.sqrt(Math.max(.000001,1-(z/104)**2)));
 const profile=Array.from({length:54},(_,i)=>{const z=-103.98+i/53*103.98;return [z,radius(z),1];});
 const frame=G.frameOf([0,0,0],[0,0,1],[1,0,0],[0,.8,0]);
 return S(G.solidOf(profile,frame,P,{smooth:{radius,slope}}),{crease:'none'});
}
let back=org('membrane',cellBowl());
back+=org('cytosol',`<path class="cell-cytosol" d="${ringPath(ell(0,0,156,124),0)}"/>`);
const rearOuter=[],rearInner=[],rearBase=[];
for(let i=0;i<=96;i++){
 const t=P.azimuth*Math.PI/180+Math.PI/2+i/96*Math.PI;
 const wave=39+5*Math.sin(i/96*Math.PI),factor=Math.sqrt(1-(wave/104)**2);
 rearOuter.push([160*factor*Math.cos(t),128*factor*Math.sin(t),wave]);
 rearInner.push([156*factor*Math.cos(t),124*factor*Math.sin(t),wave]);
 rearBase.push([160*Math.cos(t),128*Math.sin(t),0]);
}
back+=org('membrane',`<path class="iso-fill" d="${path([...rearBase,...rearOuter.slice().reverse()],true)}"/><path class="iso-shade" data-shade="3" d="${path([...rearBase,...rearInner.slice().reverse()],true)}"/>${L(path(rearOuter),'mid')}${L(path(rearInner),'faint')}`);
// A cortical actin mesh follows the edge of the illustrated cut plane.
let fibres='';
for(let j=0;j<3;j++)fibres+=L(ringPath(ell(0,0,143-j*3,112-j*2),2+j*.6),'faint');
const centrosome=[30,35,12];
for(let i=0;i<18;i++){
 const t=i/18*Math.PI*2, end=[143*Math.cos(t),110*Math.sin(t),3];
 const pts=Array.from({length:26},(_,n)=>{const u=n/25;return [centrosome[0]*(1-u)+end[0]*u+4*Math.sin(u*Math.PI)*Math.cos(t+1),centrosome[1]*(1-u)+end[1]*u,centrosome[2]*(1-u)+end[2]*u];});
 fibres+=L(path(pts),'faint')+k.dotsSvg([at(pts[0]),at(pts.at(-1))],{size:.6,tone:'faint'});
}
for(let i=0;i<9;i++){
 const a=.18+i*.26, b=a+2.1;
 const start=[137*Math.cos(a),107*Math.sin(a),3],end=[137*Math.cos(b),107*Math.sin(b),3];
 const points=Array.from({length:60},(_,j)=>{const t=j/59;return [start[0]*(1-t)+end[0]*t+8*Math.sin(t*Math.PI*2+i),start[1]*(1-t)+end[1]*t+6*Math.sin(t*Math.PI*3),4+3*Math.sin(t*Math.PI)];});
 fibres+=L(path(points),'faint')+k.dotsSvg([at(points[0]),at(points.at(-1))],{size:.5,tone:'faint'});
}
back+=org('cytoskeleton',fibres);

// A nucleus exposed by a horizontal illustrative cut, with two envelope rims.
const nc=[-42,-26,36], nr=37,cut=16,cutr=Math.sqrt(nr*nr-cut*cut),nf=G.frameAlong(nc,[0,0,1]);
const profile=Array.from({length:35},(_,i)=>{const s=-nr+.08+i/(34)*(nr+cut-.08);return [s,Math.sqrt(Math.max(0,nr*nr-s*s)),1];});
let nucleus=S(G.solidOf(profile,nf,P,{smooth:{slope:s=>-s/Math.sqrt(Math.max(.001,nr*nr-s*s))}}),{crease:'none'});
nucleus+=`<path class="cell-inner" d="${k.ring(nc[0],nc[1],cutr-2,52,P,88)}"/>`;
nucleus+=L(k.ring(nc[0],nc[1],cutr,52,P,88),'mid')+L(k.ring(nc[0],nc[1],cutr-2,52,P,88),'mid');
for(let j=0;j<3;j++){
 const pts=Array.from({length:180},(_,i)=>{
  const t=i/179*Math.PI*2,rx=15+j*4,ry=10+j*4;
  return [nc[0]+rx*Math.cos(t)+3.3*Math.sin(5*t+j),nc[1]+ry*Math.sin(t)+2.5*Math.cos(4*t+j),52.1];
 });
 nucleus+=L(path(pts,true),'lo');
}
add('nucleus',nc,nucleus);
add('nucleolus',[-44,-19,59],ball([-44,-19,59],8)+L(k.ring(-44,-19,4,63,P,32),'faint'));
// Pores on the exposed envelope surface; circles lie in the tangent plane.
for(let i=0;i<9;i++){
 const t=-.3+i/8*Math.PI, polar=.33,normal=[Math.cos(t)*Math.cos(polar),Math.sin(t)*Math.cos(polar),Math.sin(polar)];
 const pos=G.add3(nc,G.mul3(normal,nr+.15)),f=G.frameAlong(pos,normal);
 const pore=S(G.ringBand(0,.7,1.6,2.7,f,P),{crease:'none'});
 add('pores',pos,pore);
}
function crescent(cx,cy,r0,r1,start,end) {
 const n=42,pts=[];
 for(let i=0;i<=n;i++){const t=start+(end-start)*i/n;pts.push([cx+r1*Math.cos(t),cy+r1*Math.sin(t)]);}
 for(let i=n;i>=0;i--){const t=start+(end-start)*i/n;pts.push([cx+r0*Math.cos(t),cy+r0*Math.sin(t)]);}
 return pts;
}
// Four connected rough ER cisternae surround one side of the nuclear envelope.
for(let i=0;i<4;i++){
 const z=9+i*7, r0=38+i*3,r1=r0+12;
 const footprint=crescent(-42,-26,r0,r1,.8,3.84);
 let markup=S(k.extrude(footprint,z,3.8,P,{convex:false,bevel:.5}));
 markup+=L(ringPath(crescent(-42,-26,r0+2,r1-2,.86,3.78),z+3.8),'faint');
 // Short ER connections drawn on the same assembly; intentionally continuous.
 if(i<3){const x=-42+(r0+7)*Math.cos(1.8),y=-26+(r0+7)*Math.sin(1.8);markup+=S(k.cylinder(x,y,2,z+3.8,3.2,P,18));}
 add('rer',[-65,7,z],markup);
 for(let j=0;j<18;j++){
  const t=.9+j/17*2.8,r=r0+3+(j%2)*5,pos=[-42+r*Math.cos(t),-26+r*Math.sin(t),z+5.1];
  add('ribosomes',pos,ball(pos,1.45));
 }
}
// A connecting cisterna makes the outer envelope / ER continuity explicit.
add('rer',[-64,-5,25],S(k.slabOf({x:-73,y:-10,w:15,d:13,r:4},22,4,P,6)));

function tube(points,r=.95) {
 return T.tubePieces(points,r,P,{maxLength:500,spacing:1.2}).map(piece=>T.tubeSvg(piece,{tone:'lo'})).join('');
}
// Smooth ER is a connected, ribosome-free tubule network, not isolated loops.
for(let j=0;j<5;j++){
 const points=Array.from({length:15},(_,i)=>{const u=i/14;return [-30+u*76,-87+j*8+4*Math.sin(u*Math.PI*2+j*.45),7+4*Math.sin(u*Math.PI)+j*1.2];});
 add('ser',[8,-69+j*4,12],tube(points,1.5));
 if(j<4){const a=points[4],b=[a[0],a[1]+8,a[2]+1.2];add('ser',a,tube([a,b],1.5));}
}
const erConnection=Array.from({length:24},(_,i)=>{const t=i/23;return [-42+12*t,-62-25*t,24-17*t+4*Math.sin(t*Math.PI)];});
add('ser',[-36,-76,15],tube(erConnection,1.5));

function local(cx,cy,u,v,a){return [cx+u*Math.cos(a)-v*Math.sin(a),cy+u*Math.sin(a)+v*Math.cos(a)];}
function banana(cx,cy,len,width,angle,curve=9){
 const pts=[];for(let i=0;i<=40;i++){const t=i/40*Math.PI;const u=len*Math.cos(t);const v=width*Math.sin(t)+curve*(u*u/len/len-.5);pts.push(local(cx,cy,u,v,angle));}
 for(let i=40;i>=0;i--){const t=i/40*Math.PI;const u=len*Math.cos(t);const v=-width*Math.sin(t)+curve*(u*u/len/len-.5);pts.push(local(cx,cy,u,v,angle));}
 return pts;
}
for(let i=0;i<6;i++){
 const x=59+i*1.25,y=-18+i*1.7,z=9+i*5.7,ring=banana(x,y,27-i*1.35,7,-.25,10);
 let markup=S(k.extrude(ring,z,2.8,P,{convex:false,bevel:.65}));
 markup+=L(ringPath(banana(x,y,24-i*1.35,4,-.25,10),z+2.8),'faint');
 add('golgi',[x,y,z],markup);
}
const vesicleCenters=[[83,1,20],[47,-46,12],[94,26,8],[107,44,6],[89,63,7],[49,-43,25]];
vesicleCenters.forEach((pos,i)=>add('vesicles',pos,ball(pos,3.7+i%2)+L(k.ring(pos[0],pos[1],2.2,pos[2]+2.5,P,24),'faint')));

function mitochondrion(cx,cy,a,z,len=32,width=13) {
 const ring=banana(cx,cy,len,width,a,3);
 let markup=S(k.extrude(ring,z,7.6,P,{convex:false,bevel:.8}));
 markup+=`<path class="cell-inner" d="${ringPath(banana(cx,cy,len-2.4,width-2.4,a,3),z+7.6)}"/>`;
 markup+=L(ringPath(banana(cx,cy,len-2.4,width-2.4,a,3),z+7.6),'mid');
 // Cristae are inner-membrane folds continuous with the inner boundary.
 for(let i=0;i<8;i++){
  const u=-len+7+i*(len*2-14)/7,thick=(width-2.4)*Math.sqrt(1-u*u/((len-2.4)**2));
  const offset=3*(u*u/(len*len)-.5),side=i%2?1:-1;
  const fold=[local(cx,cy,u,offset+side*thick,a),local(cx,cy,u+1,offset-side*thick*.55,a),local(cx,cy,u+3,offset-side*thick*.6,a),local(cx,cy,u+4,offset+side*thick*.96,a)];
  markup+=L(k.onTop(fold,z+7.7,P),'lo');
 }
 const dna=Array.from({length:40},(_,i)=>{const t=i/40*Math.PI*2;return [...local(cx,cy,9+2.4*Math.cos(t),1.2*Math.sin(t),a),z+7.8];});
 markup+=L(path(dna,true),'faint');
 return markup;
}
add('mitochondria',[-29,76,15],mitochondrion(-29,76,-.3,8,34,14));
add('mitochondria',[101,-49,15],mitochondrion(101,-49,1.15,7,25,12));
add('mitochondria',[-111,-2,10],mitochondrion(-111,-2,.88,3,25,11));

function compartment(cx,cy,z,r,type) {
 const f=G.frameAlong([cx,cy,z],[0,0,1]),top=r*.35;
 const pro=Array.from({length:25},(_,i)=>{const s=-r+.1+i/24*(r+top-.1);return [s,Math.sqrt(Math.max(0,r*r-s*s)),1];});
 let s=S(G.solidOf(pro,f,P,{smooth:{slope:x=>-x/Math.sqrt(Math.max(.001,r*r-x*x))}}),{crease:'none'});
 const cutRadius=Math.sqrt(r*r-top*top);
 s+=`<path class="cell-inner" d="${k.ring(cx,cy,cutRadius-1,z+top,P,40)}"/>`+L(k.ring(cx,cy,cutRadius,z+top,P,40),'lo');
 for(let i=0;i<11;i++){
  const t=i*2.4,d=Math.sqrt((i+.5)/11)*(r-3),p=[cx+d*Math.cos(t),cy+d*Math.sin(t),z+top+.3];
  s+=ball(p,type==='lysosomes'?.95:.55);
 }
 if(type==='lysosomes'){s+=L(k.onTop([[cx-3,cy-1],[cx,cy+3],[cx+2,cy],[cx-3,cy-1]],z+top+.3,P,true),'mid');}
 return s;
}
add('lysosomes',[-64,59,13],compartment(-64,59,13,10,'lysosomes'));
add('lysosomes',[10,95,11],compartment(10,95,11,8,'lysosomes'));
add('peroxisomes',[38,-61,10],compartment(38,-61,10,7,'peroxisomes'));
add('peroxisomes',[57,72,11],compartment(57,72,11,7.6,'peroxisomes'));

// A centrosome with perpendicular centrioles, each with nine triplet bundles.
for(const [center,axis] of [[[29,36,15],[0,0,1]],[[35,43,10],[1,0,0]]]){
 const F=G.frameAlong(center,axis),r=4.5;
 let s='';
 for(let i=0;i<9;i++)for(let j=0;j<3;j++){
  const t=i/9*Math.PI*2+.1*j,origin=G.pointOf(F,0,r+j*.25,t),ff=G.frameAlong(origin,axis);
  s+=S(G.disc(-5,5,.42,ff,P,{steps:10}),{crease:'none'});
 }
 add('cytoskeleton',center,s);
}
for(let i=0;i<25;i++){
 const t=i*2.4,r=47+Math.sqrt(i/25)*40,x=24+r*Math.cos(t),y=23+r*.85*Math.sin(t);
 if((x/144)**2+(y/111)**2>.95)continue;
 if(Math.hypot(x+42,y+26)<42)continue;
 const pos=[x,y,4+i%3];add('ribosomes',pos,ball(pos,1.4));
}

// Soft illustration lighting gives the suspended organelles depth without
// turning the cytosol into a dark floor. These are visual cues, not a claim
// that organelles sit on a rigid surface or have measured contact positions.
const shadow=(x,y,rx,ry,a=0)=>`<path class="iso-halo" style="filter:blur(4px);opacity:.16;transform:none" d="${ringPath(ell(x,y,rx,ry,a),1)}"/>`;
const ambient=[
 shadow(-42,-26,34,31),shadow(61,-14,26,10,-.25),
 shadow(-29,76,31,12,-.3),shadow(101,-49,23,10,1.15),shadow(-111,-2,23,9,.88),
 shadow(-64,59,9,8),shadow(10,95,7,6),shadow(57,72,6,5),shadow(38,-61,6,5)
].join('');
let art=back+ambient+items.sort((a,b)=>a.depth-b.depth).map(i=>org(i.id,i.markup)).join('');
// The exposed plasma membrane rim, with two leaflets and embedded proteins.
let rim='';
const az=P.azimuth*Math.PI/180;
const front=[];
for(let i=0;i<=100;i++){const t=az-Math.PI/2+i/100*Math.PI;front.push([160*Math.cos(t),128*Math.sin(t),0]);}
rim+=L(path(front),'mid');
rim+=L(path(front.map(([x,y,z])=>[x*.974,y*.967,z])),'lo');
for(let i=0;i<85;i++){
 const t=az-Math.PI/2+i/84*Math.PI;
 const outer=[159*Math.cos(t),127*Math.sin(t),.3],inner=[156*Math.cos(t),124*Math.sin(t),.3];
 rim+=k.dotsSvg([at(outer),at(inner)],{size:.52,tone:'lo'});
}
for(let i=0;i<9;i++){
 const t=az-Math.PI/2+(i+.45)/9*Math.PI,p=[158*Math.cos(t),126*Math.sin(t),1.2];
 rim+=ball(p,2.2)+ball([p[0],p[1],p[2]+2.8],1.5);
}
art+=org('membrane',rim);
const targets={membrane:[126,74,1],cytosol:[9,28,1],nucleus:[-42,-26,53],nucleolus:[-44,-19,62],pores:[-12,-15,55],ribosomes:[-75,15,31],rer:[-77,14,29],ser:[3,-72,13],golgi:[63,-13,39],vesicles:[93,26,15],mitochondria:[-29,76,23],lysosomes:[-64,59,19],peroxisomes:[57,72,17],cytoskeleton:[30,37,20]};
const journey=[
 {name:'Transcription',org:'nucleus',location:'DNA → messenger RNA',detail:'A gene is transcribed in the nucleus. The resulting RNA is processed into messenger RNA (mRNA); the DNA stays in the nucleus.',point:[-55,-36,54],kind:'rna'},
 {name:'Export through a nuclear pore',org:'pores',location:'Processed mRNA leaves the nucleus',detail:'Processed mRNA passes through a nuclear pore into the cytosol. The transcript carries the coding sequence to a ribosome.',point:[-11,-16,51],kind:'rna'},
 {name:'Translation and ER entry',org:'ribosomes',location:'Ribosome on the rough ER',detail:'Translation begins in the cytosol. An ER-targeting signal in the growing polypeptide directs this ribosome to the rough ER, where translation feeds the chain into the lumen.',point:[-75,12,35],kind:'chain'},
 {name:'Folding and early processing',org:'rer',location:'Protein within the ER lumen',detail:'The polypeptide folds and undergoes quality control and early processing in the ER. Correctly folded cargo can proceed towards the Golgi.',point:[-78,19,26],kind:'protein'},
 {name:'ER-to-Golgi transport',org:'vesicles',location:'Protein enclosed in a transport carrier',detail:'ER-derived carriers deliver the protein towards the cis Golgi. The protein remains separated from the cytosol by a membrane.',point:[30,-38,20],kind:'vesicle'},
 {name:'Golgi processing and sorting',org:'golgi',location:'Cis side → trans side',detail:'Cargo is processed through the Golgi and sorted at the trans side. This example follows a soluble protein destined for secretion.',point:[65,-12,38],kind:'protein'},
 {name:'Delivery to the cell surface',org:'vesicles',location:'Secretory carrier at the plasma membrane',detail:'A secretory carrier transports the protein to the cell surface, where its membrane docks and fuses with the plasma membrane.',point:[119,69,4],kind:'vesicle'},
 {name:'Exocytosis',org:'membrane',location:'Protein released outside the cell',detail:'Membrane fusion opens the carrier lumen to the extracellular space and releases the soluble protein. The carrier membrane joins the plasma membrane.',point:[137,80,7],kind:'protein'}
];

export { W,H,P,at,art,structures,journey,targets,items };
