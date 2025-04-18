# skill.py (updated with get_next_level_xp for hover support)
import json

class Skill:
    XP_TABLE = [0, 83, 174, 276, 388, 512, 650, 801, 969, 1154, 1358, 1584, 1833, 2107, 2411, 2746, 3115, 3523, 3973, 4470,
                5018, 5624, 6291, 7028, 7842, 8740, 9730, 10824, 12031, 13363, 14833, 16456, 18247, 20224, 22406, 24815,
                27473, 30408, 33648, 37224, 41171, 45529, 50339, 55649, 61512, 67983, 75127, 83014, 91721, 101333, 111945,
                123660, 136594, 150872, 166636, 184040, 203254, 224466, 247886, 273742, 302288, 333804, 368599, 407015,
                449428, 496254, 547953, 605032, 668051, 737627, 814445, 899257, 992895, 1096278, 1210421, 1336443,
                1475581, 1629200, 1798808, 1986068, 2192818, 2421087, 2673114, 2951373, 3258594, 3597792, 3972294,
                4385776, 4842295, 5346332, 5902831, 6517253, 7195629, 7944614, 8771558, 9684577, 10692629, 11805606,
                13034431, 14391160, 15889109, 17542976, 19368992, 21385073, 23611006, 26068632, 28782069, 31777943,
                35085654, 38737661, 42769801, 47221641, 52136869, 57563718, 63555443, 70170840, 77474828, 85539082,
                94442737, 104273167]

    def __init__(self, name, xp=0):
        self.name = name
        self.xp = xp
        self.level = self.calculate_level()

    def add_xp(self, amount):
        self.xp += amount
        self.level = self.calculate_level()

    def calculate_level(self):
        for i, xp_required in enumerate(self.XP_TABLE):
            if self.xp < xp_required:
                return i
        return 99

    def xp_to_next_level(self):
        if self.level >= 99:
            return 0
        return self.XP_TABLE[self.level] - self.xp

    def get_next_level_xp(self):
        if self.level >= 99:
            return self.XP_TABLE[98]  # Final threshold to reach 99
        return self.XP_TABLE[self.level]

    def to_dict(self):
        return {"name": self.name, "xp": self.xp}

    @staticmethod
    def from_dict(data):
        return Skill(data["name"], data["xp"])


def save_skills(skills, filepath="data/skills.json"):
    with open(filepath, 'w') as f:
        json.dump({name: skill.to_dict() for name, skill in skills.items()}, f, indent=4)


def load_skills(filepath="data/skills.json"):
    try:
        with open(filepath, 'r') as f:
            data = json.load(f)
            return {name: Skill.from_dict(skill_data) for name, skill_data in data.items()}
    except FileNotFoundError:
        return {}