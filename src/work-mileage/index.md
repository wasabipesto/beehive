# Work Mileage

I don't love driving, but I seem to do a lot of it. Most of my driving recently has been for work, but I recently left that job. The amount of driving wasn't the _only_ concern, but it was certainly on my mind. Today I found my mileage log and decided to look back at the last three years of driving.

## Driving trends

```js
const workdaily = FileAttachment('work-daily.csv').csv({ typed: true })
const allmonthly = FileAttachment('all-monthly.csv').csv({ typed: true })
```

At my old job I drove a lot - I was consistently between 1,000 and 2,000 miles per month, with one bad month over 2,500 miles.

```js
Plot.plot({
  title: 'Total Miles Driven per Month',
  y: { grid: true },
  marks: [
    Plot.rectY(
      workdaily,
      Plot.binX({ y: 'sum' }, { x: { interval: 'month', value: 'Date' }, y: 'Miles', tip: true })
    ),
    Plot.ruleY([0])
  ]
})
```

It turns out that most of my driving was actually just commuting. My commute to the office, which was tracked as part of my truck mileage, was about 40 miles round trip.

```js
Plot.plot({
  title: 'Histogram of Miles Driven per Day',
  y: { grid: true },
  marks: [
    Plot.rectY(workdaily, Plot.binX({ y: 'count' }, { x: 'Miles', tip: true })),
    Plot.ruleY([0])
  ]
})
```

This histogram shows it even better:

- The first big spike shows the days that I didn't drive at all - weekends, holidays, working from home, etc.
- The second big spike shows days I just commuted to the office and back.
- Everything after that is when I would do site visits, drop off parts, etc.

Below I've filtered out anything under 50 miles to show the times I was actually driving somewhere beyond the office:

```js
Plot.plot({
  title: 'Histogram of Miles Driven per Day',
  y: { grid: true },
  marks: [
    Plot.rectY(
      workdaily.filter((i) => i.Miles > 50),
      Plot.binX({ y: 'count' }, { x: 'Miles', tip: true })
    ),
    Plot.ruleY([0])
  ]
})
```

Over 200 days I drove for 1-4 hours, and 27 times I drove over 4 hours in a day. My only saving grace was Friends at the Table, a podcast that I binged every time I was on the road. Without them my sanity would be even further gone.

The natural rhythm of that job came from predominantly working in schools - most of the driving would be over spring or summer breaks while students were on vacation. You can see a natural bump around July here, but there are high outliers in every month. Personally I dreaded driving through snowy northern Indiana every winter for project development.

```js
Plot.plot({
  title: 'Miles Driven per Day',
  subtitle: 'Averaged Throughout the Year',
  x: { label: 'Month' },
  y: { grid: true },
  marks: [
    Plot.boxY(workdaily, {
      x: (i) => i.Date.getMonth() + 1,
      y: 'Miles'
    }),
    Plot.ruleY([0])
  ]
})
```

## Comparison to personal driving

I don't keep records as cleanly for my personal car, but here's a decent comparison between them:

```js
Plot.plot({
  title: 'Total Miles Driven per Month',
  y: { grid: true },
  color: { legend: true, scheme: 'Paired' },
  marks: [
    Plot.rectY(
      allmonthly,
      Plot.binX(
        { y: 'sum' },
        { x: { interval: 'month', value: 'Date' }, y: 'Miles', fill: 'Type', tip: true }
      )
    ),
    Plot.ruleY([0])
  ]
})
```

And for fun, a yearly plot:

```js
Plot.plot({
  title: 'Total Miles Driven per Year',
  y: { grid: true },
  color: { legend: true, scheme: 'Paired' },
  marks: [
    Plot.rectY(
      allmonthly,
      Plot.binX(
        { y: 'sum' },
        { x: { interval: 'year', value: 'Date' }, y: 'Miles', fill: 'Type', tip: true }
      )
    ),
    Plot.ruleY([0])
  ]
})
```

```js
const total_work_miles = allmonthly
  .filter((item) => item.Type === 'Work')
  .reduce((sum, item) => sum + item.Miles, 0)
const times_sf_ny = (total_work_miles / 2470).toFixed(1)
const total_days = (total_work_miles / 60 / 24).toFixed(1)
```

In total, over three years I drove ${total_work_miles} miles for work - ${times_sf_ny} times the distance from San Francisco to New York. Assuming an average of 60 miles per hour (mostly interstate driving), that's about ${total_days} days of my life.

I'm very happy that my new job is fully remote.
