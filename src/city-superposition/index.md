# City Superposition Calculator

> if we draw lines that link every single berlin in the US to every single other berlin in the US we will find the true location of Berlin
>
> the Berlin superposition as it were
>
> \- [uss-edsall, tumblr 2024](https://uss-edsall.tumblr.com/post/769191001039503360)

Now you, too, can find your own city superposition.

## Map

```js
const us = FileAttachment('../maps/us-counties-10m.json').json()
```

```js
const nation = topojson.feature(us, us.objects.nation)
const states = topojson.feature(us, us.objects.states).features
```

```js
Plot.plot({
  projection: 'albers-usa',
  width: 975,
  height: 610,
  color: { legend: true },
  r: { range: [5, 10] },
  marks: [
    Plot.geo(states, { strokeWidth: 0.5 }),
    Plot.geo(nation, { strokeWidth: 1 }),
    Plot.dot(matched_cities, {
      x: 'lng',
      y: 'lat',
      r: (i) => (i.population ? i.population : 1e5),
      fill: 'type',
      stroke: 'type',
      fillOpacity: 0.2,
      symbol: (i) => (i.type == 'Superposition' ? 'star' : 'circle'),
      channels: { City: 'city', State: 'state_name', Population: 'population', Match: 'type' },
      tip: {
        format: {
          x: null,
          y: null,
          r: null,
          symbol: null
        }
      }
    })
  ]
})
```

## Input

```js
const uscities = FileAttachment('uscities.csv').csv({ typed: true })
//const worldcities = FileAttachment('worldcities.csv').csv({ typed: true })
```

```js
const target_city = view(
  Inputs.text({
    label: 'Target City',
    value: 'Berlin'
  })
)
```

```js
const include_partial_matches = view(
  Inputs.toggle({ label: 'Include Partial Matches', value: true })
)
```

```js
const matched_cities = [
  ...uscities.filter((i) => i.city_ascii === target_city).map((i) => ({ ...i, type: 'Exact' })),
  ...(include_partial_matches
    ? uscities
        .filter((i) => i.city_ascii.includes(target_city) && i.city_ascii !== target_city)
        .map((i) => ({ ...i, type: 'Partial' }))
    : [])
]
```

```js
Inputs.table(
  matched_cities.filter((i) => i.type != 'Superposition'),
  {
    layout: 'auto',
    maxWidth: 640,
    columns: ['city', 'state_name', 'county_name', 'population'],
    header: {
      city: 'City',
      state_name: 'State',
      county_name: 'County',
      population: 'Population'
    },
    sort: 'population',
    reverse: true
  }
)
```

```js
function geo_mean(cities, target_city) {
  const meanLat = cities.reduce((sum, { lat }) => sum + lat, 0) / cities.length
  const meanLng = cities.reduce((sum, { lng }) => sum + lng, 0) / cities.length
  //const meanPop = cities.reduce((sum, { population }) => sum + population, 0) / cities.length
  return {
    city: `True ${target_city}`,
    lat: meanLat,
    lng: meanLng,
    type: 'Superposition'
  }
}

let super_city = geo_mean(matched_cities, target_city)
matched_cities.push(super_city)
```

### Notes

This page is not entirely complete, I intend to add more location algorithms and other features in the near future.

City data is from [simplemaps.com](https://simplemaps.com/data/us-cities).

<!--
TODO:
- Remove some unnecessary fields from CSV to reduce file size
- Add more centerpoint finders
- Add a picker for some good target city choices
- Support showing multiple cities at once
-->
