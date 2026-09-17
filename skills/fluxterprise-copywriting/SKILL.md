---
name: fluxterprise-copywriting
description: "Copy and text skill for fluxterprise. Use when writing or editing prose: headlines, tone, CTAs, and anti-AI-writing patterns. Load with the core."
allowed-tools: Read Write Edit Glob Grep
---

> Created by **Candra Prasetya**
# fluxterprise-copywriting

> Fluxterprise: Rules for AI Coding Agents. Copy & Text skill

> Part of the fluxterprise system. Read together with `fluxterprise/SKILL.md` (the core). This skill deep-dives the copy and text concern: headlines, CTAs, tone, value propositions, and the patterns that make AI-written prose easy to spot. It references core rules by number and never duplicates or renumbers them. Load it when the task writes or edits marketing copy, product copy, landing-page text, or any prose meant for people to read.

## How to use this skill

- Load together with `fluxterprise/SKILL.md` whenever the task is copy or text work. The core holds the mechanism (the purpose test, the three tiers, the Delivery Gate) and the hard bans (FG-02, FG-15, FG-16, FG-17, FG-18, FG-36, FG-38). This skill holds copy-specific depth that the core does not.
- Every pattern has the same shape: **The pattern**, **Why it reads as AI**, **Before** (the slop), **After** (the fix), with the governing core rule cited as FG-XX.
- Two rules apply to everything below:
  - **Never invent facts** (FG-17, FG-36, FG-38). A rewrite adds no fact, name, number, date, quote, or citation that is not in the source text or supplied by the user. Specificity comes from the source or the user, not from the rewrite. If a sentence needs real detail to work, ask for it or write the plain version without it.
  - **Do not over-sterilize.** Avoiding AI patterns is half the job. Copy with no voice is as obviously machine-made as copy full of AI tells (FG-37). When a user supplies a voice, keep it.
- The Delivery Gate in the core remains the gate. The "Copywriting Skill Checklist" at the end of this file is the copy-specific supplement to run alongside it.

## Tone & Voice

### Empty AI Vocabulary

- **The pattern:** verbs and abstract nouns stacked to sound impressive without saying anything: *unlock, elevate, empower, delve, showcase, testament, landscape (abstract), journey, robust, game-changer, next-level, seamless, cutting-edge, revolutionary*.
- **Why it reads as AI:** these words appear far more often in machine-written text. They signal intent to impress, not intent to inform, and they are the fastest way to mark a page as AI-generated.
- **Before:**
  > Unlock the power of seamless collaboration to elevate your team's journey to the next level.
- **After:**
  > Work with your team in one shared space.
- **Rule:** FG-16 (buzzwords), FG-36 (no fabricated claims).

### Significance Inflation

- **The pattern:** "the future of X", "marking a pivotal moment", "a testament to", "revolutionizing", "a new era of".
- **Why it reads as AI:** the claim has no evidence behind it, and the sentence reads the same no matter what the product does. It is ceremony where content should be.
- **Before:**
  > Our platform is marking a pivotal moment in the evolution of team productivity, ushering in a new era of work.
- **After:**
  > Our platform cuts the time your team spends on status meetings.
- **Rule:** FG-36 (no fabricated claims), C-5 (evidence over claims).

### Empty Claims and Social Proof with No Evidence

- **The pattern:** "Trusted by thousands of teams", "industry-leading", "world-class", "loved by customers everywhere", with nothing named or verifiable.
- **Why it reads as AI:** a trust claim without evidence is a confession. It fills the space a real customer name, a real number, or a real use case should occupy.
- **Before:**
  > Trusted by thousands of teams worldwide. Industry-leading technology loved by customers everywhere.
- **After:**
  > Used by the support teams at [customer names, only if real]. If there are no real customers to name, cut the claim entirely.
- **Rule:** FG-17 (data and numbers), FG-18 (testimonials), FG-36 (no fabricated claims), C-5.

### Weasel Attributions

