# Better Spotify Wrapped

Every year Spotify shows me a summary of my music listening for the year, but I'm never impressed because I feel like I didn't actually learn anything. Let's see what we can actually learn from my listening habits.

```js
// Built from the Spotify takeout and Last.fm by the data loaders in this folder.
const artists = FileAttachment('artists.json').json()
const songs = FileAttachment('songs.json').json()
const clusters = FileAttachment('clusters.json').json()
const genre_attrs = FileAttachment('genre_map.json').json()
const top_genres = FileAttachment('top_genres.json').json()
const monthly_top_genres = FileAttachment('monthly_top_genres.json').json()
const monthly_artists = FileAttachment('monthly_artists.json').json()
const instant_favorites = FileAttachment('instant_favorites.json').json()
const underrated = FileAttachment('underrated.json').json()
const monthly_summary = FileAttachment('monthly_summary.json').json()
const monthly_listen_data = FileAttachment('monthly_listen_data.json').json()
import { trackCards, playButton, quilt, monthTimeline } from './tracks.js'
import { scrubber } from './scrubber.js'
```

<style>
  .track-cards { display: grid; grid-template-columns: repeat(auto-fill, minmax(150px, 1fr)); gap: 1rem; margin: 1rem 0; }
  .track-card { margin: 0; font-size: 14px; }
  .track-cover { position: relative; }
  .track-cover img, .track-cover .no-cover { display: block; width: 100%; aspect-ratio: 1; border-radius: 4px; object-fit: cover; background: var(--theme-background-alt); }
  .track-cover .play-button, .track-cover .play-link { position: absolute; right: 6px; bottom: 6px; }
  .track-artist { font-weight: 600; margin-top: 0.5rem; }
  .track-caption { font-size: 12px; margin-top: 0.25rem; }
  .track-card .track-name { display: none; }
  .play-button, .play-link { width: 28px; height: 28px; border-radius: 50%; border: none; cursor: pointer; display: inline-flex; align-items: center; justify-content: center; background: rgba(0, 0, 0, 0.65); color: #fff; font-size: 12px; text-decoration: none; }
  .play-button::before { content: '▶'; }
  .play-button.playing::before { content: '❚❚'; font-size: 10px; }
  .play-button:hover, .play-link:hover { background: rgba(0, 0, 0, 0.85); }
  .quilt-scroll { overflow-x: auto; margin: 1rem 0; }
  .quilt { display: grid; gap: 4px; grid-auto-rows: 64px; grid-template-rows: auto; width: max-content; }
  .quilt-label { font-size: 11px; line-height: 1.2; align-self: end; overflow: hidden; text-overflow: ellipsis; white-space: nowrap; }
  .cover-tile { width: 64px; height: 64px; padding: 0; border: none; border-radius: 3px; cursor: pointer; background: var(--theme-background-alt); overflow: hidden; position: relative; }
  .cover-tile img { display: block; width: 100%; height: 100%; object-fit: cover; }
  .cover-tile:hover img { opacity: 0.75; }
  .cover-tile.playing { outline: 2px solid var(--theme-foreground-focus); outline-offset: 1px; }
  .cover-tile.playing::after { content: '❚❚'; position: absolute; inset: 0; display: flex; align-items: center; justify-content: center; color: #fff; font-size: 14px; text-shadow: 0 0 4px #000; }
  .timeline { display: grid; grid-template-columns: 3em repeat(12, 48px); grid-auto-rows: 48px; gap: 4px; width: max-content; font-size: 11px; }
  .timeline .cover-tile { width: 48px; height: 48px; }
  .timeline-month { align-self: end; text-align: center; height: auto; }
  .timeline-year { align-self: center; }
  .scrubber { display: flex; align-items: center; gap: 0.75rem; margin: 0.5rem 0; font: 13px var(--sans-serif); }
  .scrubber input[type='range'] { width: min(450px, 60vw); vertical-align: middle; }
  .scrubber .play-button { position: static; background: var(--theme-foreground-faint); }
  .taste-subtitle > div { white-space: nowrap; overflow: hidden; text-overflow: ellipsis; max-width: 900px; }
  button.suggest { font: inherit; font-size: 13px; margin: 0.15rem 0.1rem; padding: 0.1rem 0.5rem; border-radius: 999px; border: 1px solid var(--theme-foreground-faint); background: none; color: inherit; cursor: pointer; }
  button.suggest:hover { background: var(--theme-background-alt); }
  .timeline-empty { background: var(--theme-background-alt); border-radius: 3px; opacity: 0.4; }
</style>

# My Taste

First off, something similar to the standard Spotify presentation. Which bands do I listen to a lot?

## Consistent Favorites

We'll break these out into bands across a variety of genres, so we get a nice diverse sample.

```js
quilt(clusters.quilt)
```

## Recent Favorites

And here's a similar selection of bands, but just for what I've been listening to since ${clusters.recent.since}.

```js
trackCards(clusters.recent.items)
```

# Genre Space

Let's go to the coolest chart: a map of my top genres compared to everyone else's. Hover over each dot to see what that point represents.

```js
const genres_to_show = [
  'house',
  'eurodance',
  'dance pop',
  'synthwave',
  'pop punk',
  'metal',
  'punk',
  'pop',
  'rock',
  'pov: indie',
  'soft rock',
  'classic rock',
  'urbano latino',
  'rap',
  'afrobeats',
  'funk',
  'lo-fi beats',
  'soul',
  'vocal jazz',
  'ambient folk',
  'classical',
  'deep ambient',
  'industrial noise'
]
```

```js
const contours = view(
  Inputs.radio(['Number of genres', 'Last.fm listeners'], { label: 'Background contours', value: 'Number of genres' })
)
```

```js
// Weight each genre by how many Last.fm users tag it, square-rooted so the biggest tags
// (rock, electronic) don't drown out the rest of the map.
const contour_weight = contours === 'Last.fm listeners' ? (d) => Math.sqrt(d.reach) : undefined
```

```js
Plot.plot({
  title: 'Artist Map',
  caption: 'Artists I listen to, placed at the average position of their genres.',
  inset: 10,
  width: 900,
  height: 600,
  x: { label: 'density/bounciness' },
  y: { label: 'organic/mechanical' },
  r: { range: [1.5, 16] },
  marks: [
    Plot.density(genre_attrs, { x: 'x_norm', y: 'y_norm', weight: contour_weight, strokeWidth: 0.25 }),
    Plot.text(
      genre_attrs.filter((i) => genres_to_show.includes(i.name)),
      {
        x: 'x_norm',
        y: 'y_norm',
        text: 'name',
        textAnchor: 'middle',
        fontSize: 12,
        fontWeight: 'lighter'
      }
    ),
    Plot.dot(
      artists.filter((i) => i.ms_played > 1 * 1000 * 3600 && i.x != null),
      {
        x: 'x',
        y: 'y',
        r: (i) => i.ms_played / 1000 / 3600,
        sort: { channel: '-r' },
        fill: 'genre_color',
        fillOpacity: 0.7,
        channels: { Artist: 'name', Genre: 'genre', Hours: (i) => Math.round(i.ms_played / 1000 / 360) / 10 },
        tip: { format: { x: null, y: null, r: null, fill: null } }
      }
    )
  ]
})
```

This map is built with data provided by Glenn Mcdonald's project [Every Noise at Once](https://everynoise.com), where he identified thousands of individual genres and their properties in nearly a dozen dimensions. I'm showing five dimensions here:

- Density vs Bounciness along the x-axis (left to right, respectively)
- Organic vs Mechanical along the y-axis (down to up, respectively)
- Energy, red color channel
- Dynamic Variation, green color channel
- Instrumentalness, blue color channel

<details>
  <summary>Click here for Glenn's descriptions of the various axes used.</summary>

> The calibration is fuzzy, but in general down is more organic, up is more mechanical and electric; left is denser and more atmospheric, right is spikier and bouncier. ([Glenn Mcdonald, everynoise.com](https://everynoise.com))

> [T]his works by mapping three additional acoustic metrics into the red, green and blue color-channels. I arrived at this particular combination through not-at-all-exhaustive experimentation, so maybe I'll come up with a better one, but for the moment red is energy, green is dynamic variation, and blue is instrumentalness. ([Glenn Mcdonald, furia.com](https://www.furia.com/page.cgi?type=log&id=419))

</details>

Music is not distributed along all of these axes equally. The background is a density map of genres in the ENAO database, showing where on the map more artists tend to congregate. There's a rough line from the top-right (house, techno, EDM) to bottom-left (choir, folk, instrumental) with a bulge near the middle representing the rock and pop regions. I've labeled a few of those regions with their dominant genres.

So where do my tastes tend to lie within this map? I'm almost entirely in the northern, more mechanical half of this chart - my southernmost genres include a few indie and instrumental bands but nothing further than that. I have a few genres I like along the very north, like pop punk to the west and house to the east. The bulk of my hours, however, are spent solidly within the rock/pop region.

```js
const dimension_descriptions = {
  x_norm: 'Bounciness',
  y_norm: 'Mechanical',
  r_norm: 'Energy',
  g_norm: 'Dynamic Variation',
  b_norm: 'Instrumentalness'
}
const top_genres_flat = top_genres.flatMap((item) =>
  Object.entries(item)
    .filter(([key]) => key.includes('norm'))
    .map(([key, value]) => ({
      trait: dimension_descriptions[key],
      value: value
    }))
)
```

```js
Plot.plot({
  title: 'My Top Genre Dimensions',
  marginLeft: 120,
  x: { label: 'value', grid: true },
  y: { label: null },
  marks: [
    Plot.boxX(top_genres_flat, {
      y: 'trait',
      x: 'value',
      sort: {
        y: '-x'
      }
    }),
    Plot.ruleX([0])
  ]
})
```

Breaking these out, you can see that I have a large preference for genres with a high dynamic variation and, to a lesser extent, high energy and mechanicality. I think these all match very closely with how I would describe my tastes - I get bored with music easily and it needs to "tickle my brain" to keep me interested.

# Taste Shift

Now how have these genres shifted over time?

```js
const month_name = (m) => new Date(`${m}-15T12:00`).toLocaleDateString('en-US', { month: 'long', year: 'numeric' })
const taste_month = view(scrubber(monthly_artists.months, { format: (d) => month_name(d.month), delay: 600 }))
```

```js
// One size scale for every month, so busy months look busy.
const max_month_artist_hours = d3.max(monthly_artists.months, (m) => d3.max(m.points, (p) => p[1]))
// Each month's centre of listening, weighted by hours.
const month_centers = monthly_artists.months.map((m) => {
  const total = d3.sum(m.points, (p) => p[1])
  if (!total) return null
  const at = (dim) => d3.sum(m.points, ([i, h]) => monthly_artists.artists[i][dim] * h) / total
  return { x: at('x'), y: at('y') }
})
```

```js
{
  const index = monthly_artists.months.indexOf(taste_month)
  const points = taste_month.points.map(([i, hours]) => ({ ...monthly_artists.artists[i], hours }))
  const center = month_centers[index]
  const previous = month_centers.slice(0, index).findLast((c) => c)
  const trace = center && previous ? [{ x1: previous.x, y1: previous.y, x2: center.x, y2: center.y }] : []
  // Two fixed lines, so the chart doesn't jump as the text length changes.
  const subtitle = html`<div class="taste-subtitle">
    <div>${month_name(taste_month.month)}: ${taste_month.hours} hours, ${points.length} artists</div>
    <div>Most played: ${points.slice(0, 3).map((d) => d.name).join(', ') || 'nothing'}</div>
  </div>`
  display(
    Plot.plot({
      title: 'Artist Map',
      subtitle,
      inset: 10,
      width: 900,
      height: 600,
      x: { label: 'density/bounciness', domain: [0, 100] },
      y: { label: 'organic/mechanical', domain: [0, 100] },
      r: { domain: [0, max_month_artist_hours], range: [0, 24] },
      marks: [
        Plot.density(genre_attrs, { x: 'x_norm', y: 'y_norm', strokeWidth: 0.25 }),
        Plot.text(
          genre_attrs.filter((i) => genres_to_show.includes(i.name)),
          { x: 'x_norm', y: 'y_norm', text: 'name', textAnchor: 'middle', fontSize: 10, fontWeight: 'lighter' }
        ),
        Plot.dot(points, {
          x: 'x',
          y: 'y',
          r: 'hours',
          sort: { channel: '-r' },
          fill: 'color',
          fillOpacity: 0.75,
          channels: { Artist: 'name', Genre: 'genre', Hours: (d) => d.hours.toFixed(2) },
          tip: { format: { x: null, y: null, r: null, fill: null } }
        }),
        // Last month's centre and the step to this month's (stopping short of the ✕).
        Plot.dot(previous && center ? [previous] : [], { x: 'x', y: 'y', r: 3, stroke: 'currentColor', strokeWidth: 1.5 }),
        Plot.arrow(trace, { x1: 'x1', y1: 'y1', x2: 'x2', y2: 'y2', stroke: 'currentColor', strokeWidth: 1.5, headLength: 6, insetStart: 3, insetEnd: 8 }),
        Plot.dot(center ? [center] : [], { x: 'x', y: 'y', symbol: 'times', r: 6, strokeWidth: 2, stroke: 'currentColor' })
      ]
    })
  )
}
```

Here, I'll let you scrub through my entire musical history. I've isolated the top genres for every month of my listening and you can show each of them by dragging the slider.

You can see the early days where I mainly listened to pop punk (Panic!) and slowly migrated to a more varied pop and indie palette. You can also see the months where I listened to a bunch of jazz (December 2021) or vocaloid (July 2024). In the end, though I'm still centered firmly in that rock/pop region.

## Discoveries

Every now and then, you come across a song that gets lodged in your head. To track those, I've compiled a list of the most-played songs each month that were played for the first time that month (with a minimum of four plays). Skimming through the list was a fun trip down memory lane, since several of these were songs I played a lot for a short time but never added to a playlist I listen to now.

```js
monthTimeline(
  instant_favorites,
  (d) => `${d.track} by ${d.artist} (${d.plays_first_30d} plays in the first 30 days, ${d.plays_total} in total)`
)
```

## Underrated

Artists and songs I play a lot that few others do: everything I've listened to for at least two hours (artists) or ten plays (songs), sorted by Last.fm listeners.

```js
trackCards(underrated.artists.slice(0, 5), (d) => `${d.listeners.toLocaleString()} listeners · ${d.hours} h`)
```

```js
Inputs.table(underrated.artists, {
  maxWidth: 640,
  columns: ['artist', 'genre', 'listeners', 'hours'],
  header: { artist: 'Artist', genre: 'Genre', listeners: 'Last.fm Listeners', hours: 'My Hours' },
  select: false
})
```

```js
/*
Inputs.table(underrated.songs, {
  maxWidth: 640,
  columns: ['preview', 'track', 'artist', 'listeners', 'plays'],
  header: { preview: '', track: 'Title', artist: 'Artist', listeners: 'Last.fm Listeners', plays: 'My Plays' },
  format: { preview: (_, i, data) => playButton(data[i]) },
  width: { preview: 36 },
  select: false
})
*/
```

## Find Something Similar

Type in an artist you like and I'll suggest a few from my own library that are similar, leaning towards the ones closest to the center of my taste.

```js
const recommend_input = Inputs.text({ placeholder: 'An artist you like', width: 320, autocomplete: 'off', spellcheck: false })
const recommend_query = view(recommend_input)
```

```js
// Artist names compared without case, accents, spaces or punctuation.
const artist_key = (s) =>
  s
    .normalize('NFKD')
    .replace(/[\u0300-\u036f]/g, '')
    .toLowerCase()
    .replace(/[^\p{L}\p{N}]+/gu, '')
// The index (~1 MB) is only fetched once someone starts typing.
const recommender_cache = { promise: null }
function load_recommender() {
  return (recommender_cache.promise ??= FileAttachment('recommender.json')
    .json()
    .then((d) => {
      const keys = new Map()
      const add = (n, i) => {
        const k = artist_key(n)
        keys.set(k, [...(keys.get(k) ?? []), i])
      }
      d.names.forEach(add)
      d.aliases.forEach(([n, i]) => add(n, i))
      return { ...d, keys }
    }))
}
```

```js
{
  const query = artist_key(recommend_query)
  if (!query) {
    display(html`<p class="muted">For example: ${['Lorde', 'Radiohead', 'The 1975'].map(
      (n) => html`<button class="suggest" onclick=${() => setQuery(n)}>${n}</button> `
    )}</p>`)
  } else {
    const rec = await load_recommender()
    const hits = rec.keys.get(query)
    if (!hits) {
      const near = rec.names
        .filter((n) => artist_key(n).includes(query))
        // Names that start with what was typed first, then shorter names.
        .sort((a, b) => artist_key(b).startsWith(query) - artist_key(a).startsWith(query) || a.length - b.length)
        .slice(0, 8)
      display(
        html`<p>That artist isn't near anything I listen to.${near.length
          ? html` Did you mean ${near.map((n) => html`<button class="suggest" onclick=${() => setQuery(n)}>${n}</button> `)}?`
          : ''}</p>`
      )
    } else {
      const isQuery = (m) => artist_key(m.artist) === query || (m.lastfm_name && artist_key(m.lastfm_name) === query)
      const self = rec.mine.find(isQuery)
      const match = new Map()
      for (const i of hits) for (const [m, pct] of rec.links[i]) match.set(m, Math.max(match.get(m) ?? 0, pct / 100))
      // Similarity (squared, so it leads), times a gentle boost for how much I listen to
      // them, times how close they sit to the center of my listening on the artist map.
      const closeness = (m) => Math.exp(-((m.x - rec.center.x) ** 2 + (m.y - rec.center.y) ** 2) / (2 * 20 ** 2))
      const picks = [...match]
        .map(([m, sim]) => ({ ...rec.mine[m], match: sim }))
        .filter((m) => !isQuery(m))
        .map((m) => ({ ...m, score: m.match ** 2 * m.hours ** 0.25 * closeness(m) }))
        .sort((a, b) => b.score - a.score)
        .slice(0, 5)
      display(
        html`<p>${self ? html`${self.artist} is one of mine (${self.hours} hours). ` : ''}${picks.length
          ? 'If you like them, try:'
          : "I don't have anything close enough to suggest."}</p>`
      )
      if (picks.length) display(trackCards(picks, (d) => `${Math.round(d.match * 100)}% similar · ${d.genre ?? ''}`))
    }
  }
}
```

```js
function setQuery(name) {
  recommend_input.value = name
  recommend_input.dispatchEvent(new Event('input', { bubbles: true }))
}
```

# Listening History

Spotify gives me some yearly stats, but what about a monthly breakdown? How long did I listen, and what were my top songs and artists every month?

```js
Inputs.table(monthly_summary, {
  maxWidth: 640,
  //layout: 'auto',
  columns: ['month', 'total_plays', 'total_listen_hours', 'top_track', 'top_artist'],
  header: {
    month: 'Month',
    total_plays: 'Plays',
    total_listen_hours: 'Hours',
    top_track: 'Top Track',
    top_artist: 'Top Artist'
  },
  width: {
    month: 50,
    total_plays: 40,
    total_listen_hours: 40,
    top_track: 200,
    top_artist: 200
  },
  select: false
})
```

Let's plot the number of listened hours over time.

```js
Plot.plot({
  title: 'Total Duration Listened',
  x: { label: 'date' },
  y: { label: 'hours played', grid: true },
  marks: [
    Plot.rectY(
      monthly_summary,
      Plot.binX(
        { y: 'sum' },
        {
          x: { interval: 'month', value: 'month' },
          y: 'total_listen_hours',
          tip: true
        }
      )
    ),
    Plot.ruleY([0])
  ]
})
```

This plot was very surprising to me - I thought I was listening to a lot of music recently, but apparently I was listening _way_ more in 2019. For a few months during the summer of 2019 I was listening nearly 6 hours per day, essentially non-stop from when I woke up to when I got home after work.

```js
Plot.plot({
  title: 'Proportion Skipped',
  height: 200,
  x: { label: 'date' },
  y: { label: 'percent', percent: true, grid: true },
  color: { legend: true, scheme: 'Paired', domain: ['Skipped', 'Played'] },
  marks: [
    Plot.rectY(
      monthly_listen_data.filter((i) => i.trend == 'skipped'),
      Plot.binX(
        { y: 'sum' },
        {
          x: { interval: 'month', value: 'month' },
          y: 'value',
          fill: 'label',
          tip: true
        }
      )
    ),
    Plot.ruleY([0])
  ]
})
```

How picky am I about what plays? This chart shows the total duration of song I've ever skipped, which is quite a lot. In fact, there were even a few months where I skipped more music than I actually played. It seems I just wasn’t feeling whatever Spotify was recommending during that time.

```js
Plot.plot({
  title: 'Proportion Shuffled',
  height: 200,
  x: { label: 'date' },
  y: { label: 'percent', percent: true, grid: true },
  color: { legend: true, scheme: 'Paired', domain: ['Shuffled', 'Not Shuffled'] },
  marks: [
    Plot.rectY(
      monthly_listen_data.filter((i) => i.trend == 'shuffle'),
      Plot.binX(
        { y: 'sum' },
        {
          x: { interval: 'month', value: 'month' },
          y: 'value',
          fill: 'label',
          tip: true
        }
      )
    ),
    Plot.ruleY([0])
  ]
})
```

I used to hate shuffle, and I never ever used it. Now I use it all the time. Pretty much the only time I don't shuffle is for an album or playlist someone has put in order on purpose.

```js
Plot.plot({
  title: 'Proportion by Time of Day',
  height: 200,
  x: { label: 'date' },
  y: { label: 'percent', percent: true, grid: true },
  color: { legend: true, domain: ['Morning', 'Afternoon', 'Night'] },
  marks: [
    Plot.rectY(
      monthly_listen_data.filter((i) => i.trend == 'time_of_day'),
      Plot.binX(
        { y: 'sum' },
        {
          x: { interval: 'month', value: 'month' },
          y: 'value',
          fill: 'label',
          tip: true
        }
      )
    ),
    Plot.ruleY([0])
  ]
})
```

Here I've separated out each play into morning (4AM-12PM), afternoon (12PM-8PM), and night (8PM-4AM). Most of my listening nowadays happens sporadically through the workday or evening, so this distribution rings true.

# Artist Diversity

Do I have a couple favorite artists or do I listen to a lot equally?

```js
Plot.plot({
  title: 'Duration Played per Artist',
  height: 200,
  y: { label: 'artists', grid: true },
  x: { label: 'hours' },
  marks: [
    Plot.rectY(
      artists,
      Plot.binX({ y: 'count' }, { x: (i) => i.ms_played / 1000 / 3600, tip: true })
    ),
    Plot.ruleY([0])
  ]
})
```

```js
const num_artists_over_20h = artists.filter((i) => i.ms_played > 20 * 1000 * 3600).length
const num_artists = artists.length
```

Well it's certainly not equal. I have just a couple artists I listen to a lot and a lot that I've only listened to once or twice. Just ${num_artists_over_20h} got more than 20 hours of stream time, but I've listened to ${num_artists} artists total! This actually does seem like a good thing overall for my exploration - listening to a lot of artists just a few times is a great way to find new favorites.

How deeply do I explore each artist's discography? If I like a song, do I go explore that artist's albums?

```js
Plot.plot({
  title: 'Number of Songs Played per Artist',
  height: 200,
  y: { label: 'artists', grid: true },
  x: { label: 'songs played' },
  marks: [
    Plot.rectY(artists, Plot.binX({ y: 'count' }, { x: 'num_played_songs', tip: true })),
    Plot.ruleY([0])
  ]
})
```

Well that's also a pretty clear "no". There's only ${artists.filter((i) => i.num_played_songs > 12).length} artists where I've listened to over a dozen songs.

Now if we combine these two attributes, we can find which artists I've listed to a lot but not explored thoroughly. Any artists in the bottom-right strip would good to listen to more of.

```js
Plot.plot({
  title: 'Duration Played vs Number of Songs',
  x: { label: 'hours played' },
  y: { label: 'songs played', grid: true },
  marks: [
    Plot.dot(
      artists.filter((i) => i.ms_played > 1 * 1000 * 3600),
      {
        x: (i) => i.ms_played / 1000 / 3600,
        y: 'num_played_songs',
        channels: { Artist: 'name' },
        tip: true
      }
    ),
    Plot.dot([{ x: dursong_hrs, y: dursong_plays }], { x: 'x', y: 'y', stroke: 'red' }),
    Plot.dot(artists_to_explore, {
      x: (i) => i.ms_played / 1000 / 3600,
      y: 'num_played_songs',
      fill: 'red',
      fillOpacity: 0.7
    }),
    Plot.ruleX([0]),
    Plot.ruleY([0])
  ]
})
```

Can we calculate the best artists to explore algorithmically? Sure can. I would simply divide each artist's number of hours played by the number of songs I've listened to, but that would just show a lot of artists I've listened to once and don't have any particular interest in hearing more of.

Instead, I shift each value a little before calculating this score. I've found that shifting the duration by 3-5 hours helps remove the artists I don't really care about. I don't think shifting the play count is very helpful but I've included a slider here so you can try it for yourself. You can imagine this score as the slope between this point and each artist's point, so I've plotted it on the graph above and highlighted the top-scoring artists.

```js
const dursong_hrs = view(Inputs.range([-5, 15], { label: 'Hour Shift', step: 1, value: 5 }))
const dursong_plays = view(Inputs.range([-10, 10], { label: 'Play Shift', step: 1, value: 0 }))
```

```js
const artists_to_explore = artists
  .map((artist) => ({
    ...artist,
    dursong_score:
      (artist.ms_played / 1000 / 3600 - dursong_hrs) / (artist.num_played_songs - dursong_plays)
  }))
  .filter((i) => !isNaN(i.dursong_score))
  .filter((i) => i.num_played_songs < 40)
  .sort((a, b) => b.dursong_score - a.dursong_score)
  .slice(0, 20) // Take top 20 items
```

The last thing I do here is filter out artists I've already listened to a lot (both total duration and number of songs). This is intended for me to find hidden gems, not listen to GROUPLOVE for the millionth time. Here's the final list:

```js
Plot.plot({
  title: 'Artists I Should Explore',
  subtitle: 'Based on duration and number of songs played, shifted a bit',
  marginLeft: 120,
  x: { label: 'score', grid: true },
  y: { label: null },
  marks: [
    Plot.barX(artists_to_explore, {
      x: 'dursong_score',
      y: 'name',
      sort: { y: '-x' },
      tip: true
    }),
    Plot.ruleX([0])
  ]
})
```

# Popularity

How closely do my tastes match everyone else's?

Let's plot the global popularity along the x-axis, and how much I listen to each artist on the y-axis. If my tastes match everyone else's, you'll find a straight line from the bottom-left corner to the top-right.

```js
Plot.plot({
  title: 'Popularity of My Artists',
  height: 300,
  x: { label: 'Last.fm listeners' },
  y: { label: 'hours played', grid: true },
  marks: [
    Plot.dot(
      artists.filter((i) => i.ms_played > 1 * 1000 * 3600 && i.listeners > 0),
      {
        x: 'listeners',
        y: (i) => i.ms_played / 1000 / 3600,
        stroke: 'genre_color',
        channels: { Artist: 'name' },
        tip: { format: { stroke: null } }
      }
    ),
    Plot.ruleX([0]),
    Plot.ruleY([0])
  ]
})
```

There are a few interesting outliers here, Saint Motel chief among them. I do still have a fair number of bands I like below that point (hipster cred) but I don't listen to them as much.

Now let's do the same thing for individual songs:

```js
Plot.plot({
  title: 'Popularity of My Songs',
  height: 300,
  x: { label: 'Last.fm listeners' },
  y: { label: 'hours played', grid: true },
  marks: [
    Plot.dot(
      songs.filter((i) => i.ms_played > 0.5 * 1000 * 3600 && i.listeners > 0),
      {
        x: 'listeners',
        y: (i) => i.ms_played / 1000 / 3600,
        stroke: 'genre_color',
        channels: { Title: 'title', Artist: 'artist' },
        tip: { format: { stroke: null } }
      }
    ),
    Plot.ruleX([0]),
    Plot.ruleY([0])
  ]
})
```

My tastes in individual songs are much more evenly-spread. I've listened to super-popular songs just as much as some that basically nobody has ever heard of, according to Spotify. Note the outlier in the top-left corner, that's not a bug.

# Miscellaneous

For fun, let's look at some other random stats.

## Song Durations

Is there a significant difference in the durations of songs per genre?

```js
const top_20_genres = top_genres.slice(0, 20).map((i) => i.genre)
```

```js
Plot.plot({
  title: 'Durations by Genre',
  marginLeft: 100,
  x: { label: 'minutes', grid: true },
  y: { label: null },
  marks: [
    Plot.boxX(
      songs.filter((i) => top_20_genres.includes(i.genre) && i.duration_ms),
      {
        y: 'genre',
        x: (i) => i.duration_ms / 1000 / 60,
        sort: {
          y: '-x'
        }
      }
    ),
    Plot.ruleX([0])
  ]
})
```

If there is an effect, it is very slight. Excepting post-rock as an outlier, the spreads on these are wide enough that I don't feel comfortable making any conclusions about this.

## Often-Skipped Artists

Are there artists that I listen to a lot, that I also skip a lot?

```js
Plot.plot({
  title: 'Artist Skips',
  //height: 300,
  x: { label: 'play count' },
  y: { label: 'skipped count', grid: true },
  marks: [
    Plot.dot(
      artists.filter((i) => i.ms_played > 1 * 1000 * 3600),
      {
        x: 'play_count',
        y: 'skipped_count',
        stroke: 'genre_color',
        channels: { Artist: 'name' },
        tip: { format: { stroke: null } }
      }
    ),
    Plot.ruleX([0]),
    Plot.ruleY([0])
  ]
})
```

Very much yes. Many of my favorite bands get skipped a lot! I think this is a combination of me not being in the mood for everything all of the time and Spotify shuffle bringing up certain artists way more than it should. Anything in the top-left section here is music that Spotify thinks I like _way_ more than I actually do (Mother Mother).

## Genre Groups

Here's some details on the genre groups my artists tend to fall into.

```js
html`
  <div class="grid grid-cols-2" style="grid-auto-rows: auto">
    ${clusters.clusters.map(
      (c) => html`
        <div class="card" style="margin: 0px;">
          <h2 style="color: ${c.color};">${c.genres.join(' / ')}</h2>
          <h3>${c.hours} hours, ${c.artist_count} artists</h3>
          <ul>
            ${c.artists.slice(0, 6).map((a) => html`<li>${a.name} (${a.hours} h)</li>`)}
          </ul>
        </div>
      `
    )}
  </div>
`
```

<!--

## Genre Artists

For a nice deep dive into my favorites, here's all ${top_genres.length} of my top genres and my top-played artists in each one.

```js
html`
  <div class="grid grid-cols-3" style="grid-auto-rows: auto">
    ${top_genres.map(
      (i) => html`
        <div class="card" style="margin: 0px;">
          <h2 style="color: ${i.color};">${i.genre}</h2>
          <ul>
            ${i.top_artists.map((artist) => html`<li>${artist}</li>`)}
          </ul>
        </div>
      `
    )}
  </div>
`
```

-->
