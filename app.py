function feedback(id,message) {text(id,message);}
$('baroForm').addEventListener('submit',e=>{
 e.preventDefault(); if(!s.baroStable||s.baroRecorded!==null)return;
 const a=readNumber('baroInput','baroFeedback');if(a===null)return;
 if(Math.abs(a-s.baroPressure)>.001)return feedback('baroFeedback','That does not match the display. Read all digits, including the decimal.');
 s.baroRecorded=a; log('Barometer reading recorded');notice('');render();$('atmInput').focus({preventScroll:true});
});
$('atmForm').addEventListener('submit',e=>{
 e.preventDefault();if(s.baroRecorded===null||s.atmRecorded!==null)return;
 const a=readNumber('atmInput','atmFeedback');if(a===null)return;
 const correct=round2(s.baroRecorded*MMHG_TO_KPA);
 if(Math.abs(a-correct)>.011)return feedback('atmFeedback','Multiply the recorded mmHg value by 0.1333224, then round to two decimals.');
 s.atmRecorded=round2(a);log('Atmospheric pressure calculation accepted');notice('');render();
});
$('gaugeForm').addEventListener('submit',e=>{
 e.preventDefault();if(!gaugeStable()||s.gaugeRecorded!==null)return;
 const a=readNumber('gaugeInput','gaugeFeedback');if(a===null)return;
 if(Math.abs(a-s.vesselPressure)>.001)return feedback('gaugeFeedback','Copy the stable gauge reading exactly, including its decimal.');
 s.gaugeRecorded=a;log('Stable gauge pressure recorded with valve open');notice('');render();$('absInput').focus({preventScroll:true});
});
$('absForm').addEventListener('submit',e=>{
 e.preventDefault();if(s.gaugeRecorded===null||s.absRecorded!==null)return;
 const a=readNumber('absInput','absFeedback');if(a===null)return;
 const correct=round2(s.gaugeRecorded+s.atmRecorded);
 if(Math.abs(a-correct)>.011)return feedback('absFeedback','Add your recorded gauge pressure and atmospheric pressure. Both must be in kPa.');
 s.absRecorded=round2(a);s.completed=new Date().toISOString();log('Absolute pressure calculation accepted');notice('');render();
});
const actions={placeBaro:placeBarometer,powerBaro:powerBarometer,mountGauge,powerGauge,zeroGauge,connectHose,toggleValve,ventLine,disconnectHose};
for(const [id,action] of Object.entries(actions)) $(id).addEventListener('click',action);
function bindSvgButton(id,action) {
 $(id).addEventListener('pointerdown',e=>e.stopPropagation());
 $(id).addEventListener('click',e=>{e.stopPropagation();action();});
 $(id).addEventListener('keydown',e=>{if(e.key==='Enter'||e.key===' '){e.preventDefault();e.stopPropagation();action();}});
}
bindSvgButton('baroPower',powerBarometer);bindSvgButton('gaugePower',powerGauge);bindSvgButton('gaugeZero',zeroGauge);bindSvgButton('valve',toggleValve);
function point(e) {const p=$('scene').createSVGPoint();p.x=e.clientX;p.y=e.clientY;return p.matrixTransform($('scene').getScreenCTM().inverse());}
function inRect(p,x,y,w,h) {return p.x>=x&&p.x<=x+w&&p.y>=y&&p.y<=y+h;}
function validDrop(id,p) {
 if(id==='barometer')return inRect(p,277,170,235,313);
 if(id==='gauge')return inRect(p,710,105,203,243);
 return Math.hypot(p.x-PORT.x,p.y-PORT.y)<52;
}
function home(id) {if(id==='barometer')return s.baroPlaced?DOCKS.barometer:HOMES.barometer;if(id==='gauge')return s.gaugePlaced?DOCKS.gauge:HOMES.gauge;return s.connected?PORT:LOOSE;}
function target(id) {return id==='barometer'?'airTarget':id==='gauge'?'gaugeTarget':'portTarget';}
function cancelDrag() {
 if(!activeDrag)return;
 const {id,pointerId}=activeDrag;
 if($(id).hasPointerCapture(pointerId))$(id).releasePointerCapture(pointerId);
 $(id).classList.remove('dragging');$(target(id)).classList.remove('over');
 setPosition(id,home(id));activeDrag=null;render();
}
function setupDrag(id,action) {
 const el=$(id);
 el.addEventListener('keydown',e=>{
  if(e.target!==el)return;
  if(e.key==='Enter'||e.key===' '){e.preventDefault();action();}
 });
 el.addEventListener('pointerdown',e=>{
  if(e.button!==0||activeDrag)return;
  if((id==='barometer'&&s.baroPlaced)||(id==='gauge'&&s.gaugePlaced)||(id==='coupling'&&s.connected))return;
  e.preventDefault();
  activeDrag={id,pointerId:e.pointerId,start:point(e),origin:home(id),moved:false};
  el.setPointerCapture(e.pointerId);el.classList.add('dragging');notice('');
 });
 el.addEventListener('pointermove',e=>{
  if(!activeDrag||activeDrag.id!==id||activeDrag.pointerId!==e.pointerId)return;
  const p=point(e),d=activeDrag,dx=p.x-d.start.x,dy=p.y-d.start.y;
  if(Math.hypot(dx,dy)>6)d.moved=true;
  const pos={x:d.origin.x+dx,y:d.origin.y+dy,k:d.origin.k};setPosition(id,pos);
  if(id==='coupling')hosePath(pos);
  $(target(id)).classList.toggle('over',validDrop(id,p));
 });
 el.addEventListener('pointerup',e=>{
  if(!activeDrag||activeDrag.id!==id||activeDrag.pointerId!==e.pointerId)return;
  const d=activeDrag,p=point(e);activeDrag=null;
  el.releasePointerCapture(e.pointerId);el.classList.remove('dragging');$(target(id)).classList.remove('over');
  setPosition(id,home(id));
  if(!d.moved||validDrop(id,p))action();
  else notice(id==='barometer'?'Place the barometer inside station A.':id==='gauge'?'Place the gauge in the stand above the vessel.':'Bring the coupling to the brass test port on the right side of the valve.');
  render();
 });
 el.addEventListener('pointercancel',()=>{if(activeDrag?.id===id)cancelDrag();});
 el.addEventListener('lostpointercapture',()=>{if(activeDrag?.id===id)cancelDrag();});
}
setupDrag('barometer',placeBarometer);setupDrag('gauge',mountGauge);setupDrag('coupling',connectHose);
// SVG groups do not consistently enforce touch-action in mobile browsers.
// Reserve pointer gestures at the SVG root; pan empty bench space explicitly.
let benchPan=null;
$('scene').addEventListener('pointerdown',e=>{
 if(e.pointerType==='mouse'||e.target.closest('.draggable,[role="button"]'))return;
 const scroll=document.querySelector('.scene-scroll');
 benchPan={id:e.pointerId,x:e.clientX,y:e.clientY,left:scroll.scrollLeft,top:window.scrollY};
 $('scene').setPointerCapture(e.pointerId);
});
$('scene').addEventListener('pointermove',e=>{
 if(!benchPan||benchPan.id!==e.pointerId)return;
 document.querySelector('.scene-scroll').scrollLeft=benchPan.left+benchPan.x-e.clientX;
 window.scrollTo(window.scrollX,benchPan.top+benchPan.y-e.clientY);
});
for(const eventName of ['pointerup','pointercancel','lostpointercapture'])$('scene').addEventListener(eventName,e=>{
 if(benchPan?.id===e.pointerId)benchPan=null;
});
document.addEventListener('keydown',e=>{if(e.key==='Escape'&&activeDrag)cancelDrag();});
window.addEventListener('blur',()=>{if(activeDrag)cancelDrag();});
$('resetBtn').addEventListener('click',()=>$('resetDialog').showModal());
$('cancelReset').addEventListener('click',()=>$('resetDialog').close());
$('confirmReset').addEventListener('click',()=>{$('resetDialog').close();reset();});
$('downloadCsv').addEventListener('click',()=>{
 if(s.absRecorded===null)return;
 const rows=[['Pressure Lab','Experiment record'],['Trial',trial],['Started (UTC)',s.started],['Completed (UTC)',s.completed],[],['Quantity','Student value','Unit'],['Barometer reading',s.baroRecorded.toFixed(1),'mmHg'],['Atmospheric pressure',s.atmRecorded.toFixed(2),'kPa'],['Gauge pressure',s.gaugeRecorded.toFixed(1),'kPa'],['Absolute pressure',s.absRecorded.toFixed(2),'kPa'],[],['Method','P_abs = P_gauge + P_atm'],['Conversion','1 mmHg = 0.1333224 kPa'],['Data type','Simulated instructional measurements'],[],['Time (UTC)','Procedure event'],...s.events.map(e=>[e.at,e.action])];
 const csv=rows.map(row=>row.map(v=>'"'+String(v).replaceAll('"','""')+'"').join(',')).join('\r\n');
 const url=URL.createObjectURL(new Blob(['\ufeff'+csv],{type:'text/csv;charset=utf-8;'}));
 const link=document.createElement('a');link.href=url;link.download=`pressure-lab-trial-${trial}.csv`;document.body.appendChild(link);link.click();link.remove();setTimeout(()=>URL.revokeObjectURL(url),1000);
});
reset();
setInterval(()=>{
 const now=performance.now(),dt=Math.min((now-lastTick)/1000,.25);lastTick=now;
 let changed=false;const wasStable=gaugeStable();
 if(s.baroOn&&!s.baroStable&&now-s.baroStart>=2300) {s.baroStable=true;log('Barometer reading stable');changed=true;}
 if(s.valveOpen&&s.connected) {
  s.line+=(s.vesselPressure-s.line)*(1-Math.exp(-dt/.55));
  if(s.vesselPressure-s.line<.03)s.line=s.vesselPressure;
 } else if(s.venting) {
  s.line*=Math.exp(-dt/.4);
  if(s.line<.03) {s.line=0;s.venting=false;log('Gauge line vented to atmosphere');notice('Gauge line at zero. You may disconnect the hose or reopen the valve for another reading.');changed=true;}
 }
 if(wasStable!==gaugeStable()) {changed=true;if(gaugeStable())log('Gauge pressure stable');}
 if(changed)render();else renderInstruments();
},100);
</script>
</body>
</html>

"""

# Current Streamlit versions automatically fit the iframe to its content.
# The fallback keeps the lab usable on older existing deployments.
if hasattr(st, "iframe"):
    st.iframe(LAB_HTML, height="content", tab_index=0)
else:
    import streamlit.components.v1 as components
    components.html(LAB_HTML, height=1350, scrolling=True, tab_index=0)
