# Putting JoRoScope online

JoRoScope runs as one small Python web service with no database, so any host that runs Python or
Docker can serve it. A permanent address saves sharing a tunnel from your own computer, which stops
when the computer sleeps and changes its address every time.

## Render (free plan, simplest)

The repository carries a Render blueprint, [`render.yaml`](../render.yaml).

1. Sign in at <https://render.com> with your GitHub account, and allow Render to read the
   `JoRoScope` repository (it can be private).
2. Choose **New → Blueprint**, pick the repository and choose **Apply**. Render installs
   `requirements.txt` and starts `server.py`; the first build takes a few minutes.
3. Render gives the service an address such as `https://joroscope.onrender.com`. Share that.

Every push to `main` redeploys it. On the free plan the service sleeps after about 15 minutes
without visitors, and the first visit after that takes 30 to 60 seconds to wake it.

**Optional settings** (Render dashboard → the service → Environment):

| Variable | Purpose |
| --- | --- |
| `ANTHROPIC_API_KEY` | Answers inside the Ask tab ([AI.md](AI.md)); also add `anthropic` to the build with `pip install -r requirements-ai.txt` as the build command. Without it, Copy for Claude still works. |
| `JOROSCOPE_AI_PASSCODE` | Required for Ask questions on a public server. Without it, Ask is refused, so nobody can run up your bill. |
| `JOROSCOPE_OWNER_PASSCODE` | Opens the accuracy report of collected verification marks (see below). |
| `JOROSCOPE_DATA_DIR` | Where the collected verification marks are kept. |

**Collected verification marks:** the free plan's disk is wiped on every deploy and restart, so the
marks people choose to share are lost then. Download the accuracy report regularly, or add a Render
disk (a paid add-on) mounted at, for example, `/var/data`, and set `JOROSCOPE_DATA_DIR` to it.

## Docker (Fly.io, Railway, a server of your own)

The [`Dockerfile`](../Dockerfile) builds a small image that listens on port 8080:

```bash
docker build -t joroscope .
```

```bash
docker run -p 8080:8080 joroscope
```

Set the same environment variables as above with `-e NAME=value`, and mount a volume at the
`JOROSCOPE_DATA_DIR` path to keep the collected marks.

## How the server reads its settings

- `PORT`: the port to listen on (hosting services set it); otherwise 8765, or a number given on the
  command line.
- `JOROSCOPE_HOST`: the address to listen on; `0.0.0.0` accepts connections from outside. Without it,
  only this computer can connect, which is right for the desktop launchers.
- The browser does not open by itself when `PORT` is set.
