import os
import re

diag_dir = os.path.join('docs', 'capstone', 'diagrams')
for f in os.listdir(diag_dir):
    if f.endswith('.svg') and not f.startswith('temp'):
        path = os.path.join(diag_dir, f)
        with open(path, 'r', encoding='utf-8') as fp:
            c = fp.read()
        m = re.search(r'<svg[^>]+width="([^"]+)"[^>]+height="([^"]+)"', c)
        if m:
            print(f'{f:30} : width={m.group(1)}, height={m.group(2)}')
        else:
            m2 = re.search(r'viewBox="([^"]+)"', c)
            if m2:
                print(f'{f:30} : viewBox={m2.group(1)}')
