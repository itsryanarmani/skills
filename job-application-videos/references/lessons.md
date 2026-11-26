# Lessons

Each one cost time or money in a real run.

## Sheet

- **Always give the tab name** in a range: `Companies!C2`, never `C2`. A range
  without a tab name writes to the first tab. A batch of address fixes overwrote
  17 cells on the wrong tab, including the video links. Read the tab back after
  every write and compare it with a saved copy.
- Keep a copy of the sheet before a bulk write: `gog sheets get ... --json > backup.json`.
- A row in one tab matches the row in another only when someone keeps it so.
  Match by company and role text, not by row number, when a tab is re-sorted.

## Video

- Cut times come from audio energy, not word times from the transcript.
- Convert a variable-frame-rate file to constant rate before you cut by frame.
- Check numbers on screen against the transcript. Fix speech-to-text slips in
  company names ("Neo", not "NIO").
- Batch four or five videos per agent run. Each agent has a fixed start-up cost, so
  one agent per video spends several times more tokens.

## Thumbnails

- Layout alone did not look like real thumbnails. Measure the real ones (colour,
  font, size, rotation) and build presets from the numbers, then show real and
  generated side by side.
- Keep other people's thumbnails local. Never commit them.
- `thumbnails.set` works with the `youtube.upload` scope. Editing titles or privacy
  needs the broader scope.
- Check a few in Studio: an API success does not prove the picture shows.

## Addresses

- The PostGrid **test** key returns one dummy address for every input. Use the
  live key for verification.
- The verifier covers the US and Canada. A real UK or French address fails there.
- A real, new office can fail ("no match"). Check the company's own contact page.
- A company directory (ZoomInfo, PitchBook and similar) can show the wrong company
  with a similar name. One address belonged to a different firm with a near name.
- A building the verifier calls "suite needed" is often a whole-building tenant.
  Do not invent a suite: ask the owner, and put the person's name on the first line.

## Sending

- A private YouTube video shows "Video unavailable" to anyone you did not invite.
  Test the link signed out, and set the video to unlisted before you send.
- Do not send, post, email, upload or change a public page (set a thumbnail, change a
  video to unlisted) without a go-ahead from the owner. Say what
  will go out, to whom, and what it costs, then wait.
- Postage rates change. Read the provider's price page on the day you plan.
