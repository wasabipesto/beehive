---
toc: true
---

<style>
h1.hero {
  margin: 2rem 0;
  font-size: 3rem;
  background: linear-gradient(30deg, var(--theme-foreground-focus), currentColor);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

.card {
  margin: 0;
}
.gallery img {
  max-width: 100%;
  border-radius: 8px;
  box-shadow: 0 0 0 0.75px rgba(128, 128, 128, 0.2), 0 6px 12px 0 rgba(0, 0, 0, 0.2);
  aspect-ratio: 2500 / 1900;
}
.webrings table {
  font: 14px var(--sans-serif);
  margin: 0;
}
.webrings td {
  padding: 0.5rem;
}
div.appliance {
  display: flex;
  align-items: center;
  justify-content: center;
}
</style>

<h1 class="hero">Hello, I'm wasabipesto.</h1>

I'm an engineer and also a human person.

## About me

I work in building construction as a controls engineer and project manager. I'm interested in thermodynamics, air quality, and building comfort in commercial and industrial settings.

I fiddle with computers, like the one serving you this webpage. I usually build things in python or rust and deploy them in docker. I believe in simplicity, and I believe in interpreting that term liberally.

I run a few tabletop games for my friends and family. I enjoy systems focusing on collaborative worldbuilding, genre-bending narratives, and interesting characters.

I believe in quantifying things when it's possible and helpful. I believe in trying and failing and learning.

---

## My projects

```js
const projects = FileAttachment("homepage/projects.json").json();
```

```js
var items_html = []
for (const item of projects) {
    items_html.push(
      html`
        <div class="card gallery">
          <a href="${item.link}" target="_blank">
            <h3>${item.name}</h3>
            <div>${item.description}</div>
            <p><img src="_file/assets/projects/${item.image}" /></p>
          </a>
        </div>`
    )
}
display(html`<div class="grid grid-cols-3">${items_html}</div>`)
```

---

## Webrings

<div class="webrings grid grid-cols-4">
  <div class="card grid-rowspan-2 appliance">
    <a href="https://applianceri.ng/next?host=wasabipesto.com" target="_blank">
      <img src="assets/classe-nBoPjadlesc.png" width="200px">
    </a>
  </div>
  <div class="card">
    <h3>Webring: <a href="https://fediring.net/">Fediring</a></h3>
    <table>
      <td><a href="https://fediring.net/previous?host=wasabipesto.com">Previous Entry</a></td>
      <td style="text-align: right;"><a href="https://fediring.net/next?host=wasabipesto.com">Next Entry</a></td>
    </table>
  </div>
  <div class="card">
    <h3>Webring: <a href="https://hotlinewebring.club/">Hotline Webring</a></h3>
    <table>
      <td><a href="https://hotlinewebring.club/wasabipesto/previous">Previous Entry</a></td>
      <td style="text-align: right;"><a href="https://hotlinewebring.club/wasabipesto/next">Next Entry</a></td>
    </table>
  </div>
  <div class="card">
    <h3>Webring: <a href="https://webring.bucketfish.me/">Bucket Webring</a></h3>
    <table>
      <td><a href="https://webring.bucketfish.me/redirect.html?to=prev&name=wasabipesto">Previous Entry</a></td>
      <td style="text-align: right;"><a href="https://webring.bucketfish.me/redirect.html?to=next&name=wasabipesto">Next Entry</a></td>
    </table>
  </div>
</div>

---

<table>
  <thead>
    <th><a href="https://wasabipesto.tumblr.com">tumblr</a></th>
    <th><a href="https://github.com/wasabipesto">github</a></th>
    <th><a href="https://api.github.com/users/wasabipesto/keys">ssh</a></th>
    <th><a href="https://api.github.com/users/wasabipesto/gpg_keys">gpg</a></th>
    <th><a href="https://creativecommons.org/licenses/by-nc-sa/4.0/">copyright</a></th>
    <th><a href="https://status.wasabipesto.com/">status</a></th>
  </thead>
</table>