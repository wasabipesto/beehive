# My Discord-Assigned Age & Gender

So Discord can access all of your messages in plaintext, and like any company they're pretty interested in using this data to make more money. They went ahead and ran some messages (at least some of mine) through some sort of model to estimate the sender's demographic information. In my case, they were interested in my age and gender, which are pretty standard metrics to determine my value to potential advertisers.

Unlike most companies they've decided to share their guess about my age and gender with me, let's see how accurate they are.

## The Graphs

I would have expected them to save only the latest (and presumably most accurate) model predictions, but they actually save all model predictions as events. I'm not sure if these predictions are based on messages sent around the time of the event, or if they are running based on the entire message history and fine-tuning the models over time. There is a `model_version` that changes for some of the points, so I believe there's at least some of the latter going on.

```js
const discord = FileAttachment('discord.json').json()
```

```js
Plot.plot({
  title: 'My Discord-Assigned Age',
  x: { type: 'utc' },
  y: { grid: true, percent: true },
  color: { legend: true },
  marks: [
    Plot.line(
      discord.filter((i) => i.stat == 'Age'),
      { x: 'date', y: 'value', stroke: 'label', tip: true }
    )
  ]
})
```

```js
Plot.plot({
  title: 'My Discord-Assigned Gender',
  x: { type: 'utc' },
  y: { grid: true, percent: true },
  color: { legend: true },
  marks: [
    Plot.line(
      discord.filter((i) => i.stat == 'Gender'),
      { x: 'date', y: 'value', stroke: 'label', tip: true }
    )
  ]
})
```

I find these charts very funny. According to Discord I reached peaked femininity around Christmas 2022 (at a measly 33%). It also coincided with a rapid aging, followed by a surprising return to youthfulness until early October when my curse of old age returned. Thankfully I've been under 34 ever since and my joints have never felt better.

It has correctly identified the fact I am not a teenager. In fact, many are convinced that I never was.

Their label for non-binary is also very amusing to me: `prob_non_binary_gender_expansive`. Like, yes we acknowledge that non-binary isn't just a third gender category to sort people into. That's why we stuck "gender expansive" on the third gender category we're sorting people into.

I have no idea how Discord is actually using this data. Personally I think it's fun to peek behind the curtain and see what companies are doing with my personal information, and in the end they will continue to do whatever they want. I'll continue to enjoy using Discord and I don't have any plans to stop using it because of this. Lack of privacy is part of the trade-off in using a platform like this one.

## How to learn what Discord thinks about you

As of summer 2024 this process was fairly straightforward. I believe you need to have the "Use data to improve Discord" setting turned on, but it's an opt-out and you probably forgot to turn it off anyways.

1. In the Discord app, go to Settings > Data & Privacy > Request all of my data.
2. Select at least the Activity section. You can select others but it will increase the amount of time before you get your data export. Hit Submit.
3. Wait 2-4 weeks.
4. Open up your `package.zip` and navigate to `activity` > `analytics` > `events-2024-XXXX...`.
5. Open it up and search for `predicted_gender` or `predicted_age`.
