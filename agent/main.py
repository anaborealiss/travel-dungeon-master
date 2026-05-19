from agent.memory import (
    remember_like,
    remember_dislike,
    remember_budget,
    remember_pace,
    add_to_quest_log,
    get_memory_text,
    load_profile,
    compact_quest_log
)
from agent.retriever import search_documents, make_context_text, get_query_words
from agent.prompts import build_messages
from agent.llm import ask_llm
from agent.skills import select_skills, make_skills_text


def show_help():
    print("""
Travel Dungeon Master commands:

/help
  Show commands.

/profile
  Show current traveler memory.

/like something
  Remember something you like.

/dislike something
  Remember something you dislike.

/budget low
  Remember your budget.

/pace slow
  Remember your travel pace.

/search question
  Search local travel notes without asking the AI.

/trace question
  Show retrieved documents, scores, memory, and selected skills.

/compact
  Summarize quest history into memory/quest_summary.json.

/exit
  Stop the agent.

You can also type any travel question normally.
""")


def handle_memory_command(user_input):
    if user_input.startswith("/like "):
        value = user_input.replace("/like ", "", 1)
        remember_like(value)
        print("Remembered like:", value)
        return True

    if user_input.startswith("/dislike "):
        value = user_input.replace("/dislike ", "", 1)
        remember_dislike(value)
        print("Remembered dislike:", value)
        return True

    if user_input.startswith("/budget "):
        value = user_input.replace("/budget ", "", 1)
        remember_budget(value)
        print("Remembered budget:", value)
        return True

    if user_input.startswith("/pace "):
        value = user_input.replace("/pace ", "", 1)
        remember_pace(value)
        print("Remembered pace:", value)
        return True

    return False


def answer_question(user_question):
    search_results = search_documents(user_question)
    context_text = make_context_text(search_results)
    memory_text = get_memory_text()
    selected_skills = select_skills(user_question, memory_text)
    skills_text = make_skills_text(selected_skills)

    messages = build_messages(user_question, memory_text, context_text, skills_text)
    answer = ask_llm(messages)

    sources = []
    for result in search_results:
        sources.append(result["source"])

    skill_names = []
    for skill in selected_skills:
        skill_names.append(skill["name"])

    add_to_quest_log(user_question, answer, sources, skill_names)

    print("\n" + answer + "\n")


def trace_question(user_question):
    query_words = get_query_words(user_question)
    search_results = search_documents(user_question)
    memory_text = get_memory_text()
    profile = load_profile()
    selected_skills = select_skills(user_question, memory_text)

    print("\nIR trace")
    print("Query words:", ", ".join(query_words))

    print("\nTraveler memory:")
    print("Likes:", profile["likes"])
    print("Dislikes:", profile["dislikes"])
    print("Budget:", profile["budget"])
    print("Pace:", profile["pace"])

    print("\nRetrieved documents:")
    if not search_results:
        print("No local travel notes were found.")
    else:
        for index, result in enumerate(search_results, start=1):
            print(f"{index}. {result['source']} score={result['score']}")

    print("\nSelected skills:")
    if not selected_skills:
        print("No special travel skills were selected.")
    else:
        for skill in selected_skills:
            print(f"- {skill['name']}: {skill['description']}")

    print()


def main():
    print("Travel Dungeon Master is awake.")
    print("Type /help for commands.")

    while True:
        user_input = input("\nYou: ").strip()

        if user_input == "":
            continue

        if user_input == "/exit":
            print("Goodbye, traveler.")
            break

        if user_input == "/help":
            show_help()
            continue

        if user_input == "/profile":
            print(get_memory_text())
            continue

        if user_input.startswith("/search "):
            query = user_input.replace("/search ", "", 1)
            results = search_documents(query)
            print(make_context_text(results))
            continue

        if user_input.startswith("/trace "):
            query = user_input.replace("/trace ", "", 1)
            trace_question(query)
            continue

        if user_input == "/compact":
            summary = compact_quest_log()
            print("Quest log compacted:")
            print(summary)
            continue

        memory_command_was_used = handle_memory_command(user_input)

        if memory_command_was_used:
            continue

        answer_question(user_input)


if __name__ == "__main__":
    main()
