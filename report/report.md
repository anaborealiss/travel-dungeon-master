# Travel Dungeon Master: An AI Agent with Information Retrieval

## Links

GitHub repository: https://github.com/anaborealiss/travel-dungeon-master

Video demo: TODO

## Introduction

Travel Dungeon Master is a small AI travel agent built for this Information Retrieval assignment. The agent helps a user plan trips in a Dungeons & Dragons-inspired style. The main goal was not only to call a language model, but to build a system that can find and use context before answering.

The agent uses Berget.AI through an OpenAI-compatible API. It can be run from the command line with an API key in a `.env` file.

## Agent Architecture

The system has several parts. The `main.py` file runs the command-line agent. The `retriever.py` file searches local Markdown travel notes in the `data/` folder. The `memory.py` file reads and writes JSON memory files. The `skills.py` file selects useful travel planning skills. The `prompts.py` file builds the prompt for the model, and `llm.py` sends the request to Berget.AI.

For a normal travel question, the agent first searches the local travel notes. It then reads the traveler profile and recent quest history from memory. After that, it selects skills such as `cozy_travel`, `avoid_crowds`, `slow_pace`, or `budget_guard`. These retrieved documents, memory files, and selected skills are added to the prompt before the question is sent to the LLM.

## Information Retrieval Methods

The project uses several simple IR methods. First, it uses keyword search over local Markdown files. Each document gets a score based on how many query words appear in the document. This is simple, but it makes the retrieval process easy to understand.

Second, the agent uses working memory. The file `memory/traveler_profile.json` stores preferences such as likes, dislikes, budget, and travel pace. The file `memory/quest_log.json` stores previous questions, answer previews, sources, and selected skills. This means that the agent can use both document context and user context.

Third, the agent has actions that update memory. Commands such as `/like`, `/dislike`, `/budget`, and `/pace` change the traveler profile. The `/search` command shows local document retrieval without calling the LLM. The `/trace` command shows query words, document scores, memory, and selected skills. This makes the IR process visible and easier to debug.

## OpenClaw Inspiration and Novel Part

The project was inspired by OpenClaw concepts such as memory files, skills, tool use, and compaction. My version is much smaller and simpler, but it adapts these ideas to a travel planning domain.

The more creative part of the system is that it retrieves three kinds of context: factual context from travel notes, personal context from memory files, and procedural context from selected skills. 

I also added a simple manual compaction command. The `/compact` command summarizes the quest log into `memory/quest_summary.json`. This is a small version of the compaction idea from OpenClaw. It helps keep long-term context without putting the full history into every prompt.

## Reflection on Using AI Tools

Using AI coding tools was helpful, especially for getting structure, examples, and debugging help. It made it faster to build a working prototype.

However, it was also difficult to follow the AI's structure and coding style. The AI often suggested code that was more advanced than I could understand. Because of this, I had to ask many times for simpler explanations and simpler versions of the code. Sometimes I also rewrote parts myself so that I could keep up and understand what was happening.

This made the process slower in some moments, but it was useful for learning. I learned that using AI for coding does not remove the need to understand the code. I still had to check how memory worked, how JSON files were read and written, how the retriever scored documents, and how the API connection worked. The most important lesson was that AI can help build faster, but I need to keep the code simple enough that I can explain and maintain it.

## Limitations and Future Work

The current retrieval method uses keyword matching, not embeddings. This is easy to understand, but it is not as powerful as semantic search. A future version could add vector search, web search, more travel documents, or more advanced tools.

The compaction system is also simple. It creates a deterministic summary from the quest log, but it does not use an LLM to write a natural language summary. This was chosen to keep the project understandable and reliable for the assignment.

## References

OpenClaw. (n.d.). *OpenClaw documentation*. https://docs.openclaw.ai/

OpenClaw. (n.d.). *Compaction concept*. https://github.com/openclaw/openclaw/blob/main/docs/concepts/compaction.md

Berget.AI. (n.d.). *Berget.AI API platform*. https://berget.ai/
