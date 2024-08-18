# Favorite Media

What media do I recommend? While I don't like to give unilateral recommendations, I can list some of my favorite pieces of media.

This page is generated from my database of media ratings from [Notion](https://wasabipesto.com/notion). It was last updated on ${new Date(FileAttachment('media.json').lastModified).toLocaleDateString('en-US', { month: 'long', day: 'numeric', year: 'numeric' })}.

```js
const media = FileAttachment('media.json').json()
```

```js
for (const cat of media.categorized) {
  display(html`<h2>${cat.category_name}</h2>`)
  var items_html = []
  for (const item of cat.items) {
    var full_title = html.fragment`${item.title}`
    if (item.media_link) {
      full_title = html.fragment`<a href="${item.media_link}" target="_blank">${item.title}</a>`
    }
    if (item.average > 4.75) {
      full_title = html.fragment`❤️ ${full_title}`
    }
    if (item.artist) {
      full_title = html.fragment`${full_title}<br /><span style="color: var(--theme-foreground-muted)">${item.artist}</span>`
    }

    var cover_image = html.fragment``
    if (item.image_link) {
      cover_image = html.fragment`<img src="/assets/media/posters/${item.id}.jpg" width="80" style="margin: 0 0.5rem;">`
    }
    items_html.push(html.fragment`
      <div class="card"><table style="margin: 0"><td>${cover_image}</td><td width="99%">${full_title}</td></div>
    `)
  }
  display(html`<div class="grid grid-cols-4" style="grid-auto-rows: auto;">${items_html}</div>`)
}
```

## Analysis

How do I come up with these scores to pick my favorites? Like many things, if it's worth doing then it's worth over-doing.

For most pieces of media I rate them on five scales:

- Medium: A rating of how well the work takes advantage of the medium it's in. For books, this is mainly focused on the writing style and conventions. For games, this is often about the gameplay loop. For movies and TV this is about how well they utilized the screen and perspective. How good was it at being the thing it is?
- Story: A rating of the narrative overall. This encompasses the plot, characters, and pacing. Did the story push me forward? Did I find the characters compelling?
- Tone: How well a work expresses a certain tone. Was there a specific atmosphere? Did I feel engrossed in the world?
- Enjoyability: Did I like playing/watching/reading this? Was it fun, did it keep me engaged? Often a low bar.
- Effect: How much of an effect did this work have on me? Do I often return to the concepts, or want to re-watch it over again? Sometimes I come back after a few months to adjust this as time passes.

Below I've broken out my rating on each scale (plus averages) for each type of media.

```js
function rating_histogram(type, category) {
  var series = media.all
  if (type) {
    series = series.filter((obj) => obj.type === type)
  }
  return Plot.plot({
    width: 200,
    height: 100,
    x: { label: null, domain: [0, 5] },
    y: { label: null, ticks: [] },
    marks: [
      Plot.rectY(
        series,
        Plot.binX({ y: 'count' }, { x: category, thresholds: [0, 1, 2, 3, 4, 5] })
      ),
      Plot.ruleY([0])
    ]
  })
}
```

<div class="card">
<h2>Rating breakdown per media type, per rating scale</h2>
<table style="max-width: 100%; margin: 0; text-align: center">
  <thead>
    <tr>
      <td></td>
      <td>Medium</td>
      <td>Story</td>
      <td>Tone</td>
      <td>Enjoyability</td>
      <td>Effect</td>
      <td>Average</td>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td style="vertical-align: middle">Books</td>
      <td>${rating_histogram("Book", "medium")}</td>
      <td>${rating_histogram("Book", "story")}</td>
      <td>${rating_histogram("Book", "tone")}</td>
      <td>${rating_histogram("Book", "enjoyability")}</td>
      <td>${rating_histogram("Book", "effect")}</td>
      <td>${rating_histogram("Book", "average")}</td>
    </tr>
    <tr>
      <td style="vertical-align: middle">Games</td>
      <td>${rating_histogram("Game", "medium")}</td>
      <td>${rating_histogram("Game", "story")}</td>
      <td>${rating_histogram("Game", "tone")}</td>
      <td>${rating_histogram("Game", "enjoyability")}</td>
      <td>${rating_histogram("Game", "effect")}</td>
      <td>${rating_histogram("Game", "average")}</td>
    </tr>
    <tr>
      <td style="vertical-align: middle">Movies</td>
      <td>${rating_histogram("Movie", "medium")}</td>
      <td>${rating_histogram("Movie", "story")}</td>
      <td>${rating_histogram("Movie", "tone")}</td>
      <td>${rating_histogram("Movie", "enjoyability")}</td>
      <td>${rating_histogram("Movie", "effect")}</td>
      <td>${rating_histogram("Movie", "average")}</td>
    </tr>
    <tr>
      <td style="vertical-align: middle">TV Series</td>
      <td>${rating_histogram("TV Series", "medium")}</td>
      <td>${rating_histogram("TV Series", "story")}</td>
      <td>${rating_histogram("TV Series", "tone")}</td>
      <td>${rating_histogram("TV Series", "enjoyability")}</td>
      <td>${rating_histogram("TV Series", "effect")}</td>
      <td>${rating_histogram("TV Series", "average")}</td>
    </tr>
  </tbody>
</table>
</div>

Some trends I've noticed in this data:

- I tend to rate books quite highly on enjoyability, and to a lesser extent both medium and tone. I think this is for two reasons: I find books that I like very enjoyable to read, and I simply don't finish books I don't enjoy.
- Games and movies often get low scores in the story department. Since these are often shorter-form than books and TV shows, it makes sense that their plots could often be less-developed. TV shows scored a bit behind books, which often set the gold standard for me.
- Movies are often forgettable! There are many that got very low scores in the effect category because they simply didn't make a lasting impression on me. Several of these were titles I remember quite enjoying, I just don't remember why.

```js
const chart_start = new Date('2017-01-01')
const media_filtered = media.all
  .filter((item) => item.average >= 4)
  .filter((item) => new Date(item.date) >= chart_start)
const rating_over_time = Plot.plot({
  title: 'Timeline of top-rated items',
  height: 400,
  width: 1200,
  x: { type: 'utc', inset: 20, label: 'Date', domain: [chart_start, new Date()] },
  y: { insetTop: 4, grid: true, label: 'Rating', domain: [3.9, 5] },
  marks: [
    Plot.ruleY([0]),
    Plot.image(media_filtered, {
      x: 'date',
      y: 'average',
      src: (i) => '/assets/media/posters/' + i.id + '.jpg',
      r: 20,
      preserveAspectRatio: 'xMidYMin slice',
      title: 'title',
      tip: true
    })
  ]
})
```

<div class="grid grid-cols-1">
  <div class="card">
    ${rating_over_time}
  </div>
</div>

This timeline is a bit of a wash, but I think it's neat enough to show anyways. The problem is that many of these dates are not accurate, or they don't accurately depict when I first encountered the media. It's especially bad for TV shows: Do you note when you finished the first season, or the last time you watched an episode? What about re-watching? For most of these I just put the time it was most significant in my life and eyeballed some of the dates from before I kept this media log.