- **The pattern:** "Experts say", "industry observers", "people report", "leading analysts believe", with no one named.
- **Why it reads as AI:** the attribution exists to make an unsourced claim feel authoritative. If the authority is real, name it; if not, the claim does not get a costume.
- **Before:**
  > Experts say this approach dramatically improves conversion.
- **After:**
  > [Name the source or cut the sentence. Example with a real source: "In a 2024 study by [named firm], this approach improved conversion by [real figure]."]
- **Rule:** FG-36, C-5.

### Persuasive Authority Tropes

- **The pattern:** "at its core", "the real question is", "what really matters", "fundamentally", "the deeper issue", "the heart of the matter".
- **Why it reads as AI:** these phrases pretend to cut through noise to a deeper truth, then restate an ordinary point with extra ceremony.
- **Before:**
  > At its core, what really matters is whether your team can move faster.
- **After:**
  > Whether your team can move faster depends on how quickly you can merge changes.
- **Rule:** FG-36.

### Chatbot Closers

- **The pattern:** "I hope this helps!", "Let me know if you have any questions", "Would you like me to expand on this?", "You're welcome!".
- **Why it reads as AI:** these are conversation artifacts, not copy. They appear when model chat output is pasted straight into a deliverable.
- **Before:**
  > Here is an overview of our pricing. I hope this helps! Let me know if you'd like me to break down any tier.
- **After:**
  > Here is our pricing. The Starter tier includes three seats and community support.
- **Rule:** FG-36.

### Fake-Candid Openers

- **The pattern:** "Honestly?", "Let's be honest", "Here's the thing", "Real talk", as a theatrical pause before an ordinary point.
- **Why it reads as AI:** a person being honest usually just says the thing. The pause-and-reveal is manufactured intimacy.
- **Before:**
  > Is it worth the price? Honestly? It depends on how often you'll use it.
- **After:**
  > Whether it is worth the price depends on how often you'll use it.
- **Rule:** FG-36.

### Signposting Announcements

- **The pattern:** "Let's dive in", "Here's what you need to know", "In this article we'll explore", "Without further ado".
- **Why it reads as AI:** announcing what you are about to do instead of doing it is meta-commentary. It slows the reader and gives the text a tutorial-script feel.
- **Before:**
  > Let's dive into how caching works in Next.js. Here's what you need to know.
- **After:**
  > Next.js caches data at multiple layers, including request memoization, the data cache, and the router cache.
- **Rule:** FG-36.

### All-Caps Emphasis

- **The pattern:** a whole sentence, clause, or phrase in ALL CAPS inside a paragraph to shout emphasis: "The launch is ready and WE NEED TO MOVE NOW before the window closes."
- **Why it reads as AI:** caps-as-emphasis is a blunt instrument the model reaches for to manufacture urgency instead of writing emphasis into the sentence. In long text it reads as shouting, and it flattens the real peaks by making everything loud.
- **Before:**
  > This is our last chance to win this customer, and WE MUST ACT IMMEDIATELY before they choose a competitor.
- **After:**
  > This is our last chance to win this customer. If we do not respond today, they will choose a competitor.
- **Rule:** FG-36. (FG-06 covers uppercase labels with wide tracking as a design choice; this pattern is the prose case: caps inside a paragraph doing the emphasis work.)
- **Not a ban:** a genuine headline, a deliberately shouted line in a voice that shouts, or a single all-caps word used once as an accent can keep its caps. The tell is caps used sentence after sentence to do the emphasis the words should do. Minimize, do not strip every cap.

### Actorless Passive

- **The pattern:** the passive voice with the actor deleted: "the decision was made to sunset the free tier", "the pricing page has been updated", "mistakes were made".
- **Why it reads as AI:** the model does not know who acted, so it writes around it. The team that shipped the thing does know, and says so. Deleting the actor also quietly removes accountability from the sentence, which is why the shape survives in corporate copy and nowhere else.
- **Before:**
  > The pricing page was updated to reflect the new tiers.
- **After:**
  > We rewrote the pricing page to show the new tiers.
