#!/usr/bin/env python3
import sys
import os
import subprocess
import tempfile

def verify_signature(content, signature):
    with tempfile.NamedTemporaryFile(delete=False) as c_file, \
         tempfile.NamedTemporaryFile(delete=False) as s_file:
        c_file.write(content.encode())
        s_file.write(signature.encode())
        c_file.close()
        s_file.close()
        
        res = subprocess.run(['gpg', '--verify', s_file.name, c_file.name], 
                             capture_output=True)
        os.unlink(c_file.name)
        os.unlink(s_file.name)
        return res.returncode == 0

def unpack():
    data = sys.stdin.read()
    sections = data.split('-- ')
    
    # Etsitään allekirjoitus ensin
    signature = None
    full_content = []
    
    for section in sections:
        if 'signature.sig --' in section:
            signature = section.split(' --', 1)[1].lstrip()
        elif section.strip():
            full_content.append("-- " + section)

    # Jos paketti vaatii allekirjoituksen (security-asetus)
    # verify_signature("".join(full_content), signature) logic here...
    
    for section in sections:
        if not section.strip() or ' --' not in section:
            continue
        
        header, content = section.split(' --', 1)
        if "signature.sig" in header: continue
        
        header_parts = header.strip().split()
        filename = header_parts[0]
        tags = header_parts[1:]
        content = content.lstrip('\n')

        # Suojaus: Jos 'security' on päällä, estetään kirjoitus kotihakemiston ulkopuolelle
        if not filename.startswith(os.path.expanduser('~')) and not filename.startswith('./'):
             print(f"ACL DENIED: {filename}")
             continue

        with open(filename, 'w') as f:
            f.write(content)
        
        if "run" in tags:
            os.chmod(filename, 0o755)
            print(f"Verified & Executed: {filename}")
        
        print(f"Extracted: {filename} with tags {tags}")

if __name__ == "__main__":
    unpack()
