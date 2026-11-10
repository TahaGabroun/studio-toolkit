// Original Studio Toolkit visual calibration. No narration is implied.
const SHOTS = [{start:0, end:4, tr:'cut', draw(ctx, lt, t) {
  drawSky(ctx, '#58b6eb', '#e2f4fe', 0, 1400);
  ctx.fillStyle='#b9e5a9'; ctx.fillRect(0,1150,W,H);
  drawCloud(ctx,200,460,90,4); drawCloud(ctx,870,340,110,9);
  const h = 100 + 220 * Math.abs(Math.sin(Math.PI * t / 2));
  ctx.fillStyle='rgba(20,50,70,.15)'; ellipse(ctx,735,1150,90-h*.08,18); ctx.fill();
  ctx.fillStyle='#ffb347'; circle(ctx,735,1150-h,65); fillStroke(ctx,'#ffb347',7);
  drawStick(ctx,{x:350,y:1150,s:700,bob:Math.sin(t*2)*.006,arms:{L:[.35,-.1],R:[1.2,-.5]},face:{eyes:'normal',look:[.7,0],mouth:'smile'}});
  text(ctx,'motion calibration',540,240,42,'#17334a',null,0,'Poppins',700);
}}];
