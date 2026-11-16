"""Genres for the spotify page: Last.fm tags placed on the Every Noise at Once map.

Spotify no longer gives developer apps artist genres, so each artist's genres come from
its Last.fm tags, kept only when the tag names a genre on the ENAO map (after a little
normalisation). An artist sits at the tag-weighted average position of its genres; artists
with no usable tags are placed among the similar artists I listen to instead.
"""

import json
import math
from collections import Counter, defaultdict
from pathlib import Path

import numpy as np

from lastfm import LastFM
from takeout import Play

MIN_TAG_COUNT = 10  # Last.fm tag counts are relative (top tag = 100); below this is noise
MAX_GENRES = 5
DIMS = ("x", "y", "r", "g", "b")

# Broad Last.fm tags that have no exact ENAO counterpart. Nationalities, decades and
# personal tags ("seen live", "favorites") are deliberately left unmatched.
ALIASES = {
    "indie": "indie rock",
    "alternative": "alternative rock",
    "alt rock": "alternative rock",
    "electronic": "electronica",
    "rnb": "r&b",
    "synth pop": "synthpop",
    "electro pop": "electropop",
    "electro": "electro house",
    "chillout": "chill out",
    "female vocalists": None,
}


def load_enao() -> list[dict]:
    return json.loads(Path(__file__).with_name("enao_genres.json").read_text(encoding="utf-8"))


class GenreMap:
    def __init__(self):
        self.genres = {g["name"]: g for g in load_enao()}

    def match(self, tag: str) -> str | None:
        t = tag.casefold().strip()
        if t in ALIASES:
            return ALIASES[t]
        for candidate in (t, t.replace("-", " "), t.replace(" ", "")):
            if candidate in self.genres:
                return candidate
        return None

    def from_tags(self, tags: list[tuple[str, int]]) -> dict[str, int]:
        """ENAO genres named by a tag list, as {genre: Last.fm tag count}."""
        weights = {}
        for tag, count in tags:
            g = self.match(tag)
            if g and count >= MIN_TAG_COUNT:
                weights[g] = max(weights.get(g, 0), count)
        return weights

    def position(self, genres: list[tuple[str, float]]) -> dict:
        return {d: round(sum(self.genres[g][d] * w for g, w in genres), 2) for d in DIMS}


def artist_profiles(plays: list[Play], fm: LastFM | None = None) -> dict[str, dict]:
    """Last.fm data, genres and map position for every artist in plays, keyed by Spotify name."""
    fm = fm or LastFM()
    gm = GenreMap()
    hours = Counter()
    for p in plays:
        hours[p.artist] += p.ms_played / 3.6e6
    raw = {}
    for name, _ in hours.most_common():
        a = fm.artist(name)
        raw[name] = (a, gm.from_tags(a["tags"]) if a else {})
    # Rarer genres count for more, so "indie rock" (on half my artists) doesn't swamp the
    # more specific tags an artist also has.
    df = Counter(g for _, tags in raw.values() for g in tags)
    n = len(raw)
    profiles = {}
    for name, (a, tags) in raw.items():
        scored = sorted(((g, c * (math.log(n / df[g]) + 1)) for g, c in tags.items()), key=lambda kv: -kv[1])
        top = scored[:MAX_GENRES]
        total = sum(w for _, w in top)
        profiles[name] = {
            "name": name,
            "lastfm_name": a["name"] if a else None,
            "listeners": a["listeners"] if a else None,
            "genres": [(g, w / total) for g, w in top],
            "similar": a["similar"] if a else [],
            "placed_by": "tags",
        }
    # Artists without usable tags: borrow genres from the similar artists I listen to.
    by_lastfm = {p["lastfm_name"].casefold(): p for p in profiles.values() if p["lastfm_name"] and p["genres"]}
    for p in profiles.values():
        if p["genres"]:
            continue
        borrowed = Counter()
        for sim, match in p["similar"]:
            other = by_lastfm.get(sim.casefold())
            if other:
                for g, w in other["genres"]:
                    borrowed[g] += w * match
        if borrowed:
            top = borrowed.most_common(MAX_GENRES)
            total = sum(w for _, w in top)
            p["genres"] = [(g, w / total) for g, w in top]
            p["placed_by"] = "similar"
        else:
            p["placed_by"] = None
    for p in profiles.values():
        del p["similar"]
        p["hours"] = hours[p["name"]]
        if p["genres"]:
            p.update(gm.position(p["genres"]))
            p["genre"] = p["genres"][0][0]
            p["color"] = gm.genres[p["genre"]]["color"]
        else:
            p.update({d: None for d in DIMS} | {"genre": None, "color": None})
    return profiles


