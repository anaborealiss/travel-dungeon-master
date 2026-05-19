import json
from pathlib import Path
from datetime import datetime


BASE_DIR = Path(__file__).resolve().parents[1] #python counts from a folder where a current doc is so [1] is the main folder

PROFILE_FILE = BASE_DIR / "memory" / "traveler_profile.json"
QUEST_LOG_FILE = BASE_DIR / "memory" / "quest_log.json"
QUEST_SUMMARY_FILE = BASE_DIR / "memory" / "quest_summary.json"


def read_json(file_path, default_value):
    if not file_path.exists():
        return default_value

    with open(file_path, "r", encoding="utf-8") as file:
        return json.load(file)

def write_json(file_path, data):
    with open(file_path, "w", encoding="utf-8") as file:
        json.dump(data, file, indent=2, ensure_ascii=False)


def load_profile():
    default_profile = {
        "name": "Traveler",
        "likes": [],
        "dislikes": [],
        "budget": "unknown",
        "pace": "unknown",
        "visited_places": []
    }

    return read_json(PROFILE_FILE, default_profile)


def save_profile(profile):
    write_json(PROFILE_FILE, profile)


def remember_like(new_like):
    profile = load_profile()

    if new_like not in profile["likes"]:
        profile["likes"].append(new_like)

    save_profile(profile)


def remember_dislike(new_dislike):
    profile = load_profile()

    if new_dislike not in profile["dislikes"]:
        profile["dislikes"].append(new_dislike)

    save_profile(profile)


def remember_budget(budget):
    profile = load_profile()
    profile["budget"] = budget
    save_profile(profile)


def remember_pace(pace):
    profile = load_profile()
    profile["pace"] = pace
    save_profile(profile)


def add_to_quest_log(question, answer, sources, skills=None):
    quest_log = read_json(QUEST_LOG_FILE, [])

    new_entry = {
        "time": datetime.now().isoformat(timespec="seconds"),
        "question": question,
        "answer": answer[:300],
        "sources": sources,
        "skills": skills or []
    }

    quest_log.append(new_entry)
    write_json(QUEST_LOG_FILE, quest_log)


def compact_quest_log():
    quest_log = read_json(QUEST_LOG_FILE, [])

    if not quest_log:
        summary = {
            "total_quests": 0,
            "common_sources": [],
            "common_skills": [],
            "recent_questions": []
        }
        write_json(QUEST_SUMMARY_FILE, summary)
        return summary

    source_counts = {}
    skill_counts = {}

    for entry in quest_log:
        for source in entry.get("sources", []):
            source_counts[source] = source_counts.get(source, 0) + 1

        for skill in entry.get("skills", []):
            skill_counts[skill] = skill_counts.get(skill, 0) + 1

    common_sources = sorted(source_counts, key=source_counts.get, reverse=True)
    common_skills = sorted(skill_counts, key=skill_counts.get, reverse=True)

    recent_questions = []
    for entry in quest_log[-5:]:
        recent_questions.append(entry.get("question", ""))

    summary = {
        "total_quests": len(quest_log),
        "common_sources": common_sources[:5],
        "common_skills": common_skills[:5],
        "recent_questions": recent_questions
    }

    write_json(QUEST_SUMMARY_FILE, summary)
    return summary


def get_memory_text():
    profile = load_profile()
    quest_log = read_json(QUEST_LOG_FILE, [])
    quest_summary = read_json(QUEST_SUMMARY_FILE, {})

    recent_quests = quest_log[-3:]

    memory_text = f"""
Traveler profile:
Name: {profile["name"]}
Likes: {profile["likes"]}
Dislikes: {profile["dislikes"]}
Budget: {profile["budget"]}
Pace: {profile["pace"]}
Visited places: {profile["visited_places"]}

Recent quest log:
{recent_quests}

Quest summary:
{quest_summary}
"""

    return memory_text
