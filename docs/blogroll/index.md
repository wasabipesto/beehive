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

    const homepage_link = html.fragment`<tr><td width="80px">Homepage</td><td>${
      item.site_url
        ? html.fragment`<a href="${item.site_url}" target="_blank">${item.site_url}</a>`
        : 'Link Unavailable'
    }</td></tr>`

    const rss_feed_link = html.fragment`<tr><td width="80px">RSS Feed</td><td>${
      item.url
        ? html.fragment`<a href="${item.url}" target="_blank">${item.url}</a>`
        : 'Link Unavailable'
    }</td></tr>`

    items_html.push(html.fragment`
      <div class="card">
        ${header}
        <table style="margin: 0.5rem 0 0; max-width: 100%;">
          ${homepage_link}
          ${rss_feed_link}
        </table>
      </div>
    `)
  }
  display(html`<div class="grid grid-cols-3">${items_html}</div>`)
}
```
