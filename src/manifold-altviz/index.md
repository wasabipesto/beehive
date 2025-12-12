<!--
Docs:
- Observable Framework: https://observablehq.com/framework/getting-started
- Observable Plot: https://observablehq.com/plot/features/plots
- Manifold API: https://docs.manifold.markets/api
-->

# Some Alternative Manifold Visualizations

Go ahead and paste a market link here:

```js
// Accept user input for a market
const input_url = view(
  Inputs.text({
    label: "Manifold URL",
    placeholder: "https://manifold.markets/...",
    //value: "https://manifold.markets/PaperBoy/how-long-will-the-government-shutdo"
    value: "https://manifold.markets/SG/humanitys-last-exam-score-in-2025"
  })
);
```

```js
// const input_url = view(Inputs.select(["https://manifold.markets/SG/humanitys-last-exam-score-in-2025"], {label: "Selected Market"}));
```

```js
const answer_data = FileAttachment("./answers.json").json();
```

```js
// Get the market slug and fetch market data
const market_slug = input_url.split("/").pop();
const market = await fetch(`https://api.manifold.markets/v0/slug/${market_slug}`).then(res => res.json());
```

```js
// Numeric markets don't include answers, fetch them separately
async function getNumericAnswers(market) {
  const response = await fetch(`https://api.manifold.markets/markets-by-ids?ids[]=${market.id}`).then(res => res.json());
  return response[0].answers;
}
if (market.outcomeType === "MULTI_NUMERIC") {
  market.answers = await getNumericAnswers(market);
}
```

```js
/*
// Convert answers to a map for easy lookup
let answerMap = new Map();
if (market.answers) {
  answerMap = new Map(market.answers.map(a => [a.id, a]));
}
*/
```

```js
const answerMap = answer_data[market.id].answer_details
```

```js
// Fetch all bets for the market
async function getBets(market_slug) {
  let bets = []
  let before = null
  while(true) {
    const url = `https://api.manifold.markets/v0/bets?contractSlug=${market_slug}&includeZeroShareRedemptions=true` + (before ? `&before=${before}` : '');
    const response = await fetch(url);
    const data = await response.json();
    if (!data.length) break;
    bets.push(...data);
    before = data[data.length - 1].id;
  }
  return bets;
}
const bets = await getBets(market_slug);
```

```js
// Convert a series of bets to probability segments
function betsToProbSegments(bets, endDate) {
    // Convert endDate to Date object
    endDate = new Date(endDate);
    // Sort bets by time
    bets.sort((a, b) => a.createdTime - b.createdTime);
    // Initialize segments array
    let segments = [];
    // Iterate over bets
    for (let i = 0; i < bets.length; i++) {
        // Get current bet
        let bet = bets[i];
        // Get current bet time
        let startTime = new Date(bet.createdTime);
        // Get current bet prob
        let prob = bet.probAfter;
        // Get next bet
        let nextBet = bets[i + 1];
        // Get the next bet time
        let nextBetTime = nextBet ? new Date(nextBet.createdTime) : endDate;
        // Calculate duration (ms)
        let durationMs = nextBetTime.getTime() - startTime.getTime();
        // Add segment to array
        segments.push({
            startTime: startTime,
            endTime: nextBetTime,
            durationMs: durationMs,
            prob: prob,
        });
    }
    // Return segments array
    return segments;
}
```

```js
// Calculate the average probability for the segments within the specified time range
function getAverageProbability(probSegments, start, end) {
    // Initialize total probability and duration
    let totalProb = 0;
    let totalDuration = 0;
    // For each segment...
    probSegments.forEach(segment => {
        // Calculate the overlap between segment and the specified time range
        let overlapStart = Math.max(segment.startTime.getTime(), start.getTime());
        let overlapEnd = Math.min(segment.endTime.getTime(), end.getTime());

        // Skip segments that don't overlap with the time range
        if (overlapStart >= overlapEnd) return;

        // Calculate the duration of the overlap
        let overlapDuration = overlapEnd - overlapStart;

        // Add probability weighted by overlap duration
        totalProb += segment.prob * overlapDuration;
        // Add overlap duration
        totalDuration += overlapDuration;
    });
    // Return average probability (handle case where no segments overlap)
    return totalDuration > 0 ? totalProb / totalDuration : 0;
}
```

```js
// Get the time-weighted average probability for each answer on each day
function betsToDailyProbs(bets) {
    // Initialize results array
    let results = [];
    // Get last bet time
    const lastBetTime = Math.max(...bets.map(bet => bet.createdTime));
    // Get unique answerIds
    const uniqueAnswerIds = [...new Set(bets.map(bet => bet.answerId))];
    // For each answer...
    uniqueAnswerIds.forEach(answerId => {
        // Get bets for this answer
        let answerBets = bets.filter(bet => bet.answerId === answerId);
        // Convert to prob segments
        let probSegments = betsToProbSegments(answerBets, lastBetTime);
        // Get start and end dates
        let startDate = probSegments[0].startTime;
        let endDate = probSegments[probSegments.length - 1].endTime;
        // Look through each day
        let currentDate = startDate;
        while (currentDate <= endDate) {
            // Set end of day
            let endOfDay = new Date(currentDate.getTime() + 86400000);
            // Get the average probability for this day
            let avgProb = getAverageProbability(probSegments, currentDate, endOfDay);
            // Save the date, answerId, and average probability
            results.push({
                date: currentDate,
                answerId: answerId,
                avgProb: avgProb,
            });
            // Increment the date
            currentDate = endOfDay;
        }
    });
    // Return results array
    return results;
}
const dailyProbs = betsToDailyProbs(bets);
```

```js
// For threshold type, get exclusive probability for each answer for each day
function updateThresholdProbs(answerMap, dailyProbs) {
    // Get unique days
    const dailyProbDays = [...new Set(dailyProbs.map(prob => prob.date))];

    for (const [answerId, answerDetails] of Object.entries(answerMap)) {
        // Check if threshold fixing is required
        if (answerDetails.threshold_fixing) {
            // Update answerMap with new values
            const thresholdDetails = answerDetails.threshold_fixing
            answerMap[answerId].label = thresholdDetails.new_label
            answerMap[answerId].min_value = thresholdDetails.new_min
            answerMap[answerId].max_value = thresholdDetails.new_max

            // Update dailyProbs by removing excluded answers
            dailyProbDays.forEach(day => {
                const dailyProbsThisDay = dailyProbs.filter(prob => prob.date.getTime() === day.getTime())
                const dailyProbsThisAnswer = dailyProbsThisDay.find(prob => prob.answerId === answerId);
                if (dailyProbsThisAnswer) {
                    const dailyProbsToExclude = dailyProbsThisDay.filter(prob => thresholdDetails.exclude_answers.includes(prob.answerId));
                    const newProb = dailyProbsThisAnswer.avgProb - dailyProbsToExclude.map(prob => prob.avgProb).reduce((i, a) => i + a, 0);
                    dailyProbsThisAnswer.avgProb = newProb
                } else {
                    console.log(`No daily probability found for answer ${answerId} on day ${day}`);
                }
            });
        }
    }
}
updateThresholdProbs(answerMap, dailyProbs)
```

```js
// Add answer details to daily probs
dailyProbs.forEach(prob => {
    const answerDetails = answerMap[prob.answerId];
    if (answerDetails) {
        prob.answerLabel = answerDetails.label;
        prob.minValue = answerDetails.min_value;
        prob.maxValue = answerDetails.max_value;
    }
});
```

```js
html`<div>
    <h3>${market.question}</h3>
</div>`
```

```js
market
```

```js
answerMap
```

```js
bets
```

```js
dailyProbs
```

## MC-Numeric



## MC-One

```js
Plot.plot({
  title: 'Probability for each answer, stacked',
  x: { type: "utc", label: "date" },
  y: { label: 'probability', grid: true, percent: true },
  marks: [
    Plot.areaY(dailyProbs, {
      x: 'date',
      interval: 'day',
      fill: 'answerLabel',
      y: 'avgProb',
      curve: 'step',
      tip: true
    }),
    Plot.ruleY([0])
  ]
})
```

```js
Plot.plot({
  title: 'Probability for each answer',
  marginRight: 80,
  x: { type: "utc", label: "date" },
  y: { label: 'probability', grid: true, percent: true },
  marks: [
    Plot.line(dailyProbs, {
      x: 'date',
      fy: 'answerLabel',
      y: 'avgProb',
      curve: 'step-after',
      tip: true,
    }),
    Plot.ruleY([0])
  ]
})
```
