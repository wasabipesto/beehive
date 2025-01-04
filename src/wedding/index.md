# Our Wedding

## Original Plans

On a beach in Boston in 2019, my girlfriend proposed to me. We each knew the other had plans to propose that year, but she beat me to it. That winter, I had the perfect moment to propose back at her. Obviously we both said yes. That winter we started planning our big day.

In January of 2020 we found a beautiful venue and set our date for January of 2021.

Then covid hit.

We held onto our already-printed invitations for a few months before officially postponing the wedding in October 2020. In the meantime we had a tiny wedding in my parents’ backyard so we could file taxes as a married couple.

Finally, on a beautiful day in September 2023, we were finally able to have the big wedding we had originally planned.

# The Actual Wedding

Our wedding was amazing, the day was less stressful than I expected, and it seemed like everyone had a lot of fun. How did we do it?

## People

We originally estimated 120 guests for the purposes of venue selection. There seems to be a cutoff for a lot of venues around 100 guests and we wanted to keep our venue options open to avoid feeling restricted when inviting people.

When we actually put together an invitation list in early 2023, the number of people we interacted with regularly had dropped. We ended up inviting only 90 people, several of which we knew would not be able to attend.

```js
const invites = [
  {
    side: "Groom's Side",
    response: 'Yes',
    count: 40
  },
  {
    side: "Groom's Side",
    response: 'No',
    count: 12
  },
  {
    side: "Bride's Side",
    response: 'Yes',
    count: 22
  },
  {
    side: "Bride's Side",
    response: 'No',
    count: 15
  }
]
```

```js
Plot.plot({
  title: 'Invitation Responses',
  marginLeft: 80,
  x: { grid: true, label: 'invitations' },
  y: { label: null },
  marks: [
    Plot.barX(invites, {
      y: 'side',
      x: 'count',
      fill: (i) => (i.response == 'Yes' ? 'currentColor' : '#ba2f36'),
      channels: { response: 'response' },
      tip: { format: { fill: false } }
    }),
    Plot.ruleX([0])
  ]
})
```

Out of the 90 invitations, we had 62 able to attend. This is around 70%, a fair bit lower than the rule of thumb at 80%. My family is a bit larger than my wife's, so the approximate breakdown by each side was something we had guessed in advance.

We ended up with 71 catering plates to accommodate ourselves, the photographers, and some extra helpers. Gotta make sure everyone has food!

I feel like 60-80 guests is my ideal sweet spot. It's small enough to be able to chat with everyone without having to rush or exclude people. There's several people I'm sad weren't able to make it on both sides.

## Budget

```js
const budgets = [
  {
    item: 'Caterer',
    cost: 7590
  },
  {
    item: 'Venue',
    cost: 5000
  },
  {
    item: 'Photographer',
    cost: 2350
  },
  {
    item: 'Coordinator',
    cost: 750
  },
  {
    item: 'Rings',
    cost: 600
  },
  {
    item: 'Gifts',
    cost: 600
  },
  {
    item: 'Clothing',
    cost: 400
  },
  {
    item: 'Decorations',
    cost: 400
  },
  {
    item: 'Florist',
    cost: 150
  }
]
```

```js
Plot.plot({
  title: 'Top-Level Wedding Costs',
  marginLeft: 80,
  x: { grid: true, label: 'cost' },
  y: { label: null },
  marks: [
    Plot.barX(budgets, { y: 'item', x: 'cost', tip: true, sort: { y: '-x' } }),
    Plot.ruleX([0])
  ]
})
```

Our total direct cost for the wedding was right around $18,000. There's a few things not included here, so when people ask how much it costs I tell them to budget for $20,000.

I think we got a lot of value out of this budget, and while it's a ton of money I think it would be difficult to do a similar wedding for less. Some notes about each item:

- We picked our caterer specifically for their vegetarian, gluten-free, and allergen-sensitive selections. I feel like they could have done better with the service and they were the least communicative during the day, but I still feel like they were a good choice.
- The venue was cheaper than most of the alternatives we looked at but was easily our favorite. A huge bonus was the fact that we didn't need basically any decorations. I feel like we got a great deal for both the location and timeframe - they let us keep our deposit and original pricing from 2020 when we first approached them.
- The photographer, coordinator, and florist were all friends that we asked to help. The photographer shoots weddings regularly and we paid her normal rates, but the coordinator and florist did us huge favors and each should easily have cost $1000 more for their regular services.
- Typical wedding rings and clothing are wildly overpriced. We bought the rings and dress online, both were good quality and served us well.

