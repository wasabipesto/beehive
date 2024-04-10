<style>
td {
    width: 50%
}
</style>

# My Hardware

These are the machines and other hardware I use regularly.

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

## Server: Pailiah

This is my general-purpose VPS for hosting random services and whatnot. It's serving you this webpage unless you hit Cloudflare's cache.

| Attribute        | Value                      |
| ---------------- | -------------------------- |
| Provider         | OVH Dedicated KS-16        |
| Operating System | Debian GNU/Linux 12        |
| CPU              | Intel Xeon E3-1245v2       |
| RAM              | 32 GB 1333 MHz             |
| Storage          | 3×2 TB HDD SATA Soft RAID1 |

## Phone: Leandros

The little box glued to my side. I use it for communication, photography, note-taking, reading, and a little social media. I purposefully don't have any games on my phone.

| Attribute        | Value                |
| ---------------- | -------------------- |
| Model            | Google Pixel 8, 2023 |
| Operating System | Android 14           |
| Launcher         | Niagara              |
| CPU              | Google Tensor G3     |
| Case             | dbrand Grip          |

I prefer smaller phones, anything over about 6" is too large to fit in my hand comfortably.

```js
const phone_sizes = FileAttachment('phone_sizes.json').json()
```

```js
Plot.plot({
  caption: "A plot of my phone's screen sizes over time.",
  height: 150,
  x: { type: 'utc', label: 'Date Purchased' },
  y: { grid: true, domain: [3, 7], label: 'Screen Size (in)' },
  marks: [
    Plot.dot(phone_sizes, {
      x: 'date',
      y: 'screen_size_in',
      channels: { Name: 'name' },
      tip: true
    })
  ]
})
```
