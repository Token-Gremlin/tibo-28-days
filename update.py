#!/usr/bin/env python3
"""Fetch new 'Day N/' posts from @thsottiaux and update data.json, then re-render.

Needs: X API v2 Bearer token with access to GET /2/tweets/search/recent
(Basic tier or higher), in env X_BEARER_TOKEN. Run daily (e.g. cron / GitHub Actions):
  X_BEARER_TOKEN=... python3 update.py
New days are added with en/pt = first line of the post text and category 'uncategorized'
(or 'reset' when the post says Reset) -- review/edit them in data.json afterwards.
"""
import json,os,re,sys,urllib.parse,urllib.request,datetime,subprocess
D=os.path.dirname(os.path.abspath(__file__)); P=f"{D}/data.json"
tok=os.environ.get("X_BEARER_TOKEN") or sys.exit("set X_BEARER_TOKEN")
data=json.load(open(P)); have={x["day"] for x in data["days"]}
q=urllib.parse.urlencode({"query":'from:thsottiaux "Day" -is:reply -is:retweet',"max_results":100,
  "tweet.fields":"created_at,note_tweet"})
req=urllib.request.Request("https://api.x.com/2/tweets/search/recent?"+q,headers={"Authorization":"Bearer "+tok})
posts=json.load(urllib.request.urlopen(req)).get("data",[])
BRT=datetime.timezone(datetime.timedelta(hours=-3)); added=0
for p in sorted(posts,key=lambda p:p["created_at"]):
  t=(p.get("note_tweet") or {}).get("text") or p["text"]
  m=re.search(r"\bDay (\d+)(?:\s*\([^)]*\))?/",t)
  if not m or "." in t[m.start():m.end()]: continue
  n=int(m.group(1))
  if n in have or not 1<=n<=data["total"]: continue
  dt=datetime.datetime.fromisoformat(p["created_at"].replace("Z","+00:00")).astimezone(BRT)
  body=re.sub(r"https://t\.co/\S+","",t).strip()
  first=next((l for l in body.split("\n")[1:] if l.strip()),body)[:160]
  reset=bool(re.search(r"Day \d+/\s*Reset",t))
  url="https://x.com/i/status/"+p["id"]
  data["days"].append(dict(day=n,date=dt.strftime("%Y-%m-%d %H:%M"),ids=[p["id"]],url=url,urls=[url],text=body,
    category="reset" if reset else "uncategorized",en="Full usage reset." if reset else first,
    pt="Reset completo de uso." if reset else first,auto=True))
  have.add(n); added+=1
data["days"].sort(key=lambda x:x["day"])
data["updated"]=datetime.datetime.now(BRT).strftime("%Y-%m-%d %H:%M")
json.dump(data,open(P,"w"),ensure_ascii=False,indent=1)
print("added",added); subprocess.run([sys.executable,f"{D}/render.py"])