```js
const catering = [
  {
    item: 'Dinner Package',
    type: 'Food & Drink',
    cost: 2059,
    sort: 101
  },
  {
    item: 'Iced Tea & Lemonade',
    type: 'Food & Drink',
    cost: 213,
    sort: 102
  },
  {
    item: 'Gelato',
    type: 'Food & Drink',
    cost: 426,
    sort: 103
  },
  {
    item: 'Buffet China',
    type: 'Servingware & Linen',
    cost: 284,
    sort: 201
  },
  {
    item: 'Gelato Servingware',
    type: 'Servingware & Linen',
    cost: 106,
    sort: 202
  },
  {
    item: 'Chair Cushions - Ceremony',
    type: 'Servingware & Linen',
    cost: 276,
    sort: 301
  },
  {
    item: 'Chair Cushions - Reception',
    type: 'Servingware & Linen',
    cost: 284,
    sort: 302
  },
  {
    item: 'Chair Cushions - Delivery',
    type: 'Servingware & Linen',
    cost: 100,
    sort: 303
  },
  {
    item: 'Linens - Eating Tables',
    type: 'Servingware & Linen',
    cost: 300,
    sort: 401
  },
  {
    item: 'Linens - Serving Tables',
    type: 'Servingware & Linen',
    cost: 210,
    sort: 402
  },
  {
    item: 'Linens - Napkins',
    type: 'Servingware & Linen',
    cost: 280,
    sort: 403
  },
  {
    item: 'Labor - Event Manager',
    type: 'Labor',
    cost: 374,
    sort: 501
  },
  {
    item: 'Labor - Chef',
    type: 'Labor',
    cost: 250,
    sort: 502
  },
  {
    item: 'Labor - Servers (6)',
    type: 'Labor',
    cost: 1782,
    sort: 503
  },
  {
    item: 'Labor - Delivery',
    type: 'Labor',
    cost: 35,
    sort: 504
  },
  {
    item: 'Taxes',
    type: 'Taxes',
    cost: 582,
    sort: 999
  }
]
```

```js
Plot.plot({
  title: 'Detailed Catering Costs',
  marginLeft: 120,
  x: { grid: true, label: 'cost' },
  y: { label: null },
  marks: [
    Plot.barX(catering, {
      y: 'type',
      x: 'cost',
      fill: 'item',
      sort: { y: '-x' },
      tip: true
    }),
    Plot.ruleX([0])
  ]
})
```

Our marginal cost per plate from the caterer was around $100. There were some fixed costs, such as the delivery and the event manager's time. We also had the caterer provide the chair cushions for both the ceremony and reception so that they would match the linen colors.

All said, I think the costs were reasonable given our requirements. We got some good deals on some parts and paid full price on others, and I'm not sure how we could have saved any more money reasonably.

## Timeline

Time is very important on the day, probably the most important thing - to the point that having a coordinator that can keep you on schedule will save you hours.

When making a schedule, be sure to keep in mind that not everyone is doing the same thing. You will want to have separate timelines for the bride and groom, for the wedding parties, for the friends and family who show up early to help, for the guests, and for all of the contractors. A true coordinator will have a million things on those schedules and know which are important to hit and which can fall behind if necessary.

Distilling all of that down to just the bride, groom, and wedding party's activities on the day, here's how we spent our 12 hours in the venue.

```js
const timeline = [
  {
    item: 'Arrival, Unloading',
    type: 'Decoration & Prep',
    time: 30,
    sort: 101
  },
  {
    item: 'Early Decorations',
    type: 'Decoration & Prep',
    time: 90,
    sort: 102
  },
  {
    item: 'Lunch',
    type: 'Social',
    time: 30,
    sort: 103
  },
  {
    item: 'Getting Ready',
    type: 'Decoration & Prep',
    time: 90,
    sort: 201
  },
  {
    item: 'Pre-Ceremony Photography',
    type: 'Photography',
    time: 60,
    sort: 202
  },
  {
    item: 'Pre-Ceremony Chill',
    type: 'Social',
    time: 30,
    sort: 203
  },
  {
    item: 'Ceremony',
    type: 'Ceremony',
    time: 15,
    sort: 301
  },
  {
    item: 'Family Photos',
    type: 'Photography',
    time: 45,
    sort: 302
  },
  {
    item: 'Couple Photos',
    type: 'Photography',
    time: 30,
    sort: 303
  },
  {
    item: 'Dinner',
    type: 'Social',
    time: 90,
    sort: 401
  },
  {
    item: 'Mingling',
    type: 'Social',
    time: 45,
    sort: 402
  },
  {
    item: 'Evening Photos',
    type: 'Photography',
    time: 45,
    sort: 501
  },
  {
    item: 'Clean Up',
    type: 'Decoration & Prep',
    time: 120,
    sort: 502
  }
]
```

