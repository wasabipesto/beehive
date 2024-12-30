# State of the Apps 2024

This is a list inspired by [CGP Grey's State of the Apps](https://web.archive.org/web/20240710214655/https://www.cgpgrey.com/blog/state-of-the-apps-2014), continued on the [Cortex podcast](https://cgpgrey.substack.com/p/state-of-the-apps-2025). If you're reading this around the end of 2024, these will match what's currently on my [Software](https://wasabipesto.com/software/) page, but that page will be updated over time to what I'm currently using while this one will remain static for historical interest.

# Art & Games

### Game Library: Steam

Steam is a great platform that makes playing games dead simple, even on Linux. If I buy a game, it’s on Steam. We have a Steam Deck now, and the experience is just wonderful.

### Virtual Tabletop: Foundry

Foundry is leagues better than Roll20 for D&D. It can be a little heavier, but it has way more features and has worked much smoother for me when setting up scenes. The [5e.tools](http://5e.tools) importer makes creaking new 5e characters a breeze. I’ll keep an eye on the space but I don’t see myself moving away from it anytime soon.

### Sketches: Excalidraw

This is a nice little webapp for quickly sketching things out. Comparable to sketching things on paper for me. A quick way to answer “how should this be laid out” or “what should this look like, approximately”.

### Photo Editing: GIMP

Right now this is just for bad/funny photo edits. I’m sure there are better tools in this space but I don’t use it very often and I know where enough things are that I don’t want to learn something new. If I end up doing more I should look into something easier to use.

### Generative AI: Stable Diffusion WebUI

I used the SD WebUI a while back for D&D character/location art, but haven’t used it since. I actually installed StabilityMatrix recently, but I haven’t started on the project that I’ll actually use these for yet. I imagine new apps in this realm will pop up over the next year, and I may or may not pick a few favorite by then.

### Miscellaneous:

- Inkarnate: Online map-making software for fantasy games.
- OBS Studio: Online map-making software for fantasy games.
- Piper: Configure gaming devices like my Logitech G502.

# Communication

### Primary Messaging: Beeper

It’s extremely convenient to get all of my messages in one place, on mobile or desktop. Auto-copying OTP messages is also super nice. Recently purchased by Automattic so I’m waiting on the Desktop app update. I don’t see myself changing main apps anytime soon.

### Other Messaging: Discord, Google Messages

Beeper doesn’t support all interactions yet, so sometimes you have to go to the native app to get something done. Happens more often with Discord with Nitro features.

### Email: Protonmail, SimpleLogin, Sendgrid, Thunderbird, Gmail

Okay, this will sound like a lot. Protonmail is my main inbox provider that stores everything, and I use their service SimpleLogin to create new inboxes for every account. With these two I can receive any email sent to any of my domains (or a burner domain), and respond from the same address transparently without revealing my main email address. I can then block senders, domains, or mailboxes independently.

Next, I have Sendgrid for sending automated emails. This is nice because they have an API and SMTP relays which can hook into pretty much anything for automated messages.

On desktop I use Thunderbird for viewing emails. I like having a separate application for emails so it can tile next to my other messages. On mobile I use the Protonmail app.

Finally, I still have Gmail for when I need to make sure an email gets where it needs to go (job applications, personal correspondence, etc.)

### AI: Ollama, Whisper

I don’t use these applications very often, but every now and then I need automated interaction a little bit more involved than a script and I rely on these.

### Miscellaneous:

- BuzzKill: Android notification management utilities.

# Development/Utility

### DE: GNOME, Forge

I enjoy the Gnome look and feel over KDE, though I might try out the new Plasma here soon.

I started dabbling in tiling window managers and I particularly enjoy how Forge provides a nice middleground between a traditional window manager and something fully tiling. I may dive further into sway when I try Nix again in the future.

### Desktop Terminal: Alactritty

After using the default Gnome terminal emulator for a while I tried out Alactritty and didn’t really notice a difference. I might try out Ghostty here soon, or switch back to the default.

### Mobile SSH Client:

I honestly forgot I had this installed since I haven’t used it in so long. There’s probably something that works better but this one works well enough for me.

### Shell: Fish

I haven’t customized my fish shell very much but I do really like it so far. The auto-completions are phenomenal and I love all of the little bells and whistles, plus all of the themes.

### Browser: LibreWolf

I’m not usually a privacy nut, but I was annoyed that I had to turn off the annoying Mozilla stuff (Mozilla VPN, Pocket, search suggestions, home page ads) so I switched to this. LibreWolf is a well-maintained FF fork that is clearly opinionated but works well for me. For websites where the anti-fingerprinting is too strict, I disable protections manually for that site or use a backup Firefox installation.

### IDE: Zed, Code Server

I used Code Server for several years so I could have a consistent development environment no matter where I connected from. I plan to use it at the very least for managing docker container configurations, plus for the extensions to manage databases directly or run Jupyter notebooks.

I started using Zed this year and it’s nice to be able to develop fully locally. It’s very fast and the language plugins just work. There are several improvements I’d like to see, such as better git integration and true remote development. I will also need to figure out how to actually use something like Nix shells or devshells so I can continue my streak of never installing node on an actual host.

### Containerization: Docker, Compose

I quite like using Docker for containerized applications, it runs basically everything and it’s easy to write Dockerfiles for applications that don’t come prepackaged. I looked into Podman this year, but never actually switched anything over. I also daydream about a potential future setup on Kubernetes, but that always seems like it would add more problems than it would solve.

I manage app versions and updates via pull requests to my docker compose files on GitHub issued by Renovate. It’s not perfect but it works better than `:latest`.

### I Swear I Tried It: Nix

I tried Nix this year. I have more to say about this but nothing I say will be new. I can see how it would be useful but I just haven’t gotten there yet.

### Miscellaneous:

- AppImage Launcher: Automatically manages AppImages like normal programs.
- Chezmoi: Dotfile management and sync utilites.
- Flathub: An app store for flatpak applications.
- GitHub: Source code hosting and issue tracker.
- Hishtory: Terminal history sync and search across hosts.
- Wine: Run Windows applications on linux. Not an emulator.
- Virt-Manager: Manage virtual machines on desktop.

# Home

### Calendar: Google Calendar

I use Google Calendar because it’s simple and shareable. I can see my scheduled events, meal plan, work meetings, reminders, birthdays, and anything else all in one place. I can share that with everyone else in my household and everyone sees the same thing. I’d be interested in seeing alternatives but hesitant to change.

### To-Do Lists: Google Tasks

Tasks live side by side with my calendar, and when they have due dates they live on top of it. Recurring reminders to take out the trash and do litter are always right in front of me so I never forget. When I brainstorm what stores I need to stop by this weekend, those go on a new Tasks list.

### Projects: Notion

When I get to the point I need to take notes about something, that’s typically when it goes in Notion. I love that I can have very different databases (Clippings, Projects, Software, Recommendations, Media, etc.) and just hit a button to add a new item and start typing. It’s reasonably fast for being all web-first Javascript and I can pull out anything I want from the API.

### Quick Notes: Obsidian

I love Obsidian but I think it’s on the way out for me. Really the only time I use it now is when I don’t have an internet connection at all, which is rarer and rarer. It’s still nice for notes I access often that I need to have at hand quickly.

### Search: Kagi

To be honest I’m not sure how much better Kagi is at finding exactly what I need at any moment, but it’s certainly more convenient than scrolling through all of the ads and listicles that Google gives now. Really, the “block domain” feature is enough to carry the cost of the subscription.

### Shopping/Recipes: AnyList

It doesn’t have to be this app, but I highly recommend something along these lines if you cook at all. Pick out your recipes in advance, mark off what you already have, and _then_ go to the store. Save time and money by only buying what you need. Bring back recipes you haven’t had in a while and keep your diet varied.

I like this app because it automatically categorizes the ingredients you add to your list. If you set up the order of categories the same way your store is organized, it will show you exactly what you need to be looking for next as you walk through the aisles. You can scan the barcode of anything to add it straight to the list with a photo and everything. Then you can link it to your calendar or share it with everyone else in your household.

I’ve heard of some nice self-hosted recipe apps recently and I intend to check them out, but AnyList has served me well for many years and I will be hard-pressed to give it up at this point.

### Password Manager: Bitwarden

PLEASE use a password manager. I like Bitwarden because it’s nice and convenient but anything is better than using a notebook or, god forbid, the same password for everything.

I know that having TOTP codes in the same place as my passwords is not technically great, but if anyone gets my vault I’m fucked anyways.

### Documents: Notion

I use Google Docs a little, but for most word processing I’m using Notion nowadays. For instance, I’m typing this blog post in Notion, I do my D&D character sheets in Notion, I draft some emails in Notion. If I need to do advanced typesetting, I’d probably use Typst or Overleaf.

### Spreadsheets: Google Sheets

I think in spreadsheets and I need someplace where I can get to them quickly and do absolutely everything imaginable with them. Google Sheets is simply the easiest way to do that. I use it for everything from budgeting to vehicle mileage to Factorio ratio calculators.

### File Management: Nextcloud, Syncthing

You have files on one computer and you want them to be on another. If you own both, set up Syncthing. You can make them sync, or push from one to the other. If you want to send or receive files with other people, set up Nextcloud. I know Nextcloud does a ton more, but that's really all I use it for right now.

### Home Automation: Home Assistant

If you own a home, you'll probably want Home Assistant. It runs light bulbs, switches, thermostats, cameras, energy monitoring, routines, notifications, anything you can think of. Just make sure the devices you buy can play nice, and Home Assistant will make them do exactly what you want.

# Media

### eBooks: Calibre, Calibre-Web, Kindle, Moon+ Reader

Calibre seems like a software relic now but I haven't found anything better. I do love the way Calibre-Web can just shoot ebooks straight to Kindle devices (and apps) but I might move away from Kindle entirely soon.

I recently installed the Moon+ Reader, which has worked well so far to just read epub files on my phone storage. I might transition to just using that or a similar app, and syncing books manually.

### Photos: Google Photos, Ente Photos

So I'm a little locked into Google Photos, and I'm trying to find a good alternative. I really like Ente Photos, and I've loaded in some photos to test it out, but most of the times I go to look for something the natural search just doesn't find it. If none of the other apps can nail search, I'll have to stay on Google Photos.

I still back up my photos elsewhere, just in case my Google account gets nuked, but they're not particularly accessible without a good app.

### Videos: YouTube, FreeTube

I use YouTube and FreeTube for random short videos, usually less than 20 minutes each, to watch occasionally while I eat lunch. I tend to stick to FT, which will just show me videos from my subscribed channels, and only venture to the YT feed when I specifically want to get shown random stuff from across the platform.

### RSS Feeds: FreshRSS & Capy Reader

RSS feeds are a godsend in the modern algorithm-heavy world. You only see exactly what you subscribe to and nothing more.

FreshRSS is has a nice Web UI but it's also an excellent server to sync your subscriptions and read status. I discovered Capy Reader this year, which dethroned FocusReader as my Android reader of choice. I don't like that Capy marks items as read automatically but I do love the “load full content” button that just grabs the full article instead of just using the summary given in the feed itself.

### Video Streaming & Sharing: Plex

Plex is king.

### Music Streaming: Spotify

Often I just want to hit play and have some background music, hear some new artists, or just throw every song I like into a bowl and play at random. I don’t have time to manage music on top of everything else, so I let Spotify do it.

### Miscellaneous:

- Smarter Playlists: Algorithmic playlist manipulation for Spotify.
- SomaFM: Electronic internet radio.

# Media Processing

### Requests: Overseerr

It took a while for someone to make a request program that I felt comfortable unleashing on my family. With this they just log in with their Plex account, they can see what’s already available and what’s already requested, submit their requests, and have it go directly to me to approve. I set up a weekly request limit so people don’t get too crazy but so far nobody’s hit it. 95%+ of requests get downloaded and imported immediately after I approve them, and the remainder are weird edge cases I’d have to manually pick out anyways.

Development has pretty much stopped on this but I still plan on using it until it breaks. Hopefully someone picks it up and starts maintaining a fork before then.

### Media Ingest: Prowlarr, Sonarr, Radarr, Readarr

I’ve reduced the number of hours I spend managing media immensely since installing these. No complaints.

### BitTorrent: rTorrent, ruTorrent

I’ve used this combo for a decade, it’s the de facto standard by this point. I use a docker container provided by crazy-max which makes it easy to set up, and all of the -arr programs hook directly into it for auto-add and auto-labeling.

### Social Archiving: Gallery-DL, YouTube-DL

These apps are invaluable for getting content out of walled gardens. I can save stuff to watch later, remix and edit, or just have on my hard drive for later.

# Monitoring

My monitoring setup is pretty standard. Aside from adding more exporters, I don’t have plans to change anything here.

### Scrapers:

- Node-Exporter: Export prometheus stats for host machines.
- cAdvisor: Export prometheus stats for docker containers.

### Visualization:

- Prometheus: Scrape endpoints and save it for monitoring or alerts.
- Loki: Like Prometheus but for log storage and metrics.
- Grafana: Visualize internal metrics and alerts.

### Status Page:

- Uptime Kuma: Monitor web services and machines from afar.

### Miscellaneous:

- NUT: Monitor your power supply and shut down if required.

# Networking

### Backups: Restic, Backblaze

I use a set of simple scripts to make backups on every machine every day with Restic. These are deduplicated, encrypted, and shipped off to Backblaze B2 for storage.

### DNS Nameserver: Cloudflare

I have all of my domains set up through Cloudflare for DNS. Running through Cloudlare’s edge sets up HTTPS automatically, runs through any redirects or page rules I set up, and serves from a cache if possible. A no-brainer to reduce server load.

### Ingress Tunnel: Cloudflare

All of those DNS entries are CNAME’d to a tunnel, which pipes data directly into the correct machine. With a tunnel I don’t need to have public IP’s in my DNS and can even close those ports to avoid any unintended access.

At this level I also use Cloudflare Access to protect non-public sites, which I can optionally set up to be shared with a few other users. Once a request makes it to the server, the Cloudflare daemon will automatically reverse-proxy it to the correct service.

### VPN: Tailscale

I love that Tailscale makes setting up a VPN foolproof. I can just have all of my machines connect to each other without fiddling with Wireguard, going over the public internet, or anything else. It also has a few nice bells and whistles that I’ve come to enjoy.

### DNS Resolver: NextDNS, Pi-Hole

This is one of the Tailscale features I like, which is the ability to redirect all DNS queries to a custom resolver. NextDNS integrates nicely and basically replaced my Pi-Hole for all of my connected devices.

For devices I don’t have on Tailscale, like our TV, Pi-Hole still catches plenty of ads.

### Miscellaneous:

- EndleSSH: Tarpit for inbound SSH connections.
- nginx: The king of web servers.
