# My Software

What software do I use regularly? These are the programs and apps I use, though of course my needs are going to be different from yours.

This page is generated from my software notes in [Notion](https://wasabipesto.com/notion). It was last updated on ${new Date(FileAttachment('software.json').lastModified).toLocaleDateString('en-US', { month: 'long', day: 'numeric', year: 'numeric' })}.

```js
const software = FileAttachment('software.json').json()
```

```js
for (const cat of software) {
  display(html`<h2>${cat.category_name}</h2>`)
  var items_html = []
  for (const item of cat.items) {
    if (item.link == null) {
      items_html.push(html.fragment`
        <div class="card"><h3 style="color: var(--theme-foreground)">${item.emoji} ${item.name}</h3>${item.description}</div>
      `)
    } else {
      items_html.push(html.fragment`
        <div class="card"><a href="${item.link}" target="_blank"><h3 style="color: var(--theme-foreground)">${item.emoji} ${item.name}</h3>${item.description}</a></div>
      `)
    }
  }
  display(html`<div class="grid grid-cols-3">${items_html}</div>`)
}
```
