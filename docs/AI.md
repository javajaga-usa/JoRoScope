# Ask about my chart (AI answers)

The **💬 Ask about my chart** tab on Life Predictions answers questions about a chart, and can write
an overall reading, using Claude from Anthropic. It is optional: without it the rest of JoRoScope
works exactly as before.

## How it stays accurate

The AI does not calculate anything. JoRoScope calculates the chart with the Swiss Ephemeris as
usual, then sends Claude a condensed fact sheet of that chart: placements, houses and lords, the
Vimshottari dasas and bhuktis, yogas, doshas, current transits and Saturn cycles, the marriage,
career, remedy and annual reports, the next months' transit forecast, and the person's own
Chart Verification marks. Claude is told to answer only from that sheet, to cite the dasas and
placements it used, to say when the chart does not answer a question, and never to predict a
date of death. The fact sheet is built in `src/joroscope/core/ai.py` (`fact_sheet`).

## Setting it up

1. Install the Anthropic SDK into JoRoScope's Python environment:

   ```bash
   .venv/bin/python -m pip install -r requirements-ai.txt
   ```

2. Create an API key at <https://console.anthropic.com> (Settings, API keys). Questions are billed
   to that account.

3. Put the key, and a passcode for anyone using JoRoScope from another computer, in a private file
   in your home folder (not in the project):

   ```bash
   mkdir -p ~/.config/joroscope && chmod 700 ~/.config/joroscope
   ```

   Then create `~/.config/joroscope/ai.env` containing:

   ```
   ANTHROPIC_API_KEY=sk-ant-...
   JOROSCOPE_AI_PASSCODE=choose-a-passcode
   ```

   and make it readable only by you: `chmod 600 ~/.config/joroscope/ai.env`. Environment variables
   of the same names work too, and take precedence over the file.

4. Restart JoRoScope.

## Who can ask

- **On the computer running JoRoScope** (opened at `localhost` or `127.0.0.1`), no passcode is
  needed.
- **From anywhere else**, such as through a shared tunnel link, the passcode is required. Without a
  passcode set, questions from other computers are refused, so a forwarded link cannot run up the
  bill. A wrong passcode is answered after a one-second delay to slow guessing.

The passcode is kept in the browser only for that session.

## Model and cost

The default model is Claude Opus 5.5 (`claude-opus-5-5`) at medium effort. Set
`JOROSCOPE_AI_MODEL` (for example to `claude-sonnet-5-5`) to use a different one. Each question
sends the fact sheet (about 5,000 tokens) with the conversation so far; follow-up questions about
the same chart reuse it from the prompt cache at a tenth of the price. If Claude declines a
question on safety grounds, the request is retried on Anthropic's recommended fallback model.

## Privacy

Asking sends the birth date, time and place and the calculated chart to Anthropic to prepare the
answer; the Ask tab says so beside the question box. Nothing is sent until someone asks.
