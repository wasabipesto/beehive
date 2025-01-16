# Spending Budget

How do we spend money? Where does it go?

```js
const rawexpenses = FileAttachment('expense-log.csv').csv({ typed: true })
const budget = FileAttachment('income-budget.csv').csv({ typed: true })
const utilities = FileAttachment('utilities.csv').csv({ typed: true })
const electricity = FileAttachment('electricity.csv').csv({ typed: true })
```

```js
const expenses = rawexpenses.filter((i) => i.Category !== 'Other')
```

I've tracked our monthly spending for a few years now, since we moved into our current house. I don't use a budget manager, though I've heard Actual and YNAB are quite handy. What I've ended up doing is just grabbing the CSV file exports from my banks, tossing them in a big spreadsheet, and using a couple ill-advised `VLOOKUP` functions to auto-sort and categorize each expense. It's worked well for me for years and I don't plan on changing systems anytime soon.

The data here includes my budget and expenses up to ${new Date(FileAttachment('expense-log.csv').lastModified).toLocaleDateString('en-US', { month: 'long', day: 'numeric', year: 'numeric' })}.

## The Categories

I do my best to categorize expenses in the following categories:

- Housing, including our loan payments, home insurance, and any other structural expenses.
- Utilities, for electricity, gas, water, sewage, and any other regularly-paid necessity.
- Groceries, food for cooking and eating at home. This can also include some home goods that would typically fall under Household if we buy them at the grocery store.
- Household, which covers clothes, toiletries, and many other non-food consumables. This will also include expenses relating to our animals, such as vet bills or cat food.
- Restaurants, covering any pre-made meal. This ties in very closely with Entertainment, but I track it separately since I have a lot of expense here from work lunches that aren't entertainment.
- Entertainment, covering anything fun that my wife and I do together. We sometimes refer to this as our Date Budget, but it can include fun things for home as well.
- Transport, mainly for costs relating to our car. Gas, oil, maintenance, tolls, parking, etc.
- Projects, which is kinda messy:

> The Project bucket is intended for large, seasonal ("spiky") purchases for specific projects. When we first bought our house we had a list of projects we wanted to complete. For each one, we would come up with a timeframe and a budget, then schedule them out based on when we would have saved up enough to take them on. Our budget for this was originally $600, so if a project would cost around $2000 we would schedule it for about 4 months out, then a $1200 one 2 months after that. This let us set aside money for specific improvements we wanted to tackle and establish a plan for when they could be done, and it worked quite well! An additional use we found for this was Christmas - we could simply schedule a "Christmas" project every year for December with a budget of $1500, which would cover all of our gifts, food, and travel for the holidays.
>
> As we've completed all of our big projects over time, this has become a bit more of a catch-all than I would like. There are many expenses that end up in this bucket that might be better suited to Household - small home improvement items, furniture, etc. Many Amazon purchases also get automatically categorized under Projects, which muddies the categories a bit. The bulk of the expenses, however, are still large, one-time expenses that meet the spirit of the thing.

In addition to those discretionary budgets, I show the following "categories" that are automatically deducted from my paycheck:

- Taxes, self-explanatory.
- Healthcare, covering medical and dental premiums, along with our HSA contributions.
- Retirement, a Roth IRA with medium-risk investments.
- Savings, automatically deposited in a separate savings account.
- Allowances, automatically deposited in my and my wife's personal checking accounts. We're allowed to use this money for whatever we want without justification.

## Spending

How closely do we stick to our budget? Let's look at our average monthly spending and the budget for each.

```js
const first_date = new Date(expenses[0].Date)
const last_date = new Date(expenses[expenses.length - 1].Date)
const num_months = (last_date - first_date) / (1000 * 60 * 60 * 24 * 30)

let newbudget = []
budget.forEach((item) => {
  const total_spent = expenses
    .filter((expense) => expense.Category === item.Category)
    .reduce((sum, expense) => sum + expense.Amount, 0)
  let monthly_avg = total_spent / num_months

  newbudget.push({
    Category: item.Category,
    Amount: item.Amount,
    Type: 'Budget',
    Subtype: 'Budget'
  })

  if (total_spent > 0) {
    newbudget.push({
      Category: item.Category,
      Amount: monthly_avg,
      Type: 'Spent',
      Subtype: 'Spent (Discretionary)'
    })
  } else {
    newbudget.push({
      Category: item.Category,
      Amount: item.Amount,
      Type: 'Spent',
      Subtype: 'Spent (Automatic)'
    })
  }
})
```

```js
Plot.plot({
  title: 'Monthly Budget & Utilitization',
  marginBottom: 80,
  fx: { padding: 0, label: 'Category', tickRotate: -45, tickSize: 6 },
  x: { axis: null, paddingOuter: 0.2 },
  y: { label: 'Dollars', grid: true },
  color: { legend: true },
  marks: [
    Plot.barY(newbudget, {
      fx: 'Category',
      x: 'Type',
      fill: 'Subtype',
      y: 'Amount',
      sort: { fx: '-y' },
      tip: {
        format: {
          x: null,
          fill: null
        }
      }
    }),
    Plot.ruleY([0])
  ]
})
```

You can see our top expenditures are taxes and housing, together taking around 35% of our budget. Beyond that we have our project budget, which is over-utilized, followed by groceries and healthcare which are coincidentally the same proportion of our budget. Further down you can see restaurants which are over-utilized, and entertainment which is under-utilized.

