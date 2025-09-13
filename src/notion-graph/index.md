# My Notion Graph

One of the party members in my main D&D group finally downloaded Obsidian and has started converting his hellish notes doc into Actual Proper Markdown With Frontmatter in order to get the nice links and graphs. And since I'm infinitely jealous I wanted to make my D&D notes, which live in Notion, into their own little knowledge graph.

Surely someone has a little plug-in for this, I foolishly thought. There are a few apps that claim to do this but I couldn't get any of them to work in the few minutes I was willing to spend. Instead, I vibed up a "download all Notion pages and throw then into a network" script to do something similar enough.

# Interactive

Throwing everything into D3, we get a nice simulated network plot. There's a couple thousand nodes, so I disabled simulation by default. Hit Play to watch it go.

```js
const data = FileAttachment("graph_data.json").json();
```

```js
const playPauseButton = view(Inputs.button("▶️ Start/Stop Simulation"));
```

```js
const resetButton = view(Inputs.button("🔄 Reset Positions"));
```

```js
const linkStrengthSlider = view(Inputs.range([0, 2], {
  label: "Link Strength",
  step: 0.1,
  value: 1
}));
```

```js
const chargeStrengthSlider = view(Inputs.range([-10, 0], {
  label: "Charge Strength",
  step: 0.5,
  value: -0.5
}));
```

```js
const centerStrengthSlider = view(Inputs.range([0, 1], {
  label: "Center Force",
  step: 0.1,
  value: 0.1
}));
```

```js
const width = 1000;
const height = 640;
const color = d3.scaleOrdinal(d3.schemeObservable10);

// Copy the data to protect against mutation by d3.forceSimulation.
const links = data.links.map((d) => Object.create(d));
const nodes = data.nodes.map((d) => Object.create(d));

// Store initial positions for reset
const initialNodes = data.nodes.map((d) => ({
  ...d,
  x: Math.random() * width,
  y: Math.random() * height
}));

const simulation = d3.forceSimulation(nodes)
    .force("link", d3.forceLink(links).id((d) => d.id).distance(10))
    .force("charge", d3.forceManyBody().strength(-0.5))
    .force("center", d3.forceCenter(width / 2, height / 2).strength(0.1))
    .on("tick", ticked)
    .stop();

const svg = d3.create("svg")
    .attr("width", width)
    .attr("height", height)
    .attr("viewBox", [0, 0, width, height])
    .attr("style", "max-width: 100%; height: auto;");

const link = svg.append("g")
    .attr("stroke", "var(--theme-foreground-faint)")
    .attr("stroke-opacity", 0.6)
    .selectAll("line")
    .data(links)
    .join("line")
    .attr("stroke-width", (d) => Math.sqrt(d.value));

const node = svg.append("g")
    .attr("stroke", "var(--theme-background)")
    .attr("stroke-width", 1)
    .selectAll("circle")
    .data(nodes)
    .join("circle")
    .attr("r", (d) => Math.max(Math.sqrt(d.word_count / 100), 3))
    .attr("fill", (d) => color(d.color))
    .style("cursor", "pointer");

const labels = svg.append("g")
    .selectAll("text")
    .data(nodes)
    .join("text")
    .text((d) => d.title)
    .attr("font-size", "12px")
    .attr("text-anchor", "left")
    .attr("fill", "var(--theme-foreground)")
    .attr("dx", "2em")
    .attr("dy", "0.35em");

function ticked() {
    link
        .attr("x1", (d) => d.source.x)
        .attr("y1", (d) => d.source.y)
        .attr("x2", (d) => d.target.x)
        .attr("y2", (d) => d.target.y);

    node
        .attr("cx", (d) => d.x)
        .attr("cy", (d) => d.y);

    labels
        .attr("x", (d) => d.x)
        .attr("y", (d) => d.y);
}

display(svg.node());
```

```js
// Setup drag behavior - separate from main cell to avoid re-execution
const dragBehavior = d3.drag()
    .on("start", function(event, d) {
        if (!event.active) simulation.alphaTarget(0.3).restart();
        d.fx = d.x;
        d.fy = d.y;
    })
    .on("drag", function(event, d) {
        d.fx = event.x;
        d.fy = event.y;
    })
    .on("end", function(event, d) {
        if (!event.active) simulation.alphaTarget(0);
        // Keep nodes fixed at their dragged position
    });

// Apply drag behavior to nodes
node.call(dragBehavior);
```

```js
// Handle play/pause button
playPauseButton;
const playPauseButtonGo = (function* () {
    if (playPauseButton % 2 == 1) {
        simulation.restart();
    } else {
        simulation.stop();
    }
})();
```

```js
// Handle reset button
resetButton;
const resetButtonGo = (function* () {
    // Reset node positions
    nodes.forEach((node, i) => {
        node.x = initialNodes[i].x;
        node.y = initialNodes[i].y;
        node.fx = null; // Clear any fixed positions from dragging
        node.fy = null;
    });

    // Update visualization immediately
    ticked();

    // Just update visualization immediately - don't restart simulation
    // The user can manually restart if they want movement
})();
```

```js
// Handle force control updates - these only update forces, don't check play/pause state
linkStrengthSlider;
const linkForceUpdate = (function* () {
    simulation.force("link").strength(linkStrengthSlider);
})();
```

