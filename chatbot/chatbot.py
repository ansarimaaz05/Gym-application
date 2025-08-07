import pandas as pd
import re

# Load calorie dataset
df = pd.read_csv("data/calorie_data.csv")

def get_chatbot_response(user_input):
    user_input = user_input.lower().strip()

    greetings = ["hi", "hello", "hey", "how are you", "what's up"]
    if any(greet in user_input for greet in greetings):
        return "Hey there! 👋 I'm your gym and diet assistant. Ask me about calories, food, fat loss diets, or workouts!"

    # Lookup calorie data (partial match)
    user_words = set(user_input.split())
    for _, row in df.iterrows():
        item_words = set(row["item"].lower().split())
        if row["item"].lower() in user_input or user_input in row["item"].lower() or user_words & item_words:
            return f"🍽️ **{row['item'].title()}** has approximately **{row['calories_per_100g']} calories per 100 grams**."

    # Nutrition advice with detailed responses
    if "protein" in user_input:
        return (
            "💪 **Why Protein is Important:**\n"
            "- Helps build and repair muscles.\n"
            "- Supports metabolism and satiety.\n"
            "- Aids recovery post-workout.\n\n"
            "**Top Protein Sources:**\n"
            "- Animal: Eggs, chicken, fish, Greek yogurt, whey protein.\n"
            "- Plant: Tofu, lentils, chickpeas, quinoa, peanuts."
        )
    elif "carb" in user_input:
        return (
            "⚡ **Carbohydrates (Carbs) Overview:**\n"
            "- Main source of energy for workouts and daily life.\n"
            "- Choose complex carbs for slow, steady energy.\n\n"
            "**Good Carb Sources:**\n"
            "- Oats, brown rice, sweet potatoes, whole wheat bread.\n"
            "- Fruits like bananas, apples, oranges (for quick energy)."
        )
    elif "fat" in user_input:
        return (
            "🥑 **Healthy Fats Role:**\n"
            "- Support hormone balance (testosterone, estrogen).\n"
            "- Aid vitamin absorption (A, D, E, K).\n"
            "- Provide sustained energy during fat loss.\n\n"
            "**Best Fat Sources:**\n"
            "- Nuts (almonds, walnuts), seeds (chia, flax).\n"
            "- Avocados, olive oil, peanut butter.\n"
            "- Fatty fish like salmon and sardines."
        )
    elif "pre workout" in user_input:
        return (
            "🏋️‍♂️ **Pre-Workout Fuel (30–60 mins before):**\n"
            "- Focus on carbs + small protein.\n"
            "- Avoid high fat or fiber (slow digestion).\n\n"
            "**Examples:**\n"
            "- Banana + peanut butter\n"
            "- Oats with whey protein\n"
            "- Toast with egg whites"
        )
    elif "post workout" in user_input:
        return (
            "🍽️ **Post-Workout Nutrition (within 60 mins):**\n"
            "- Replenish glycogen and promote muscle repair.\n"
            "- Combine protein and fast carbs.\n\n"
            "**Examples:**\n"
            "- Protein shake with banana\n"
            "- Grilled chicken + sweet potato\n"
            "- Greek yogurt with honey and fruit"
        )
    elif "meal plan" in user_input:
        return (
            "📅 **Basic Meal Plan Structure:**\n"
            "- 3 major meals + 2 small snacks.\n"
            "- Protein + complex carbs + healthy fats each meal.\n\n"
            "**Sample Meal:**\n"
            "- Breakfast: Oats + banana + almonds\n"
            "- Lunch: Chicken + rice + veggies\n"
            "- Snack: Boiled eggs or whey shake\n"
            "- Dinner: Tofu + stir-fry vegetables + quinoa"
        )
    elif "water" in user_input:
        return (
            "💧 **Hydration Tips:**\n"
            "- Drink 2–3 liters daily.\n"
            "- More if you sweat heavily or exercise.\n"
            "- Start your day with 1 glass of water.\n"
            "- Sip water throughout the workout, not just after."
        )
    elif "supplements" in user_input:
        return (
            "🧪 **Common Gym Supplements:**\n"
            "- **Whey Protein:** Muscle recovery.\n"
            "- **Creatine:** Boosts power and strength.\n"
            "- **Omega-3s:** Anti-inflammatory benefits.\n"
            "- **Multivitamins:** Fills micronutrient gaps.\n"
            "- **Electrolytes:** Rehydrate after heavy sweating."
        )
    elif "fat loss" in user_input or "lose weight" in user_input or "reduce weight" in user_input:
        return (
            "🔥 **Ultimate Fat Loss Strategy:**\n\n"
            "1. **Calorie Deficit:** Burn more than you consume.\n"
            "2. **High Protein:** Retain muscle while losing fat.\n"
            "3. **Smart Carbs:** Avoid sugar, prefer oats, fruits.\n"
            "4. **Healthy Fats:** Crucial for hormones.\n"
            "5. **Hydration:** Minimum 3 liters/day.\n"
            "6. **Workout:** 4x strength + 3x cardio weekly.\n"
            "7. **Sleep:** 7–8 hours supports fat metabolism.\n\n"
            "✅ Ask: 'give me a fat loss meal plan for 100kg' to get a full diet!"
        )
    elif "fat loss" in user_input and "plan" in user_input or "my weight is" in user_input:
        weight_match = re.search(r"(\d{2,3})\s?kg", user_input)
        if weight_match:
            weight = int(weight_match.group(1))
            maintenance = weight * 22
            deficit = maintenance - 500
            return (
                f"🧮 Based on your weight of **{weight}kg**, here's your personalized fat loss plan:\n\n"
                f"**Target Calories:** ~{deficit} kcal/day\n\n"
                "**🥗 Sample Fat Loss Meal Plan:**\n"
                "**1️⃣ Breakfast:**\n"
                "- 3 egg whites + 1 whole egg\n"
                "- 2 brown bread slices OR oats\n\n"
                "**2️⃣ Mid-Morning Snack:**\n"
                "- 1 apple + 5 almonds\n\n"
                "**3️⃣ Lunch:**\n"
                "- Grilled chicken or paneer\n"
                "- 1 cup brown rice or 2 roti + veggies\n"
                "- Salad + curd\n\n"
                "**4️⃣ Evening Snack:**\n"
                "- Black coffee + roasted chana or boiled egg\n\n"
                "**5️⃣ Dinner:**\n"
                "- Stir-fried veggies + tofu/chicken\n"
                "- Optional: Clear soup or dal\n\n"
                "**💡 Tips:**\n"
                "- Avoid sugary drinks/snacks.\n"
                "- Sleep 7–8 hours for best fat metabolism.\n"
                "- Exercise 5–6 days/week (mix cardio + strength)."
            )

    # Fallback
    return "I'm still learning 🤖 — try asking about calories, Indian food, fruits, or fat loss diet tips!"
