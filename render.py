"""Builds index.html (data embedded as fallback) and visual.png from data.json."""
import json,subprocess,os,tempfile
D=os.path.dirname(os.path.abspath(__file__))
data=json.load(open(f"{D}/data.json"))
html=open(f"{D}/template.html").read().replace("__DATA__",json.dumps(data,ensure_ascii=False).replace("</","<\\/"))
open(f"{D}/index.html","w").write(html)
# 1960 clipped the row that starts at day 17. 2800 clipped the footer once Day 21 landed.
# 3100 clipped the footer once Day 22's taller card landed. 3400 fit through Day 24.
# 3400 clipped the footer once Day 25's five-item card landed. 3800 fits the filled grid plus the footer.
# 3800 still fits the complete 28-day grid: Days 27–28 fill the last row, and the series-complete footer stays clear of the bottom.
# The `google-chrome` on this image is a wrapper that pins a debugging profile and does not
# exit after --screenshot, and the capture can land before the cards paint. The stable binary,
# a throwaway profile, and a virtual-time budget wait for the grid, then return.
chrome="/usr/bin/google-chrome-stable" if os.path.exists("/usr/bin/google-chrome-stable") else "google-chrome"
profile=tempfile.mkdtemp(prefix="tibo-chrome-")
subprocess.run([chrome,"--headless=new","--no-sandbox","--disable-gpu","--hide-scrollbars","--allow-file-access-from-files",
 f"--user-data-dir={profile}","--virtual-time-budget=8000","--timeout=20000",
 "--window-size=1600,3800",f"--screenshot={D}/visual.png",f"file://{D}/index.html"],check=True,capture_output=True)
print("ok")
