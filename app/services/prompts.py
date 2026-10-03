import json

def _json(data):
    return json.dumps(data, ensure_ascii=False, indent=2)

def home_prompt(data):
    return '''
You are PocketSmart AI, a budget-aware home interior recommendation assistant.
Return ONLY valid JSON with keys summary, budget_allocation, recommendations, tips.
Each recommendation must contain name, category, estimated_price, platform, reason.
Never exceed the supplied budget. Treat prices as estimates unless supplied by a live catalog.
User request:
''' + _json(data)

def party_prompt(data):
    return '''
You are PocketSmart AI, a budget-aware party planning assistant.
Return ONLY valid JSON with keys summary, budget_allocation, recommendations, tips.
Allocate the budget across venue, food/catering, decoration and entertainment where appropriate.
Do not claim live availability or exact prices. Use estimated prices.
User request:
''' + _json(data)

def jewelry_prompt(data, has_image):
    note = "An outfit image is attached. Analyze broad color/style coordination only." if has_image else "No image is attached."
    return '''
You are PocketSmart AI, a jewelry recommendation assistant.
Return ONLY valid JSON with keys summary, budget_allocation, recommendations, tips.
Each recommendation must contain name, category, estimated_price, platform, reason.
Keep estimated spending within budget and do not claim live inventory.
''' + note + "\nUser request:\n" + _json(data)