- **Rule:** FG-02 (text must feel natural and human).
- **Not a ban:** passive is the right choice when the actor is unknown, irrelevant, or deliberately withheld ("the server was restarted at 03:00"), and when the object is the real subject of the paragraph. The tell is passive chosen by default, page after page, with an actor that was available the whole time.

### Inanimate Subject, Human Verb

- **The pattern:** an abstraction given agency: "the data tells us", "the design decides", "the complaint becomes a fix", "the roadmap wants to focus on retention".
- **Why it reads as AI:** it sounds active while naming nobody, so it passes a passive-voice check and still hides the actor. It also flatters the product, since a dashboard that "understands" is doing something no dashboard does.
- **Before:**
  > The dashboard understands what your team needs and surfaces the right numbers.
- **After:**
  > The dashboard opens on the three metrics your team checks every morning.
- **Rule:** FG-02, FG-16 (specific language over claims).
- **Not a ban:** ordinary product verbs are fine, and so are established idioms. "The report shows", "the form submits", "the filter narrows the list" describe what the thing does. The tell is a verb that needs a mind behind it: understands, knows, decides, wants, believes, cares.

## Rhythm & Structure

### Rule of Three Overuse

- **The pattern:** every idea forced into a group of three to sound complete: "innovation, inspiration, and insights".
- **Why it reads as AI:** real lists have the number of items the content requires. A forced trio is a rhythm tell, and it appears across every section at once.
- **Before:**
  > Attendees can expect keynote sessions, panel discussions, and networking opportunities. They'll leave with innovation, inspiration, and industry insights.
- **After:**
  > The event includes talks, panels, and time for informal networking between sessions.
- **Rule:** FG-05 (page structure), FG-36.

### Negative Parallelism and Tailing Negations

- **The pattern:** "It's not just X, it's Y", "Not only X, but also Y", and clipped fragments tacked on as emphasis: "no guessing", "no wasted motion".
- **Why it reads as AI:** the construction is a formula the model reaches for to sound emphatic, whether or not the emphasis is earned.
- **Before:**
  > It's not just a dashboard, it's a command center. The options come from the selected item, no guessing.
- **After:**
  > The dashboard shows the data you select. The options come from the selected item without forcing you to guess.
- **Rule:** FG-36.

### Aphorism Formulas

- **The pattern:** "X is the language of Y", "X is the currency of Z", "X is not a tool but a mirror", "Efficiency becomes a trap when".
- **Why it reads as AI:** a reusable formula that sounds profound without adding precision. It gestures at a point instead of stating it.
- **Before:**
  > Symmetry is the language of trust. Efficiency becomes a trap when teams forget the human layer.
- **After:**
  > Symmetric layouts feel more predictable to users. Teams can over-optimize workflows and miss how people actually work.
- **Rule:** FG-36.

### Staccato Drama

- **The pattern:** a run of short declarative fragments to manufacture a punchline: "It had no preference. No prior. No nostalgia."
- **Why it reads as AI:** one short sentence for emphasis is fine; a run of them sounds engineered. The rhythm is even, the effect is theatrical.
- **Before:**
  > Then the old rules were gone. No templates. No defaults. No safety.
- **After:**
  > The old rules no longer applied, and every page had to be designed from scratch.
- **Rule:** FG-36.

### Synonym Cycling

- **The pattern:** swapping synonyms to avoid repeating a word: "the protagonist faces a challenge, the main character must adapt, the central figure persists".
- **Why it reads as AI:** models rewrite to dodge repetition penalties. Human writers repeat the clearest word when it is clearest.
- **Before:**
  > The checkout is fast. The process is quick. The flow is speedy.
- **After:**
  > The checkout is fast. Everything happens in three clicks.
- **Rule:** FG-36.

### False Ranges

- **The pattern:** "from X to Y" where X and Y are not on a meaningful scale: "from onboarding to scale", "from first click to final invoice, and everything in between".
- **Why it reads as AI:** the range is an impressive-sounding frame that covers nothing specific.
- **Before:**
  > From first touch to final invoice, and everything in between.
