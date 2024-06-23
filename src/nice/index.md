<style>
.inline {
  max-width: 640px
}
</style>

# Nice Numbers

I'm looking for numbers that have a special property: square-cube pandigitals. There's no particular reason; they're not the key to unlocking some proof or formula. We call them “nice numbers” but that's not an official term. There's no Wikipedia page for “nice numbers”. But math isn't about why, it's about why not! So bring out the lemons and let's get cracking.

<div class="card inline">A number ${tex`n`} is nice if ${tex`n^2`} and ${tex`n^3`} contain every possible digit exactly once.</div>

Let's take, say, 68. The square of 68 is 4624. The cube is 314,432. Between them you can find the digit 1 once, and the digit 2 twice. 3 is also in there twice, and 4 is there four times. Meanwhile we're missing 5, 7, 8, 9, and 0. This number is not nice.

```js
function squbify(num, base) {
  // raw square and cube numbers
  const square = num * num
  const cube = num * num * num

  // arrays of the digits in each, convered to base b
  const square_array = square.toString(base).split('')
  const cube_array = cube.toString(base).split('')
  const sqube_array = square_array.concat(cube_array)

  // build list of objects with data for each digit
  const rich_digits_data = []
  for (let digit_num = 0; digit_num < base; digit_num++) {
    const digit_str = digit_num.toString(base) // convert digit to the correct symbol in specified base
    const frequency = sqube_array.filter((d) => d === digit_str).length // count occurrences
    // Push object with digit, frequency, and color
    rich_digits_data.push({
      digit_num: digit_num,
      digit_str: digit_str,
      frequency: frequency
      //color: 'var(--theme-green)'
    })
  }

  // get summary stats
  const sqube_array_len = sqube_array.length
  const sqube_uniques = rich_digits_data.filter((i) => i.frequency > 0).length
  const sqube_perfects = rich_digits_data.filter((i) => i.frequency == 1).length
  const sqube_duplicates = rich_digits_data.filter((i) => i.frequency > 1).length
  const niceness = sqube_perfects / base

  return {
    num: num,
    base: base,
    square: square,
    cube: cube,
    square_array: square_array,
    cube_array: cube_array,
    sqube_array: sqube_array,
    sqube_array_len: sqube_array_len,
    rich_digits_data: rich_digits_data,
    sqube_uniques: sqube_uniques,
    sqube_perfects: sqube_perfects,
    sqube_duplicates: sqube_duplicates,
    niceness: niceness
  }
}
```

```js
function digits_frequencies_plot(rich_data) {
  return Plot.plot({
    height: 150,
    x: { label: 'Digit', type: 'band' },
    y: { label: 'Frequency', grid: true },
    //color: { legend: true },
    marks: [
      Plot.barY(rich_data, {
        x: 'digit_str',
        y: 'frequency',
        fill: (d) => (d.frequency > 1 ? 'var(--theme-red)' : 'var(--theme-green)'),
        tip: {
          format: {
            x: (x) => `${x.toString().toUpperCase()}`,
            y: (y) => `${y} occurrences`,
            fill: null
          }
        }
      }),
      Plot.ruleY([0])
    ]
  })
}
```

```js
function basic_sqube_card(num) {
  const sqube_data = squbify(num, 10)
  const description = html`<div style="margin: 0 1rem 1rem">
    The number ${sqube_data.num} has a square of ${sqube_data.square} and a cube of ${sqube_data.cube}.<br />
    There are ${sqube_data.sqube_uniques}/10 unique digits in the square-cube set.
  </div>`
  const histogram = digits_frequencies_plot(sqube_data.rich_digits_data)
  return html`<div class="card inline">${description}${histogram}</div>`
}
```

${basic_sqube_card(68)}

But if we go up to 69, then our square and cube are 4671 and 328,509. There's exactly one of each digit from 0-9, so we found it! The one and only known nice number. This is funny for obvious reasons.

${basic_sqube_card(69)}

# 69 is the only nice number

Here, I'll give you the controls. Try it out and find another nice number.

```js
const user_1_num_input = html`<input type="number" style="width: 100px" min="1" value="68" />`
const user_1_num = Generators.input(user_1_num_input)
```

```js
const user_1_sqube = squbify(user_1_num, 10)
```

<div class="card inline">
  <div style="margin: 0 1rem 1rem">
    Choose a number: ${user_1_num_input}<br />
    The number ${user_1_sqube.num} has a square of ${user_1_sqube.square.toLocaleString()} and a cube of ${user_1_sqube.cube.toLocaleString()}. <br />
    There are ${user_1_sqube.sqube_uniques}/10 unique digits and ${user_1_sqube.sqube_duplicates} duplicates in the square-cube set. <br />
    This leaves <b>${user_1_sqube.sqube_perfects}/10</b> in the set exactly once.
  </div>
  ${digits_frequencies_plot(user_1_sqube.rich_digits_data)}
