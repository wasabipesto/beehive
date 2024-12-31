# SSH Tarpit

I use Cloudflare for my public web ingress tunneling and Tailscale for my private services, and between these two I don't actually need to have any ports open on my machines. I do still leave my SSH server open on a non-standard port (key auth only) just in case something happens to the Tailscale connection. This leaves port 22 - what do you do with that? Just leave it closed? No, you stick a tarpit on it so you can waste some spammer's time.

```js
const time_wasted = FileAttachment('time-wasted.json').json()
const concurrent_connections = FileAttachment('concurrent-connections.json').json()
const top_clients = FileAttachment('top-clients.json').json()
```

## The Tarpit

I use the docker container from [this repository](https://github.com/shizunge/endlessh-go), which takes the original idea from EndleSSH and adds some more features. Namely, this one geolocates attackers by IP and exports everything to Prometheus. It also packages everything up in a handy Docker container.

## The Data

I've had this exporter running for about a year now. Let's see how much time we've wasted.

```js
Plot.plot({
  title: 'Total Hours Wasted per Week',
  y: { grid: true },
  marks: [
    Plot.rectY(
      time_wasted,
      Plot.binX(
        { y: 'sum' },
        {
          x: { interval: 'week', value: 'date' },
          y: (i) => i.trapped_seconds_total / 3600,
          tip: true
        }
      )
    ),
    Plot.ruleY([0])
  ]
})
```

```js
const total_hours_wasted =
  time_wasted.reduce((sum, obj) => sum + obj.trapped_seconds_total, 0) / 3600
```

It turns out we have, on average, a little over one concurrent connection at any given time. In the last year we wasted ${total_hours_wasted.toFixed(0)} hours - ${(total_hours_wasted/365/24).toFixed(3)} times the number of hours in a year.

```js
Plot.plot({
  title: 'Concurrent Connections per Week',
  subtitle: '10th through 99th percentiles',
  y: { grid: true, label: 'connections' },
  color: { type: 'linear', scheme: 'RdYlBu' },
  marks: [
    Plot.line(
      concurrent_connections,
      Plot.binX(
        { y: 'mean' },
        {
          x: { interval: 'week', value: 'date' },
          y: 'value',
          stroke: 'percentile',
          strokeWidth: 1,
          tip: true
        }
      )
    ),
    Plot.ruleY([0])
  ]
})
```

While we typically hover around 1 concurrent connection at any point, there have been some very busy days. You can see a huge spike caused by one moment on 11/24 where we briefly had over 200 simultaneous connections. Here's a version of the plot without the 99th percentile:

```js
Plot.plot({
  title: 'Concurrent Connections per Week',
  subtitle: '10th through 95th percentiles',
  y: { grid: true, label: 'connections' },
  color: { type: 'linear', scheme: 'RdYlBu' },
  marks: [
    Plot.line(
      concurrent_connections.filter((i) => i.percentile < 99),
      Plot.binX(
        { y: 'mean' },
        {
          x: { interval: 'week', value: 'date' },
          y: 'value',
          stroke: 'percentile',
          strokeWidth: 1,
          tip: true
        }
      )
    ),
    Plot.ruleY([0])
  ]
})
```

There seems to have been a lull through this past fall (October, mainly). I also expected much more of a spike over the summer after the xz vulnerability.

# The Attackers

So who's trying to connect? And where are they?

Here's the top offending IPs from the last three months, ranked by total number of connections:

```js
Inputs.table(top_clients, {
  rows: 16.5,
  //maxWidth: 640,
  layout: 'auto',
  columns: ['count', 'country', 'ip', 'rdns'],
  header: {
    ip: 'IP',
    count: 'Connections',
    country: 'Country',
    rdns: 'Reverse DNS'
  },
  align: {
    ip: 'left',
    count: 'left',
    country: 'left',
    rdns: 'left'
  },
  sort: 'count',
  reverse: true
})
```

Let's go ahead and throw those on a map.

```js
const world = FileAttachment('../maps/countries-110m.json').json()
```

```js
const land = topojson.feature(world, world.objects.land)
```

```js
Plot.plot({
  projection: 'equirectangular',
  r: { range: [0, 40] },
  width: 900,
  height: 450,
  marks: [
    Plot.geo(land, { fill: 'currentColor', fillOpacity: 0.2 }),
    Plot.sphere(),
    Plot.dot(top_clients, {
      x: 'long',
      y: 'lat',
      r: 'count',
      fill: 'red',
      fillOpacity: 0.2,
      stroke: 'red',
      channels: { IP: 'ip', Country: 'country', RDNS: 'rdns' },
      tip: {
        format: {
          lat: null,
          long: null
        }
      }
    })
  ]
})
```

I expect many of these are proxied, and so are more revealing of locations that just aren't as responsive to takedown requests or reports of malicious activity than the locations of actual attackers. Still, it's interesting to see where the hotspots are.

We can also break down the stats by country or domain to see just how egregious some are.

```js
let top_countries = top_clients.reduce((acc, { country, count }) => {
  const existing = acc.find((item) => item.country === country)
  if (existing) {
    existing.count += count
  } else {
    acc.push({ country, count })
  }
  return acc
}, [])

top_countries.sort((a, b) => b.count - a.count)
top_countries = top_countries.slice(0, 20)
```

```js
Plot.plot({
  title: 'Top Countries by Attacking Connections',
  subtitle: 'IPs with at least 10 connections in the last 90d',
  marginLeft: 120,
  x: { grid: true, label: 'connections' },
  marks: [
    Plot.barX(top_countries, { y: 'country', x: 'count', sort: { y: '-x' }, tip: true }),
    Plot.ruleX([0])
  ]
})
```

```js
let top_domains = top_clients.reduce((acc, { rdns, count }) => {
  if (!rdns) return acc
  const domainParts = rdns.split('.')
  const topTwoLevels = domainParts.slice(-2).join('.')

  const existing = acc.find((item) => item.domain === topTwoLevels)
  if (existing) {
    existing.count += count
  } else {
    acc.push({ domain: topTwoLevels, count })
  }
  return acc
}, [])

top_domains.sort((a, b) => b.count - a.count)
top_domains = top_domains.slice(0, 20)
```

```js
Plot.plot({
  title: 'Top Domains by Attacking Connections',
  subtitle: 'IPs with at least 10 connections in the last 90d',
  marginLeft: 120,
  x: { grid: true, label: 'connections' },
  marks: [
    Plot.barX(top_domains, { y: 'domain', x: 'count', sort: { y: '-x' }, tip: true }),
    Plot.ruleX([0])
  ]
})
```
