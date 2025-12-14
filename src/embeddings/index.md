```js
const metrics = FileAttachment('platform_metrics.json').json()
```

```js
const clusters = FileAttachment('clusters.jsonl').text().then(text => 
  text.trim().split('\n').map(line => JSON.parse(line))
)
```

```js
const tsne_points = FileAttachment('clusters_tsne_interactive_points.json').json()
```

```js
const platforms = new Map(Object.entries({
    "kalshi": {
        "label": "Kalshi",
        "color": "#00d298",
        "total_markets": metrics.total_markets.kalshi
    },
    "manifold": {
        "label": "Manifold",
        "color": "#4337c9",
        "total_markets": metrics.total_markets.manifold
    },
    "metaculus": {
        "label": "Metaculus",
        "color": "#3f5266",
        "total_markets": metrics.total_markets.metaculus
    },
    "polymarket": {
        "label": "Polymarket",
        "color": "#0072f9",
        "total_markets": metrics.total_markets.polymarket
    },
}))
```

# Betting with Embeddings

Prediction markets are great. You can go bet on them and potentially make a lot of money, you can do research and get rewarded, or you can just sit back and let other people do all the hard work. That's actually how I use prediction markets a lot of the time - I'll read some news and go "that can't be right", then go check a couple prediction market sites to get a better idea of what's going on. This is awesome when you're interested in some big news event, but less good when you're wondering about something niche like [China's rebar failure rate](https://manifold.markets/MikhailTal/chinas-rebar-failure-rate-below-20). Most prediction market platforms don't have an interest in answering *every question ever*, and with limited liquidity they have to focus their attention on the most popular questions. 

So how likely is it that any particular market platform will answer the one specific question that you're interested in? Well to answer that for yourself, just go to each site and search for your question. They may or may not have it, and if they don't you can usually suggest that they create it (or make it yourself, on [Manifold](https://manifold.markets/create) or [Metaculus](https://www.metaculus.com/questions/create/)). This is all well and good for you, the person with a question. But can we generalize this? 

## Who am I?

Hi, I'm [wasabipesto](https://wasabipesto.com). I like to quantify things, especially around prediction markets - you might recognize [Brier.fyi](https://brier.fyi/), my project to evaluate how accurate prediction markets are in general and can if we can find a way to fairly compare accuracy between different market platforms. I like to find ways to operationalize big questions like this.

We'll be looking at a single snapshot in time - right now, how many platforms have the exact thing you're looking for? We should expect that most really popular questions would be covered by roughly every platform, so we'll be more interested in the less-common ones. Some sites make dozens of markets about a single topic, so we can't just count the number of markets on each one. It would be nice if we had a way to mathematically distinguish how similar or different two questions or markets were.

It turns out that there is an entire mechanism within natural language processing called [word embedding](https://en.wikipedia.org/wiki/Word_embedding) that does exactly this. The rough idea is that words that are used in similar contexts will have similar embedding values, and vice versa for words used in different contexts. By comparing how close two embedding values are, we can mathematically distinguish how similar or different the corresponding ideas are. They really are quite amazing, and if you want to learn more I'd recommend [this visual explainer](https://vizuara.substack.com/p/from-words-to-vectors-understanding).

These language embeddings are the secret sauce that lets us actually generalize. They transfer entire concepts and phrases into this high-dimensional space that represents all possible ideas. Since we can do math with them, we can blindly ignore the nuance around what they represent and just focus on some numbers. Needless to say, we'll be overgeneralizing a little bit. For science!

## Aims

* This post will be a fairly casual walkthrough of a handful of metrics, each of which is designed to answer some big question about how prediction markets are actually distributed in this natural language embedding space. We'll tally up whichever platform comes out on top of each.
* We won't be doing tests for statistical significance here, just looking at some raw numbers and rewarding which platform comes out on top of each. Either a platform clearly wins a metric, or it doesn't. If you have to squint to see who won, it'll be a tie.
* Many of these metrics will be quite simple for ease of explanation. They aren't meant to be perfectly tuned to every possible scenario, more akin to rough benchmarks.

# Methodology

As part of my pipeline for Brier.fyi, I already generate natural language embeddings for every single market from the titles, descriptions, and resolution criteria. I use them to find equivalent markets across platforms, but you could also use them for semantic search or sentiment analysis. The model I use is [nomic-embed-text-v1.5](https://huggingface.co/nomic-ai/nomic-embed-text-v1.5), which is easy to run locally, and for any text string input it produces a series of 768 numbers which correspond to a coordinate vector in 768-dimensional space.

The market dataset follows the same procedure as Brier.fyi, which is [detailed here](https://brier.fyi/about/#market-types). The dataset includes only closed, resolved markets from Kalshi, Polymarket, Metaculus, and Manifold which are binary or can be decomposed into a collection of binary markets. For instance, we have Kalshi's numeric questions, since they are a small number of discrete splits, but not Metaculus's numeric questions since they are a continuous function. We also discard any markets with zero trades. For this post I am also excluding Kalshi's recent NFL MVE markets, which do not have traditional descriptions and don't fit well with this analysis ([example here](https://kalshi.com/markets/KXMVENFLSINGLEGAME)).

This leaves us with ${metrics.total_markets_all.toLocaleString()} total markets, with their stats shown below:

<div class="card" style="max-width: 640px;">

# Market Dataset Statistics

```js
const data = Object.entries(metrics.total_markets).map(([platform_slug, value]) => ({
  platform_name: platforms.get(platform_slug).label,
  platform_color: platforms.get(platform_slug).color,
  value: value
}));
display(Plot.plot({
  caption: "The total number of markets per platform.",
  marginLeft: 80,
  x: { label: 'Number of markets', grid: true },
  y: { label: null },
  marks: [
    Plot.barX(data, {
      y: 'platform_name',
      fill: 'platform_color',
      x: 'value',
      tip: true
    }),
    Plot.ruleX([0])
  ]
}))
```

```js
const data = Object.entries(metrics.boxplot_data.volume_usd).map(([platform_slug, obj]) => ({
  platform_name: platforms.get(platform_slug).label,
  platform_color: platforms.get(platform_slug).color,
  ...obj
}));
display(Plot.plot({
  caption: "A box plot of market volume per platform.",
  marginLeft: 80,
  x: { label: 'Volume (USD)', grid: true },
  y: { label: null },
  marks: [
    Plot.ruleY(data, {
      y: 'platform_name',
      fill: 'platform_color',
      x1: 'lower_whisker',
      x2: 'upper_whisker',
    }),
    Plot.rectX(data, {
      y: 'platform_name',
      fill: 'platform_color',
      x1: 'q1',
      x2: 'q3',
    }),
    Plot.tickX(data, {
      y: 'platform_name',
      fill: 'platform_color',
      x: "median",
      strokeWidth: 2
    }),
    Plot.ruleX([0])
  ]
}))
```

```js
const data = Object.entries(metrics.boxplot_data.traders_count).map(([platform_slug, obj]) => ({
  platform_name: platforms.get(platform_slug).label,
  platform_color: platforms.get(platform_slug).color,
  ...obj
}));
display(Plot.plot({
  caption: "A box plot of unqiue trader count per platform.",
  marginLeft: 80,
  x: { label: 'Number of traders', grid: true },
  y: { label: null },
  marks: [
    Plot.ruleY(data, {
      y: 'platform_name',
      fill: 'platform_color',
      x1: 'lower_whisker',
      x2: 'upper_whisker',
    }),
    Plot.rectX(data, {
      y: 'platform_name',
      fill: 'platform_color',
      x1: 'q1',
      x2: 'q3',
    }),
    Plot.tickX(data, {
      y: 'platform_name',
      fill: 'platform_color',
      x: "median",
      strokeWidth: 2
    }),
    Plot.ruleX([0])
  ]
}))
```

```js
const data = Object.entries(metrics.boxplot_data.duration_days).map(([platform_slug, obj]) => ({
  platform_name: platforms.get(platform_slug).label,
  platform_color: platforms.get(platform_slug).color,
  ...obj
}));
display(Plot.plot({
  caption: "A box plot of market duration per platform.",
  marginLeft: 80,
  x: { label: 'Duration (days)', grid: true },
  y: { label: null },
  marks: [
    Plot.ruleY(data, {
      y: 'platform_name',
      fill: 'platform_color',
      x1: 'lower_whisker',
      x2: 'upper_whisker',
    }),
    Plot.rectX(data, {
      y: 'platform_name',
      fill: 'platform_color',
      x1: 'q1',
      x2: 'q3',
    }),
    Plot.tickX(data, {
      y: 'platform_name',
      fill: 'platform_color',
      x: "median",
      strokeWidth: 2
    }),
    Plot.ruleX([0])
  ]
}))
```

```js
const data = Object.entries(metrics.boxplot_data.resolution).map(([platform_slug, obj]) => ({
  platform_name: platforms.get(platform_slug).label,
  platform_color: platforms.get(platform_slug).color,
  ...obj
}));
display(Plot.plot({
  caption: "The average final resolution value per platform.",
  marginLeft: 80,
  x: { label: 'Resolved percent', grid: true, percent: true, domain: [0, 100] },
  y: { label: null },
  marks: [
    Plot.barX(data, {
      y: 'platform_name',
      fill: 'platform_color',
      x: "mean",
      tip: true,
    }),
    Plot.ruleX([0])
  ]
}))
```

</div>

You can see that Kalshi has far and away the most markets, mainly due to their large number of recurring market series. Polymarket tends to have higher mean volume per market, while Metaculus has both the most traders per market and the longest ones.

Once we have the language embeddings, what can we do with them? Since each embedding point is a 768-dimensional vector you can't visualize it directly. We can do some work with libraries optimized for this sort of task, such as [Faiss](https://github.com/facebookresearch/faiss), which allow us to find the "nearest neighbors" to each point. Once we have those we can calculate the distances to those neighbors - markets that are further away from all others are more unique, so a higher distance equals a higher novelty score. For this analysis I've used the distance to each point's tenth-nearest neighbor to represent the novelty. 

```js
const data = Object.entries(metrics.boxplot_data.novelty).map(([platform_slug, obj]) => ({
  platform_name: platforms.get(platform_slug).label,
  platform_color: platforms.get(platform_slug).color,
  ...obj
}));
display(Plot.plot({
  caption: "A box plot of market novelty per platform.",
  marginLeft: 80,
  x: { label: 'Novelty', grid: true },
  y: { label: null },
  marks: [
    Plot.ruleY(data, {
      y: 'platform_name',
      fill: 'platform_color',
      x1: 'lower_whisker',
      x2: 'upper_whisker',
    }),
    Plot.rectX(data, {
      y: 'platform_name',
      fill: 'platform_color',
      x1: 'q1',
      x2: 'q3',
    }),
    Plot.tickX(data, {
      y: 'platform_name',
      fill: 'platform_color',
      x: "median",
      strokeWidth: 2
    }),
    Plot.ruleX([0])
  ]
}))
```

Unfortunately, we start running into the [curse of dimensionality](https://en.wikipedia.org/wiki/Curse_of_dimensionality) pretty quickly. In order to do much more with these points we need to find a way to simplify them and reduce the number of dimensions. Since the nomic embedding dataset is designed to generalize over all text in ~100 languages, there are many dimensions with essentially zero useful information on our dataset. We can use an algorithm such as [PCA](https://en.wikipedia.org/wiki/Principal_component_analysis) to preserve most of the information while drastically reducing the number of dimensions. When reducing from 768 to 300 dimensions, we can actually keep 96% of the variance explained and make all of our subsequent operations much more manageable.

```js
const data = [
    {"dimensions": 768, "variance": 1.0000},
    {"dimensions": 600, "variance": 0.9980},
    {"dimensions": 500, "variance": 0.9930},
    {"dimensions": 400, "variance": 0.9830},
    {"dimensions": 300, "variance": 0.9600},
    {"dimensions": 200, "variance": 0.9140},
    {"dimensions": 100, "variance": 0.8090},
    {"dimensions": 50, "variance": 0.6920},
    {"dimensions": 20, "variance": 0.5490},
    {"dimensions": 10, "variance": 0.4470},
    {"dimensions": 2, "variance": 0.2680},
    {"dimensions": 0, "variance": 0.0000},
];
display(Plot.plot({
  height: 150,
  x: { label: 'Dimensions' },
  y: { label: 'Percent variance explained', percent: true },
  marks: [
    Plot.line(data, {
      x: 'dimensions',
      y: 'variance',
      tip: true
    }),
    Plot.ruleX([0])
  ]
}))
```

It's still hard to visualize in 300 dimensions, but if you imagine a huge space with many dense "clusters" and many more sparse regions then you'll be pretty close. This huge space loosely correlates to a field of all possible markets, with the denser regions representing a bunch of very similar markets. There's a few ways we can identify those clusters, the one I went with was called [HDBSCAN](https://github.com/scikit-learn-contrib/hdbscan). This algorithm will identify each dense region, draw boundaries and then return a collection of clusters and all the sparse outliers. (If you're interested in reproducing this, I used 10 samples and an epsilon of 0.5 on the normalized vectors from nomic).

We ended up with ${metrics.total_clusters.toLocaleString()} clusters, covering ${metrics.total_clustered_markets.toLocaleString()}/${metrics.total_markets_all.toLocaleString()} markets (${(metrics.total_clustered_markets/metrics.total_markets_all*100).toFixed(0)}%) with the rest remaining as outliers. These clusters are mini-topics, covering anything from flight delays to Oscars awards to senate elections, and they have up to 100,000 markets each.

```js
Inputs.table(clusters, {
    columns: [
        "market_count",
        "top_platform",
        "keywords",
        "top_market_title",
    ],
    width: {
        market_count: 100,
        keywords: 180,
        top_platform: 100,
    },
    header: {
        market_count: "Market Count",
        top_platform: "Top Platform",
        keywords: "Keywords",
        top_market_title: "Sample Market Title"
    },
    format: {
        market_count: (x) => x.toLocaleString(),
        top_platform: (x) => platforms.get(x).label,
    },
    sort: "market_count",
    reverse: true,
    select: false
})
```

Finally, we can apply another dimension reduction technique specifically designed for visualization ([t-SNE](https://en.wikipedia.org/wiki/T-distributed_stochastic_neighbor_embedding)) in order to fit everything down into 2D, which we can then plot. Remember that this is being boiled down from hundreds of dimensions, so a lot of information is lost! The only real meaningful information remaining is that two points that are closer together tend to be more similar. Since each dot is a market, we can also show which cluster it was sorted into via a color map.

<div class="card" style="max-width: 1000px;">

# Map of Prediction Market Embeddings

```js
const minscore = view(Inputs.range([0, 15], {value: 3, step: 1, label: "Minimum Score"}));
const colorby = view(Inputs.select([
    {value: "cluster", label: "Cluster ID"}, 
    {value: "platform_name", label: "Platform"}, 
    {value: "category_slug", label: "Category"}, 
    {value: "novelty", label: "Novelty"}, 
    {value: "score", label: "Score"}, 
    {value: "volume_usd", label: "Trade Volume (USD)"}, 
    {value: "traders_count", label: "Unique Traders"}, 
    {value: "duration_days", label: "Duration (Days)"}, 
    {value: "open_time", label: "Open Date"}, 
    {value: "resolution", label: "Resolution"}
], {label: "Color By", format: (t) => t.label}));
```

```js
const data = tsne_points.map((obj) => ({
  platform_name: platforms.get(obj.platform_slug).label,
  platform_color: platforms.get(obj.platform_slug).color,
  open_time: new Date(obj.open_datetime),
  pos_x: obj.embedding_2d[0],
  pos_y: obj.embedding_2d[1],
  ...obj
})).filter((obj) => obj.score > minscore);

display(Plot.plot({
  marginTop: 0,
  width: 900,
  height: 800,
  x: { axis: null },
  y: { axis: null },
  color: { 
      legend: true, 
      label: colorby.label,
      scheme: "Viridis",
  },
  marks: [
    Plot.dot(data, {
      x: 'pos_x',
      y: 'pos_y',
      r: 1,
      fill: colorby.value,
      channels: {
          Title: "title",
          Platform: "platform_name"
      },
      tip: {
          format: {
              x: null,
              y: null,
          }
      }
    }),
  ]
}))
```

</div>

This is actually pretty useful "map" of prediction market topics! There are distinct regions for politics, finance, culture, and sports, with dozens of little distinct clusters within each. The financial regions take up most of the map right now, from about 11 o'clock to 6 o'clock.

# Metrics

Now let's explore some questions, and try to find a few metrics that can help us understand each one.

## Which platforms cover the widest range of topics?

### Convex Hull Volume

One way to measure total topic coverage is with the convex hull volume. If you were to put a bunch of pushpins on a map, then wrap a string around the outside ones so that they're all encompassed by a single loop, you'd have the [convex hull](https://en.wikipedia.org/wiki/Convex_hull) of those points. You could do this with, say, the locations of midwest-only grocery store Meijer versus the multinational Walmart and get two very different-looking shapes. It would then be very easy to calculate how much "reach" each retailer has by comparing the area within each shape. Meijer is pretty local to my area, so the area would be pretty small compared to the thousands of Walmarts across the globe. Note that the number of points on the map doesn't directly affect this metric - it doesn't matter how many stores you have if they're all in one tiny area.

If we generalize this to a large number of dimensions we can do the same thing with prediction market topic coverage. In our high-dimensional space, each market's location represents a meaning and the distance to its neighbors represents how similar they are. If we were to do the same sort of thing here, drawing a multidimensional shape around the outer edges of this cluster of points, we would have the same sort of convex hull.

The market embedding values we generated earlier roughly correspond to points in an abstract idea space, and the further away two points are the more dissimilar their ideas are. So what if we looked at the convex hull around the markets from a platform and saw that the volume was much higher than another platform's markets? We should be able to infer that the platform with the highest volume has the most diverse or dissimilar set of markets.

Unfortunately, there are two problems with calculating the convex hull in a large number of dimensions. First, it's very computationally taxing. Second, in higher dimensions each point has a much higher chance of becoming an "outside point" that inflates the total volume. In order to address both of those concerns, we'll use the same PCA strategy from earlier to reduce the dataset down to 6 dimensions. This is a good balance that allows us to keep a good amount of the variance in the data while reducing the computational cost and vertex explosion risk.

<div class="card" style="max-width: 640px;">

```js
const data = Object.entries(metrics.convex_hull_volume_lowdim).map(([platform_slug, value]) => ({
  platform_name: platforms.get(platform_slug).label,
  platform_color: platforms.get(platform_slug).color,
  value: value
}));
display(Plot.plot({
  title: "Convex Hull Volume",
  marginTop: 0,
  marginLeft: 80,
  x: { label: 'Volume, 6 dimensions', grid: true },
  y: { label: null },
  marks: [
    Plot.barX(data, {
      y: 'platform_name',
      fill: 'platform_color',
      x: 'value',
      tip: true
    }),
    Plot.ruleX([0])
  ]
}))
```

</div>

And Manifold is a clear winner here, with a final volume over double each of the other platforms.

### Mean Effective Radius

Going back to the map of Meijer and Walmart, we might notice that there's one Walmart in Kodiak, Alaska that [Pitbull visited in 2012](https://www.bbc.com/news/newsbeat-19060579). This is pretty far from the rest of the Walmart locations, and one could argue that this single location is inflating Walmart's convex hull area. Especially in higher dimensions, outliers can significantly impact the convex hull metrics, so we should look for alternatives that aren't as sensitive and see if our results still hold up.

First, let's find the centroid of all the Walmart store locations - the point that minimizes the squared distance between itself and each store. From that central point, we can draw a line to each Walmart store and measure the distance, recording each one. Once we have them all, we can calculate the average distance and use that as our metric. This mitigates the Alaska outlier if it's singular, but if there are a lot of very distant points they will still be represented in this metric.

We'll be applying this strategy to our market dataset with the same goal. If the average distance is very high, that means a lot of markets on this platform are unusual or unique. For comparison's sake, this distance is calculated using the same 6-dimensional dataset as the convex hull volume metric. 

<div class="card" style="max-width: 640px;">

```js
const data = Object.entries(metrics.effective_radius_lowdim_mean).map(([platform_slug, value]) => ({
  platform_name: platforms.get(platform_slug).label,
  platform_color: platforms.get(platform_slug).color,
  value: value
}));
display(Plot.plot({
  title: "Mean Effective Radius",
  marginTop: 0,
  marginLeft: 80,
  x: { label: 'Radius, 6 dimensions', grid: true, domain: [0, 1] },
  y: { label: null },
  marks: [
    Plot.barX(data, {
      y: 'platform_name',
      fill: 'platform_color',
      x: 'value',
      tip: true
    }),
    Plot.ruleX([0])
  ]
}))
```

</div>

Interestingly, the mean radius values for Kalshi and Polymarket are fairly similar so this will be our first tie. It would seem that while Manifold has a high number of very unique outliers, some other platforms have a more consistent spread of diversity.

### Topic Participation Rate

Both of the previous metrics are calculated based on raw market embedding points, which works fine in theory. However, just because a market is *different* doesn't mean it's *valuable*. For instance, a market on someone's [testosterone level](https://manifold.markets/ian/what-range-will-sgs-testosterone-le) is very unique, but not particularly useful. We should try to find a metric that still represents how broad a reach each platform has, but within established topics.

Thankfully, we already found our topic clusters! Each cluster we found has anywhere from 20 to 100,000 markets each, and they represent natural groupings like stock tickers or election polling. What if we just counted how many clusters each platform participates in? 

A platform that has a market in every single topic would have a 100% participation rate, while one that only participates in a couple of topics would be much lower. We should expect that the more unique topics a platform participates in, the more effort they put into making sure they cover all *useful* questions.

<div class="card" style="max-width: 640px;">

```js
const data = Object.entries(metrics.effective_reach_1market).map(([platform_slug, value]) => ({
  platform_name: platforms.get(platform_slug).label,
  platform_color: platforms.get(platform_slug).color,
  value: value / metrics.total_clusters
}));
display(Plot.plot({
  title: "Topic Participation Rate",
  marginTop: 0,
  marginLeft: 80,
  x: { label: 'Percent of clusters', grid: true, percent: true },
  y: { label: null },
  marks: [
    Plot.barX(data, {
      y: 'platform_name',
      fill: 'platform_color',
      x: 'value',
      tip: true
    }),
    Plot.ruleX([0])
  ]
}))
```

</div>

Of course a prediction market platform that has exactly one item for each category isn't exactly stunning, but it's a good indicator that they've spotted a lot of good topics to cover. Manifold covers nearly 60% of the topics in our dataset which puts them firmly in the lead here.

## Which platforms cover topics that others don't?

What if we reframed the question: Instead of looking at total breadth of topics, what if we looked at topic uniqueness? If three platforms are already covering a specific topic really well, a fourth platform doesn't usually add much marginal value. It may be better for that fourth platform to find some new topic that the others don't cover at all. 

With our supermarket metaphor, we could say we're less concerned about the raw area covered by each chain and more interested in which store is more likely to pop up in an underserved town or neighborhood.

### High-Novelty Proportion

The simplest way we can calculate this is with the "novelty" metric described earlier. Here, novelty is calculated by finding a point's neighbors and getting the distance to the tenth-nearest one. Since embedding point closeness is equivalent to similarity, a market far away from all the others will be very unique and a market very close to its neighbors is likely a duplicate.

The most novel markets, the ones furthest from its neighbors, represent extreme uniqueness. In order to calculate this metric, we can simply count how many markets from each platform are in the top fifth percentile of markets by novelty. 

```js
const data = Object.entries(metrics.high_novelty_count_p95).map(([platform_slug, value]) => ({
  platform_name: platforms.get(platform_slug).label,
  platform_color: platforms.get(platform_slug).color,
  value: value
}));
display(Plot.plot({
  marginLeft: 80,
  x: { label: 'Number of high-novelty markets', grid: true },
  y: { label: null },
  marks: [
    Plot.barX(data, {
      y: 'platform_name',
      fill: 'platform_color',
      x: 'value',
      tip: true
    }),
    Plot.ruleX([0])
  ]
}))
```

Of course, a platform with many markets will naturally have a better change of finding some unique markets by happenstance alone. So generate the final metric, we'll divide this by the total number of markets on each platform to get the proportion.

<div class="card" style="max-width: 640px;">

```js
const data = Object.entries(metrics.high_novelty_count_p95).map(([platform_slug, value]) => ({
  platform_name: platforms.get(platform_slug).label,
  platform_color: platforms.get(platform_slug).color,
  value: value / platforms.get(platform_slug).total_markets
}));
display(Plot.plot({
  title: "High-Novelty Market Proportion",
  marginTop: 0,
  marginLeft: 80,
  x: { label: 'Percent of high-novelty markets', grid: true, percent: true },
  y: { label: null },
  marks: [
    Plot.barX(data, {
      y: 'platform_name',
      fill: 'platform_color',
      x: 'value',
      tip: true
    }),
    Plot.ruleX([0])
  ]
}))
```

</div>

Metaculus will win this metric, with over a quarter of their questions falling into the top fifth percent of our sample!

However, keep in mind that unique doesn't necessarily mean useful. In fact, this metric is often self-defeating since a new, interesting, unique market on one platform is often copied by at least a few other platforms. Once there is a duplicate elsewhere, the novelty of the original market drops and this score goes down.

### Outlier Proportion

Instead of looking at raw distance to other markets, what if we looked at the markets that were too unique to fit in a topic cluster? HDBSCAN, our clustering algorithm, will choose to ignore any remaining points that don't seem to fit instead of blindly grouping everything into the nearest cluster. By definition these markets weren't similar enough to fit into any established topic, which means that they must be quite unique. 

Similarly to the high-novelty proportion, we'll first look at the raw number of markets from each platform that didn't fit into any cluster.

```js
const data = Object.entries(metrics.outlier_count).map(([platform_slug, value]) => ({
  platform_name: platforms.get(platform_slug).label,
  platform_color: platforms.get(platform_slug).color,
  value: value
}));
display(Plot.plot({
  marginLeft: 80,
  x: { label: 'Number of outlier markets', grid: true },
  y: { label: null },
  marks: [
    Plot.barX(data, {
      y: 'platform_name',
      fill: 'platform_color',
      x: 'value',
      tip: true
    }),
    Plot.ruleX([0])
  ]
}))
```

Again, we'll divide this by each platform's total number of markets to get the final score as a proportion.

<div class="card" style="max-width: 640px;">

```js
const data = Object.entries(metrics.outlier_proportion).map(([platform_slug, value]) => ({
  platform_name: platforms.get(platform_slug).label,
  platform_color: platforms.get(platform_slug).color,
  value: value
}));
display(Plot.plot({
  title: "Outlier Proportion",
  marginTop: 0,
  marginLeft: 80,
  x: { label: 'Percent of outlier markets', grid: true, percent: true },
  y: { label: null },
  marks: [
    Plot.barX(data, {
      y: 'platform_name',
      fill: 'platform_color',
      x: 'value',
      tip: true
    }),
    Plot.ruleX([0])
  ]
}))
```

</div>

Metaculus will win this metric as well, with over 80% of their questions lying outside any of the acknowledged clusters.

This metric is slightly better than the high-novelty metric, since additional markets on the "bandwagon" won't retroactively reduce the score of these outliers until there's enough to form a whole topic cluster, which is then scored in other ways. It's still not perfect, though, since it's still rewarding the potentially-less-useful markets outside the established clusters.

### Majority Cluster Count

Let's look again at the markets that were actually sorted into topic clusters. A lot of the clusters are overwhelmingly comprised of just one platform's markets, such as gas prices in a particular city or niche competitions such as the [James Beard Award](https://kalshi.com/markets/kxjbeardoc/beard-outstanding-chef/kxjbeardoc-2025). What if we wanted to look at those niches where there are enough markets to form a natural topic cluster, but where the topic cluster is still dominated by one platform?

To operationalize this, we can record the proportion of markets in each cluster that belong to each platform. For any cluster where over 95% are from a single platform, we tally that cluster as being dominated by that platform.

<div class="card" style="max-width: 640px;">

```js
const data = Object.entries(metrics.majority_clusters_95pct).map(([platform_slug, value]) => ({
  platform_name: platforms.get(platform_slug).label,
  platform_color: platforms.get(platform_slug).color,
  value: value
}));
display(Plot.plot({
  title: "Majority Cluster Count",
  marginTop: 0,
  marginLeft: 80,
  x: { label: 'Number of clusters', grid: true },
  y: { label: null },
  marks: [
    Plot.barX(data, {
      y: 'platform_name',
      fill: 'platform_color',
      x: 'value',
      tip: true
    }),
    Plot.ruleX([0])
  ]
}))
```

</div>

Over half of all clusters are dominated by Manifold! This is interesting, since we would expect that barring situations that restrict some sites (such as governmental regulation) most platforms would just copy popular market ideas from the others. If we accept that each cluster is representing some reasonably salient topic, then any platform that controls the vast majority of a cluster must have some unique reason why they are able to do so. 

While it's theoretically possible that some platforms would have unique market mechanisms that make some topics more viable, in practice most platforms just use simple binary contracts. Additionally, most topics aren't overly regulated so I think that effect is likely not responsible for most of the effect. I think it's more likely that each platform simply focuses their market pool around their specific userbase, targeting their limited efforts where they think it will be the most useful. This ends up creating niches for each platform and these numbers are a reflection of either how broad the userbase's interests are or how much time the site's staff (or mods) spend on creating and managing smaller markets.

## Which platforms innovate the most?

Thus far we've been ignoring one very important axis: time. 

Despite the fact that Meijer was founded earlier and closer to me than Walmart, the first of the two to open a location in my city was actually Walmart. Walmart was simply more aggressive - they knew that there was money to be made by opening new stores here, and they did so early. (Ignore the fact that they were both were beat by Kroger by over 60 years.)

In the huge space that is "all potential market topic ideas", finding an interesting, untapped idea isn't nearly as easy. Successfully identifying and capitalizing on a new topic is quite difficult even for established platforms, let alone those still trying to find their product-market fit. So how can we score those that are actually innovative?

### Cluster Founder Count

A very straightforward way to measure this would be to look at the first-created market in each topic cluster. When this first market was created, the topic "landscape" looked very different and the area was likely pretty empty. Having the first market in a given region would have given the platform a unique advantage - any user interested in that topic only has one place to go! Even if other sites take notice and steal the idea, we should reward the one that started it all.

Calculating this is fairly straightforward. We simply need to find the first-created market in each cluster, then tally up the number of clusters each platform founded.

<div class="card" style="max-width: 640px;">

```js
const data = Object.entries(metrics.clusters_founded).map(([platform_slug, value]) => ({
  platform_name: platforms.get(platform_slug).label,
  platform_color: platforms.get(platform_slug).color,
  value: value
}));
display(Plot.plot({
  title: "Cluster Founder Count",
  marginTop: 0,
  marginLeft: 80,
  x: { label: 'Number of clusters founded', grid: true },
  y: { label: null },
  marks: [
    Plot.barX(data, {
      y: 'platform_name',
      fill: 'platform_color',
      x: 'value',
      tip: true
    }),
    Plot.ruleX([0])
  ]
}))
```

</div>

Manifold wins this metric quite clearly, with the first market in over half of all clusters. We would expect that this metric will naturally favor platforms that have been around for longer, since they would naturally had more time to come up with each idea before the newer sites even launched. However, the oldest platform (Metaculus) ironically has the lowest score of all. This seems to be mostly due to Metaculus's low volume of markets and fairly narrow topic range rather than any lack of innovation.

### Cluster Growth Score

The founder count is simple and intuitive, but we lose information by just looking at the very first market. If everyone sees that there's a huge news story and goes to make markets about it, one platform may rush it and get the market out first while everyone else gets their versions out a few hours later. Should we reward the first platform every time? 

This metric avoids that issue by looking at all markets made within the first two weeks of the first one. The very first market gets 100 weight for being first, and then every subsequent market gets some weight based on how soon it was made with a dropoff function. This should alleviate the winner-takes-all approach from the previous metric.

```js
function dropoff(hours) {
    const score = 105/(1+0.05*hours)-5
    if (score < 1) {
        return 0;
    } else {
        return Math.round(score);
    }
}

display(Plot.plot({
  height: 150,
  x: { label: 'Days after first market' },
  y: { label: 'Weighting score' },
  marks: [
    Plot.line(Array(500).fill(0).map((n, i) => n + i), {
      x: (i) => i / 24,
      y: (i) => dropoff(i),
      tip: true
    }),
    Plot.ruleX([0])
  ]
}))
```

Once we have the total score for each market within each cluster, we use those weights to assign a proportional "growth score" from 0-1 to each platform that had a market within that first window. A platform that made dozens of markets within the first few hours will beat out one that made just a few markets several days later.

<div class="card" style="max-width: 640px;">

```js
const data = Object.entries(metrics.growth_score_total).map(([platform_slug, value]) => ({
  platform_name: platforms.get(platform_slug).label,
  platform_color: platforms.get(platform_slug).color,
  value: value
}));
display(Plot.plot({
  title: "Cluster Growth Score",
  marginTop: 0,
  marginLeft: 80,
  x: { label: 'Growth score', grid: true },
  y: { label: null },
  marks: [
    Plot.barX(data, {
      y: 'platform_name',
      fill: 'platform_color',
      x: 'value',
      tip: true
    }),
    Plot.ruleX([0])
  ]
}))
```

</div>

Interestingly, the scores here are almost exactly the same as the founder count! It seems that there just isn't that much competition to make new markets on most topics early on. Since this metric is mostly echoing the previous one with essentially zero new information, I'll award Manifold a half-point for this.

# Discussion

<div class="card" style="max-width: 640px;">

```js
const data = [
    {
        "platform_name": platforms.get("kalshi").label,
        "platform_color": platforms.get("kalshi").color,
        "value": 1
    },
    {
        "platform_name": platforms.get("manifold").label,
        "platform_color": platforms.get("manifold").color,
        "value": 4.5
    },
    {
        "platform_name": platforms.get("metaculus").label,
        "platform_color": platforms.get("metaculus").color,
        "value": 2
    },
    {
        "platform_name": platforms.get("polymarket").label,
        "platform_color": platforms.get("polymarket").color,
        "value": 1
    },
];
display(Plot.plot({
  title: "Number of Metrics Won",
  marginTop: 0,
  marginLeft: 80,
  x: { label: 'Number of metrics', grid: true },
  y: { label: null },
  marks: [
    Plot.barX(data, {
      y: 'platform_name',
      fill: 'platform_color',
      x: 'value',
      tip: true,
    }),
    Plot.ruleX([0])
  ]
}))
```

</div>

Manifold did great on the first few metrics looking at raw diversity, but lost out to Kalshi and Polymarket when looking at the mean radius. When looking at uniqueness, Manifold had a huge number of novel and outlier markets but lost to Metcaulus when evaluating by proportion. Manifold's biggest wins were in the natural clusters, where they consistently had markets covering a huge proportion of topics. A significant proportion of topics were either founded by or completely dominated by Manifold, giving them a unique advantage on more niche questions.

In my estimation, these results are likely due to a couple of reasons:

**First**, Manifold has a lot of very active market creators. All markets are created and fully managed by users, and in exchange the market creator gets bonuses for each unique trader. Manifold has experimented with giving market creators a percentage of the house fee on their markets, giving real-money payouts based on new users brought into the site, and official partnerships with influential figures to make their own markets. This has built a community of people who are always looking for new and interesting topics to make markets about. Even new users that have no prior experience with prediction markets can make wildly unique markets - see [Mary's Bread Market](https://manifold.markets/MarySmith/-improve-my-bread) for a recent example.

**Second**, real-money platforms like Kalshi and Polymarket will naturally attract people who are comfortable with gambling, which is not the majority of people. Those users tend to have a more homogeneous set of interests than the wider population and those sites tailor their markets to their userbase well. Manifold, on the other hand, uses a play-money currency. Far more people are comfortable with a "prediction game" with fake points than a high-intensity betting app, and those people bring with them a wider set of interests. For instance, Manifold saw huge numbers of people join the site from communities like [One Piece](https://manifold.markets/topic/one-piece-stocks) and [Destiny](https://manifold.markets/topic/destinygg) that likely would not have happened on a real-money platform. 

**Third**, Manifold staff have themselves fostered an atmosphere of widespread experimentation and innovation. They've experimented with the structure of the site dozens of times, leaning into the title of "[crazed scientist barons](https://manifold.markets/JamesGrugett/will-the-mad-scientists-theory-of-g)" as they launch and re-launch various features to expand the site's reach. The new features lead to new types of markets, new ideas about how markets could work, and real innovation beyond just cool new market topics.

These effects lead to a site that doesn't have the most markets, or the most users, or the most volume, or the best accuracy. As long as Manifold is a play money site, it will never be those things - it'll never have the amount of sheer activity that real money brings. But it does have some things that shouldn't be ignored: a vibrant creator community, a wide and thoughtful userbase, and a market for just about anything you could want to bet on.

## Next Steps

All that being said, these metrics aren't some incredibly robust, peer-reviewed end-all-be-all test of how well each site is run. Manifold came out in the lead on these metrics within this dataset but looking into any particular subtopic will undoubtedly favor other platforms differently. It would be interesting to re-run this on major categories such as politics or science, or at other points in time.

There were also a ton of metrics I considered when making this post but decided against for various reasons. Some were too complicated to explain, some were overwhelmed by random noise, and some were too complex to implement before my self-imposed deadline. Some metrics on my wishlist that didn't make the cut:

- A cross-platform isolation score
- Local outlier factor analysis
- Platform-to-platform topic flow network
- Platform topic overlap matrix
- Herfindahl-Hirschman Index
- Independent t-SNE visualizations for each cluster
- Median market novelty score over time
- Hierarchical topic categorization

I would also love to try all of these experiments again with some more fundamental changes, such as:
- I want to incorporate still-open markets to the dataset, since right now it's only on closed and resolved markets. I would also love to include more complex numeric or continuous markets, though the relative count of those is fairly low compared to the binary markets.
- The embedding model I chose was literally the first one I saw on ollama when I was working on matching markets all those months ago, it would be interesting to see if other embedding models produce similar results. 
- The novelty scores are based on the distance to each point's k-nearest neighbor, and I chose the tenth-nearest neighbor pretty arbitrarily. In my limited testing, choosing the fifth- or twentieth-nearest neighbors appeared not to influence final rankings but it would be a good axis to explore.
- I had to eyeball the clustering hyperparameters until the outputs were reasonable, which introduces a human element I'd like to remove. I'd like to implement something like a Calinski-Harabasz index to demonstrate that the clusters are meaningful and statistically significant.

I also have a couple of ideas for larger projects, from things I've learned here:
- Can you predict a market's resolution from a model trained on the embedding features? Could we make a bot that predicts based on semantics without the latency of an LLM?
- We've seen a 2D representation of the markets, but we can visualize more than that. We can do three dimensions with an interactive explorer, and a few more if we include color. Would that grant us any useful intuition?
- What topics do prediction markets cover significantly more or less than mainstream news? Are there obvious opportunities for new market topics?

So let me know if there's any metric I forgot or any project you want to see next!