</div>

It's not that hard to check exhaustively, you can write a script to do that in a couple minutes. For every number, get the square and the cube and see if there are any missing or repeated digits.

```js
const bunch_of_squbes = []
for (let num = 1; num <= 750; num++) {
  const sqube = squbify(num, 10)
  bunch_of_squbes.push({
    num: num,
    sqube_array_len: sqube.sqube_array_len,
    sqube_perfects: sqube.sqube_perfects
  })
}
```

<div class="card inline">

```js
Plot.plot({
  height: 150,
  x: { label: 'Number' },
  y: { label: 'Digits present exactly once', grid: true },
  marks: [
    Plot.dot(bunch_of_squbes, {
      x: 'num',
      y: 'sqube_perfects',
      r: 2,
      fill: (d) => (d.sqube_perfects !== 10 ? 'var(--theme-red)' : 'var(--theme-green)'),
      tip: {
        format: {
          r: null,
          fill: null
        }
      }
    })
  ]
})
```

</div>

At a certain point the square and cube have so many digits it's impossible to avoid repeats. If there are less than 10 digits in the set, there aren't enough to get one of each digit. If there are too many there's at least one guaranteed duplicate.

<div class="card inline">

```js
Plot.plot({
  height: 150,
  x: { label: 'Number' },
  y: { label: 'Total digits in the set', grid: true },
  marks: [
    Plot.dot(bunch_of_squbes, {
      x: 'num',
      y: 'sqube_array_len',
      r: 2,
      fill: (d) => (d.sqube_array_len !== 10 ? 'var(--theme-red)' : 'var(--theme-green)'),
      tip: {
        format: {
          r: null,
          fill: null
        }
      }
    })
  ]
})
```

</div>

So we're done then?

Well, only if we limit ourselves to base 10.

## Other bases

You may be familiar with binary, using 0s and 1s to represent numbers. That's base 2, since it uses two digits to represent possible values. We typically use base 10, which uses 10 digits (0-9). So when we were checking to see if all possible digits were present, we were checking against these 10 values. But there’s nothing in the rules that says we have to use base 10.

<div class="card inline">
  Revision 1: A number ${tex`n`} is nice in base ${tex`b`} if ${tex`n^2`} and ${tex`n^3`}, as represented in base ${tex`b`}, contain every digit of ${tex`b`} exactly once.
</div>

Now there's so much more room ~~for activities~~ to search! Pick a number and a base and I'll do the same thing as before, except this time I'll convert the square and cube into your selected base before plotting the result.

```js
const user_2_num_input = html`<input type="number" style="width: 100px" min="1" value="8675309" />`
const user_2_base_input = html`<input
  type="range"
  style="width: 100px;"
  min="4"
  value="16"
  max="36"
/>`
const user_2_num = Generators.input(user_2_num_input)
const user_2_base = Generators.input(user_2_base_input)
```

```js
const user_2_sqube = squbify(user_2_num, user_2_base)
```

<div class="card inline">
  <div style="margin: 0 1rem 1rem">
    Choose a number: ${user_2_num_input}<br />
    Choose a base: ${user_2_base_input} ${user_2_base}<br />
    The number ${user_2_sqube.num} has a square of ${user_2_sqube.square.toLocaleString()} and a cube of ${user_2_sqube.cube.toLocaleString()}. <br />
    These are converted into the sets ${user_2_sqube.square_array} and ${user_2_sqube.cube_array}. <br />
    There are ${user_2_sqube.sqube_uniques}/${user_2_base} unique digits and ${user_2_sqube.sqube_duplicates} duplicates in the square-cube set. <br />
    This leaves <b>${user_2_sqube.sqube_perfects}/${user_2_base}</b> in the set exactly once.
  </div>
  ${digits_frequencies_plot(user_2_sqube.rich_digits_data)}
</div>

...

Wait, you couldn’t find any? Are you sure you looked everywhere?

```js
const bunch_of_squbes_more_bases = []
for (let base = 4; base <= 26; base++) {
  for (let num = 1; num <= 750; num++) {
    const sqube = squbify(num, base)
    bunch_of_squbes_more_bases.push({
      num: num,
      base: base,
      sqube_array_len: sqube.sqube_array_len,
      sqube_perfects: sqube.sqube_perfects
    })
  }
}
```

<div class="card">

