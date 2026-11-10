from pathlib import Path
import os

def kit_path():
    if os.environ.get('ANIMATION_KIT'): return str(Path(os.environ['ANIMATION_KIT']).expanduser().resolve())
    candidates=[Path(__file__).resolve().parents[3]/'kit']
    if os.environ.get('STUDIO_TOOLKIT_SKILL'): candidates.insert(0,Path(os.environ['STUDIO_TOOLKIT_SKILL'])/'references/animation-runtime/kit')
    candidates += [Path(os.environ.get('CODEX_HOME',Path.home()/'.codex'))/'skills/studio-toolkit/references/animation-runtime/kit',Path.home()/'.agents/skills/studio-toolkit/references/animation-runtime/kit']
    for path in candidates:
        if (path/'package.json').is_file(): return str(path)
    raise RuntimeError('Set ANIMATION_KIT to the installed or extracted runtime kit directory')
