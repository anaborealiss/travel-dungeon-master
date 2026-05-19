# Travel Dungeon Master

Travel Dungeon Master is a simple AI travel agent.

The agent helps a user plan trips in a Dungeons & Dragons-inspired style. It does not answer only from the language model. Before answering, it retrieves useful context from local travel notes and memory files.

## Goal

The goal of this project is to show how an AI agent can use Information Retrieval to give more relevant answers.

For each normal travel question, the agent:

1. Searches local Markdown files in the `data/` folder.
2. Reads traveler memory from JSON files.
3. Selects useful travel skills from the question and memory.
4. Builds a prompt using the retrieved context and selected skills.
5. Sends the prompt to a Berget.AI model through an OpenAI-compatible API.
6. Saves the question, answer, and sources in a quest log.

The project also includes a trace mode that shows the retrieval process without calling the LLM.

It also includes a small manual compaction command inspired by OpenClaw. The `/compact` command summarizes the quest log into `memory/quest_summary.json`, so older context can still be used without putting every past answer into the prompt.

## Information Retrieval Features

The project includes:

- Keyword search over local travel notes.
- Working memory in `memory/traveler_profile.json`.
- Conversation history in `memory/quest_log.json`.
- A simple skill selection layer in `agent/skills.py`.
- A trace command that shows query words, document scores, memory, and selected skills.
- A manual compaction command that creates a small quest summary.
- Commands that update the agent memory.
- Source tracking for retrieved documents.

## Commands

```text
/help
/profile
/like something
/dislike something
/budget low
/pace slow
/search question
/trace question
/compact
/exit
```

Example:

```text
/like cozy cafes
/dislike crowds
/budget low
/pace slow
/trace Plan me a cozy day in Prague without crowds
Plan me a cozy day in Prague
/compact
```

## Project Structure

```text
agent/
  main.py        Main command-line loop
  memory.py      Reads and writes memory files
  retriever.py   Searches local travel notes
  skills.py      Selects travel planning skills
  prompts.py     Builds LLM messages
  llm.py         Connects to the API

data/
  prague.md
  kyoto.md
  warsaw.md
  budapest.md
  split.md

memory/
  traveler_profile.json
  quest_log.json
  quest_summary.json

report/
  report.md
```

## Setup

Install dependencies:

```bash
pip install -r requirements.txt
```

Create a `.env` file in the project root:

```text
OPENAI_API_KEY=your_berget_api_key_here
OPENAI_BASE_URL=https://api.berget.ai/v1
OPENAI_MODEL=meta-llama/Llama-3.3-70B-Instruct
```

The project uses Berget.AI with an OpenAI-compatible API. The model can be changed by editing `OPENAI_MODEL`.

Do not commit the `.env` file to GitHub.

## Run

Start the agent:

```bash
python -m agent.main
```

Then type a command or a travel question.

## Demo Scenario

```text
/like cozy cafes
/dislike crowds
/budget low
/pace slow
Plan me a cozy day in Prague
```

In this demo, `/trace` first shows the IR process: query words, retrieved documents, document scores, memory, and selected skills. Then the normal question retrieves local notes from `data/prague.md`, uses the saved traveler memory, selects skills such as `cozy_travel` and `avoid_crowds`, asks the LLM for an answer, and writes the interaction, sources, and selected skills to `memory/quest_log.json`.

## Deliverables

- GitHub repository: https://github.com/anaborealiss/travel-dungeon-master
- Video demo: https://drive.google.com/file/d/1uNFhjvI7syOmYLrvtDdwvhBULsFyGG4q/view?usp=sharing
- Report: `report/report.md`

## Limitations

The retrieval system uses simple keyword matching instead of embeddings. This makes the code easy to understand, but it is less powerful than semantic search.

A future version could add vector search, web search, more cities, or more advanced agent tools.