- **After:**
  > Handles quotes, invoices, and payment reminders.
- **Rule:** FG-36.

## Honesty & Evidence

### Fabricated Specifics

- **The pattern:** invented numbers, testimonials, names, dates, or features that look realistic but are not real.
- **Why it reads as AI:** a specific-looking fabrication is worse than a vague claim, because it reads as honest while being false. This is the one pattern that is a defect even when it sounds more human.
- **Before:**
  > Trusted by 10,000+ teams. "Fluxterprise cut our review time in half." - Sarah Chen, VP Engineering at [fictional company].
- **After:**
  > If no real customer exists, write no number and no quote. Say what the product does instead. Any real statistic needs a real source (FG-17, FG-36).
- **Rule:** FG-17, FG-18, FG-36, FG-38, C-5.

### Speculative Gap-Filling

- **The pattern:** when the writer does not know a fact, they write a sentence about not knowing it, then invent plausible filler: "the company was likely founded in the 1990s", "she maintains a low profile".
- **Why it reads as AI:** a guess dressed as fact. The model cannot find a source, so it papers over the gap.
- **Before:**
  > While specific details are limited, the founder likely started small and grew through word of mouth.
- **After:**
  > The founding details are not documented in our sources. (Or omit the sentence entirely. State a date only if a source provides one.)
- **Rule:** FG-17, FG-36.

### Generic Positive Conclusion

- **The pattern:** "The future looks bright", "Exciting times lie ahead", "This is a major step in the right direction".
- **Why it reads as AI:** an upbeat send-off that restates nothing and promises nothing. It pads the ending with optimism instead of information.
- **Before:**
  > The future looks bright for our customers as we continue our journey toward excellence.
- **After:**
  > (Cut the sentence. End on the last concrete fact, or state real plans if they exist.)
- **Rule:** FG-36.

## Microcopy

Microcopy is the most-read text on any product: error messages, empty states, loading text, tooltips, placeholder text, confirmation messages. AI agents almost always produce generic, unhelpful microcopy. This section fixes that.

### Error Messages

- **The pattern:** "An error occurred", "Something went wrong", "Error 500", "Failed to load".
- **Why it reads as AI:** the message names nothing: not what failed, not why, not what the user can do about it. It is the digital equivalent of a shrug.
- **Fix:** every error message names the failure and gives one action: "Could not load your posts. Check your connection and try again." or "Payment declined. Your card was charged $0. Try a different card."
- **Rule:** FG-16 (specific language), C-2 (functional completeness).

### Empty States

- **The pattern:** "No data available" with a sad illustration, or a bare list showing nothing.
- **Why it reads as AI:** it tells the user nothing: no cause, no next action, no idea whether this is normal.
- **Fix:** every empty state says why it is empty and gives the one action that fills it: "No posts yet. Write your first post." or "No results for 'x'. Try a different search."
- **Rule:** FG-27 (UI states), C-3 (content-driven).

### Loading Messages

- **The pattern:** bare `CircularProgressIndicator()` or "Loading..." with no context.
- **Why it reads as AI:** the user has no idea what is loading, how long it will take, or whether the app is frozen.
- **Fix:** name what is loading: "Loading your posts..." or "Syncing your data...". If the operation is long, show progress or an estimate.
- **Rule:** FG-27 (UI states).

### Placeholder Text

- **The pattern:** "Enter text here", "Type something", "Lorem ipsum", "John Doe", "johndoe@example.com".
- **Why it reads as AI:** generic placeholder teaches nothing about what the field expects.
- **Fix:** placeholder should hint at format and example: "your@email.com", "Jakarta, Indonesia", "e.g. Project Alpha". Never use fake but plausible data (John Doe) as placeholder.
- **Rule:** FG-23 (visual assets), FG-38 (real content or honest placeholder).

### Tooltips

