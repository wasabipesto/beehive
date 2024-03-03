# My Software

What software do I use regularly?

```js
const software = FileAttachment("software.json").json();
```

```js
for (const [key, category] of Object.entries(software)) {
    display(html`<h2>${category.name}</h2>`)
    var items_html = []
    for (const item of category.items) {
        items_html.push(html`<div class="card"><a href="${item.link}" target="_blank"><h3>${item.name}</h3>${item.description}</a></div>`)
    }
    display(html`<div class="grid grid-cols-4">${items_html}</div>`)
}
```