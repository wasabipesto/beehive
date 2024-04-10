# Favorite Media

What media do I recommend? While I don't like to give unilateral recommendations, I can list some of my favorite pieces of media.

This page is generated from my database of media ratings from [Notion](https://wasabipesto.com/notion). It was last updated on ${new Date(FileAttachment('media.json').lastModified).toLocaleDateString('en-US', { month: 'long', day: 'numeric', year: 'numeric' })}.

```js
const media = FileAttachment('media.json').json()
```

```js
for (const cat of media) {
  display(html`<h2>${cat.category_name}</h2>`)
  var items_html = []
  for (const item of cat.items) {
    var full_title = html.fragment`${item.title}`
    if (item.media_link) {
      full_title = html.fragment`<a href="${item.media_link}" target="_blank">${item.title}</a>`
    }
    if (item.artist) {
      full_title = html.fragment`${full_title}<br /><span style="color: var(--theme-foreground-muted)">${item.artist}</span>`
    }

    var cover_image = html.fragment``
    if (item.image_link) {
      cover_image = html.fragment`<img src="${item.image_link}" width="80" style="margin: 0 0.5rem;">`
    }
    items_html.push(html.fragment`
      <div class="card"><table style="margin: 0"><td>${cover_image}</td><td width="99%">${full_title}</td></div>
    `)
  }
  display(html`<div class="grid grid-cols-4">${items_html}</div>`)
}
```
