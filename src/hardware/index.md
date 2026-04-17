<style>
td {
    width: 50%
}
</style>

# My Hardware

These are the machines and other hardware I use regularly.

## Phone: Leandros

The little box glued to my side. I use it for communication, photography, note-taking, reading, and a little social media. I purposefully don't have any games on here, if I have long enough to play a game I should be [reading](/media/). 

I prefer smaller phones, anything over about 6" is too large to fit in my hand comfortably. If someone released a new small phone with a flagship processor I would buy it day one. I'm hoping that better battery tech makes this feasible [in the next 3-5 years](https://manifold.markets/wasabipesto/when-will-small-phones-come-back) but right now it seems like they're just trying to go thinner, not smaller.

| Phone            | Leandros                |
| ---------------- | ----------------------- |
| Model            | Google Pixel 8, 2023    |
| Launcher         | Niagara                 |
| Case             | Spigen Liquid Air       |
| Headphones       | Bose QuietComfort Ultra |

---

## Laptop: Yumi

I got a cute little Framework 12 to replace the XPS 13 I got right before college in 2015. I love having a lightweight, durable machine to take on the go, mainly for coffee work dates and travel. This model is a yoga-style 2-in-1 with a touchscreen, which is nice for the occasional D&D note-taking or wild artistic hair.

Of course for the price point at another manufacturer you'd probably get a bit more performance and battery life, but with a Framework you're buying the modularity, upgradability, and repairability. Plus, with apps like Zed (with remote server over ssh) I don't need a super high-powered laptop very often. Currently my only wish is for a longer battery life.

| Laptop              | Yumi                           |
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

I really enjoy scrolling window managers, I like how they feel like a physical viewport that I can move around with a clear structure rather than a cramped, messy desk top. To dip my toe in I used [PaperWM](https://github.com/paperwm/PaperWM) for about a year and enjoyed it a lot, I think it's a great introduction if you already use Gnome. However, [niri](https://github.com/niri-wm/niri) is leagues better if you can dedicate a few days to setting everything up just right. I wish niri and more of that ecosystem was packaged for Debian but that's basically my only complaint at the moment.

| Desktop             | Demoux                            |
| ------------------- | --------------------------------- |
| Operating System    | Debian GNU/Linux 14 (forky)       |
| Desktop Environment | Niri (previously Gnome + PaperWM) |
| CPU                 | AMD Ryzen 5 5600X (12) @ 3.700GHz |
| GPU                 | Radeon RTX 9070 XT                |
| RAM                 | 128 GB 3200 MHz                   |
| Storage             | SAMSUNG 870 EVO 1TB               |
| Mouse               | Logitech G502                     |
| Keyboard            | Keychron K17 Max                  |
| Headset             | HyperX Cloud II                   |
| Monitors            | 34" Gigbyte M34WQ                 |
|                     | 24” ViewSonic (salvaged)          |

---

## Server: Celebrimbor

This is my media storage box, with enough CPU to transcode lots of streams on Plex and enough drives to hold it all. The core is a hand-me-down server motherboard stored in a massive tower case. Eventually I'll have to buy a real server rack, but not today!

| Server           | Celebrimbor                              |
| ---------------- | ---------------------------------------- |
| Operating System | Ubuntu 20.04.6 LTS                       |
| CPU              | Intel(R) Xeon(R) CPU E5-2678 v3          |
| RAM              | 64 GB 2133 MHz                           |
| Storage          | SAMSUNG 860 EVO 1TB                      |
| Storage          | 6x WD Elements 12TB (shucked) Soft RAID5 |
| UPS              | CyberPower 1500VA                        |

---

## Server: Shalash

For legal reasons Shalash isn't actually a server. She has no ECC memory, no server-grade CPU, and no redundant power supply because she's a laptop.

The story here is that I used to run my databases on a VPS with a spinning disk, no SSD. This was obviously not great, and I was shopping around for a replacement but everything I could find that fit my requirements (large amount of very fast storage) also had insane amounts of memory and compute that I didn't need or want to pay for. Really, I needed a place for lots of data to lay at rest most of the time with brief bursts of activity. It seemed bizarre that I could get that easily from most consumer equipment but not a server, so I just got some consumer equipment and walked away with a pretty good ROI. 

Now she's mounted to the wall in the closet next to a router, where she sips power most of the time. She hosts a lot of lightweight services and some very large databases which is a fun dichotomy.

| Server           | Shalash                                  |
| ---------------- | ---------------------------------------- |
| Operating System | Debian GNU/Linux 13 (trixie)             |
| Mainboard        | FW13 AMD Ryzen 7 7840U                   |
| RAM              | Corsair DDR5-5600 2x48GB                 |
| Storage          | Samsung 990 PRO 4 TB M.2 2280            |
| Case             | Cooler Master Mainboard Case             |
| Power            | Anker Prime 200W GaN USB-C               |

---

## Server: Mayalaran

[One of my projects](https://nicenumbers.net/) has an effectively unbounded appetite for raw compute power, which is bad for my wallet but good for the part of my brain that likes testing a bunch of weird computers. I keep a running spreadsheet of every computer I've been able to benchmark, from Raspberry Pis to gaming rigs to servers in Germany to supercomputer clusters, and the amount of money each cost to run. With those points I can calculate a performance-per-dollar metric which is my bottom line for "most valuable compute". 

Mayalaran is a Mac Mini that I picked up on sale to play around with and benchmark Apple hardware more generally, but the results for this project's benchmarks were amazing. Even including the purchase cost in addition to the electricity, the M4 chip is the top of my list in terms of performance per dollar. It takes about 30W at full throttle but performs on par with my desktop running at triple that. And even while the CPU is fully loaded, it can still run stuff like ollama on the GPU + integrated memory.

| Server           | Mayalaran                   |
| ---------------- | --------------------------- |
| Model            | Mac Mini M4                 |
| CPU              | M4 10-core CPU/GPU          |
| Memory           | 16 GB Unified               |
| Storage          | 256 GB SSD                  |

---

## Server: Jak & Ivory

Whenever I need a little extra compute for testing something or running a long, intensive thing I can always rely on Hetzner to have servers at suspiciously-low prices. I primarily use the CAX and CPX series (which I call Jak-series) and the CX series for smaller needs (which I call Ivory). These can get spun up in a few seconds with everything I need, connected to my internal network and ready for whatever I want to throw at it. 

| Server           | Jak-class                    |
| ---------------- | ---------------------------- |
| Provider         | Hetzner CAX & CPX Series     |
| Operating System | Debian GNU/Linux 13 (trixie) |

| Server           | Ivory-class                  |
| ---------------- | ---------------------------- |
| Provider         | Hetzner CX Series            |
| Operating System | Debian GNU/Linux 13 (trixie) |

---

## Server: Pailiah

This is my older general-purpose VPS for hosting random services and whatnot. I have like one thing left running on this server, when that's done I'll retire it for good.

| Server           | Pailiah                        |
| ---------------- | ------------------------------ |
| Provider         | OVH Dedicated KS-16            |
| Operating System | Debian GNU/Linux 12 (bookworm) |
| CPU              | Intel Xeon E3-1245v2           |
| RAM              | 32 GB 1333 MHz                 |
| Storage          | 3×2 TB HDD SATA Soft RAID1     |
