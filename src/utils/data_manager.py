"""
Data Manager — synthetic data generation and merging.
"""

import pandas as pd
import random
import os
from . import templates, constants


class DataManager:
    def add_noise(self, text):
        """Add typos or emojis for realistic training data."""
        if random.random() < 0.3:
            text = (text.replace("i", "ı").replace("ç", "c")
                    .replace("ş", "s").replace("ğ", "g")
                    .replace("ü", "u").replace("ö", "o"))

        if random.random() < 0.3:
            is_neg = any(x in text for x in ["çöp", "kötü", "yok", "rezalet", "iğrenç"])
            emojis = templates.neg_emojis if is_neg else templates.pos_emojis
            text += " " + random.choice(emojis)
        return text.lower()

    def generate_synthetic_data(self, target_count=None):
        """Generate synthetic data from all template categories."""
        target_count = target_count or constants.SYNTHETIC_COUNT
        data = []
        print(f"Generating synthetic data (target: {target_count})...")

        categories = list(constants.CATEGORY_WEIGHTS.keys())

        while len(data) < target_count:
            cat = random.choice(categories)
            text, label, cat_name = self._generate_sample(cat)
            data.append({
                "text": self.add_noise(text),
                "label": label,
                "category": cat_name
            })

        return pd.DataFrame(data)

    def _generate_sample(self, category):
        """Generate a single sample from a given category."""
        if category == "fashion":
            if random.random() < 0.5:
                return f"{random.choice(templates.fashion_items)} {random.choice(templates.fashion_neg)}.", 0, "Fashion"
            return f"{random.choice(templates.fashion_items)} {random.choice(templates.fashion_pos)}.", 2, "Fashion"

        elif category == "cosmetic":
            if random.random() < 0.5:
                return f"{random.choice(templates.cosmetic_items)} {random.choice(templates.cosmetic_neg)}.", 0, "Cosmetic"
            return f"{random.choice(templates.cosmetic_items)} {random.choice(templates.cosmetic_pos)}.", 2, "Cosmetic"

        elif category == "tech":
            if random.random() < 0.5:
                return f"{random.choice(templates.tech_items)} {random.choice(templates.tech_neg)}.", 0, "Tech"
            return f"{random.choice(templates.tech_items)} {random.choice(templates.tech_pos)}.", 2, "Tech"

        elif category == "student":
            if random.random() < 0.6:
                return f"{random.choice(templates.student_context)} {random.choice(templates.student_neg)}.", 0, "Student"
            return f"{random.choice(templates.student_context)} {random.choice(templates.student_pos)}.", 2, "Student"

        elif category == "art":
            if random.random() < 0.5:
                return f"{random.choice(templates.art_items)} {random.choice(templates.art_neg)}.", 0, "Art"
            return f"{random.choice(templates.art_items)} {random.choice(templates.art_pos)}.", 2, "Art"

        elif category == "2ndhand":
            if random.random() < 0.5:
                return random.choice(templates.secondhand_neg), 0, "2ndHand"
            return random.choice(templates.secondhand_pos), 2, "2ndHand"

        elif category == "ks":
            if random.random() < 0.5:
                return random.choice(templates.ks_neg), 0, "KS"
            return random.choice(templates.ks_pos), 2, "KS"

        elif category == "neutral":
            return random.choice(templates.neutral_statements), 1, "Neutral"

        elif category == "irony":
            text = random.choice(templates.irony_templates)
            text = text.replace("{time}", random.choice(templates.times))
            text = text.replace("{adjective}", random.choice(templates.adjectives))
            return text, 0, "Irony"

        elif category == "culture_neg":
            pool = templates.cultural_irony + templates.daily_struggles + templates.context_neg
            return random.choice(pool), 0, "Cultural_Neg"

        elif category == "culture_pos":
            return random.choice(templates.cultural_pos), 2, "Cultural_Pos"

        elif category == "gamer":
            text = random.choice(templates.gamer_slang)
            label = 2 if any(w in text for w in ["efsane", "güzel", "ezdim", "carryledim"]) else 0
            return text, label, "Gamer"

        elif category == "rel":
            text = random.choice(templates.rel_slang)
            label = 2 if any(w in text for w in ["Shipledim", "yakıştınız"]) else 0
            return text, label, "Rel"

        elif category == "food":
            return random.choice(templates.food_hate), 0, "Food"

        elif category == "life":
            return random.choice(templates.life_struggle), 0, "Life"

        elif category == "noise":
            return random.choice(templates.noise_texts), 1, "Noise"

        return "...", 1, "Misc"
