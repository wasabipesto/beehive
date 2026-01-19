# State of the Apps 2025

This is a list inspired by [CGP Grey's State of the Apps](https://web.archive.org/web/20240710214655/https://www.cgpgrey.com/blog/state-of-the-apps-2014). 

If you're reading this around the end of 2025, these will match what's currently on my [Software](https://wasabipesto.com/software/) page, but that page will be updated over time to reflect what I'm currently using while this one will remain static for historical interest. I've noted the items that stayed the same from [2024](/sota-2024/) and added descriptions when something has changed.

# Art & Games

- Game Library: [Steam](https://store.steampowered.com/)
- Virtual Tabletop: [Foundry](https://foundryvtt.com/)
- Sketches: [Excalidraw](https://excalidraw.com/)
- Photo Editing: [GIMP](https://gitlab.gnome.org/GNOME/gimp)
- 2D Art: [Krita](https://krita.org/en/)
- 3D Art: [Blender](https://www.blender.org)
- Other:
    - [OBS Studio](https://github.com/obsproject/obs-studio)
    - [Piper](https://github.com/libratbag/piper)

### Updates

I removed Stable Diffusion WebUI this year, mainly because I just never used it. I have ideas for things I want to do in that space, but I'm sure by then there will be fourteen new tools to pick from. I also removed Inkarnate, because we weren't using it enough to justify their prices. If you have any good alternatives for large fantasy maps, please let me know.

I also started learning Krita and Blender, in the very early stages. So far I like Blender quite a bit, especially the node workflows, but there are still quite a few things that are foreign to me. I'm sure I'll pick up on it eventually, as long as I keep toying with it.

# Communication

- Primary Messaging: [Beeper](https://www.beeper.com/)
- Other Messaging: [Discord](https://discord.com/), Google Messages
- Email: [Protonmail](https://proton.me/), [SimpleLogin](https://simplelogin.io/), [Mailgun](https://mailgun.com), [Thunderbird](https://www.thunderbird.net/en-US/), [Gmail](https://mail.google.com/)
- AI: [Ollama](https://github.com/ollama/ollama), [Whisper](https://github.com/openai/whisper)

### Updates

This year Sendgrid [removed their free plan](https://www.twilio.com/en-us/changelog/sendgrid-free-plan), which I was using for email notifications. I was totally okay with paying around $5 for 100 emails/month but most plans were about 100 times that volume, minimum. Thankfully there were some free plans that had good support and decent daily limits, like Mailgun.

I'm still using Thunderbird on my desktop, which I like because I don't have notifications for it enabled anywhere. This allows me to check it while I'm already at my desk and respond on my own time. Unfortunately, Thunderbird lacks some configuration options I want, lags often, and struggles to search my mailbox or even send emails sometimes. I'd love a better desktop email client but for now I just use the Protonmail webapp for most things.

# Development/Utility

- DE: [GNOME](https://gitlab.gnome.org/GNOME), [Forge](https://github.com/forge-ext/forge)
- Desktop Terminal: [Alacritty](https://github.com/alacritty/alacritty)
- Mobile SSH Client: [JuiceSSH](https://juicessh.com/)
- Shell: [Fish](https://github.com/fish-shell/fish-shell)
- Browser: [LibreWolf](https://codeberg.org/librewolf)
- IDE: [Zed](https://zed.dev/)
- Containerization: [Docker](https://docs.docker.com/manuals/), [Compose](https://docs.docker.com/compose/), [Apptainer](https://github.com/apptainer/apptainer)
- Code Forge: [GitHub](https://github.com/)
- Languages:
    - [cargo](https://github.com/rust-lang/cargo)
    - [uv](https://github.com/astral-sh/uv)
- Other:
    - [AppImage Launcher](https://github.com/TheAssassin/AppImageLauncher)
    - [Chezmoi](https://github.com/twpayne/chezmoi)
    - [Flathub](https://flathub.org)
    - [Hishtory](https://github.com/ddworken/hishtory)
    - [OpenSCAD](https://github.com/openscad/openscad/)
    - [Virt-Manager](https://github.com/virt-manager/virt-manager)
    - [Wine](https://gitlab.winehq.org/wine/wine)
    - [Waydroid](https://github.com/waydroid/waydroid)

### Updates

This year we removed Code Server when Zed [gained support for remote development](https://zed.dev/docs/remote-development). Previously I had been using it to edit config files and remotely manage some deployments, but now I can do all of that in Zed without having to manage all the crust of VS Code.

I started using uv for Python, which I recommend heavily. It makes it so easy to set up virtual environments, manage dependencies, and even make little self-contained scripts. It's also super fast.

I was also introduced to Apptainer this year, which is like docker for research computing. You can even feed it docker images which is way easier than trying to manage whatever software is installed on the compute node. It has a lot of quirks but is actually well thought-out and very easy to use.

Finally, I tried out Waydroid for an experiment. It seems like a very convenient tool to have in my back pocket.

# Home

- Calendar: [Google Calendar](https://calendar.google.com/calendar)
- To-Do Lists: [Google Tasks](https://tasks.google.com/)
- Projects: [Notion](https://www.notion.so/)
- Quick Notes: [Obsidian](https://obsidian.md/), [rnote](https://github.com/flxzt/rnote)
- Search: [Kagi](https://kagi.com/)
- Shopping/Recipes: [AnyList](https://www.anylist.com/)
- Password Manager: [Bitwarden](https://bitwarden.com/)
- Documents: [Notion](https://www.notion.so/)
- Spreadsheets: [Google Sheets](https://sheets.google.com/)
- File Management: [Nextcloud](https://github.com/nextcloud/server), [Syncthing](https://github.com/syncthing/syncthing)
- Home Automation: [Home Assistant](https://github.com/home-assistant/core)

### Updates

I got a [laptop with a touchscreen](https://frame.work/laptop12) this year, and had to test every note-taking app ever to see which one I liked best. I really enjoyed using the stylus with my old work iPad, so I really wanted something that could replicate that feeling. I ended up settling on rnote, an infinite canvas app that handles both drawings and diagrams well. It's not perfect, but it's the one that meshed the best with how I wanted it look and feel.

# Media

- eBooks: [Calibre](https://github.com/kovidgoyal/calibre), [Calibre-Web](https://github.com/janeczku/calibre-web), [ReadEra](https://readera.org/)
- Photos: [Ente Photos](https://ente.io/)
- Videos: [YouTube](https://youtube.com), [FreeTube](https://github.com/FreeTubeApp/FreeTube)
- RSS Feeds: [FreshRSS](https://github.com/FreshRSS/FreshRSS) & [Capy Reader](https://github.com/jocmp/capyreader)
- Video Streaming & Sharing: [Plex](https://www.plex.tv/)
- Music Streaming: [Spotify](https://spotify.com/)
- Podcasts: [Spotify](https://spotify.com/), [AntennaPod](https://github.com/AntennaPod/AntennaPod)
- Other:
    - [Smarter Playlists](http://playlistmachinery.com/)
    - [SomaFM](https://somafm.com/)
    - [Czkawka](https://github.com/qarmin/czkawka)

### Updates

I started using ReadEra this year, which has been exactly what I wanted in an eBook reader. I like the layout and formatting options better than Moon Reader, and it can open basically anything with zero fuss, unlike Kindle. Over time I can just accumulate books on my "to-read" shelf, then when I want something new I just go grab one at random.

I also started using AntennaPod for podcasts that only distribute over RSS. Since Spotify doesn't support those, I had to add them to AntennaPod. I don't like that there's no easy way to sync progress between devices, so I'll continue using Spotify where I can.

I was also able to fully migrate over to Ente this year. I love that Ente is always adding new features (OCR, public links, custom domains, map timelines) while still supporting the "boring" stuff like self-hosting and CLI export.

# Media Processing

- Requests: [Overseerr](https://github.com/sct/overseerr)
- Media Ingest: [Prowlarr](https://github.com/Prowlarr/Prowlarr), [Sonarr](https://github.com/Sonarr/Sonarr), and [Radarr](https://github.com/Radarr/Radarr)
- BitTorrent: [rTorrent](https://github.com/rakshasa/rtorrent), [ruTorrent](https://github.com/Novik/ruTorrent)
- Social Archiving: [Gallery-DL](https://github.com/mikf/gallery-dl), [YouTube-DL](https://github.com/yt-dlp/yt-dlp)

### Updates

In addition to other sources, I highly recommend Anna’s Archive for finding eBooks.

# Monitoring

- Scrapers: [Node-Exporter](https://github.com/prometheus/node_exporter), [cAdvisor](https://github.com/google/cadvisor)
- Time-Series Database: [Prometheus](https://github.com/prometheus/prometheus)
- Visualization: [Grafana](https://github.com/grafana/grafana)
- Status Page: [Uptime Kuma](https://github.com/louislam/uptime-kuma)
- Other:
    - [NUT](https://github.com/networkupstools/nut)

### Updates

I recently migrated my monitoring setup to a new server. I was going to take the opportunity to modernize it, but I haven't gotten around to it yet. So currently I am logless, but I expect to be using Loki and maybe Alloy again in the next few months.

# Networking

- Backups: [Restic](https://github.com/restic/restic), [Backblaze](https://backblaze.com)
- DNS Nameserver: [Cloudflare](https://developers.cloudflare.com/dns/)
- Ingress Tunnel: [Cloudflare](https://developers.cloudflare.com/cloudflare-one/networks/connectors/cloudflare-tunnel/)
- VPN: [Tailscale](https://github.com/tailscale/tailscale)
- DNS Resolver: [NextDNS](https://nextdns.io/), [Pi-Hole](https://github.com/pi-hole/pi-hole)
- Web Server: [nginx](https://nginx.org/)
- Other:
    - [EndleSSH](https://github.com/shizunge/endlessh-go)

### Updates

No changes here! I like to keep networking simple and boring, so fewer changes make me happy.
