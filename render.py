"""Builds index.html (data embedded as fallback) and visual.png from data.json."""
import json,subprocess,os
D=os.path.dirname(os.path.abspath(__file__))
data=json.load(open(f"{D}/data.json"))
html=open(f"{D}/template.html").read().replace("__DATA__",json.dumps(data,ensure_ascii=False).replace("</","<\\/"))
open(f"{D}/index.html","w").write(html)
# 1960 clipped the row that starts at day 17. 2800 clipped the footer once Day 21 landed.
# 3100 fits the filled grid plus the footer.
subprocess.run(["google-chrome","--headless=new","--no-sandbox","--disable-gpu","--hide-scrollbars","--allow-file-access-from-files",
 "--window-size=1600,3100",f"--screenshot={D}/visual.png",f"file://{D}/index.html"],check=True,capture_output=True)
print("ok")