```js
Plot.plot({
  height: 250,
  width: 1200,
  x: { label: 'Number' },
  y: { label: 'Base' },
  color: {
    label: 'Digits in sqube',
    scheme: 'Magma'
  },
  marks: [
    Plot.dot(bunch_of_squbes_more_bases, {
      x: 'num',
      y: 'base',
      r: 2,
      fill: 'sqube_perfects',
      sort: { channel: 'fill' },
      tip: true
    })
  ]
})
```

</div>

## Getting smart

Okay, it doesn’t seem feasible to check every single number in every single base. That would take literally forever. We have to make some optimizations.

First, We’re going to be talking about “${tex`n^2`} and ${tex`n^3`}, as represented in base ${tex`b`}" a lot, so I’m going to call that set the <b>sqube</b>.

Second, let's look at that plot again, but this time at the total number of digits in the sqube.

<div class="card">

```js
Plot.plot({
  height: 250,
  width: 1200,
  x: { label: 'Number' },
  y: { label: 'Base' },
  color: {
    label: 'Total digits in sqube',
    scheme: 'Magma'
  },
  marks: [
    Plot.dot(bunch_of_squbes_more_bases, {
      x: 'num',
      y: 'base',
      r: 2,
      fill: (d) => d.sqube_array_len,
      sort: { channel: 'fill' },
      tip: true
    })
  ]
})
```

</div>

Remember if there are too many (or not enough) digits in the sqube, it's impossible to get exactly one of each digit. Let's highlight the spots where the sqube has the correct number of digits.

<div class="card">

```js
Plot.plot({
  height: 250,
  width: 1200,
  x: { label: 'Number' },
  y: { label: 'Base' },
  color: {
    label: 'Correct number of digits',
    domain: [false, true],
    range: ['var(--theme-background)', 'var(--theme-green)']
  },
  marks: [
    Plot.dot(bunch_of_squbes_more_bases, {
      x: 'num',
      y: 'base',
      r: 2,
      fill: (d) => d.sqube_array_len == d.base,
      sort: { channel: 'fill' },
      tip: true
    })
  ]
})
```

</div>

That just eliminated the vast majority of possibilities! Now we only have to search those green lines, where there's just the right number of digits to be possible.

Another thing: notice how there are no green dots in base 6 or 11? We won't have to search those because there's no chance of a nice number in those bases at all.

We just took this problem from "stupid and literally impossible" to "stupid and very difficult". Progress!

## A brief aside