- **The pattern:** tooltip restates the button label: tooltip on "Save" says "Save".
- **Why it reads as AI:** the tooltip adds zero information. It exists because the tool told the agent every element needs a tooltip.
- **Fix:** tooltip adds context the label does not: "Save as draft (Ctrl+S)" or "Save changes to this document". If the tooltip says the same thing as the label, remove it.
- **Rule:** FG-31 (every decision must have a reason).

### Confirmation Messages

- **The pattern:** "Success!", "Done!", "Operation completed successfully".
- **Why it reads as AI:** it confirms nothing specific. "Success" after deleting a project is alarming.
- **Fix:** name what happened: "Post published. View it here." or "3 items deleted. Undo?".
- **Rule:** FG-16 (specific language).

### Microcopy Skill Checklist

Run these alongside the core Quality Gate. All answers must be **yes**:

- [ ] Does every error message name the failure and give one action?
- [ ] Does every empty state say why it is empty and give the action that fills it?
- [ ] Does every loading state name what is loading?
- [ ] Does every placeholder hint at format and example, with no fake data?
- [ ] Does every tooltip add context the label does not?
- [ ] Does every confirmation message name what happened?

## SEO Copy

### Title Tags

- **The pattern:** "Product Name - Best Product for Everyone" or "Product | Tagline | Keywords".
- **Why it reads as AI:** keyword-stuffed, generic, and the same structure as every other AI-generated title.
- **Fix:** primary keyword + specific benefit, under 60 characters: "Fluxterprise - Quality Gate for Flutter Apps" or "Invoice Software for Freelancers - Fluxterprise".
- **Rule:** FG-16 (specific language).

### Meta Descriptions

- **The pattern:** "Learn more about our product. We provide the best solutions for your needs."
- **Why it reads as AI:** says nothing specific, wastes 160 characters.
- **Fix:** one sentence what it does, one sentence who it's for, one CTA: "Quality gate system for AI coding agents. Enforces craft standards before UI ships. Try it free."
- **Rule:** FG-16, C-5 (evidence over claims).

### Heading Hierarchy

- **The pattern:** H1 contains the brand name, H2s are section names, H3s are feature names. No keywords in headings.
- **Why it reads as AI:** the hierarchy serves the template, not the content or crawlers.
- **Fix:** H1 contains the primary keyword and value prop. H2s contain secondary keywords. H3s contain supporting topics. Each heading is meaningful on its own.
- **Rule:** FG-05 (layout & structure), FG-31 (every decision has a reason).

## Hygiene & Markdown

### Em Dashes

- **The pattern:** the em dash character (`—`) used as an aside or connector: *"institutions — not the people — continue"*.
- **Why it reads as AI:** it is one of the most reliable AI tells, and the core bans it outright.
- **Rule:** FG-02 forbids the em dash in any text. Replace each one, in rough order of preference: a period (start a new sentence), a comma (a tight aside), a colon (introduce an explanation), parentheses (a true aside), or restructure the sentence. Also catch spaced em dashes (` — `) and double hyphens (` -- `) used the same way.
- **Before:**
  > The policy — announced without warning — affects thousands of workers.
- **After:**
  > The policy, announced without warning, affects thousands of workers.
- **Before:**
  > You don't say "Netherlands, Europe" as an address — yet this mislabeling continues.
- **After:**
  > You don't say "Netherlands, Europe" as an address, yet this mislabeling continues.
