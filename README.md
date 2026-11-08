# AlibiGraph

AlibiGraph is a cyber-forensics app that compares a suspect's alibi with the evidence. It turns statements, CCTV images and logs into a knowledge graph, then uses two AI agents to find claims that can't both be true.

## What it does

- **Reads mixed evidence.** Upload PNG, JPG, PDF, TXT or Markdown files, paste text, or start from one of two built-in sample cases.
- **Agent 1, the profiler,** extracts claims from each exhibit and tags them by topic, such as `LOCATION_ALIBI` or `TIMESTAMP`.
- **Agent 2, the cross-examiner,** compares new claims with the rest of the case, explains each contradiction and writes a question to put to the suspect. Questions follow the interrogation tactic you save for the case.
- **Builds a graph for each case.** Suspects, exhibits, claims, topics and contradictions are stored in FalkorDB and shown in an interactive graph.
- **Shows its work.** The Cypher log lists the parameterized queries behind each update to the graph.

> AlibiGraph is a project and demo, not a certified forensic tool. An AI model produces its findings, so a person should verify them.

## How it works

```text
Evidence file --> Agent 1: extract claims --> Agent 2: find contradictions
                                                        |
Interactive graph and cross-examination <-- FalkorDB <--+
```

Re-ingesting the same exhibit is safe: claims and contradictions are merged, not duplicated.

## Tech stack

| Area | Tools |
|---|---|
| App | Python, Streamlit |
| Graph database | FalkorDB, Cypher |
| Graph display | streamlit-agraph |
| AI agents | Grok (`grok-4.7` by default), through xAI's OpenAI-compatible API |
| File handling | pypdf, Pillow |

## Run it locally

You need Python 3.11 or newer, an [xAI API key](https://console.x.ai/) and a [FalkorDB](https://www.falkordb.com/) database.

```bash
git clone https://github.com/NotADIM2/AlibiGraph.git
cd AlibiGraph
python -m venv venv
```

Activate the environment with `venv\Scripts\activate` on Windows or `source venv/bin/activate` on macOS and Linux. Then install the packages:

```bash
pip install -r requirements.txt
```

Add your key to `.streamlit/secrets.toml`, which Git ignores:

```toml
XAI_API_KEY = "your_key_here"
# Optional: use a different Grok model
# XAI_MODEL = "grok-4.7"
```

You can also set `XAI_API_KEY` and `XAI_MODEL` as environment variables. The app's dark theme lives in `.streamlit/config.toml`.

Start the app:

```bash
streamlit run app.py
```

Choose **Enter Investigation Matrix**, open **Connection, case & tactic settings**, enter your FalkorDB host, port, username and password, and select **Connect**.

### Try it without FalkorDB Cloud

Run FalkorDB locally with Docker and connect to `localhost` on port `6379`:

```bash
docker run -p 6379:6379 falkordb/falkordb
```

## Using it

1. Enter a case ID, or open an existing case. Each case gets its own graph.
2. In the **Evidence** tab, name the suspect and either paste text, load a sample case or upload a file. The checklist shows what is still missing before you can run the analysis.
3. Select **Analyze & ingest evidence**. You'll see the extracted claims, and if Agent 2 finds contradictions, the app opens the **Contradictions** tab.
4. Add more evidence for the same case, explore the results in the **Graph matrix** tab, and check the queries in the **Cypher log**.
5. To start a case again, use **Wipe case…** in the settings. It asks for confirmation first.