I should probably calrify some things. I did not come up with this problem, nor most of the clever tricks in this post. Most of this came from the exceptional Jacob Cohen, AKA Conflux, and you can read his account of the search for nice numbers over [on his blog](https://beautifulthorns.wixsite.com/home/post/is-69-unique). I am but your humble guide on this safari into the savannah of pointless math, and I beg you indulge me for just a few minutes more.

Also for any pedants: I'm only counting real, positive integers here. That should technically be in the definition, so here you go:

<div class="card inline">
  Revision 2: A number ${tex`n`} in ${tex`\set{ x \in \Reals | x > 0 }`} is nice in base ${tex`b`} if ${tex`n^2`} and ${tex`n^3`}, as represented in base ${tex`b`}, contain every digit of ${tex`b`} exactly once.
</div>

# The search

Let's take a look at what we know so far:

- For most bases there is a single continuous range of numbers where the sqube has the right number of digits to possibly be nice.
- In the remaining bases (6, 11, and more) there are no possible nice numbers.
- The ranges of possible numbers in each base do not overlap.
- Each number is valid in at most one base.

<!--
And let's define a new term to help us generalize a bit:

<div class="card inline">
  A number's <b>niceness</b> is equal to the ratio of unique digits in the square/cube set (the sqube) to the total number of possible digits (the base). A number with niceness equal to 1 is "nice".
</div>
-->

So now when we look at a number, first we'll check if it's in any of those magic ranges for the bases. If it's not, we can toss it right out. If it is, we check which range it's in and work in that base. Those ranges end up being:

<div class="card inline" style="padding: 0 2rem; max-width: 640px;">

| Base | Start | End    |
| ---- | ----- | ------ |
| 10   | 47    | 100    |
| 11   | -     | -      |
| 12   | 144   | 329    |
| 13   | 398   | 609    |
| 14   | 734   | 1138   |
| 15   | 1369  | 3375   |
| 16   | -     | -      |
| 17   | 4913  | 12632  |
| 18   | 15285 | 24743  |
| 19   | 29898 | 48838  |
| 20   | 58945 | 160000 |

</div>

These continue on infinitely, but our search doesn't.

<!-- TODO: Add a card to allow someone to plug in a number, detect the range, and plot it. -->

## How long is this thing, anyways?

How far are we going to have to search before we find another nice number? In order to figure that out we need two pieces of information: how large each base range is, and frequent nice numbers are in that range. We know the first bit, so let's focus on the second.

<div class="card inline">

We don't care what order the unique digits are in, so for a hypothetical nice number in base ${tex`b`}, there are ${tex`b!`} valid (nice) ways the digits can be arranged.

Since there are ${tex`b`} digits in ${tex`b`} possible positions, there are ${tex`b^b`} possible combinations of digits.

Therefore, the probability of a number in base ${tex`b`} being nice is ${tex`b!/b^b`}.

</div>

Let's plot it to see these probabilities! Here's the chance that any specific valid number happens to be nice:

```js
const base_data = []
const base_ticks = [10, 20, 30, 40, 50, 60, 70, 80, 90, 100, 110, 120, 130]
for (let base = 6; base <= 130; base++) {
  const prob = Math.sqrt(2 * Math.PI * base) / Math.exp(base)
  const size = Math.pow(base, base / 5) - Math.pow(base, base / 5 - 1 / 3)
  base_data.push({
    base: base,
    prob: prob,
    size: size,
    total: prob * size
  })
}
```

<div class="card">

```js
Plot.plot({
  height: 200,
  width: 1200,
  x: { label: 'Base', ticks: base_ticks },
  y: { label: 'Probability (%)', percent: true, grid: true },
  marks: [
    Plot.rectY(base_data, {
      x: 'base',
      y: 'prob',
      tip: true
    }),
    Plot.ruleY([0])
  ]
})
```

</div>

Well that doesn't look too good.

## Never tell me the odds

You might think we're at a dead end. The probability of a nice number anywhere past base 16 is zero! There's nothing for us to find!

Thankfully for us, it's not <i>actually</i> zero. It's just so incredibly small that every calculator in the world will round down. (Aren't we having fun yet?)

For completeness's sake, let's show the other half of our equation: the size of each base range.

<div class="card">

```js
Plot.plot({
  height: 200,
  width: 1200,
  x: { label: 'Base', ticks: base_ticks },
  y: { label: 'Total numbers', grid: true },
  marks: [
    Plot.rectY(base_data, {
      x: 'base',
      y: 'size',
      tip: true
    }),
    Plot.ruleY([0])
  ]
})
```

</div>

And then we multiply them to get the probability for there to be any nice number in the range:

<div class="card">

```js
Plot.plot({
  height: 200,
  width: 1200,
  x: {
    label: 'Base',
    ticks: base_ticks
  },
  y: { label: 'Probability of any nice (%)', percent: true, grid: true },
  marks: [
    Plot.rectY(base_data, {
      x: 'base',
      y: 'total',
      tip: true
    }),
    Plot.ruleY([0])
  ]
})
```

</div>

Exponential scaling to the rescue! These ranges are unbelievably massive, and they more than balance out the incredibly small chance that any one number is nice. According to this, there's a very high chance of a nice number past base 120, and maybe even infinitely many out past base 140!

## The downside

Let's see how long it'll take to get to those endless fields of nice numbers...

| Base   | Total Range | Chance of a Nice Number | Time to Search    |
| ------ | ----------- | ----------------------- | ----------------- |
| to 30  | 8.31e+08    | ~0%                     | 72 seconds        |
| to 45  | 8.70e+14    | ~0%                     | 2.4 years         |
| to 65  | 4.27e+23    | 1%                      | 130 years         |
| to 85  | 7.29e+32    | 3%                      | 1.1 million years |
| to 100 | 1.16e+40    | 10%                     | 3.18e25 years     |
| to 110 | 9.41e+44    | 50%                     | 2.58e30 years     |
| to 120 | 9.18e+49    | 100%                    | 2.52e35 years     |

So maybe exponential scaling isn't all that great.

<!--

# Advanced techniques

We can do better!

(TODO: Explain residue class filtering, software optimizations, etc.)

-->

<!--

# What we have so far

```js
const base_data_from_api = FileAttachment('base_data.json').json()
```

So far we've exhaustively searched through base 48, and we have detailed analytics through base 44. We've found no nice numbers, though we did find one number that was surprisingly close (4,134,931,983,708). We've found no specific patterns in digit distribution or niceness, but that doesn't mean we've come away empty-handed.

One metric we gather of each base range is the "niceness", or the ratio of uniques to the base (if the niceness of any number is 1, it's a perfectly nice number). This could be useful to see if there's a pattern of specific bases being "nicer" than others.

-->
