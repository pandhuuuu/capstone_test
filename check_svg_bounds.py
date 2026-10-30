import re

with open('docs/capstone/diagrams/gambar_bpmn_asis.svg', 'r', encoding='utf-8') as f:
    text = f.read()

# find all cy
cys = [float(x) for x in re.findall(r'cy="([0-9\.]+)"', text)]
ys = [float(x) for x in re.findall(r'y="([0-9\.]+)"', text)]
print("Max cy:", max(cys) if cys else None)
print("Max y:", max(ys) if ys else None)

m = re.search(r'height="([0-9\.]+)px"', text)
print("SVG height attribute:", m.group(1) if m else None)
m_vb = re.search(r'viewBox="([^"]+)"', text)
print("viewBox:", m_vb.group(1) if m_vb else None)
