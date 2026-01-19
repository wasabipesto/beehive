# State of the Apps 2025

This is a list inspired by [CGP Grey's State of the Apps](https://web.archive.org/web/20240710214655/https://www.cgpgrey.com/blog/state-of-the-apps-2014). 

If you're reading this around the end of 2025, these will match what's currently on my [Software](https://wasabipesto.com/software/) page, but that page will be updated over time to reflect what I'm currently using while this one will remain static for historical interest. I've noted the items that stayed the same from [2024](/sota-2024/) and added descriptions when something has changed.

# Art & Games

- Game Library: Steam
- Virtual Tabletop: Foundry
- Sketches: Excalidraw
- Photo Editing: GIMP
- 2D Art: Krita
- 3D Art: Blender

### Updates

I removed Stable Diffusion WebUI this year, mainly because I just never used it. I have ideas for things I want to do in that space, but I'm sure by then there will be fourteen new tools to pick from. I also removed Inkarnate, because we weren't using it enough to justify their prices. If you have any good alternatives for large fantasy maps, please let me know.

I also started learning Krita and Blender, in the very early stages. So far I like Blender quite a bit, especially the node workflows, but there are still quite a few things that are foreign to me. I'm sure I'll pick up on it eventually, as long as I keep toying with it.

# Communication

- Primary Messaging: Beeper
- Other Messaging: Discord, Google Messages
- Email: Protonmail, SimpleLogin, Mailgun, Thunderbird, Gmail
- AI: Ollama, Whisper

### Updates

This year Sendgrid [removed their free plan](https://www.twilio.com/en-us/changelog/sendgrid-free-plan), which I was using for email notifications. I was totally okay with paying around $5 for 100 emails/month but most plans were about 100 times that volume, minimum. Thankfully there were some free plans that had good support and decent daily limits, like Mailgun.

I'm still using Thunderbird on my desktop, which I like because I don't have notifications for it enabled anywhere. This allows me to check it while I'm already at my desk and respond on my own time. Unfortunately, Thunderbird lacks some configuration options I want, lags often, and struggles to search my mailbox or even send emails sometimes. I'd love a better desktop email client but for now I just use the Protonmail webapp for most things.

# Development/Utility

- DE: GNOME, Forge
- Desktop Terminal: Alacritty
- Mobile SSH Client: JuiceSSH
- Shell: Fish
- Browser: LibreWolf
- IDE: Zed
- Containerization: Docker, Compose, Apptainer
- Code Forge: GitHub
- Languages:
    - cargo
    - uv
- Other:
    - AppImage Launcher
    - Chezmoi
    - Flathub
    - Hishtory
    - Virt-Manager
    - Wine
    - Waydroid

### Updates

This year we removed Code Server when Zed [gained support for remote development](https://zed.dev/docs/remote-development). Previously I had been using it to edit config files and remotely manage some deployments, but now I can do all of that in Zed without having to manage all the crust of VS Code.

I started using uv for Python, which I recommend heavily. It makes it so easy to set up virtual environments, manage dependencies, and even make little self-contained scripts. It's also super fast.

I was also introduced to Apptainer this year, which is like docker for research computing. You can even feed it docker images which is way easier than trying to manage whatever software is installed on the compute node. It has a lot of quirks but is actually well thought-out and very easy to use.

Finally, I tried out Waydroid for an experiment. It seems like a very convenient tool to have in my back pocket.

# Home

- Calendar: Google Calendar
- To-Do Lists: Google Tasks
- Projects: Notion
- Quick Notes: Obsidian, rnote
- Search: Kagi
- Shopping/Recipes: AnyList
- Password Manager: Bitwarden
- Documents: Notion
- Spreadsheets: Google Sheets
- File Management: Nextcloud, Syncthing
- Home Automation: Home Assistant

### Updates

I got a [laptop with a touchscreen](https://frame.work/laptop12) this year, and had to test every note-taking app ever to see which one I liked best. I really enjoyed using the stylus with my old work iPad, so I really wanted something that could replicate that feeling. I ended up settling on rnote, an infinite canvas app that handles both drawings and diagrams well. It's not perfect, but it's the one that meshed the best with how I wanted it look and feel.

# Media

- eBooks: Calibre, Calibre-Web, ReadEra
- Photos: Ente Photos
- Videos: YouTube, FreeTube
- RSS Feeds: FreshRSS & Capy Reader
- Video Streaming & Sharing: Plex
- Music Streaming: Spotify
- Podcasts: Spotify, AntennaPod
- Other:
    - Smarter Playlists
    - SomaFM

### Updates

I started using ReadEra this year, which has been exactly what I wanted in an eBook reader. I like the layout and formatting options better than Moon Reader, and it can open basically anything with zero fuss, unlike Kindle. Over time I can just accumulate books on my "to-read" shelf, then when I want something new I just go grab one at random.

I also started using AntennaPod for podcasts that only distribute over RSS. Since Spotify doesn't support those, I had to add them to AntennaPod. I don't like that there's no easy way to sync progress between devices, so I'll continue using Spotify where I can.

I was also able to fully migrate over to Ente this year. I love that Ente is always adding new features (OCR, public links, custom domains, map timelines) while still supporting the "boring" stuff like self-hosting and CLI export.

# Media Processing

- Requests: Overseerr
- Media Ingest: Prowlarr, Sonarr, Radarr, Readarr
- BitTorrent: rTorrent, ruTorrent
- Social Archiving: Gallery-DL, YouTube-DL

### Updates

In addition to other sources, I highly recommend Anna’s Archive for finding eBooks.

# Monitoring

- Scrapers:Node-Exporter, cAdvisor
- Time-Series Database: Prometheus
- Visualization: Grafana
- Status Page: Uptime Kuma
- Other:
    - NUT

### Updates

I recently migrated my monitoring setup to a new server. I was going to take the opportunity to modernize it, but I haven't gotten around to it yet. So currently I am logless, but I expect to be using Loki and maybe Alloy again in the next few months.

# Networking

- Backups: Restic, Backblaze
- DNS Nameserver: Cloudflare
- Ingress Tunnel: Cloudflare
- VPN: Tailscale
- DNS Resolver: NextDNS, Pi-Hole
- Other:
    - EndleSSH
    - nginx

### Updates

No changes here! I like to keep networking simple and boring, so fewer changes make me happy.
