# Draws the app icon with the game's own drawing code. Usage: python3 make-icon.py out.png 1024  (needs Playwright; writes icon-gen.html beside where it runs)
import asyncio, base64, sys
from playwright.async_api import async_playwright
SRC=__import__('os').path.join(__import__('os').path.dirname(__import__('os').path.abspath(__file__)),'..','..','index.html')
ICON = r"""
window.__icon=function(S){
  const c=document.createElement('canvas');c.width=S;c.height=S;const old=ctx;ctx=c.getContext('2d');ctx.lineJoin='round';ctx.lineCap='round';
  const u=S/1024;ctx.scale(u,u);
  const gunWas=M.T.gun,sightWas=M.T.sight,trigWas=M.T.trigger,stWas=G.state,kWas=G.kick;
  try{
    /* sky: the game's dusk, with a low sun */
    const g=ctx.createLinearGradient(0,0,0,860);g.addColorStop(0,'#2b2466');g.addColorStop(.45,'#7a4470');g.addColorStop(.8,'#d9694f');g.addColorStop(1,'#f2a35a');
    ctx.fillStyle=g;ctx.fillRect(0,0,1024,1024);
    ctx.fillStyle='#ffe08a';ctx.beginPath();ctx.arc(560,860,250,0,7);ctx.fill();
    ctx.fillStyle='rgba(255,241,208,.9)';for(const s of [[120,110,7],[330,70,5],[520,150,6],[760,90,7],[920,210,5],[210,250,4],[880,60,4]]){ctx.beginPath();ctx.arc(s[0],s[1],s[2],0,7);ctx.fill();}
    /* ground */
    ctx.fillStyle='#2f4a2c';ctx.fillRect(0,860,1024,170);ctx.fillStyle='#1b1436';ctx.fillRect(0,852,1024,12);
    /* Bob, calm, with his shotgun */
    M.T.gun=3;M.T.sight=0;M.T.trigger=0;G.state='menu';G.kick=0;
    ctx.save();ctx.translate(250,870);ctx.scale(9.6,9.6);ctx.translate(-218,-(GROUND-FH));drawBob();ctx.restore();
    /* the zombie, mid-lunge */
    const t=TYPES.walker,z={type:'walker',t,fly:false,x:0,y:0,r:t.r,h:t.h,hp:1,max:1,shield:0,shieldMax:1,anim:1.35,flash:0,atk:0,burn:0,frozen:0,hop:0,slow:0,held:0,dropN:3,rope:0,carry:false,cargoLeft:0,stopX:-999};
    ctx.save();ctx.translate(735,862);ctx.scale(9,9);ctx.rotate(.1);drawZombie(z);ctx.restore();
    /* John's pink sofa, arriving on its head */
    ctx.save();ctx.translate(735,862);ctx.scale(9,9);
    const hx=4,hy=-t.h-13;
    ctx.fillStyle='#ffe27a';ctx.strokeStyle=OUT;ctx.lineWidth=2.5;ctx.beginPath();
    for(let i=0;i<16;i++){const a=i*Math.PI/8-.2,r=i%2?13:25;ctx[i?'lineTo':'moveTo'](hx+Math.cos(a)*r,hy+6+Math.sin(a)*r*.62);}ctx.closePath();ctx.fill();ctx.stroke();
    drawItem(hx-2,hy-5,2,-.36);
    ctx.restore();
    /* speed lines behind the sofa */
    ctx.strokeStyle='rgba(255,241,208,.85)';ctx.lineWidth=12;for(const l of [[450,190,560,245],[425,255,535,305],[490,130,590,180]]){ctx.beginPath();ctx.moveTo(l[0],l[1]);ctx.lineTo(l[2],l[3]);ctx.stroke();}
  }finally{M.T.gun=gunWas;M.T.sight=sightWas;M.T.trigger=trigWas;G.state=stWas;G.kick=kWas;ctx=old;}
  return c.toDataURL('image/png');
};
"""
async def main(out, size):
    html=open(SRC,encoding='utf-8').read()
    tail='\n})();\n</script>\n<script>if(\'serviceWorker\''
    assert html.count(tail)==1
    html=html.replace(tail,'\n'+ICON+tail)
    open('icon-gen.html','w',encoding='utf-8').write(html)
    async with async_playwright() as pw:
        b=await pw.chromium.launch(); pg=await b.new_page(viewport={'width':844,'height':390}); errs=[]
        pg.on('pageerror',lambda e:errs.append(str(e)))
        await pg.goto('file://'+__import__('os').getcwd()+'/icon-gen.html'); await pg.wait_for_timeout(700)
        d=await pg.evaluate('window.__icon(%d)'%size)
        open(out,'wb').write(base64.b64decode(d.split(',')[1])); print('errors',errs); await b.close()
asyncio.run(main(sys.argv[1], int(sys.argv[2])))
