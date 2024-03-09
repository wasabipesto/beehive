# My Blogroll

I use RSS for most of my news and light reading since it brings me stories and posts directly from people I care about. I don't have to worry about getting sucked into endless scrolling but there's always plenty of interesting things to read.

Here is a list of all of the feeds registered in FreshRSS, my feed server.

```js
const blogroll = FileAttachment('blogroll.json').json()
```

```js
for (const grp of blogroll) {
  display(html`<h2>${grp.group.title}</h2>`)
  var items_html = []
  for (const item of grp.feeds) {
    const header = html.fragment`<h3><img src="data:${item.favicon}" width="12px" style="margin: 0 0.5rem;" />${item.title}</h3>`

    const last_updated = html.fragment`<tr><td width="90px">Last Updated</td><td>${item.last_updated}</td></tr>`

    const update_frequency = html.fragment`
      <tr><td>Frequency</td><td>${item.items_per_week_avg} per week</td></tr>`

    const update_schedule = html.fragment`
      <tr><td>Schedule</td><td>${Plot.lineY(item.items_per_week).plot({
        axis: null,
        width: 160,
        height: 12
      })}</td></tr>`

    const homepage_link = html.fragment`<tr><td>Homepage</td><td>${
      item.site_url
        ? html.fragment`<a href="${item.site_url}" target="_blank">${item.site_url}</a>`
        : 'Link Unavailable'
    }</td></tr>`

    const rss_feed_link = html.fragment`<tr><td>RSS Feed</td><td>${
      item.url
        ? html.fragment`<a href="${item.url}" target="_blank">${item.url}</a>`
        : 'Link Unavailable'
    }</td></tr>`

    items_html.push(html.fragment`
      <div class="card">
        ${header}
        <table style="margin: 0.5rem 0 0; max-width: 100%;">
          ${last_updated}
          ${update_frequency}
          ${update_schedule}
          ${homepage_link}
          ${rss_feed_link}
        </table>
      </div>
    `)
  }
  display(html`<div class="grid grid-cols-3" style="grid-auto-rows: auto;">${items_html}</div>`)
}
```
