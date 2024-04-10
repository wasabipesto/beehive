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
    if (['Album', 'Book', 'Game', 'Other'].includes(item.type) && item.artist) {
      items_html.push(html.fragment`
        <div class="card"><h3 style="color: var(--theme-foreground)">${item.title}, ${item.artist}</h3></div>
      `)
    } else {
      items_html.push(html.fragment`
        <div class="card"><h3 style="color: var(--theme-foreground)">${item.title}</h3></div>
      `)
    }
  }
  display(html`<div class="grid grid-cols-4">${items_html}</div>`)
}
```
