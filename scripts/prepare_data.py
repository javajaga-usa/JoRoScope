from pathlib import Path
import csv, json
root=Path(__file__).resolve().parent
legacy=root.parent/'legacy-inspection'/'recovered'
def coord(text):
    text=text.strip(); sign=-1 if text[-1] in 'WS' else 1
    whole,minute=text[:-1].split('.')
    if not 0<=int(minute)<60: raise ValueError('invalid minutes')
    return round(sign*(int(whole)+int(minute)/60),6)
cities=[]; skipped=[]
for i,row in enumerate(csv.reader((legacy/'files'/'JOCITYN.DAT').read_text(encoding='latin1').splitlines())):
    try:
        lat,lon=coord(row[3]),coord(row[2])
        if not -90<=lat<=90 or not -180<=lon<=180: raise ValueError('out of range')
        cities.append(dict(name=row[0].strip(),latitude=lat,longitude=lon,legacy_offset=row[1]))
    except (ValueError,IndexError): skipped.append(dict(line=i+1,row=row))
(root/'web'/'cities.json').write_text(json.dumps(cities,ensure_ascii=False),encoding='utf-8')
(root/'city-import-report.json').write_text(json.dumps(dict(imported=len(cities),skipped=skipped),indent=2))
print(f'{len(cities)} cities imported; {len(skipped)} rows skipped.')
