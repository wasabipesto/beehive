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
      cover_image = html.fragment`<img src="/_file/assets-raw/media/posters/${item.id}.jpg" width="80" style="margin: 0 0.5rem;">`
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

```js
function rating_histogram(category) {
  return Plot.plot({
    title: 'Histogram of ' + category.toLowerCase() + ' ratings',
    //caption: 'A histogram of scores in the ' + category + ' category.',
    height: 200,
    x: { label: 'Rating' },
    y: { grid: true },
    color: { type: 'ordinal', scheme: 'Observable10' },
    marks: [
      Plot.rectY(
        media.all,
        Plot.binX(
          { y: 'count' },
          {
            x: category.toLowerCase(),
            thresholds: 5,
            fill: 'category_name',
            tip: true
          }
        )
      ),
      Plot.ruleY([0])
    ]
  })
}
```

<div class="grid grid-cols-3">
  <div class="card">
    ${rating_histogram("Medium")}
  </div>
  <div class="card">
    ${rating_histogram("Story")}
  </div>
  <div class="card">
    ${rating_histogram("Tone")}
  </div>
  <div class="card">
    ${rating_histogram("Enjoyability")}
  </div>
  <div class="card">
    ${rating_histogram("Effect")}
  </div>
  <div class="card">
    ${rating_histogram("Average")}
  </div>
</div>

```js
const chart_start = new Date('2017-01-01')
const media_filtered = media.all
  .filter((item) => item.average >= 4)
  .filter((item) => new Date(item.date) >= chart_start)
const rating_over_time = Plot.plot({
  title: 'Top items',
  height: 400,
  width: 1200,
  x: { type: 'utc', inset: 20, label: 'Date', domain: [chart_start, new Date()] },
  y: { insetTop: 4, grid: true, label: 'Rating', domain: [3.9, 5] },
  marks: [
    Plot.ruleY([0]),
    Plot.image(media_filtered, {
      x: 'date',
      y: 'average',
      src: (i) => '/_file/assets-raw/media/posters/' + i.id + '.jpg',
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
