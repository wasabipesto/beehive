"""Read Spotify "Extended streaming history" exports into a list of music plays.

Shared by the spotify data loaders. Point SPOTIFY_TAKEOUT_DIR at a folder holding the
export zips (or their extracted folders); every Streaming_History_Audio*.json found is
read, and plays that appear in more than one export are kept once.

Only the fields the page needs are kept. The exports also carry IP addresses and
connection countries, which never leave this module.
"""

import io
import json
import os
import zipfile
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo

from dotenv import load_dotenv

load_dotenv()

# Local time for "time of day" and month bucketing.
LOCAL_TZ = ZoneInfo("America/New_York")


@dataclass(frozen=True, slots=True)
class Play:
    ts: datetime  # local time (LOCAL_TZ) the play ended
    track_uri: str
    track: str
    artist: str  # album artist, as Spotify reports it
    album: str
    ms_played: int
    shuffle: bool
    skipped: bool
    reason_start: str
    reason_end: str

    @property
    def track_id(self) -> str:
        return self.track_uri.rsplit(":", 1)[1]

    @property
    def month(self) -> str:
        return self.ts.strftime("%Y-%m")


def _history_files(root: Path):
    """Yield (name, bytes) for every extended-history audio file under root, zipped or not."""
    for path in sorted(root.rglob("*")):
        if path.suffix == ".zip":
            with zipfile.ZipFile(path) as z:
                for name in sorted(z.namelist()):
                    if Path(name).name.startswith("Streaming_History_Audio"):
                        yield f"{path.name}:{name}", z.read(name)
        elif path.name.startswith("Streaming_History_Audio") and path.suffix == ".json":
            yield str(path), path.read_bytes()


def load_plays(root: str | os.PathLike | None = None) -> list[Play]:
    """All music plays (no podcasts, audiobooks or video), deduplicated, oldest first."""
    root = Path(root or os.environ["SPOTIFY_TAKEOUT_DIR"]).expanduser()
    seen = set()
    plays = []
    for _, raw in _history_files(root):
        for r in json.load(io.BytesIO(raw)):
            uri = r.get("spotify_track_uri")
            if not uri or not r.get("master_metadata_track_name"):
                continue
            key = (r["ts"], uri, r["ms_played"])
            if key in seen:
                continue
            seen.add(key)
            ts = datetime.fromisoformat(r["ts"].replace("Z", "+00:00")).astimezone(LOCAL_TZ)
            plays.append(
                Play(
                    ts=ts,
                    track_uri=uri,
                    track=r["master_metadata_track_name"],
                    artist=r["master_metadata_album_artist_name"],
                    album=r["master_metadata_album_album_name"],
                    ms_played=r["ms_played"],
                    shuffle=bool(r.get("shuffle")),
                    skipped=bool(r.get("skipped")),
                    reason_start=r.get("reason_start") or "",
                    reason_end=r.get("reason_end") or "",
                )
            )
    if not plays:
        raise SystemExit(f"no extended streaming history found under {root}")
    plays.sort(key=lambda p: p.ts)
    return plays
