# Better Spotify Wrapped

Every year Spotify shows me a summary of my music listening for the year, but I'm never impressed because I feel like I didn't actually learn anything. Let's see what we can actually learn from my listening habits.

```js
const artists = FileAttachment('artists.json').json()
const discovered_monthly = FileAttachment('discovered_monthly.json').json()
const genre_attrs = FileAttachment('genre_attrs.json').json()
const songs = FileAttachment('songs.json').json()
const top_genres = FileAttachment('top_genres.json').json()
const monthly_summary = FileAttachment('monthly_summary.json').json()
const monthly_listen_data = FileAttachment('monthly_listen_data.json').json()
const monthly_top_genres = FileAttachment('monthly_top_genres.json').json()
```

# Genre Space

Let's start with the coolest chart: a map of my top genres compared to everyone else's. Hover over each dot to see what that point represents.

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
Plot.plot({
  title: 'Genre Map',
  caption: 'My top genres overlaid on a "map" of global genres.',
  inset: 10,
  width: 900,
  height: 600,
  x: { label: 'density/bounciness' },
  y: { label: 'organic/mechanical' },
  r: { range: [5, 20] },
  marks: [
    Plot.density(genre_attrs, { x: 'x_norm', y: 'y_norm', strokeWidth: 0.25 }),
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
    Plot.dot(top_genres, {
      x: 'x_norm',
      y: 'y_norm',
      r: 'hours_played',
      sort: { channel: '-r' },
      fill: 'color',
      fillOpacity: 0.8,
      channels: { Genre: 'genre', 'Top Artist': 'top_artist', 'Hours Played': 'hours_played' },
      tip: { format: { x: null, y: null, r: null, fill: null } }
    })
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

Now how have these genres shifted over time?

```js
Plot.plot({
  title: 'Genre Map',
  subtitle: 'My top genres circa ' + genre_month,
  inset: 10,
  x: { label: 'density/bounciness' },
  y: { label: 'organic/mechanical' },
  r: { range: [2, 12] },
  marks: [
    Plot.density(genre_attrs, { x: 'x_norm', y: 'y_norm', strokeWidth: 0.25 }),
    Plot.text(
      genre_attrs.filter((i) => genres_to_show.includes(i.name)),
      {
        x: 'x_norm',
        y: 'y_norm',
        text: 'name',
        textAnchor: 'middle',
        fontSize: 10,
        fontWeight: 'lighter'
      }
    ),
    /*Plot.density(monthly_top_genres[genre_month]['top_genres'], {
      x: 'x_norm',
      y: 'y_norm',
      //weight: 'hours_played',
      thresholds: 4,
      bandwidth: 30,
      strokeWidth: 0.5
    }),*/
    Plot.dot(monthly_top_genres[genre_month]['top_genres'], {
      x: 'x_norm',
      y: 'y_norm',
      r: 'hours_played',
      sort: { channel: '-r' },
      fill: 'color',
      fillOpacity: 0.8,
      channels: { Genre: 'genre', 'Top Artist': 'top_artist', 'Hours Played': 'hours_played' },
      tip: { format: { x: null, y: null, r: null, fill: null } }
    })
  ]
})
```

```js
const num_months = Object.keys(monthly_top_genres).length
const month_num = view(
  Inputs.range([0, num_months - 1], { step: 1, value: 39, width: 450, label: 'Month Index' })
)
```

```js
const genre_month = Object.keys(monthly_top_genres).sort()[month_num]
```

Here, I'll let you scrub through my entire musical history. I've isolated the top genres for every month of my listening and you can show each of them by dragging the slider.

You can see the early days where I mainly listened to pop punk (Panic!) and slowly migrated to a more varied pop and indie palette. You can also see the months where I listened to a bunch of jazz (December 2021) or vocaloid (July 2024). In the end, though I'm still centered firmly in that rock/pop region.

For even more proof that my tastes don't really change, here are the centroids of my genre distributions for each month with the routes between them.

```js
Plot.plot({
  title: 'Genre Map',
  subtitle: 'The journey of my taste over time',
  inset: 10,
  x: { label: 'density/bounciness' },
  y: { label: 'organic/mechanical' },
  marks: [
    Plot.density(genre_attrs, { x: 'x_norm', y: 'y_norm', strokeWidth: 0.25 }),
    Plot.text(
      genre_attrs.filter((i) => genres_to_show.includes(i.name)),
      {
        x: 'x_norm',
        y: 'y_norm',
        text: 'name',
        textAnchor: 'middle',
        fontSize: 10,
        fontWeight: 'lighter'
      }
    ),
    Plot.line(Object.values(monthly_top_genres), {
      x: 'centroid_x',
      y: 'centroid_y',
      curve: 'catmull-rom',
      marker: true,
      strokeWidth: 0.5,
      channels: { Month: 'month' },
      tip: true //{ format: { x: null, y: null } }
    })
    /*Plot.text(Object.values(monthly_top_genres), {
      filter: (d) => d.month.includes('01'),
      x: 'centroid_x',
      y: 'centroid_y',
      text: 'month',
      dx: -8
    })*/
  ]
})
```

It's like the tracks after an ice skater does a spin right around (38, 68).

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

This plot was very surprising to me - I thought I was listening to a lot of music recently, but apparently I was listening _way_ more in 2019. For a few months during the summer of 2019 I was listening over 8 hours per day, essentially non-stop from when I woke up to when I got home after work.

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
  title: 'Proportion Explicit',
  height: 200,
  x: { label: 'date' },
  y: { label: 'percent', percent: true, grid: true },
  color: { legend: true, scheme: 'Paired', domain: ['Explicit', 'Not Explicit'] },
  marks: [
    Plot.rectY(
      monthly_listen_data.filter((i) => i.trend == 'explicit'),
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

I don't listen to a ton of explicit music, but I'd be very curious to see how this stacks up against other users or what proportion of songs on the platform are marked explicit. Apparently my tastes have gotten only slightly edgier over time.

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

```js
/* Commented out because I think I misinterpreted Spotify's popularity metric.
Plot.plot({
  title: 'Proportion by Popularity',
  height: 200,
  x: { label: 'date' },
  y: { label: 'percent', percent: true, grid: true },
  color: { legend: true, domain: ['Super', 'High', 'Medium', 'Low'] },
  marks: [
    Plot.rectY(
      monthly_listen_data.filter((i) => i.trend == 'popularity'),
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
*/
```

```js
Plot.plot({
  title: 'Proportion by Release Age',
  height: 200,
  x: { label: 'date' },
  y: { label: 'percent', percent: true, grid: true },
  color: { legend: true, domain: ['Under 1 year', '1-2 years', '2-5 years', '5+ years'] },
  marks: [
    Plot.rectY(
      monthly_listen_data.filter((i) => i.trend == 'release_age'),
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

This chart is shaming me very thoroughly - I've been doing a decent job at finding music new to me, but that music is still pretty old on average. I should work on finding some music that's a little more current, or looking into the albums that my favorite artists have released recently.

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
  x: { label: 'popularity' },
  y: { label: 'hours played', grid: true },
  marks: [
    Plot.dot(
      artists.filter((i) => i.ms_played > 1 * 1000 * 3600),
      {
        x: 'popularity',
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

Well it's certainly not a straight line, except maybe a vertical one. Let's stick the x-axis on a log plot, since it seems it may be scored that way. (The Dragons have skewed my plot once more.)

```js
Plot.plot({
  title: 'Popularity of My Artists',
  subtitle: "But it's a log plot this time",
  height: 300,
  x: { label: 'popularity', type: 'log' },
  y: { label: 'hours played', grid: true },
  marks: [
    Plot.dot(
      artists.filter((i) => i.ms_played > 1 * 1000 * 3600),
      {
        x: 'popularity',
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

Here we can actually see something! My favorite bands seem to already be reasonably popular, above Spotify's popularity score of 70,000. I do still have a fair number of bands I like below that point (hipster cred) but I don't listen to them as much.

Now let's do the same thing for individual songs:

```js
Plot.plot({
  title: 'Popularity of My Songs',
  height: 300,
  x: { label: 'popularity' },
  y: { label: 'hours played', grid: true },
  marks: [
    Plot.dot(
      songs.filter((i) => i.ms_played > 0.5 * 1000 * 3600 && i.popularity > 0),
      {
        x: 'popularity',
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

My tastes in individual songs are much more evenly-spread. I've listened to super-popular songs just as much as some that basically nobody has ever heard of, according to Spotify. Though I do doubt some of these - are you telling me that I'm the only one listening to Australia by The Shins?

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
      songs.filter((i) => top_20_genres.includes(i.specific_genre)),
      {
        y: 'specific_genre',
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

If there is an affect, it is very slight. Neo-synthpop is the longest genre on average, while "alt z" is the shortest, but the spreads on both are wide enough that I don't feel comfortable making any conclusions about this.

## Discoveries

Every now and then, you come across a song that gets lodged in your head. To track those, I've compiled a list of the most-played songs each month that were played for the first time that month (with a minimum of three plays). Reading through the list was a fun trip down memory lane, since several of these were songs I played a lot for a short time but never added to a playlist I listen to now.

```js
Inputs.table(discovered_monthly, {
  maxWidth: 640,
  //layout: 'auto',
  columns: ['month', 'title', 'artist'],
  header: {
    month: 'Month',
    title: 'Title',
    artist: 'Artist'
  },
  width: {
    month: 100,
    title: 250,
    artist: 200
  },
  select: false
})
```

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
        tip: { format: { genre_color: null } }
      }
    ),
    Plot.ruleX([0]),
    Plot.ruleY([0])
  ]
})
```

Very much yes. Many of my favorite bands get skipped a lot! I think this is a combination of me not being in the mood for everything all of the time and Spotify shuffle bringing up certain artists way more than it should. Anything in the top-left section here is music that Spotify thinks I like _way_ more than I actually do (Mother Mother).

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
