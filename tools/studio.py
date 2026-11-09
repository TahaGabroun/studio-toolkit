from pathlib import Path
import runpy,sys
p=Path(__file__).resolve().parents[1]/'skills/studio-toolkit/scripts/studio.py'
sys.path.insert(0,str(p.parent))
runpy.run_path(str(p),run_name='__main__')
