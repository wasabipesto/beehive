```js
const san = FileAttachment('signal-and-noise-20251015144213.json').json()
```

# Hyperstition

While browsing the recent [ACX grant winners](https://www.astralcodexten.com/p/acx-grants-results-2025), I came across a project whose goal is to create a large volume of benevolent AI fiction that’s “slightly-less-sloplike AI slop than usual”. I was skeptical that they could make a full, intelligible novel for just a dollar, let alone that this will have any impact on LLM training. However, they offered to create a full novel with any prompt so I went ahead and submitted one to see what it could do.

## Prompting

I didn’t need to create an account and I was able to use the code “ACX” to get 50 credits free (enough for a full novel, street price $0.10 per credit). The API response implies I’m the 128th user and my book was the 104th generated.

When you go to [submit a prompt](https://www.hyperstitionai.com/generate), it asks for the following:

- Book concept: a long free-form prompt
- Author name: free-form, presumably for your name
- Genre: thriller, mystery, science fiction, fantasy, or romance
- Voice: humorous, professional, casual, dark, suspenseful, inspirational, academic, or conversational
- Number of chapters: defaults to 10 but seems to accept any number
- Themes: another free-form prompt

I didn’t trust that this system would create anything compelling without creative prompting, so I workshopped a story outline with ChatGPT. Looking at the result I actually don’t think this is necessary, but answering questions gave me a chance to add some creative details which I thought was helpful.

My prompt was a romance in the near-future between an AI and a human, bridging the differences between their experiences and falling in love. I was hoping for something that put the alien-ness of an AI’s interiority in the forefront with a creative spin. The final result was better than I expected it would be, probably on par with my own writing skills if I was forced to write a novel. It took a little under an hour and came out to about 67,000 words. You can [read it here if you wish](https://www.hyperstitionai.com/book/signal-and-noise-20251015144213).

I was quite surprised at the continuity and structure. The character work was decent and the worst thing about it in my opinion was the use of asterisks for emphasis which annoy me for no good reason. It’s pretty obvious that it was written by an LLM and it won’t be winning any awards anytime soon.

## Structure

I was actually trying to save the full text of the story to an epub format when I stumbled upon a trove of data from the API. Instead of just the book text, we have the entire generation log and structure given to the model!

Here's the full API data, including all setup and the actual text of the story (click to expand):

```js
san.novel_data
```

Based on this information, here’s a rough breakdown of how I believe the story generator works behind the scenes.

1. Based on selected story type (romance in my case), find or create a list of standard story beats in order. These are steps like “the meet-cute”, “an inkling of desire”, “an inkling of doubt”, “the break-up”, ‘the wake-up”, and “what whole-hearted looks like”. Arrange these to fill out the selected number of chapters.
2. Generate a title and a high-level summary based on the original concept presented by the user.
3. With the summary and beats, generate a high-level outline of each chapter. Example: *“Chapter 6: Signal Decay - Nara's overwhelming honesty about experiencing all humans as data patterns makes Elara feel insignificant, while Elara's need for individual recognition confuses Nara, causing their communications to become stilted and formal as old fears resurface.”*
4. Create a story bible for the characters and setting. This includes facts about characters, locations, and the world, along with notes on the themes and tone. This seems to help keep things consistent and avoid tonal drift but doesn’t add much novelty.
5. Create individual scene descriptions for each chapter based on the story bible, chapter outline, story beats to hit in that chapter. For me this was five scenes per chapter, and each one was more detailed than the chapter summary. They also included notes on character motivations and pacing.
6. Read all scene descriptions (and probably also the chapter summaries and story bible) and check for continuity errors. This API call seems to have failed on my book due to returning plaintext instead of JSON.
7. Finally, create the full text of every scene. I assume these steps get all pertinent information including the story bible and outline summary. According to the generation logs this appears to be sequential, so they must be feeding it the previous chapter (or several chapters) to keep continuity.

The planning stages, from generating summaries and story beats up through individual scene descriptions, took about five minutes total. The rest of the time (about 45 minutes) was creating the full text of the book at about a minute per scene or five minutes per chapter.

## Reflection

Prior to this I would not have been surprised if, with some prompting, LLMs could write something pretty good on the scale of a short story. I expected that at novel length, the stories would be closer to “nonsense” than “uninspired”, but I think the bar has been raised by pretty simply adding this structure. I'd bet that following some more academic literature on modern story structure could expand this even further.

My last brush was story generation was with [Xe Iaso’s use of Plotto](https://xeiaso.net/blog/automuse/) a few years ago. Since Plotto can be a bit erratic I think it’s good for novelty (rimshot) but the simple structure worked surprisingly well for a standard romance book. Maybe this sort of story generator is extremely common now and I've just been behind the times? It certainly doesn't seem like it'll be disrupting the NYT bestseller list anytime soon but it feels pretty close to my own writing level.

I think a lot of current models struggle with novelty (for obvious reasons) but some of that can be alleviated by injecting creativity from something like Plotto or even more random. Similarly to how an author can get inspiration from random things, models could have an external source of linguistic entropy like [Dreamtap](https://dreamtap.xyz/). Also I expect that many models would skirt around or simply refuse to write on some topics.

## Ideas

I would have loved the ability to edit or collaborate on the story bible before the full novel was generated. That would be a great spot to add subtle details that would be woven into the full story later, or just make some tweaks to character motivations. Re-creating the title and outline after this step could bring that creativity to the structure as a whole.

It was annoying to see asterisks when I knew they were intended as italics, it would be nice if markdown would be rendered on the output page. It would also be nice if you could export the story as an epub for easier reading.
