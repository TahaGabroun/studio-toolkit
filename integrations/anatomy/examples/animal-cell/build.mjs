import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import * as k from '../../kit/iso-kit.mjs';
import { kitScript } from '../../scripts/inline-kit.mjs';
import {W,H,P,art,structures,journey,targets,items} from './parts.mjs';
import {processPose,STAGE_COUNT,STAGE_SECONDS} from './model.mjs';
import {validateProcess} from './validate.mjs';

const here=path.dirname(fileURLToPath(import.meta.url)),theme=process.argv.includes('--light')?'light':'dark';
const why={
 membrane:'The bilayer makes a boundary; its proteins make that boundary selectively permeable and responsive.',
 cytosol:'An aqueous phase lets molecules meet and react, while internal membranes maintain separate conditions elsewhere.',
 nucleus:'Keeping DNA in a separate compartment allows RNA to be processed before it meets the translation machinery.',
 nucleolus:'Concentrating ribosome assembly in one nuclear region brings RNA processing and assembly factors together.',
 pores:'Large molecules cross through regulated protein complexes rather than through an open tear in the envelope.',
 ribosomes:'The two subunits align an RNA message with the machinery that builds an amino-acid chain.',
 rer:'A membrane interface couples synthesis to delivery into a lumen; the new protein can fold in a different environment from the cytosol.',
 ser:'A connected tubular membrane network provides surface and space for specialised lipid and calcium-handling functions.',
 golgi:'Its receiving and shipping faces support ordered processing and sorting rather than indiscriminate mixing of cargo.',
 vesicles:'A closed carrier can move cargo without exposing it to the cytosol, then deliver it by membrane fusion.',
 mitochondria:'Folding the inner membrane provides surface for electron transport and ATP-synthesising machinery.',
 lysosomes:'A surrounding membrane maintains an acidic digestive compartment and allows its products to be recycled.',
 peroxisomes:'Compartmentalisation brings oxidative enzymes and peroxide-handling enzymes into the same organelle.',
 cytoskeleton:'Fibres provide both mechanical support and tracks; the centrosome organises many microtubules.',
 journey:[
 'Watch the RNA strand appear beside chromatin. The illustration does not turn DNA into a travelling protein.',
 'The RNA strand crosses the nuclear envelope at a pore; no cargo vesicle leaves the nucleus.',
 'The message arrives at a ribosome. A new chain grows on the other side of the ER membrane.',
 'The chain becomes compact cargo. The RNA stays at the translation site and fades from emphasis; the fade does not represent its destruction. Carrier formation is schematic.',
 'A membrane now surrounds the cargo as it travels between the ER and the receiving face of the Golgi.',
 'Delivery removes the incoming carrier. Processing and sorting precede formation of an outgoing carrier.',
 'The closed carrier approaches the cell surface with its soluble cargo still enclosed.',
 'An opening in the membrane boundary appears during fusion. Soluble cargo continues into extracellular space.'
 ]
};
const scene={structures,journey,projection:P,targets,width:W,height:H,why};
const body=`<div id="anatomy-cell">
 <style>${fs.readFileSync(path.join(here,'cell.css'),'utf8')}</style>
 <header class="cell-heading"><div><span class="cell-kicker">Anatomy · specimen 02</span><h1>Inside an animal cell</h1><p>Explore the structures, then watch how they work together to produce and secrete a protein.</p></div><button type="button" class="cell-btn" data-theme-toggle>${theme==='light'?'Dark theme':'Light theme'}</button></header>
 <section class="cell-shell" aria-label="Interactive animal cell">
  <div class="cell-toolbar"><div class="cell-toolbar-group"><button type="button" class="cell-btn" data-mode="structures" aria-pressed="true">Cell structures</button><button type="button" class="cell-btn" data-mode="journey" aria-pressed="false">Protein production</button></div><div class="cell-toolbar-group"><button type="button" class="cell-btn" data-focus aria-pressed="false">Focus selected</button><button type="button" class="cell-btn cell-btn-primary" data-play hidden>Play sequence</button></div></div>
  <div class="cell-main">
   <div class="cell-stage">${k.figureSvg({width:W,height:H,label:'A schematic curved animal-cell cutaway with nuclear and organelle interiors exposed. Use the structure selector, focus view, and process controls. Sizes, positions, and motion are teaching simplifications.',body:`<g data-camera="">${art}<g data-process="" hidden="" aria-hidden="true"><path data-fusion-mask="" class="cell-fusion-mask"/><path data-fusion="" class="cell-thread"/><path data-carrier="" class="cell-carrier"/><path data-neck="" class="cell-thread"/><path data-rna="" class="cell-thread"/><path data-chain="" class="cell-thread"/><path data-cargo="" class="cell-ink"/></g></g>`})}<div class="cell-figure-note"><span>Top and front cut away · not to scale</span><span data-readout>Selected · Plasma membrane</span></div></div>
   <aside class="cell-sidebar"><div><label data-choice-label for="cell-choice">Explore a structure</label><select id="cell-choice" class="cell-select" data-choice>${structures.map((e,i)=>`<option value="${i}">${e.name}</option>`).join('')}</select></div><div class="cell-info" aria-live="polite" aria-atomic="true"><span class="cell-role" data-role>Cell boundary</span><h2 data-heading>Plasma membrane</h2><p data-detail>${structures[0].detail}</p><div class="cell-why"><strong data-why-heading>How structure helps</strong><p data-why>${why.membrane}</p></div></div><p class="cell-hint">Select a part in the drawing or use the menu. Focus selected opens a closer view.</p><div class="cell-nav"><button type="button" class="cell-btn" data-prev disabled>Previous</button><button type="button" class="cell-btn" data-next>Next</button></div><span class="cell-role" data-counter>Structure 1 / 14</span></aside>
  </div>
 </section>
 <p class="cell-caption">A typical nucleated animal cell, shown schematically. The cutaway exposes selected lumens; organelle sizes, counts, positions and transport timing are illustrative. The protein sequence simplifies intermediate compartments and recycling traffic. The RNA message and the newly made protein are different molecules.</p>
 <footer class="cell-footer"><span>Drawn with Ryan’s Anatomy kit · MIT</span><span><a href="https://medlineplus.gov/genetics/understanding/basics/cell/">Cell structures · NLM</a> / <a href="https://www.ncbi.nlm.nih.gov/books/NBK26841/">ER targeting · Molecular Biology of the Cell</a></span></footer>
</div>`;
const model=fs.readFileSync(path.join(here,'model.mjs'),'utf8').replace(/^export /gm,'');
const script=kitScript()+`\nconst CELL_SCENE=${JSON.stringify(scene)};\nconst CELL_MODEL=(()=>{${model}\nreturn {processPose,timelinePose,STAGE_SECONDS,STAGE_COUNT};})();\n`+fs.readFileSync(path.join(here,'live.js'),'utf8');
let html=k.pageHtml({title:'Inside an Animal Cell — Anatomy',theme,body,script,width:1180});
html=html.replace('<!doctype html>',`<!doctype html>\n<!--\n${fs.readFileSync(path.join(here,'../../LICENSE'),'utf8')}\n-->`);
const file=path.join(here,'animal-cell'+(theme==='light'?'-light':'')+'.html');fs.writeFileSync(file,html);
if(process.argv.includes('--check')){
 validateProcess();
 for(const part of items){if(!part.center.every(Number.isFinite))throw new Error('Invalid compartment position');}
 console.log('Animal-cell model checks passed: finite poses, RNA/protein distinction, stage positions and rendered opacity continuity. Does not validate compartment containment or membrane topology. Biological schematic; engineering support audit not claimed.');
}
console.log(file);
