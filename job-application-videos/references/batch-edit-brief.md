# Batch edit brief

Use this with `talking-head-graphics` when you edit many videos in one look. Give
one agent four or five videos. Each agent costs a fixed start-up amount, so one agent
per video spends several times more.

## Look

One visual at a time. Few colours. Show, do not tell: a logo, a number, a paper-cut
picture or a card of one to three words. No sentences. The opening shows only the
name tag. Panel colours alternate.

Pick four to six scenes. Give one visual to each phrase with real content: a company
or product the speaker names, a number the speaker says, a role or skill word, the
calendar link at the end. Skip phrases with nothing concrete. Use only the speaker's
own numbers. Use a logo only for a brand the speaker names. Otherwise show the name
on a card.

## Per video

1. Read the word list with times and the trim point.
2. Write one story file, about eight lines of helper calls (name tag, logo scene,
   number scene, word card, picture, calendar scene).
3. Run the builder: it builds, copies logos, cuts the speaker, renders and checks.
4. Look at the one contact sheet of the final video: right logos, text not clipped,
   no two speakers, no empty tile.
5. Fix the story and rerun if needed. The result must say `pass: true`.

## Rules the builder enforces

- The first visual starts at least 1.1 s after the scene enters.
- Each visual shows at least 0.65 s with a 0.1 s gap.
- A visual ends before its scene exits. The next scene enters after the previous one
  leaves.
- At most one big word behind the speaker, in a gap of 3 s or more.
- A missing logo means a name card instead. A pacing message names the broken rule.

## Check

Compare every number on screen with the transcript. Fix name slips from speech
to text. Report in 40 words: output path, pass or fail, scenes in one line, doubts.
