```js
const tautulli = FileAttachment('tautulli.json').json()
```

# My Plex Server

Part of the purpose of my home server is to download, process, and serve media to my close friends and family through a software called [Plex](https://plex.tv). The server runs from my office closet and doesn't have anywhere near 100% uptime, but it's awfully convenient as an alternative to Netflix.

## Libraries

My two main libraries are Movies and TV. On the server there are ${tautulli.library_movies.count} movies, which have been watched a total of ${tautulli.library_movies.plays} times. In the TV library there are ${tautulli.library_tv.count} shows with a total of ${tautulli.library_tv.parent_count} seasons and ${tautulli.library_tv.child_count} episodes, watched a total of ${tautulli.library_tv.plays} times.

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

Most of the movies I download are around 5GB each, though there are plenty of exceptions both larger and smaller. I've been moving towards 1080p files for most new releases, which are higher quality but take up a bit more space. At current storage prices, this comes out to about 7 cents for a typical movie.

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

Do I have a bias towards more recently released movies? Definitely. But how many of those have been watched more than once?

```js
Plot.plot({
  caption: 'Histogram of movies by year released.',
  height: 250,
  round: true,
  x: { tickFormat: 'd' },
  y: { grid: true },
  color: { type: 'ordinal', scheme: 'Observable10' },
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
          fill: (i) =>
            i.play_count > 9
              ? '10+ plays'
              : i.play_count > 4
              ? '5-9 plays'
              : i.play_count > 0
              ? '1-4 plays'
              : '0 plays'
        }
      )
    ),
    Plot.ruleY([0])
  ]
})
```