```js
Plot.plot({
  title: 'Day-of Timeline',
  marginLeft: 120,
  x: { grid: true, label: 'minutes' },
  y: { label: null },
  marks: [
    Plot.barX(timeline, {
      y: 'item',
      x: 'time',
      //fill: 'item',
      channels: { sort: 'sort' },
      sort: { y: 'sort' },
      tip: true //{ format: { sort: null } }
    }),
    Plot.ruleX([0])
  ]
})
```

```js
Plot.plot({
  title: 'Schedule Budget',
  marginLeft: 120,
  x: { grid: true, label: 'minutes' },
  y: { label: null },
  marks: [
    Plot.barX(timeline, {
      y: 'type',
      x: 'time',
      fill: 'item',
      sort: { y: '-x' },
      tip: true
    }),
    Plot.ruleX([0])
  ]
})
```

## Advice

We ignored a lot of traditional wedding advice, but I think we did so strategically. My mindset regarding changes was:

- Create a list of which typical events you (both) are interested in, which you are okay with, and which you would prefer not to do.
- Your average guest has a mental plan of events for the wedding. Do your best to understand what that is before you start changing things.
- Each change you make from the default "traditional" wedding will have some impact. There's not a good way to quantify this, but try to imagine how non-traditional of a wedding you would be comfortable with and use this as a "budget" of possible changes.
- For events you remove, try to understand its purpose or value and find an alternative that can fulfill that. You'll find that many events don't serve a purpose at all.
- For events you are on the fence about, see if you can add flexibility to the schedule to give you an out on the day of. This is especially good for photographs in case you need to duck out early to chill.
- At the end of the day, weigh your own preferences 5-10 times higher than your guests. Not an overwhelming amount, but significantly more than you might expect.

Some examples of this strategy:

- We had a very short, non-religious ceremony. I knew religion was very important to my family but a non-religious ceremony was very important to both of us. Our preferences significantly outweighed the tradition. As for length, we didn't want anything to feel like filler. I think this is an objectively good decision since it keeps the focus on the vows.
- We only had two dances at the reception, and no open dancing. I'm sure lots of people would have enjoyed dancing, but it makes me very uncomfortable and I veto'd it. (My wife had to fight for the dances that we did have.)
- Neither of us are huge fans of cake, so we got gelato for dessert. Cake is traditional but is commonly changed, so it was an easy change to make. It was also a huge hit with guests and got us out of the "slicing the cake" tradition.
- We sat at a long table with our wedding party for the reception instead of our own table. We knew we would be exhausted and would rather listen to our friends talk than chat between ourselves. This is technically against tradition, but nobody ever seems to care.

Other miscellaneous advice:

- Get married in advance! A wedding is both a huge commitment and a stressful party. If you do all of the legal stuff in advance, you can just focus on the party.
- Don’t gender-segregate the parties if you don’t want to. I wanted my sister on my side of the aisle so instead of Bridesmaids and Groomsmen we had the Bride’s Party and Groom’s Party.
- Make a list of photographs you want in rough order of priority. Know exactly which family group shots you want and in which order. Scout out good photo locations around the venue in advance. That way when you get to your lower-priority shots you can quit early if you want.
- Type out everything in as clear a fashion as possible - a list of names and phone numbers, a timeline of events, seating arrangements, decoration guides, and anything else you can think of. Print multiple copies and have them around so other people can answer their own questions.
- Specifically ask your guests not to film or photograph the ceremony if you’re already paying for a photographer and/or videographer. Nobody likes having to peer around someone else’s phone.
- Also include in the program if there’s anything else you do/don’t want your guests to do. We asked them not to clink their glasses or give any impromptu speeches. Great decision.
