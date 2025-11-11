"""
All prompt templates in one place
"""

CATEGORIZATION_PROMPT = """Analyze this bedtime story request: "{user_input}"

Determine:
1. Primary category (choose ONE): adventure, fantasy, educational, friendship, courage, animal
2. Key themes
3. Main characters
4. Setting
5. Tone

Respond in EXACT JSON format:
{{
    "category": "<category>",
    "themes": ["<theme1>", "<theme2>"],
    "characters": ["<character1>"],
    "setting": "<setting or 'unspecified'>",
    "tone": "<tone>"
}}"""


STORY_ARC_PROMPT = """Create a story arc for ages 5-10: "{user_input}"

Category: {category}
Themes: {themes}

Create 5 parts (2-3 sentences each):
1. SETUP - Introduce character and setting
2. RISING ACTION - Present challenge
3. CLIMAX - Main exciting moment
4. FALLING ACTION - Overcome challenge
5. RESOLUTION - Happy ending with lesson

Respond in EXACT JSON format:
{{
    "setup": "<text>",
    "rising_action": "<text>",
    "climax": "<text>",
    "falling_action": "<text>",
    "resolution": "<text>"
}}"""


STORY_GENERATION_PROMPT = """You are a children's storyteller. Create a bedtime story for ages 5-10.

REQUEST: "{user_input}"
CATEGORY: {category}
STYLE: {guidelines}

STORY ARC:
1. SETUP: {setup}
2. RISING ACTION: {rising_action}
3. CLIMAX: {climax}
4. FALLING ACTION: {falling_action}
5. RESOLUTION: {resolution}

REQUIREMENTS:
- Simple vocabulary for ages 5-10
- Follow the story arc
- Include positive moral/lesson
- 350-450 words
- Safe content
- Peaceful ending

Write the complete story:"""


STORY_EVALUATION_PROMPT = """Evaluate this bedtime story for ages 5-10:

{story}

Rate on 1-10 scale:
1. AGE APPROPRIATENESS
2. STORY STRUCTURE
3. ENGAGEMENT
4. EDUCATIONAL VALUE

Respond in EXACT JSON format:
{{
    "age_appropriateness": <score>,
    "story_structure": <score>,
    "engagement": <score>,
    "educational_value": <score>,
    "overall_score": <average>,
    "feedback": "<suggestions or 'Excellent story!'>"
}}"""


STORY_REFINEMENT_PROMPT = """Improve this bedtime story:

STORY:
{story}

FEEDBACK:
{feedback}

Keep core story but address the feedback. Maintain age 5-10 appropriateness.

Provide the IMPROVED story:"""


USER_FEEDBACK_PROMPT = """Modify this story based on user request:

STORY:
{story}

USER REQUEST:
"{user_feedback}"

Incorporate the change naturally. Keep age-appropriate and similar length.

Provide the REVISED story:"""