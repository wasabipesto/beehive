```js
const tautulli = FileAttachment('tautulli.json').json()
```

# My Plex Server

Part of the purpose of my home server is to download, process, and serve media to my close friends and family through a software called [Plex](https://plex.tv). The server runs from my office closet and doesn't have anywhere near 100% uptime, but it's awfully convenient as an alternative to Netflix.

## Libraries

My two main libraries are Movies and TV. On the server there are ${tautulli.library_movies.count.toLocaleString("en-US")} movies, which have been watched a total of ${tautulli.library_movies.plays.toLocaleString("en-US")} times. In the TV library there are ${tautulli.library_tv.count.toLocaleString("en-US")} shows with a total of ${tautulli.library_tv.parent_count.toLocaleString("en-US")} seasons and ${tautulli.library_tv.child_count.toLocaleString("en-US")} episodes, watched a total of ${tautulli.library_tv.plays.toLocaleString("en-US")} times.

In the last month the most popular movie has been ${tautulli.popular_movies.rows[0].title}, watched ${tautulli.popular_movies.rows[0].total_plays} times by ${tautulli.popular_movies.rows[0].users_watched} people. The most popular TV show has been ${tautulli.popular_tv.rows[0].title}, streamed by ${tautulli.popular_tv.rows[0].users_watched} people.

## Usage

On average we stream about ${tautulli.plays_history_summary.avg_hours_movies} hours of movies and ${tautulli.plays_history_summary.avg_hours_tv} hours of TV every month. This isn't evenly distributed, though - most of the watch time is in the evening between 5PM and midnight.

I've plotted the total watch time for each month for the last several years - we're pretty steady! The only blip was in May 2023, where a configuration error prevented Tautulli from keeping logs for a few weeks.

```js
Plot.plot({
  caption: 'Hours of video streamed from Plex each month.',
  height: 250,
  round: true,
  x: { type: 'utc', label: null },
  y: { grid: true, label: 'hours' },
  color: { legend: true, scheme: 'Paired' },
  marks: [
    Plot.areaY(tautulli.plays_history, {
      y: 'hours',
      x: 'month',
      fill: 'library',
      curve: 'step-after',
      tip: true
    }),
    Plot.ruleY([0])
  ]
})
```

## Movies

Most of the movies I download are around 5GB each, though there are plenty of exceptions both larger and smaller. Some of my new downloads come in 1080p, which are higher quality but take up a bit more space. At current storage prices, this comes out to about 7 cents for a typical movie.

For quite a while I had lower-quality screens or watched TV from a distance, and so I never really noticed a difference between 720p and 1080p. Over time I've started noticing these differences more and more, and now when I download something I think is visually impressive I'll grab it in 1080p. Eventually I would like to upgrade my entire collection and standardize on 1080p, but that will take a significant storage upgrade to accomplish.

```js
Plot.plot({
  caption: 'Histogram of movies by file size.',
  height: 250,
  round: true,
  x: { tickFormat: '.1s' },
  y: { grid: true },
  color: { type: 'ordinal', scheme: 'Observable10' },
  marks: [
    Plot.rectY(
      tautulli.library_movies_items,
      Plot.binX({ y: 'count' }, { x: 'file_size', fill: 'video_resolution', tip: true })
    ),
    Plot.ruleY([0])
  ]
})
```

Around 80% of the movies I download are brand-new, hot out of the theater. I usually set up automatic requests for any new movie I think is interesting or my users would want to watch. The remaining 20% are movies that have been out for a while or old classics that I (or my users) would like to see. This distribution leads to a significant number of the titles in my collection being more recent (and possibly lower quality, depending on who you ask).

Occasionally I will prune titles that have never been watched, or were specific requests that can be safely deleted. The below chart shows movies in my collection by release year, with breakouts for highly-watched and never-watched movies. 2019 was a great year for the sheer quantity of movies, and a huge number of them were very popular with my users!

```js
Plot.plot({
  caption: 'Histogram of movies by year released.',
  height: 250,
  round: true,
  x: { tickFormat: 'd' },
  y: { grid: true },
  color: { type: 'ordinal', scheme: 'Observable10', legend: true },
  marks: [
    Plot.rectY(
      tautulli.library_movies_items,
      Plot.binX(
        { y: 'count' },
        {
          domain: [1900, 2100],
          thresholds: 100,
          x: 'year',
          tip: true,
          fill: (i) => (i.play_count > 9 ? '10+ plays' : i.play_count > 0 ? '1-9 plays' : '0 plays')
        }
      )
    ),
    Plot.ruleY([0])
  ]
})
```
