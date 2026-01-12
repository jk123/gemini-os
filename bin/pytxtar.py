#!/usr/bin/env python3
import sys
import os

def unpack():
    data = sys.stdin.read()
    files = data.split('-- ')
    for section in files:
        if not section.strip() or ' --' not in section:
            continue
        
        header, content = section.split(' --', 1)
        filename = header.strip()
        content = content.lstrip('\n')
        
        os.makedirs(os.path.dirname(filename) or '.', exist_ok=True)
        with open(filename, 'w') as f:
            f.write(content)
        print(f"Extracted: {filename}")

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "unpack":
        unpack()
    else:
        # Oletusarvoisesti puretaan stdin
        unpack()