- **False positive:** many editors and journalists use em dashes deliberately. On its own an em dash is not proof of AI. It counts when it sits in a cluster with other tells (FG-02 still bans it in output, but do not rewrite the user's deliberate style without saying so).
- **Voice override:** if the user provides a writing sample that uses em dashes at a certain frequency, match the sample's frequency instead of cutting them all (see Voice calibration).

### Boldface Overuse

- **The pattern:** every key term bolded mechanically: **"OKRs**, **KPIs**, **BMC**".
- **Why it reads as AI:** emphasis everywhere is emphasis nowhere. The page shouts at the reader.
- **Before:**
  > It blends **OKRs**, **KPIs**, and **visual strategy tools** for planning.
- **After:**
  > It blends OKRs, KPIs, and visual strategy tools for planning.
- **Rule:** FG-36.
- **Carve-out:** the structural labels inside the fluxterprise rules themselves (the `**FORBIDDEN**` / `**REQUIRED**` markers in `fluxterprise/SKILL.md`) are documentation conventions, not the mechanical bold-every-key-term pattern above, and are exempt.

### Excessive Quotation Marks

- **The pattern:** long text studded with quotation marks: quoting words that do not need quoting, scare quotes around ordinary terms, and quotes used as a default for emphasis or hedging. The page reads quoted rather than written.
- **Why it reads as AI:** models reach for quotation marks as a default way to add distance, irony, or emphasis without writing it into the sentence. Dense quoting is a reliable machine tell in longer text.
- **Before:**
  > The "solution" "streamlines" your "workflow" so you can "focus" on "what matters."
- **After:**
  > The solution streamlines your workflow so you can focus on what matters.
- **Rule:** FG-36.
- **Not a ban:** dialogue, short stories, quoted real sources, and titles of works keep their quotes. The tell is quotes doing the work the sentence should do. One scare quote used once for a real reason is fine; a cluster of them is not. Minimize, do not strip quotes that carry meaning.

### Inline-Header Lists

- **The pattern:** list items that start with a bolded header followed by a colon: "- **User Experience:** The UX has been improved".
- **Why it reads as AI:** the header restates what the item already says. It is a formatting habit, not a structure.
- **Before:**
  > - **User Experience:** The interface is easier to use.
  > - **Performance:** Load times are faster.
  > - **Security:** Data is encrypted.
- **After:**
  > The update improves the interface, speeds up load times, and encrypts data in transit.
- **Rule:** FG-36.
- **Carve-out:** the `- **Tell:**` / `- **Why:**` / `- **Fix:**` headers that structure every fluxterprise skill entry are a documentation convention, not the header-restates-the-item habit above, and are exempt.

### Emojis in Headings

- **The pattern:** decoration emojis leading headings or bullets: 🚀 Launch, 💡 Key insight, ✅ Next steps.
- **Why it reads as AI:** the emoji carries no information. It decorates instead of communicating.
- **Before:**
  > 🚀 **Launch Phase:** The product ships in Q3
  > 💡 **Key Insight:** Users prefer simple pricing
- **After:**
  > The product ships in Q3. User research showed a preference for simple pricing.
- **Rule:** FG-36.

### Filler Phrases

- **The pattern:** "In order to" for "to", "Due to the fact that" for "because", "At this point in time" for "now", "It is important to note that" for nothing.
- **Why it reads as AI:** filler inflates the sentence without adding meaning. It is padding a model adds to sound formal.
- **Before:**
  > In order to achieve this goal, it is important to note that we need more data.
- **After:**
  > To reach this goal, we need more data.
- **Rule:** FG-36.

### Excessive Hedging

- **The pattern:** multiple qualifiers stacked on one claim: "could potentially possibly", "may perhaps".
- **Why it reads as AI:** hedging everywhere makes the text sound evasive. One qualifier does the work.
- **Before:**
  > This could potentially possibly be the reason the feature went unused.
- **After:**
  > This may be why the feature went unused.
- **Rule:** FG-36.

## What NOT to flag

A clean human writer can hit several patterns above without any AI involvement. Before editing, sanity-check that you are not gutting legitimate prose. These are **not** reliable indicators on their own:

- **Perfect grammar and consistent style.** Many writers are professionals or have been edited. Polish does not equal AI.
- **Mixed casual and formal registers.** This often signals a real person, not a chatbot.
- **"Bland" or "robotic" prose.** AI prose has specific tells. Generic dryness without those tells is just dry writing.
- **Formal vocabulary.** AI overuses *specific* words (see Empty AI Vocabulary), not all fancy words. Do not flatten a precise word just because it sounds brainy.
- **Common transition words in isolation.** One "however" or "additionally" is not a tell. They count only when piled up.
- **Curly quotes alone.** macOS, Word, and most CMSes auto-curl by default. Curly quotes count only when stacked with other tells.
- **Em dashes alone.** Editors and journalists use them. An em dash is evidence only inside a cluster.
- **One short emphatic sentence.** Humans use clipped sentences to land a point. Flag staccato drama only when several fragments appear in a row.
- **Unsourced claims.** Most of the web is unsourced. Lack of citations proves nothing.
- **Secondhand text.** Do not rewrite phrases inside quotations, titles, proper names, or examples where the phrase is being discussed rather than used.

**Look for clusters, not isolated tells.** A single em dash means nothing. Em dashes plus rule of three plus "vibrant tapestry" plus a generic conclusion is a confession. This matches the core's own guidance: Part 1 is a diagnostic scan, not a ban list.

## Signs of human writing (preserve these)

Lean toward leaving the prose alone when you see these. They are evidence of a real person, and over-editing destroys what makes the copy sound human:

- **Specific, unusual, hard-to-fabricate detail.** A real address. A weird quote. LLMs round off specifics; humans hoard them.
- **Mixed feelings and unresolved tension.** "I think this is mostly good, but it bothers me." LLMs default to clean takes.
- **Dated, era-bound references.** Slang, memes, or in-jokes that map to a specific year and subculture.
- **Variety in sentence length.** Real writing alternates short and long. AI writing tends toward an even, mid-length cadence.
- **Genuine asides and self-corrections.** "(I keep wanting to say 'almost' here, but it really was certain.)"

## Voice calibration (optional)

If the user provides a sample of their own writing, match it before rewriting:

1. Read the sample first. Note its sentence lengths, vocabulary, paragraph openings, punctuation, and recurring phrases.
2. Match those habits instead of merely deleting AI patterns. Do not upgrade casual words or regularize deliberate quirks.
3. The sample outranks this skill's style rules. If the sample uses em dashes, keep them at roughly the sample's frequency (FG-02 still applies to any copy the user did not authorize; when the user's own voice uses them, the voice wins).

Without a sample, use the defaults above. Matching the author beats scrubbing the tell.

## Draft, audit, final

Run this loop before delivering copy:

1. **Draft.** Rewrite the text applying the patterns above. Check that it reads naturally aloud, varies sentence length, prefers specific detail and simple constructions, and keeps the appropriate register.
2. **Audit.** Ask two questions and answer them briefly: "What makes this obviously AI generated?" and "Does it state any fact, name, number, date, or citation that is not in the source?" A fabrication is a defect even when it sounds more human than the vague original.
3. **Final.** Revise to address both answers. Check for em and en dashes one last time (FG-02). A hit means the draft is not done.

## Copywriting Skill Checklist

Run these alongside the core Delivery Gate when the task is copy work. Every line below must be true:

- [ ] No fabricated numbers, testimonials, names, dates, or claims; everything real or a labeled placeholder (FG-17, FG-18, FG-36, FG-38)
- [ ] Buzzwords from FG-16 and the Empty AI Vocabulary list replaced with specific, evidenced language
- [ ] No em dashes in the output (FG-02), unless the user's own sample voice uses them
- [ ] No excessive quotation marks: quotes only where they carry meaning (dialogue, real citations, titles), not as default emphasis (FG-36)
- [ ] No all-caps emphasis clauses: emphasis written into the sentence, not shouted with caps (FG-36)
- [ ] Every sentence names its actor: no actorless passive, no abstraction given a human verb, where a real subject was available (FG-02, FG-16)
- [ ] CTAs specific to the action, not generic templates (FG-15)
- [ ] No AI-rhythm tells: no forced rule of three, no negative parallelism, no staccato drama, no aphorism formulas, no false ranges (FG-36)
- [ ] Voice present: the copy has a real voice (the user's sample or a clearly chosen tone), not a sterile default (FG-37)
- [ ] Read aloud: the copy sounds like a person wrote it, not like a model padded it
