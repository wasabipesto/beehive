// Track cards, cover grids and a shared 30-second preview player for the spotify page.
// Items come from the loaders' "track items": {artist, track, album, url, cover, cover_small, preview}.
import {html} from "npm:htl";

const audio = new Audio();
audio.preload = "none";
let playing = null; // the element showing the pause state

function setPlaying(el) {
  if (playing) playing.classList.remove("playing");
  playing = el;
  if (playing) playing.classList.add("playing");
}
audio.addEventListener("ended", () => setPlaying(null));
audio.addEventListener("pause", () => setPlaying(null));

// Toggle the preview for `item`, showing the state on `el`.
function toggle(item, el) {
  if (playing === el && !audio.paused) {
    audio.pause();
    return;
  }
  audio.src = item.preview;
  audio.play().then(() => setPlaying(el), () => setPlaying(null));
}

function describe(item) {
  return [item.track, item.artist].filter(Boolean).join(" — ");
}

// A small play/pause button for a 30-second preview, or a Spotify link if there's no preview.
export function playButton(item) {
  if (item.preview) {
    const b = html`<button class="play-button" title=${`Play a preview: ${describe(item)}`} aria-label=${`Play ${describe(item)}`}></button>`;
    b.onclick = (e) => {
      e.preventDefault();
      e.stopPropagation();
      toggle(item, b);
    };
    return b;
  }
  return item.url ? html`<a class="play-link" href=${item.url} target="_blank" rel="noopener" title="Open in Spotify">↗</a>` : "";
}

// Cards with cover art, artist, track and a caption line, e.g. "indie pop · 99.5 h".
export function trackCards(items, caption = (d) => `${d.hours} h`) {
  return html`<div class="track-cards">
    ${items.map(
      (d) => html`<div class="card track-card">
        <div class="track-cover">
          ${d.cover
            ? html`<a href=${d.url} target="_blank" rel="noopener" title="Open in Spotify"><img src=${d.cover} alt="" loading="lazy" /></a>`
            : html`<div class="no-cover"></div>`}
          ${playButton(d)}
        </div>
        <div class="track-artist">${d.artist}</div>
        <div class="track-name">${d.track ?? ""}</div>
        <div class="track-caption" style=${d.color ? `color: ${d.color}` : ""}>${caption(d)}</div>
      </div>`
    )}
  </div>`;
}

// A clickable cover tile: plays the preview (or opens Spotify), with a hover title.
function tile(d, title) {
  const t = html`<button class="cover-tile" title=${title}>
    ${d.cover_small ? html`<img src=${d.cover_small} alt="" loading="lazy" />` : html`<span class="no-cover"></span>`}
  </button>`;
  t.onclick = () => (d.preview ? toggle(d, t) : d.url && window.open(d.url, "_blank", "noopener"));
  return t;
}

// The album quilt: one column per genre cluster, its top artists as their most-played album.
export function quilt(columns) {
  return html`<div class="quilt-scroll"><div class="quilt" style=${`grid-template-columns: repeat(${columns.length}, 64px)`}>
    ${columns.map(
      (c, i) => html`<div class="quilt-label" style=${`grid-column: ${i + 1}; color: ${c.color}`} title=${c.label}>${c.label.split(" / ")[0]}</div>`
    )}
    ${columns.flatMap((c, i) =>
      c.tiles.map((d, j) => {
        const t = tile(d, `${d.artist} — ${d.album ?? d.track} (${d.hours} h)`);
        t.style.gridColumn = i + 1;
        t.style.gridRow = j + 2;
        return t;
      })
    )}
  </div></div>`;
}

const MONTHS = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"];

// One row per year, one slot per month, each holding that month's track.
export function monthTimeline(items, title = (d) => describe(d)) {
  const byMonth = new Map(items.map((d) => [d.month, d]));
  const years = [...new Set(items.map((d) => d.month.slice(0, 4)))].sort().reverse();
  return html`<div class="quilt-scroll"><div class="timeline">
    <span></span>${MONTHS.map((m) => html`<span class="timeline-month">${m}</span>`)}
    ${years.flatMap((y) => [
      html`<span class="timeline-year">${y}</span>`,
      ...MONTHS.map((_, i) => {
        const d = byMonth.get(`${y}-${String(i + 1).padStart(2, "0")}`);
        return d ? tile(d, `${MONTHS[i]} ${y}: ${title(d)}`) : html`<span class="timeline-empty"></span>`;
      })
    ])}
  </div></div>`;
}
