"""Builds index.html (data embedded as fallback) and visual.png from data.json."""
import json,subprocess,os
D=os.path.dirname(os.path.abspath(__file__))
data=json.load(open(f"{D}/data.json"))
html=open(f"{D}/template.html").read().replace("__DATA__",json.dumps(data,ensure_ascii=False).replace("</","<\\/"))
open(f"{D}/index.html","w").write(html)
rows=(data["total"]+3)//4
subprocess.run(["google-chrome","--headless=new","--no-sandbox","--disable-gpu","--hide-scrollbars","--allow-file-access-from-files",
 f"--window-size=1600,{1680+0*rows}",f"--screenshot={D}/visual.png",f"file://{D}/index.html"],check=True,capture_output=True)
print("ok")
