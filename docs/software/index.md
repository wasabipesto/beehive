# My Software

What software do I use regularly?

```js
const software = FileAttachment("software.json").json();
```

```js
for (const cat of software) {
    display(html`<h2>${cat.category_name}</h2>`)
    var items_html = []
    for (const item of cat.items) {
        if (item.link == null) {
            items_html.push(html`<div class="card"><h3>${item.emoji} ${item.name}</h3>${item.description}</div>`)
        } else {
            items_html.push(html`<div class="card"><a href="${item.link}" target="_blank"><h3>${item.emoji} ${item.name}</h3>${item.description}</a></div>`)
        }
    }
    display(html`<div class="grid grid-cols-4">${items_html}</div>`)
}
```