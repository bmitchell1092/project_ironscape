# quests.py (updated to handle weekly and milestone quests)
import json
import os
from support import get_asset_path

QUESTS_PATH = get_asset_path('data', 'quests.json')

DEFAULT_QUESTS = {
    "last_updated": None,
    "weekly": {
        "Strength": {
            "description": "Go to the gym at least once this week",
            "completed": False,
            "xp_reward": 5000
        },
        "Cooking": {
            "description": "Prep 2 balanced meals",
            "completed": False,
            "xp_reward": 2000
        },
        "Agility": {
            "description": "Climb once this week",
            "completed": False,
            "xp_reward": 3500
        },
        "Hitpoints": {
            "description": "Run around the block",
            "completed": False,
            "xp_reward": 4000
        }
    },
    "milestones": {
        "Strength": [
            {
                "description": "Reach Strength level 10",
                "completed": False,
                "xp_reward": 10000
            },
            {
                "description": "Bench press 135lbs",
                "completed": False,
                "xp_reward": 8000
            }
        ],
        "Cooking": [
            {
                "description": "Cook 5 different meals",
                "completed": False,
                "xp_reward": 6000
            }
        ],
        "Agility": [
            {
                "description": "Climb a V4 route",
                "completed": False,
                "xp_reward": 7000
            }
        ]
    }
}

class QuestLog:
    def __init__(self, path=QUESTS_PATH):
        self.path = path
        self.data = self.load_or_initialize_quests()

    def load_or_initialize_quests(self):
        if os.path.exists(self.path):
            with open(self.path, 'r') as file:
                return json.load(file)
        else:
            self.save_quests(DEFAULT_QUESTS)
            return DEFAULT_QUESTS

    def save_quests(self, data=None):
        if data is None:
            data = self.data
        with open(self.path, 'w') as file:
            json.dump(data, file, indent=4)

    def get_weekly_quests(self):
        return self.data.get("weekly", {})

    def get_milestone_quests(self):
        return self.data.get("milestones", {})

    def complete_weekly_quest(self, skill):
        if skill in self.data["weekly"]:
            self.data["weekly"][skill]["completed"] = True
            self.save_quests()
            return self.data["weekly"][skill].get("xp_reward", 0)
        return 0

    def complete_next_milestone_quest(self, skill):
        milestones = self.data["milestones"].get(skill, [])
        for quest in milestones:
            if not quest["completed"]:
                quest["completed"] = True
                self.save_quests()
                return quest.get("xp_reward", 0)
        return 0

    def reset_weekly_quests(self):
        for quest in self.data.get("weekly", {}).values():
            quest["completed"] = False
        self.save_quests()

    def get_xp_reward(self, category, skill):
        if category == "weekly" and skill in self.data["weekly"]:
            return self.data["weekly"][skill].get("xp_reward", 0)
        elif category == "milestones" and skill in self.data["milestones"]:
            for quest in self.data["milestones"][skill]:
                if not quest["completed"]:
                    return quest.get("xp_reward", 0)
        return 0

    def is_weekly_quest_clicked(self, skill, rect, mouse_pos):
        return skill in self.data["weekly"] and rect.collidepoint(mouse_pos)

    def is_milestone_quest_clicked(self, skill, quest, rect, mouse_pos):
        return not quest["completed"] and rect.collidepoint(mouse_pos)



