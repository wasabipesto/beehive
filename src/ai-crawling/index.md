# Thoughts on AI Crawling

A while ago I noticed a push within my community to block all AI web crawlers:

- https://coryd.dev/posts/2024/go-ahead-and-block-ai-web-crawlers/
- https://neil-clarke.com/block-the-bots-that-feed-ai-models-by-scraping-your-website/

I think these posts bring up valid concerns about the control that creators have over their work, and how little information is disclosed by many of the groups gathering this information. Data is becoming extremely valuable in this industry and scrapers can also end up eating bandwidth or other resources at the expense of the creators.

I’m still working through how I feel about these for my own site, so this is a kind of thinking-out-loud post.

## Different Kinds of Bots

One of the services I use has started blocking requests from specific user-agents using [this list](https://github.com/ai-robots-txt/ai.robots.txt). I don’t have any huge objections with this list, these agents are all at least tangentially related to AI. Blocking these agents will definitely save the operator some bandwidth, and it will block very few direct user requests. However, there are a few distinct types of bots on the list:

- Research crawlers, such as Common Crawl, that collect information for scientific purposes. The datasets can also be used for training AI, but it is not their primary purpose.
- User-initiated crawlers that are dispatched by an AI or automated system to fulfill a specific request on behalf of the user. These may not present the data in the same way as a browser but are still serving a similar purpose.
- Training crawlers which collect all available data specifically for training or fine-tuning models without attribution.

Each of these levels could of course be broken down even more (and there is often a blurring of lines between them) but I think these three tend to cover most “AI scrapers” that people tend to block.

When evaluating if you would want to allow one of these scrapers to access your site, you could use something like the following rubric:

- Accessibility: Is someone using this agent to get information from your site in a way that makes it accessible to them? Often this would cover web browsers but it could be the result of e.g. a Siri search or a browser extension that summarizes your page.
- Social Value: Is the agent using your data to build social value for your community? Proprietary models may not count for you, but what about open-weight or libre models? What about data used for web research?
- Attribution: Is the agent providing proper attribution when they use your content? Are they clearly showing what was used and where the source could be found?
- Cost/Benefit to the Creator: Is use of the agent benefitting the content creator somehow? If they are taking bandwidth but not providing the income a typical ad-viewing visitor would, how are they compensating the site?

## Evaluating Scrapers

Now let’s try to evaluate the different types of scrapers from above:

- Research Crawlers:
  - Accessibility: Basically no direct user requests, but they do make data more accessible for researchers.
  - Social Value: I would argue that datasets like Common Crawl have immense social value, not only because of the [sheer number of citations](https://commoncrawl.org/blog/the-increase-of-common-crawl-citations-in-academic-research) but also the fact that the data is freely available for all to use.
  - Attribution: Research datasets keep attribution and other metadata intact, since that’s often part of the research corpus.
  - Cost/Benefit: These crawlers do take some bandwidth, but they also usually take pains to not cause undue load on the server.
- User-Initiated Crawlers:
  - Accessibility: Triggered by a user by definition. This could be something like a social link preview, a search result, or a summarizer. Blocking one of these agents makes your site inaccessible for that user until they switch to a different agent, like a browser.
  - Social Value: Since it’s only serving one user at a time, there’s not enough of an impact to cause (or remove) social value.
  - Attribution: Most services will include a link to the source, but it’s up to that service to make the link visible. The service may also transform the source in some way that skews the intent.
  - Cost/Benefit: Each request will take resources unless the service caches your page. They probably won’t show your ads or other ways of making money from the user on their interface.
- Training Crawlers:
  - Accessibility: Not triggered by a user.
  - Social Value: I would argue that the social value is not zero, but I will admit it is low when being used to build non-free datasets.
  - Attribution: Often none is collected, and even when it is, it’s not surfaced to the end user.
  - Cost/Benefit: Each request will take resources, and unless you’re as large as Reddit they won’t pay you for access to your data.

I think this pretty closely matches my thoughts: all requests by an AI or a human will take resources, and the traditional way to offset those resources is to serve ads or build a following/collect influence over time. When the content is used out of context it still takes some resources to serve (plus whatever it took to produce) but the creator no longer gets those traditional benefits. Depending on how much each request costs you, how much you make from ads/impressions, and how much you value making your content accessible for other people, this will change where the line is for you.

## Comparing to Other Technologies

While the comparisons are not perfect, I think it’s valuable to compare these scrapers to other alternative web browsing applications:

- Adblock: The user gets all of your content but without any ads or “subscribe to my newsletter” pop-ups, depriving you of income.
- RSS Readers: Strips out most of your formatting, animations, and ads all at once. Thousands of RSS readers will re-download your feed every few minutes for eternity, eating your bandwidth.
- Screenshots: Someone sees a snip of your content but without any context or attribution. You no longer have control over how they see it, how they represent it, or how they share it.

Personally, I would categorize these three as more impactful to most web creators than any of the AI scrapers. These haven’t caused any significant disruption to me or my community, so I wouldn’t expect AI crawlers to do so either.

## AI Scrapers on My Site

I looked into a few ways of blocking AI scrapers on my site/content:

- For content hosted on other sites, using those sites’ tools to restrict access for AI use.
- For content hosted myself, adding a robots.txt or blocking through Cloudflare.
- For content hosted anywhere, adding a license that restricts use for AI training.

Personally I don’t think any of these are great options. I think a license is a good standard to move towards, while the Cloudflare block has the best chance of succeeding at actually stopping anything. I expect that the Cloudflare blocking will add relatively few false positives, but I would like to increase accessibility, not decrease it. For now I am keeping my content copyrighted as [CC BY-NC-SA](https://creativecommons.org/licenses/by-nc-sa/4.0/), though I would like to move towards CC BY or CC0. I value my writing but I also think that more open copyright licenses are generally preferable and have appreciated it when others have freer licenses.
