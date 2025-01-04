# Work Emails

> basically in corporate you either have email job or you have excel job. sometimes you have meeting job. sometimes it could be all 3. but thats it
>
> \- [averagefairy, tumblr 2024](https://www.tumblr.com/averagefairy/741216509642326016)

I think my job is around 70% excel, 30% email. Most of my meetings are actually emails, and some of my emails are actually excel.

## Over time

```js
const emails = FileAttachment('emails.csv').csv({ typed: true })
const recipients = FileAttachment('recipients.csv').csv({ typed: true })
```

```js
const sent = emails.filter((i) => i.Type == 'Sent')
const received = emails.filter((i) => i.Type == 'Received')
const emails_since_may = emails.filter((i) => i.Date > new Date('2024-05-01'))
```

Let's look at the emails I sent over the last 3 years:

```js
Plot.plot({
  title: 'Emails Sent per Month',
  subtitle: 'Since November 2021',
  y: { grid: true, label: 'emails' },
  marks: [
    Plot.rectY(
      sent,
      Plot.binX({ y: 'count' }, { x: { interval: 'month', value: 'Date' }, tip: true })
    ),
    Plot.ruleY([0])
  ]
})
```

I only have the past few months of received emails, but they look something like this:

```js
Plot.plot({
  title: 'Emails Received per Week',
  subtitle: 'Since May 2024',
  y: { grid: true, label: 'emails' },
  marks: [
    Plot.rectY(
      received,
      Plot.binX({ y: 'count' }, { x: { interval: 'week', value: 'Date' }, tip: true })
    ),
    Plot.ruleY([0])
  ]
})
```

That's about three times more emails received than sent (on average). To compare:

```js
Plot.plot({
  title: 'Emails Sent and Received per Week',
  subtitle: 'Since May 2024',
  y: { grid: true, label: 'emails' },
  color: { legend: true, scheme: 'Paired' },
  marks: [
    Plot.rectY(
      emails_since_may,
      Plot.binX({ y: 'count' }, { x: { interval: 'week', value: 'Date' }, fill: 'Type', tip: true })
    ),
    Plot.ruleY([0])
  ]
})
```

At around 150 emails (sent and received) per week, comprising around 30% of my work, we can determine that my total job is a worth a little over 500 email-equivalents per week. At my current salary that's around $3.27 per email-equivalent.

## Recipients

Who did I email? I've ranked the top 50 users I corresponded with, along with if they were internal to my company or external users.

```js
Plot.plot({
  title: 'Top Email Recipients',
  subtitle: 'Since November 2021',
  x: { ticks: [], label: 'rank' },
  y: { grid: true, label: 'emails' },
  color: { legend: true, scheme: 'Paired' },
  marks: [
    Plot.rectY(recipients, { x: 'Rank', y: 'Count', fill: 'Company', tip: true }),
    Plot.ruleY([0])
  ]
})
```

The top entry here is my direct boss, who I emailed (or CC'd) over 350 times in 3 years. That's honestly less than I expected.
