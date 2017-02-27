"""Rename model files from ALL CAPS with TXT extension to lower case with
sas extension.
"""

import os

txt_files = [
    'V22H79H1.TXT', 'V2216O2M.TXT', 'V22I9ED1.TXT', 'V22H79L1.TXT',
    'V2216O2P.TXT', 'SCOREVAR.TXT', 'V22I0ED1.TXT', 'AGESEXV2.TXT']

sas_files = [
    txt_file.replace('TXT', 'SAS').lower() for txt_file in txt_files]

for tf, sf in zip(txt_files, sas_files):
    cmnd = 'cp {} {}'.format(tf, sf)
    print(cmnd)
    os.system(cmnd)
