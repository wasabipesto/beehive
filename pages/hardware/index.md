<style>
td {
    width: 50%
}
</style>

```js
const prometheus = FileAttachment('prometheus.json').json()
```

```js
function histogram_percent(series, instance, label, width) {
  const series_filtered = series.filter((obj) => obj.instance === instance)
  return Plot.plot({
    caption: 'Histogram of ' + instance + ' ' + label + ' usage',
    height: 200,
    width: width,
    round: true,
    x: { percent: true, domain: [0, 100], label: 'Percent of ' + label + ' used' },
    y: { grid: true },
    color: { type: 'ordinal', scheme: 'Observable10' },
    marks: [
      Plot.rectY(
        series_filtered,
        Plot.binX({ y: 'count' }, { x: 'value', domain: [0, 1], thresholds: 50, tip: true })
      ),
      Plot.ruleY([0])
    ]
  })
}
```

```js
function histogram_over_day(series, instance, label, width) {
  const series_filtered = series
    .filter((obj) => obj.instance === instance)
    .filter((obj) => obj.value > 0)
    .filter((obj) => obj.value < 1)
  return Plot.plot({
    caption: 'Histogram of ' + instance + ' ' + label + ' usage over the day',
    height: 200,
    width: width,
    //round: true,
    x: { label: 'Hour of day' },
    y: { percent: true, domain: [0, 100], label: 'Percent of ' + label + ' used' },
    color: { scheme: 'Magma' },
    marks: [
      Plot.rect(
        series_filtered,
        Plot.bin(
          { fill: 'count' },
          {
            x: (d) =>
              new Date(d.time * 1000).getUTCHours() - 5 > 0
                ? new Date(d.time * 1000).getUTCHours() - 5
                : new Date(d.time * 1000).getUTCHours() + 19,
            y: (d) => (d.value < 1 ? d.value : null),
            thresholds: 15,
            tip: true
          }
        )
      )
    ]
  })
}
```

# My Hardware

These are the machines and other hardware I use regularly.

Some of the stats on page are generated from data collected by my prometheus instance over the last 6 months. It was last updated on ${new Date(FileAttachment('prometheus.json').lastModified).toLocaleDateString('en-US', { month: 'long', day: 'numeric', year: 'numeric' })}.

## Phone: Leandros

The little box glued to my side. I use it for communication, photography, note-taking, reading, and a little social media. I purposefully don't have any games on my phone. I prefer smaller phones, anything over about 6" is too large to fit in my hand comfortably.

| Attribute        | Value                |
| ---------------- | -------------------- |
| Model            | Google Pixel 8, 2023 |
| Operating System | Android 14           |
| Launcher         | Niagara              |
| CPU              | Google Tensor G3     |
| Case             | dbrand Grip          |

---

## Desktop: Demoux

This is my general-purpose machine for development, gaming, and anything else I do while at home.

| Attribute           | Value                             |
| ------------------- | --------------------------------- |
| Operating System    | Debian GNU/Linux trixie/sid       |
| Desktop Environment | GNOME 44                          |
| CPU                 | AMD Ryzen 5 5600X (12) @ 3.700GHz |
| GPU                 | NVIDIA GeForce RTX 3060           |
| RAM                 | 48 GB 2133 MHz                    |
| Storage             | SAMSUNG 870 EVO 1TB               |
| Mouse               | Logitech G502                     |
| Keyboard            | Das Keyboard Prime 13             |
| Gamepad             | Logitech G13                      |
| Headset             | HyperX Cloud II                   |
| Monitors            | 25” HP 2511x                      |
|                     | 24” ViewSonic (salvaged)          |
|                     | 24” Acer (salvaged)               |

<div class="grid grid-cols-3">
  <div class="card">
    ${resize((width) => histogram_percent(prometheus.cpu_used_pct, "demoux", "CPU", width))}
  </div>
  <div class="card grid-colspan-2">
    ${resize((width) => histogram_over_day(prometheus.cpu_used_pct, "demoux", "CPU", width))}
  </div>
  <div class="card">
    ${resize((width) => histogram_percent(prometheus.memory_used_pct, "demoux", "memory", width))}
  </div>
  <div class="card grid-colspan-2">
    ${resize((width) => histogram_over_day(prometheus.memory_used_pct, "demoux", "memory", width))}
  </div>
</div>

---

## Server: Celebrimbor

This is my media storage server, with enough CPU to transcode lots of streams on Plex.

| Attribute        | Value                                    |
| ---------------- | ---------------------------------------- |
| Operating System | Ubuntu 20.04.6 LTS                       |
| CPU              | Intel(R) Xeon(R) CPU E5-2678 v3          |
| RAM              | 64 GB 2133 MHz                           |
| Storage          | SAMSUNG 860 EVO 1TB                      |
| Storage          | 6x WD Elements 12TB (shucked) Soft RAID5 |
| UPS              | CyberPower 1500VA                        |

<div class="grid grid-cols-3">
  <div class="card">
    ${resize((width) => histogram_percent(prometheus.cpu_used_pct, "celebrimbor", "CPU", width))}
  </div>
  <div class="card grid-colspan-2">
    ${resize((width) => histogram_over_day(prometheus.cpu_used_pct, "celebrimbor", "CPU", width))}
  </div>
  <div class="card">
    ${resize((width) => histogram_percent(prometheus.memory_used_pct, "celebrimbor", "memory", width))}
  </div>
  <div class="card grid-colspan-2">
    ${resize((width) => histogram_over_day(prometheus.memory_used_pct, "celebrimbor", "memory", width))}
  </div>
</div>

---

## Server: Pailiah

This is my general-purpose VPS for hosting random services and whatnot. It's serving you this webpage unless you hit Cloudflare's cache.

| Attribute        | Value                      |
| ---------------- | -------------------------- |
| Provider         | OVH Dedicated KS-16        |
| Operating System | Debian GNU/Linux 12        |
| CPU              | Intel Xeon E3-1245v2       |
| RAM              | 32 GB 1333 MHz             |
| Storage          | 3×2 TB HDD SATA Soft RAID1 |

<div class="grid grid-cols-3">
  <div class="card">
    ${resize((width) => histogram_percent(prometheus.cpu_used_pct, "pailiah", "CPU", width))}
  </div>
  <div class="card grid-colspan-2">
    ${resize((width) => histogram_over_day(prometheus.cpu_used_pct, "pailiah", "CPU", width))}
  </div>
  <div class="card">
    ${resize((width) => histogram_percent(prometheus.memory_used_pct, "pailiah", "memory", width))}
  </div>
  <div class="card grid-colspan-2">
    ${resize((width) => histogram_over_day(prometheus.memory_used_pct, "pailiah", "memory", width))}
  </div>
</div>
