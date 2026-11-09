# Optional integrations and limits

YouTube: requirements-youtube.txt pins read-only Google API/OAuth clients and yt-dlp. Public Data API calls need YOUTUBE_API_KEY; private Analytics needs the user's read-only OAuth grant. State lives outside production projects in ~/.local/share/studio-toolkit or STUDIO_STATE_DIR. Never commit tokens. Quota files estimate only this toolkit's requests. Caption fetching depends on availability and platform restrictions. Live account retrieval was not exercised; CSV/JSON analysis works without credentials.

Transcription: requirements-transcription.txt provides faster-whisper CPU ASR. Model acquisition is an explicit optional network step. Import existing reviewed transcript/word timestamps for a no-model workflow.

Content discovery: chunk_corpus.py uses SQLite; image_optimizer.py uses Pillow; local Ollama insight extraction uses requests and a separately installed model. find_threads.py uses optional scikit-learn lexical similarity. No automatic pip installations occur in adopted scripts. Ollama and scikit-learn model workflows are not baseline-required.

Asset services: svgl and Mixkit helpers discover assets online; a fetched file still needs a rights/source record. The toolkit does not bundle brand logos, upstream showcase videos or downloaded music. Image/video generation and premium voices are optional user-authorized external tools, not simulated integrations. The demos use original SVG/React diagrams and generated test audio; Noto fonts retain OFL notices.

Remotion is a separately licensed dependency. All @remotion packages are pinned consistently in demos. Review current Remotion license eligibility for your organization; MIT coverage of the original skill repositories does not relicense Remotion. FFmpeg/Chromium also retain their respective licenses. Basic toolkit functions do not require paid APIs.
