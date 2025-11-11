"""
Bedtime Story Generator - Main Entry Point

Before submitting the assignment, describe here in a few sentences what you would 
have built next if you spent 2 more hours on this project:

If I had 2 more hours, I would:
1. Add story saving/loading - save generated stories to JSON files for later retrieval
2. Implement story length options (short/medium/long) for different bedtimes
3. Add comprehensive unit tests with mocked OpenAI responses
4. Create better error handling and retry logic for API failures
5. Build a simple web interface using Streamlit for better user experience
"""

from agents import StoryGenerator


def main():
    """Main application"""
    print("\n" + "="*60)
    print("🌟 BEDTIME STORY GENERATOR 🌟")
    print("   (For children ages 5-10)")
    print("="*60)
    print("\nFeatures:")
    print("  • Smart story categorization")
    print("  • Structured story arcs")
    print("  • Quality evaluation")
    print("  • User feedback")
    print("="*60)
    
    # Get user input
    user_input = input("\nWhat kind of story would you like? ").strip()
    if not user_input:
        print("Please provide a story request!")
        return
    
    # Generate story
    generator = StoryGenerator()
    story, evaluation, story_request = generator.generate(user_input)
    
    # Display story
    print("\n" + "="*60)
    print("📖 YOUR BEDTIME STORY:")
    print("="*60 + "\n")
    print(story)
    print("\n" + "="*60)
    print(f"Category: {story_request.category.value.upper()}")
    print(f"Quality Score: {evaluation.overall_score:.1f}/10")
    print("="*60)
    
    # Feedback loop
    while True:
        response = input("\nMake changes? (yes/no): ").strip().lower()
        
        if response in ['no', 'n', '']:
            print("\n✨ Enjoy your story!")
            break
        
        if response in ['yes', 'y']:
            change = input("What to change? ").strip()
            if change:
                story = generator.apply_user_feedback(story, change, story_request.category)
                
                # Re-evaluate the updated story
                print("\n👨‍⚖️ Re-evaluating updated story...")
                evaluation = generator._evaluate(story)
                generator._print_scores(evaluation)
                
                print("\n" + "="*60)
                print("📖 UPDATED STORY:")
                print("="*60 + "\n")
                print(story)
                print("\n" + "="*60)
                print(f"Updated Quality Score: {evaluation.overall_score:.1f}/10")
                print("="*60)
    
    print("\n🌙 Sweet dreams! 🌙\n")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nGoodbye! 👋")
    except Exception as e:
        print(f"\n❌ Error: {e}")
        print("Check your .env file has OPENAI_API_KEY set.")