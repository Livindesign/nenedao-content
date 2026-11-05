#!/usr/bin/env python3
"""Validate the public catalog before committing changes."""
import json
from pathlib import Path
p=Path(__file__).with_name("daily-signs.json")
c=json.loads(p.read_text())
assert c["schemaVersion"]==1 and isinstance(c["revision"],int) and c["revision"]>0
entries=c["entries"];assert 0<len(entries)<=5000
assert len({e["id"] for e in entries})==len(entries),"Duplicate ids"
roles={"pupu","juanjuan","doudou","rongrongtu","paopaota"}
for e in entries:
    assert 0<len(e["id"])<=80,e
    assert e.get("character") in roles|{None},e
    assert 0<len(e["headline"])<=12 and "\n" not in e["headline"],e
    lines=e["message"].split("\n")
    assert len(lines)==2 and all(0<len(x.strip()) and len(x)<=24 for x in lines),e
    if "invitation" in e:assert 0<len(e["invitation"])<=14 and "\n" not in e["invitation"],e
    assert not any(ord(x)<32 and x!="\n" for x in e["headline"]+e["message"]+e.get("invitation","")),e
print(f"OK: revision {c['revision']}, {len(entries)} entries")
