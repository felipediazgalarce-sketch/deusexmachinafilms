"""Renderiza un dict {ruta: svg} a PNG transparente con Chrome sin cabeza (puerto 9333)."""
import asyncio,json,urllib.request,websockets,base64,os,re
async def _r(V,OUT,W):
    t=json.load(urllib.request.urlopen("http://127.0.0.1:9333/json"))
    ws_url=[x for x in t if x["type"]=="page"][0]["webSocketDebuggerUrl"]
    async with websockets.connect(ws_url,max_size=None) as ws:
        i=0
        async def cmd(m,p={}):
            nonlocal i; i+=1; await ws.send(json.dumps({"id":i,"method":m,"params":p}))
            while True:
                r=json.loads(await ws.recv())
                if r.get("id")==i: return r
        await cmd("Emulation.setDefaultBackgroundColorOverride",{"color":{"r":0,"g":0,"b":0,"a":0}})
        for k,s in V.items():
            vw,vh=map(float,re.search(r'viewBox="[-\d.]+ [-\d.]+ ([\d.]+) ([\d.]+)"',s).groups()); H=round(W*vh/vw)
            await cmd("Emulation.setDeviceMetricsOverride",{"width":W,"height":H,"deviceScaleFactor":1,"mobile":False})
            p=os.path.join(OUT,k); os.makedirs(os.path.dirname(p),exist_ok=True); open(p+".svg","w").write(s)
            html='<!doctype html><html><body style="margin:0;background:transparent">'+s.replace("<svg ",'<svg width="%d" height="%d" '%(W,H),1)+'</body></html>'
            open("/tmp/_v.html","w").write(html)
            await cmd("Page.navigate",{"url":"file:///tmp/_v.html"}); await asyncio.sleep(0.5)
            r=await cmd("Page.captureScreenshot",{"format":"png","clip":{"x":0,"y":0,"width":W,"height":H,"scale":1}})
            open(p+".png","wb").write(base64.b64decode(r["result"]["data"]))
def render(V,OUT,W=3840): asyncio.run(_r(V,OUT,W))
