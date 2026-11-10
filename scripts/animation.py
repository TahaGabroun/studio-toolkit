#!/usr/bin/env python3
from pathlib import Path
import runpy,sys
scripts=Path(__file__).resolve().parents[1]/'skills/studio-toolkit/scripts'
sys.path.insert(0,str(scripts))
runpy.run_path(str(scripts/'animation.py'),run_name='__main__')
