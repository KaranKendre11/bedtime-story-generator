"""
Configuration and constants
"""
import os
from enum import Enum
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# API Configuration
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
OPENAI_MODEL = "gpt-3.5-turbo"

# Verify API key is loaded
if not OPENAI_API_KEY:
    print("\n⚠️  WARNING: OPENAI_API_KEY not found!")
    print("Please create a .env file with your API key:")
    print("OPENAI_API_KEY=your_api_key_here\n")

# Generation Settings
QUALITY_THRESHOLD = 7.0
MAX_REFINEMENTS = 2

# Temperature Settings
TEMP_CATEGORIZATION = 0.3
TEMP_PLANNING = 0.5
TEMP_STORYTELLING = 0.8
TEMP_EVALUATION = 0.2
TEMP_REFINEMENT = 0.7


class StoryCategory(Enum):
    """Story categories"""
    ADVENTURE = "adventure"
    FANTASY = "fantasy"
    EDUCATIONAL = "educational"
    FRIENDSHIP = "friendship"
    COURAGE = "courage"
    ANIMAL = "animal"


# Category-specific guidelines
CATEGORY_GUIDELINES = {
    StoryCategory.ADVENTURE: "Action-packed but safe. Journey, obstacles, exciting discoveries.",
    StoryCategory.FANTASY: "Magical and imaginative. Magic, mythical creatures, enchanted places.",
    StoryCategory.EDUCATIONAL: "Fun learning. Interesting facts, discovery, curiosity.",
    StoryCategory.FRIENDSHIP: "Warm relationships. Cooperation, kindness, helping others.",
    StoryCategory.COURAGE: "Overcoming fears. Facing challenges, building confidence.",
    StoryCategory.ANIMAL: "Animal characters. Animal behaviors, nature, friendships."
}


def validate_config():
    """Ensure API key is set"""
    if not OPENAI_API_KEY:
        raise ValueError(
            "OPENAI_API_KEY not found!\n"
            "Please:\n"
            "1. Create a .env file in the project root\n"
            "2. Add this line: OPENAI_API_KEY=your_actual_api_key_here\n"
            "3. Make sure python-dotenv is installed: pip install python-dotenv"
        )


# Verify configuration when imported
if __name__ == "__main__":
    # Test script to verify .env is loaded correctly
    print("\n" + "="*60)
    print("🔧 Configuration Test")
    print("="*60)
    
    if OPENAI_API_KEY:
        print(f"✅ API Key loaded: {OPENAI_API_KEY[:10]}...{OPENAI_API_KEY[-4:]}")
        print(f"✅ Model: {OPENAI_MODEL}")
        print(f"✅ Quality Threshold: {QUALITY_THRESHOLD}")
        print(f"✅ Max Refinements: {MAX_REFINEMENTS}")
        print("\n✨ Configuration is valid! Ready to run main.py")
    else:
        print("❌ API Key NOT found!")
        print("\nPlease create a .env file with:")
        print("OPENAI_API_KEY=your_actual_key_here")
    
    print("="*60 + "\n")