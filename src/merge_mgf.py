import os
import re
import sys

from pyteomics import mgf


def natural_sort(s, _nsre=re.compile('([0-9]+)')):
    return [int(text) if text.isdigit() else text.lower()
            for text in _nsre.split(s)]    


mgf_dir = sys.argv[1] if len(sys.argv) > 1 else '.'

scan_nr = 1
spectra = []
for filename in sorted(os.listdir(mgf_dir), key=natural_sort):
    if filename.endswith('.mgf'):
        print(f'{filename}\t{scan_nr}')
        for spectrum_dict in mgf.read(os.path.join(mgf_dir, filename), use_index=False):
            spectrum_dict['params']['scans'] = str(scan_nr)
            spectra.append(spectrum_dict)
            scan_nr += 1

f_out = mgf.write(spectra, os.path.join(mgf_dir, 'merged.mgf'), file_mode='w')
f_out.close()
