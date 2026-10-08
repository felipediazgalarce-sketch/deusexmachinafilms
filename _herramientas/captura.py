"""Capturas del sitio local con Chrome sin cabeza.
Uso: python3 _herramientas/captura.py URL salida.jpg [ancho alto movil(0/1) espera js]
Necesita el servidor local (dxm-preview, puerto 5055)."""
import asyncio,json,urllib.request,websockets,base64,sys,subprocess,os,time,tempfile
url,salida=sys.argv[1],sys.argv[2]
w=int(sys.argv[3]) if len(sys.argv)>3 else 1400; h=int(sys.argv[4]) if len(sys.argv)>4 else 900
movil=len(sys.argv)>5 and sys.argv[5]=="1"; espera=float(sys.argv[6]) if len(sys.argv)>6 else 4; js=sys.argv[7] if len(sys.argv)>7 else ""
perfil=os.path.join(tempfile.gettempdir(),"dxm-chrome")
subprocess.run(["pkill","-f","remote-debugging-port=9333"]); os.makedirs(perfil,exist_ok=True)
try: os.remove(os.path.join(perfil,"SingletonLock"))
except OSError: pass
subprocess.Popen(["/Applications/Google Chrome.app/Contents/MacOS/Google Chrome","--headless=new","--user-data-dir="+perfil,
  "--remote-debugging-port=9333","--autoplay-policy=no-user-gesture-required","about:blank"],stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
for _ in range(40):
    try: urllib.request.urlopen("http://127.0.0.1:9333/json"); break
    except Exception: time.sleep(0.5)
async def main():
    t=json.load(urllib.request.urlopen("http://127.0.0.1:9333/json"))
    ws_url=[x for x in t if x["type"]=="page"][0]["webSocketDebuggerUrl"]
    async with websockets.connect(ws_url,max_size=None) as ws:
        i=0
        async def cmd(m,p={}):
            nonlocal i; i+=1; await ws.send(json.dumps({"id":i,"method":m,"params":p}))
            while True:
                r=json.loads(await ws.recv())
                if r.get("id")==i: return r
        await cmd("Emulation.setDeviceMetricsOverride",{"width":w,"height":h,"deviceScaleFactor":2 if movil else 1,"mobile":movil})
        await cmd("Page.navigate",{"url":url}); await asyncio.sleep(espera)
        if js: await cmd("Runtime.evaluate",{"expression":js}); await asyncio.sleep(1.2)
        s=await cmd("Page.captureScreenshot",{"format":"jpeg","quality":65}); open(salida,"wb").write(base64.b64decode(s["result"]["data"]))
asyncio.run(main()); subprocess.run(["pkill","-f","remote-debugging-port=9333"])
