#!/usr/bin/env python3
"""Forward PROJECT [--voice-id ID] to Studio's cached timestamp-aware provider."""
import os
from pathlib import Path
import runpy
import sys
candidates=[Path(os.environ['STUDIO_TOOLKIT_SKILL'])] if os.environ.get('STUDIO_TOOLKIT_SKILL') else []
candidates += [Path(__file__).resolve().parents[5],Path(os.environ.get('CODEX_HOME',Path.home()/'.codex'))/'skills/studio-toolkit',Path.home()/'.agents/skills/studio-toolkit']
for skill in candidates:
    if (skill/'scripts/elevenlabs_narration.py').is_file():
        sys.path.insert(0,str(skill/'scripts'))
        runpy.run_path(str(skill/'scripts/elevenlabs_narration.py'),run_name='__main__')
        break
else: raise SystemExit('Set STUDIO_TOOLKIT_SKILL to the installed/extracted skill directory')
