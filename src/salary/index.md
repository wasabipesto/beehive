# Salary Transparency

A number of people I know have started sharing their salary publicly. I think this is a good thing because more public data allows people to make better decisions about their careers.

> As someone who has seen pay discrimination work in action first-hand, data is one of the ways that we can end this pointless hiding of information that leads to people being uninformed and hurt by their lack of knowledge. By laying my hand out in the open like this, I hope to ensure that people are better informed about how much money they can make, so that they can be paid equally for equal work.
>
> \- [Xe Iaso, xeiaso.net](https://xeiaso.net/salary-transparency/)

## My Salary

I've decided to share my current salary here, as well as my past compensation in previous roles. I plan to keep this up to date as my situation changes.

Of course, this information does not include all variables. The construction industry varies wildly across the US and is unrecognizable in other countries. Reach out to me if you're interested in speaking more about the numbers listed here or other methods of compensation in the field.

```js
let salary = FileAttachment('salary.json').json()
```

```js
Inputs.table(salary, {
  maxWidth: 640,
  layout: 'auto',
  columns: ['title', 'start', 'end', 'pay_description', 'leave_reason'],
  header: {
    start: 'Start',
    end: 'End',
    title: 'Title',
    pay_description: 'Pay Description',
    leave_reason: 'Leave Reason'
  },
  select: false,
  sort: 'start',
  reverse: true
})
```

We can plot these on a graph to see how they've changed over time. You can see the initial period of time I was an intern, followed by the jump to my first full-time position and subsequent moves/raises.

```js
Plot.plot({
  title: 'Salary over Time',
  marginLeft: 60,
  x: { type: 'utc' },
  y: { label: 'dollars', grid: true },
  marks: [
    Plot.line(salary, {
      x: 'start',
      y: 'pay_yearly',
      curve: 'step-after',
      channels: {
        Start: 'start',
        'Yearly Pay': 'pay_yearly',
        Title: 'title'
      },
      tip: true
    }),
    Plot.ruleY([0])
  ]
})
```

## Inflation

We can use the [Consumer Price Index](https://fred.stlouisfed.org/series/CPIAUCSL#0) to calculate the purchasing power of my salary over time. It tracks a number of consumer goods, including food, clothing, shelter, and fuels. If the CPI goes up by 10%, that means the weighted average of those items have gone up by 10% and that the purchasing power of my salary has gone down by 10%.

```js
let cpi = FileAttachment('cpi.json').json()
```

Here's the raw index since 2000, for reference:

```js
Plot.plot({
  title: 'Consumer Price Index',
  height: 200,
  x: { type: 'utc' },
  y: { label: null, grid: true },
  marks: [
    Plot.line(cpi, {
      x: 'date',
      y: 'value',
      curve: 'step-after',
      tip: true
    }),
    Plot.ruleY([0])
  ]
})
```

We're more interested in the relative change in the CPI over time. In the chart below, a positive value shows inflation while a negative value shows deflation.

```js
Plot.plot({
  title: 'Consumer Price Index',
  subtitle: 'Monthly Delta',
  height: 200,
  x: { type: 'utc' },
  y: { label: null, grid: true },
  marks: [
    Plot.line(cpi, {
      x: 'date',
      y: 'delta',
      curve: 'step-after',
      tip: true
    }),
    Plot.ruleY([0])
  ]
})
```

If we zoom into the period where I have been working, we can adjust my compensation by this index to show my salary in January 2020 dollars:

```js
// Replace final end date with today's date
let last_salary_item = salary[salary.length - 1]
if (last_salary_item.end === null) {
  last_salary_item.end = new Date().toISOString().split('T')[0]
}

// Copy of CPI values since salary start
const cpi_recent_start = '2018-05-01'
let cpi_recent = cpi.filter((entry) => entry.date >= cpi_recent_start)

// Baseline CPI to reference against
// const cpi_refdate = '2020-01-01' // based off input
const cpi_refdate_label = cpi_refdate + ' dollars'
const cpi_refvalue = cpi.find((entry) => entry.date === cpi_refdate)?.value

let adjusted_data = []
for (const month of cpi_recent) {
  // Find the current salary based on the date range
  const current_salary = salary.find(
    (s) => new Date(s.start) <= new Date(month.date) && new Date(month.date) <= new Date(s.end)
  )?.pay_yearly

  if (!current_salary) {
    console.warn(`No salary found for month: ${month.date}`)
    continue // Skip months without a salary range
  }

  // Add unadjusted entry
  adjusted_data.push({ ...month, adj: 'No Adjustment', pay_yearly: current_salary })

  // Add adjusted entry
  const adjusted_pay = (current_salary * cpi_refvalue) / month.value
  adjusted_data.push({ ...month, adj: cpi_refdate_label, pay_yearly: adjusted_pay })
}
```

```js
Plot.plot({
  title: 'Salary over Time',
  subtitle: 'Adjusted for inflation',
  x: { type: 'utc' },
  y: { label: 'dollars', grid: true },
  color: { label: 'adjustment', legend: true },
  marks: [
    Plot.line(adjusted_data, {
      x: 'date',
      y: 'pay_yearly',
      stroke: 'adj',
      curve: 'step-after',
      channels: {
        'yearly pay': 'pay_yearly'
      },
      tip: true
    }),
    Plot.ruleY([0])
  ]
})
```

<style>
.inline {
  max-width: 640px
}
</style>

<div class="card inline">

Change this date to show the salary over time in today's dollars, or compare against any other year.

```js
const cpi_refdate = view(
  Inputs.select(
    cpi
      .map((i) => i.date)
      .filter(
        (date, index, array) =>
          date.includes('01-01') || // first of the year
          index === array.length - 1 // most recent
      ),
    {
      value: '2020-01-01',
      label: 'Reference Date'
    }
  )
)
```

</div>

With this view you can see that my regular raises in 2022-2024 were just barely keeping up with inflation. The rule of thumb used to be 5% per year was enough to keep up with inflation, but that hasn't been the case recently.

The data shown here does not include bonuses, benefits, or any other incentives. It only includes pay from my main job and is not intended as a proper accounting of wealth.

---

> Please consider publishing your salary data like this as well. By open, voluntary transparency we can help to end stigmas around discussing pay and help ensure that the next generations of people in tech are treated fairly. Stigmas thrive in darkness but wither and die in the light of day. You can help end the stigma by playing your cards out in the open like this.
>
> \- [Xe Iaso, xeiaso.net](https://xeiaso.net/salary-transparency/)