Unfortunately this chart a little misleading - it makes us look great at sticking exactly to our budgeted amounts. For one, it includes the automatic spending which will always be spot-on to the budgets. Second, we adjust our budgets over time to accommodate changes in our spending habits (and we just completed another one of those), so it's more descriptive than prescriptive.

How good are we at maintaining a _consistent_ budget?

```js
Plot.plot({
  title: 'Expenses per Category',
  subtitle: '3-month intervals',
  y: { grid: true },
  color: { legend: true },
  marks: [
    Plot.rectY(
      expenses,
      Plot.binX(
        { y: 'sum' },
        {
          x: { interval: '3 months', value: 'Date' },
          y: 'Amount',
          fill: 'Category',
          tip: true
        }
      )
    ),
    Plot.ruleY([0])
  ]
})
```

We're actually quite good, but the naturally-spiky Projects budget throws a wrench in the visualization. Here's the same plot without that item:

```js
Plot.plot({
  title: 'Expenses per Category',
  subtitle: '3-month intervals, excluding projects',
  y: { grid: true },
  color: { legend: true },
  marks: [
    Plot.rectY(
      expenses.filter((i) => i.Category !== 'Projects'),
      Plot.binX(
        { y: 'sum' },
        {
          x: { interval: '3 months', value: 'Date' },
          y: 'Amount',
          fill: 'Category',
          tip: true
        }
      )
    ),
    Plot.ruleY([0])
  ]
})
```

Each budget item seems to follow its own rough cycle through the year, though there are some overall trends. You can see a gradual trend upwards, especially since mid-2023, but it's washed out completely by how wildly variable the Projects budget is.

## Transaction Amounts

I love histograms and box plots, so I had to throw this one in. How large are each of our individual transactions?

```js
Plot.plot({
  title: 'Histogram of Transaction Amounts',
  height: 200,
  x: { label: 'Dollars', grid: true },
  y: { label: 'Category' },
  marks: [
    Plot.rectY(expenses, Plot.binX({ y: 'count' }, { x: 'Amount', tip: true })),
    Plot.ruleX([0])
  ]
})
```

Mostly pretty small, less than $100. What about if we broke that down per category?

```js
Plot.plot({
  title: 'Transaction Amounts per Category',
  marginLeft: 80,
  x: { label: 'Dollars', grid: true },
  y: { label: 'Category' },
  marks: [
    Plot.boxX(expenses, {
      y: 'Category',
      x: 'Amount',
      sort: {
        y: '-x'
      }
    }),
    Plot.ruleX([0])
  ]
})
```

Obviously our mortgage payments are pretty big and pretty consistent. There are a lot of huge project expenses, as expected. A lot of the rest seem to have a median cost less than $100 - let's zoom in there.

```js
Plot.plot({
  title: 'Transaction Amounts per Category',
  subtitle: 'Transactions less than $1,000',
  marginLeft: 80,
  x: { label: 'Dollars', grid: true },
  y: { label: 'Category' },
  marks: [
    Plot.boxX(
      expenses.filter((i) => i.Amount < 1000),
      {
        y: 'Category',
        x: 'Amount',
        sort: {
          y: '-x'
        }
      }
    ),
    Plot.ruleX([0])
  ]
})
```

Groceries are at the top of the list here, due to lots of $100-150 weekly shopping trips. Utilities are also consistently high, with some summer cooling bills around $250. Entertainment and Restaurant sit at the bottom here, which makes sense. Apparently I've only spent more than $120 at a restaurant on very rare occasions!

## Utilities

Next, let's break down that single utilities number into what we're actually paying for. Note that not all of these expenses may seem like traditional utilities, but we categorize them all in this bucket because they're regular expenses for services we expect to have available for the home. It's also beneficial for us to be able to plan ahead and expect that these costs will continue at approximately the same monthly rate for the foreseeable future.

```js
Plot.plot({
  title: 'Monthly Utility Spending',
  height: 300,
  marginBottom: 110,
  x: { label: 'Category', tickRotate: -45, tickSize: 6 },
  y: { label: 'Dollars' },
  color: { legend: true },
  marks: [
    Plot.barY(utilities, {
      x: 'Category',
      y: 'Amount',
      sort: { x: '-y' },
      tip: true
    }),
    Plot.ruleY([0])
  ]
})
```

I was quite surprised that our sewer connection costs significantly more than our clean water every month! It's also interesting that our electricity bill is significantly higher than anything else - even our home insurance.

Since our electricity costs are so high, let's dig into those even further. I anticipate that our electricity bill is periodic though the year, let's check that.

```js
Plot.plot({
  title: 'Monthly Electricity Spending',
  subtitle: 'Layered year over year',
  height: 300,
  x: { label: 'Month' },
  y: { label: 'Dollars', grid: true },
  color: { legend: true, type: 'ordinal', scheme: 'Observable10', label: 'Year' },
  marks: [
    Plot.line(electricity, {
      x: (i) => new Date(i.Date).getMonth(),
      y: 'Amount',
      stroke: (i) => new Date(i.Date).getFullYear().toString(),
      tip: {
        format: {
          z: null
        }
      }
    }),
    Plot.ruleY([0])
  ]
})
```

It seems like it might correspond to exterior temperature somewhat, but there's a high base load from our oven, dryer, and other appliances, not to mention servers and other computers. There's also not enough data to really build a good box plot since we've only been here for a few years. I'll have to check back in once we have more data!

<!--
TODO:
- Correlate electricity pricing with temperature
- Show gas/water usage as well
-->
