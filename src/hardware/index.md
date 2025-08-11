<style>
td {
    width: 50%
}
</style>

```js
const prometheus = FileAttachment('prometheus.json').json()
```

```js
function histogram_norm(series, instance, label, width, percent, max) {
  let domain_y
  let domain_bin
  if (percent) {
    domain_y = [0, 100]
    domain_bin = [0, 1]
  }
  if (max) {
    series = series.filter((obj) => obj.value < max)
    domain_y = [0, max]
  }
  const series_filtered = series.filter((obj) => obj.instance === instance)
  return Plot.plot({
    //caption: 'Histogram of ' + instance + ' ' + label,
    height: 150,
    width: width,
    round: true,
    x: { percent: percent, domain: domain_y, label: label },
    y: { grid: true },
    color: { type: 'ordinal', scheme: 'Observable10' },
    marks: [
      Plot.rectY(
        series_filtered,
        Plot.binX({ y: 'count' }, { x: 'value', domain: domain_bin, thresholds: 50, tip: true })
      ),
      Plot.ruleY([0])
    ]
  })
}
```

# My Hardware

These are the machines and other hardware I use regularly.

Some of the stats on this page are generated from data collected by my prometheus instance over the last month. It was last updated on ${new Date(FileAttachment('prometheus.json').lastModified).toLocaleDateString('en-US', { month: 'long', day: 'numeric', year: 'numeric' })}.

## Phone: Leandros

The little box glued to my side. I use it for communication, photography, note-taking, reading, and a little social media. I purposefully don't have any games on my phone. I prefer smaller phones, anything over about 6" is too large to fit in my hand comfortably.

| Attribute        | Value                   |
| ---------------- | ----------------------- |
| Model            | Google Pixel 8, 2023    |
| Operating System | Android 14              |
| Launcher         | Niagara                 |
| CPU              | Google Tensor G3        |
| Case             | dbrand Grip             |
| Headphones       | Soundcore Liberty 3 Pro |

---

## Laptop: Yumi

I got a cute little Framework 12 to replace the XPS 13 I got right before college in 2015. I love having a lightweight, durable machine to take on the go, mainly for coffee work dates and travel. This model is a yoga-style 2-in-1 with a touchscreen, which is nice for the occasional D&D note-taking or wild artistic hair.

Of course for the price point at another manufacturer you'd probably get a bit more performance and battery life, but with a Framework you're buying the modularity, upgradability, and repairability. Plus, with apps like Zed (with remote server over ssh) I don't need a super high-powered laptop very often. Currently my only wish is for a longer battery life.

| Attribute           | Value                          |
| ------------------- | ------------------------------ |
| Model               | Framework 12 (Lavender)        |
| Operating System    | Debian GNU/Linux 12 (bookworm) |
| Desktop Environment | Vanilla GNOME                  |
| CPU                 | Intel 13th Gen i5-1334U        |
| RAM                 | 48 GB DDR5-5600                |
| Storage             | WD Black SN770M 2TB            |
| Screen              | 12.2” 1920x1200 60 Hz          |
| Battery             | 50 Whr                         |
| Case                | MoKo 12.9" Tablet Sleeve Bag   |

---

## Desktop: Demoux

This is my general-purpose machine for development, gaming, and anything else I do while at home. I've rebuilt this machine several times, most recently in 2022.

| Attribute           | Value                             |
| ------------------- | --------------------------------- |
| Operating System    | Debian GNU/Linux trixie/sid       |
| Desktop Environment | GNOME + PaperWM                   |
| CPU                 | AMD Ryzen 5 5600X (12) @ 3.700GHz |
| GPU                 | Radeon RTX 9070 XT                |
| RAM                 | 128 GB 3200 MHz                   |
| Storage             | SAMSUNG 870 EVO 1TB               |
| Mouse               | Logitech G502                     |
| Keyboard            | Keychron K17 Max                  |
| Headset             | HyperX Cloud II                   |
| Monitors            | 34" Gigbyte M34WQ                 |
|                     | 24” ViewSonic (salvaged)          |

<div class="grid grid-cols-3">
  <div class="card">
    ${resize((width) => histogram_norm(prometheus.cpu_used_pct, "demoux", "percent CPU usage", width, true, null))}
  </div>
  <div class="card">
    ${resize((width) => histogram_norm(prometheus.memory_used_pct, "demoux", "percent memory usage", width, true, null))}
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
    ${resize((width) => histogram_norm(prometheus.cpu_used_pct, "celebrimbor", "percent CPU usage", width, true, null))}
  </div>
  <div class="card">
    ${resize((width) => histogram_norm(prometheus.memory_used_pct, "celebrimbor", "percent memory usage", width, true, null))}
  </div>
  <div class="card">
    ${resize((width) => histogram_norm(prometheus.cloudflared_responses, "celebrimbor", "requests per second", width, false, 1))}
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
    ${resize((width) => histogram_norm(prometheus.cpu_used_pct, "pailiah", "percent CPU usage", width, true, null))}
  </div>
  <div class="card">
    ${resize((width) => histogram_norm(prometheus.memory_used_pct, "pailiah", "percent memory usage", width, true, null))}
  </div>
  <div class="card">
    ${resize((width) => histogram_norm(prometheus.cloudflared_responses, "pailiah", "requests per second", width, false, 1))}
  </div>
</div>
