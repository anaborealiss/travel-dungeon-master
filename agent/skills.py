SKILLS = {
    "cozy_travel": {
        "keywords": ["cozy", "calm", "quiet", "cafe", "cafes", "relax", "soft"],
        "description": "Use calm streets, cafes, parks, and rest breaks. Keep the plan warm and comfortable."
    },
    "avoid_crowds": {
        "keywords": ["crowd", "crowds", "crowded", "busy", "tourists", "quiet"],
        "description": "Avoid very crowded places when possible. If a famous place is useful, suggest visiting early or late."
    },
    "slow_pace": {
        "keywords": ["slow", "relaxed", "easy", "not too much", "rest", "chill"],
        "description": "Plan fewer stops and add enough time between places."
    },
    "food_buffs": {
        "keywords": ["food", "eat", "restaurant", "snack", "dessert", "buff", "buffs"],
        "description": "Suggest local food as Dungeons & Dragons-style buffs, but keep the advice practical."
    },
    "budget_guard": {
        "keywords": ["cheap", "budget", "low", "free", "affordable"],
        "description": "Prefer low-cost activities, walking routes, parks, markets, and simple food stops."
    }
}


def select_skills(user_question, memory_text):
    selected_skills = []
    search_text = (user_question + " " + memory_text).lower()

    for skill_name, skill_data in SKILLS.items():
        for keyword in skill_data["keywords"]:
            if keyword in search_text:
                selected_skills.append({
                    "name": skill_name,
                    "description": skill_data["description"]
                })
                break

    return selected_skills


def make_skills_text(selected_skills):
    if not selected_skills:
        return "No special travel skills were selected."

    lines = []

    for skill in selected_skills:
        line = f"- {skill['name']}: {skill['description']}"
        lines.append(line)

    return "\n".join(lines)