```js
chargeStrengthSlider;
const chargeForceUpdate = (function* () {
    simulation.force("charge").strength(chargeStrengthSlider);
})();
```

```js
centerStrengthSlider;
const centerForceUpdate = (function* () {
    simulation.force("center").strength(centerStrengthSlider);
})();
```

### Thoughts

This was definitely interesting to see! I knew I had a lot of notes in various databases, but I didn't realize how large my clippings were or how connected my projects database was to software.

My biggest clusters ended up being:
- My Software/Projects/Blog Posts amalgamation, where I take notes on all of my computer-y stuff and publish some of them.
- My Internet Clippings, where I save bookmarks that could be helpful later. These get linked to from Projects occasioanlyl but are otherwise isolated.
- My Recommendations and Media Log databases, where I log who suggested things to me and how much I liked them.
- My D&D Notes, both public and private, which have all of my prep work, session notes, vignettes, and evil plans.

# Experimenting

I also spent some time with the built-in NetworkX graph visualizers. I know that it isn't designed for visualization, but they were very helpful for debugging things along the way.

```js
function linkedImage(original, thumb, alt) {
    return html`<a href="${original.href}" target="_blank">
      <img src="${thumb.href}" width="640" />
    </a>`;
}
```

## The Useful Ones

Both of these did a good job of showing the relative densities of pages, the clumps of high word-count pages, and connections across databases. I never really picked a favorite between these two, when in doubt I'd say go with the spring.

### Spring Layout

The classic force-directed layout that treats nodes like physical objects connected by springs. Strongly connected nodes get pulled together while disconnected ones get pushed apart. This is your bread-and-butter for most network visualization - it naturally clusters related content and gives you a good intuitive sense of what's connected to what. Unfortunately it can take a while to compute for large graphs.

```js
const original = FileAttachment("spring_layout.png");
const thumb = FileAttachment("spring_layout_sm.png");
display(linkedImage(original, thumb))
```

### Fruchterman Reingold Layout

Another force-directed approach, but with more sophisticated math behind the scenes. It tends to produce more evenly distributed layouts than plain spring, with better edge crossing minimization. Still, it ends up looking basically the same as the spring layout.

```js
const original = FileAttachment("fruchterman_reingold_layout.png");
const thumb = FileAttachment("fruchterman_reingold_layout_sm.png");
display(linkedImage(original, thumb))
```

## Honorable Mentions

I was surprised at how useful these two were, all things considered. They aren't ideal for actual use, but they gave some good insights.

### Kamada Kawai Layout

The Kamada Kawai was actually the first one I tried after good ol' spring. This layout tries to make all shortest-path distances match up with euclidean distances on the page, which means it's really good at spreading everything out evenly. Anything not in a cluster gets thrown way out there, which is nice for viewing strict hierarchies.

```js
const original = FileAttachment("kamada_kawai_layout.png");
const thumb = FileAttachment("kamada_kawai_layout_sm.png");
display(linkedImage(original, thumb))
```

### Random Layout

It turns out if you just throw everything on a page at random and draw lines between the connections you basically just have a red-string murder-board. But honestly? Sometimes this is exactly what you need. It strips away any algorithmic bias about what "should" be close together and just shows you the raw connectivity patterns. It's a good sanity check - if the random layout still shows obvious clusters purely through edge density, you know you've got some real structure in your data.

```js
const original = FileAttachment("random_layout.png");
const thumb = FileAttachment("random_layout_sm.png");
display(linkedImage(original, thumb))
```

## The Circles

I'm not actually sure what these circular layouts are supposed to be good for. Maybe if my connections were less hierarchical it could be helpful?

### Circular Layout

This one just puts all your nodes in a big circle and draws the edges. It's deterministic and looks very neat, but completely ignores the actual structure of your network. The only time this might be useful is if you have a small number of nodes and you want to see every possible connection clearly, or if you're making a poster and need something that fits in a specific circular frame. Otherwise, it's basically just decoration.

```js
const original = FileAttachment("circular_layout.png");
const thumb = FileAttachment("circular_layout_sm.png");
display(linkedImage(original, thumb))
```

### Shell Layout

Like circular, but with multiple concentric circles (shells). NetworkX tries to put more central nodes in the inner shells and less important ones on the outside. This can actually be pretty useful for networks with a consistent hierarchical structure (known in advance) where you want to see all "levels" of importance.

```js
const original = FileAttachment("shell_layout.png");
const thumb = FileAttachment("shell_layout_sm.png");
display(linkedImage(original, thumb))
```


## The Rest

### Spiral Layout

I thought this one was pretty funny. I have no idea how the databases got stuck on the end of each of these arms, seemingly connected at random to other arms.

```js
const original = FileAttachment("spiral_layout.png");
const thumb = FileAttachment("spiral_layout_sm.png");
display(linkedImage(original, thumb))
```

### ARF Layout

Maximum spread. No cohesion. It spreads everything out as much as possible with no regard for the actual connections, like a circle version of the random layout.

```js
const original = FileAttachment("arf_layout.png");
const thumb = FileAttachment("arf_layout_sm.png");
display(linkedImage(original, thumb))
```


### BFS Layout

The [$1 trillion line](https://en.wikipedia.org/wiki/The_Line,_Saudi_Arabia).

```js
const original = FileAttachment("bfs_layout.png");
const thumb = FileAttachment("bfs_layout_sm.png");
display(linkedImage(original, thumb))
```