def genre_totals(plays: list[Play], profiles: dict[str, dict], n: int) -> list[dict]:
    """Top n genres by hours. Each play's time is split across its artist's genres by weight."""
    gm = GenreMap()
    ms, plays_n, skips = Counter(), Counter(), Counter()
    artist_ms = defaultdict(Counter)
    for p in plays:
        for g, w in profiles[p.artist]["genres"]:
            ms[g] += p.ms_played * w
            plays_n[g] += w
            skips[g] += w * bool(p.skipped)
            artist_ms[g][p.artist] += p.ms_played * w
    out = []
    for g, total in ms.most_common(n):
        top_artists = [a for a, _ in artist_ms[g].most_common(3)]
        out.append(
            {
                "genre": g,
                "artist_count": len(artist_ms[g]),
                "play_count": round(plays_n[g]),
                "skipped_pct": round(skips[g] / plays_n[g], 4) if plays_n[g] else 0,
                "hours_played": round(total / 3.6e6, 1),
                **{f"{d}_norm": gm.genres[g][d] for d in DIMS},
                "color": gm.genres[g]["color"],
                "top_artist": top_artists[0],
                "top_artists": top_artists,
            }
        )
    return out


def clusters(profiles: dict[str, dict], k: int = 8, min_hours: float = 1.0, seed: int = 0) -> list[dict]:
    """Group artists I've played for at least min_hours by genre, with spherical k-means.

    Genre weights are tf-idf scaled so broad genres every artist shares ("indie rock")
    don't dominate. Clusters are ordered by total hours.
    """
    artists = [p for p in profiles.values() if p["genres"] and p["hours"] >= min_hours]
    vocab = sorted({g for p in artists for g, _ in p["genres"]})
    index = {g: i for i, g in enumerate(vocab)}
    df = Counter(g for p in artists for g, _ in p["genres"])
    idf = np.array([math.log(len(artists) / df[g]) + 1 for g in vocab])
    X = np.zeros((len(artists), len(vocab)))
    for i, p in enumerate(artists):
        for g, w in p["genres"]:
            X[i, index[g]] = w
    X *= idf
    X /= np.linalg.norm(X, axis=1, keepdims=True)
    weights = np.array([p["hours"] for p in artists])

    rng = np.random.default_rng(seed)
    best = None
    for _ in range(20):
        C = X[rng.choice(len(X), k, replace=False, p=weights / weights.sum())]
        for _ in range(100):
            labels = (X @ C.T).argmax(axis=1)
            newC = np.array([(X[labels == j] * weights[labels == j, None]).sum(axis=0) if (labels == j).any() else C[j] for j in range(k)])
            newC /= np.linalg.norm(newC, axis=1, keepdims=True)
            if np.allclose(newC, C):
                break
            C = newC
        score = (weights * (X @ C.T)[np.arange(len(X)), labels]).sum()
        if best is None or score > best[0]:
            best = (score, labels, C)
    _, labels, C = best
    mean = (X * weights[:, None]).sum(axis=0)
    mean /= np.linalg.norm(mean)

    out = []
    for j in range(k):
        members = sorted((artists[i] for i in np.flatnonzero(labels == j)), key=lambda p: -p["hours"])
        if not members:
            continue
        # Label by what sets the cluster apart (weight relative to the average artist), using
        # only genres shared by enough members that one artist's stray tags can't name it.
        shared = Counter(g for p in members for g, _ in p["genres"])
        floor = max(2, min(5, 0.1 * len(members)))
        ranked = [vocab[i] for i in np.argsort(-(C[j] - mean)) if shared[vocab[i]] >= floor]
        top = (ranked or [vocab[i] for i in np.argsort(-C[j])])[:3]
        out.append(
            {
                "genres": top,
                "color": GenreMap().genres[top[0]]["color"],
                "hours": round(sum(p["hours"] for p in members), 1),
                "artists": [p["name"] for p in members],
            }
        )
    return sorted(out, key=lambda c: -c["hours"])
