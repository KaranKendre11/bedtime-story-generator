"""
All agent classes
"""
import json
from dataclasses import dataclass
from typing import List, Tuple
from openai import OpenAI

import config
from prompts import *


@dataclass
class StoryRequest:
    """Story request data"""
    user_input: str
    category: config.StoryCategory
    themes: List[str]
    characters: List[str]
    setting: str
    tone: str


@dataclass
class StoryArc:
    """Story structure"""
    setup: str
    rising_action: str
    climax: str
    falling_action: str
    resolution: str


@dataclass
class StoryEvaluation:
    """Evaluation results"""
    age_appropriateness: int
    story_structure: int
    engagement: int
    educational_value: int
    overall_score: float
    feedback: str


class OpenAIClient:
    """Simple OpenAI wrapper"""
    
    def __init__(self):
        config.validate_config()
        self.client = OpenAI(api_key=config.OPENAI_API_KEY)
    
    def call(self, prompt: str, max_tokens: int = 1000, temperature: float = 0.7) -> str:
        """Call GPT-3.5-turbo"""
        response = self.client.chat.completions.create(
            model=config.OPENAI_MODEL,
            messages=[{"role": "user", "content": prompt}],
            max_tokens=max_tokens,
            temperature=temperature,
        )
        return response.choices[0].message.content
    
    @staticmethod
    def parse_json(response: str, fallback: dict) -> dict:
        """Parse JSON with fallback"""
        try:
            cleaned = response.replace("```json", "").replace("```", "").strip()
            return json.loads(cleaned)
        except:
            return fallback


class StoryGenerator:
    """Main story generator - coordinates all agents"""
    
    def __init__(self):
        self.client = OpenAIClient()
    
    def generate(self, user_input: str) -> Tuple[str, StoryEvaluation, StoryRequest]:
        """Generate complete story"""
        print("\n" + "="*60)
        print("🌙 GENERATING YOUR BEDTIME STORY...")
        print("="*60)
        
        # Step 1: Categorize
        print("\n🔍 Analyzing request...")
        story_request = self._categorize(user_input)
        print(f"   Category: {story_request.category.value.upper()}")
        print(f"   Themes: {', '.join(story_request.themes)}")
        
        # Step 2: Plan arc
        print("\n📐 Planning story structure...")
        story_arc = self._plan_arc(story_request)
        print("   ✓ Story arc created")
        
        # Step 3: Generate story
        print(f"\n📝 Writing {story_request.category.value} story...")
        story = self._write_story(story_request, story_arc)
        
        # Step 4: Evaluate and refine
        evaluation = self._evaluate_and_refine(story)
        
        print("\n" + "="*60)
        print("✨ STORY COMPLETE!")
        print("="*60 + "\n")
        
        return story, evaluation, story_request
    
    def _categorize(self, user_input: str) -> StoryRequest:
        """Categorize story request"""
        prompt = CATEGORIZATION_PROMPT.format(user_input=user_input)
        response = self.client.call(prompt, max_tokens=300, temperature=config.TEMP_CATEGORIZATION)
        
        data = self.client.parse_json(response, {
            "category": "adventure",
            "themes": ["bravery"],
            "characters": ["hero"],
            "setting": "unspecified",
            "tone": "exciting"
        })
        
        return StoryRequest(
            user_input=user_input,
            category=config.StoryCategory(data["category"]),
            themes=data["themes"],
            characters=data["characters"],
            setting=data["setting"],
            tone=data["tone"]
        )
    
    def _plan_arc(self, story_request: StoryRequest) -> StoryArc:
        """Plan story arc"""
        prompt = STORY_ARC_PROMPT.format(
            user_input=story_request.user_input,
            category=story_request.category.value,
            themes=", ".join(story_request.themes)
        )
        response = self.client.call(prompt, max_tokens=500, temperature=config.TEMP_PLANNING)
        
        data = self.client.parse_json(response, {
            "setup": "Introduce character.",
            "rising_action": "Challenge appears.",
            "climax": "Face challenge.",
            "falling_action": "Find solution.",
            "resolution": "Happy ending."
        })
        
        return StoryArc(**data)
    
    def _write_story(self, story_request: StoryRequest, story_arc: StoryArc) -> str:
        """Generate story"""
        guidelines = config.CATEGORY_GUIDELINES.get(
            story_request.category,
            config.CATEGORY_GUIDELINES[config.StoryCategory.ADVENTURE]
        )
        
        prompt = STORY_GENERATION_PROMPT.format(
            user_input=story_request.user_input,
            category=story_request.category.value,
            guidelines=guidelines,
            setup=story_arc.setup,
            rising_action=story_arc.rising_action,
            climax=story_arc.climax,
            falling_action=story_arc.falling_action,
            resolution=story_arc.resolution
        )
        
        return self.client.call(prompt, max_tokens=900, temperature=config.TEMP_STORYTELLING)
    
    def _evaluate_and_refine(self, story: str) -> StoryEvaluation:
        """Evaluate and refine story"""
        for iteration in range(config.MAX_REFINEMENTS):
            print(f"\n👨‍⚖️ Judge evaluating (Attempt {iteration + 1})...")
            evaluation = self._evaluate(story)
            
            self._print_scores(evaluation)
            
            if evaluation.overall_score >= config.QUALITY_THRESHOLD:
                print(f"\n✅ Approved! Score: {evaluation.overall_score:.1f}/10")
                return evaluation
            
            print(f"\n🔄 Refining story...")
            print(f"   Feedback: {evaluation.feedback}")
            story = self._refine(story, evaluation.feedback)
        
        return evaluation
    
    def _evaluate(self, story: str) -> StoryEvaluation:
        """Evaluate story"""
        prompt = STORY_EVALUATION_PROMPT.format(story=story)
        response = self.client.call(prompt, max_tokens=500, temperature=config.TEMP_EVALUATION)
        
        data = self.client.parse_json(response, {
            "age_appropriateness": 7,
            "story_structure": 7,
            "engagement": 7,
            "educational_value": 7,
            "overall_score": 7.0,
            "feedback": "Acceptable."
        })
        
        return StoryEvaluation(**data)
    
    def _refine(self, story: str, feedback: str) -> str:
        """Refine story"""
        prompt = STORY_REFINEMENT_PROMPT.format(story=story, feedback=feedback)
        return self.client.call(prompt, max_tokens=900, temperature=config.TEMP_REFINEMENT)
    
    def apply_user_feedback(self, story: str, user_feedback: str, category: config.StoryCategory) -> str:
        """Apply user changes"""
        print("\n🔄 Updating story...")
        prompt = USER_FEEDBACK_PROMPT.format(
            story=story,
            user_feedback=user_feedback
        )
        return self.client.call(prompt, max_tokens=900, temperature=config.TEMP_REFINEMENT)
    
    @staticmethod
    def _print_scores(evaluation: StoryEvaluation):
        """Print evaluation scores"""
        print(f"\n📊 SCORES:")
        print(f"   Age Appropriateness: {evaluation.age_appropriateness}/10")
        print(f"   Story Structure: {evaluation.story_structure}/10")
        print(f"   Engagement: {evaluation.engagement}/10")
        print(f"   Educational Value: {evaluation.educational_value}/10")
        print(f"   Overall: {evaluation.overall_score:.1f}/10")
