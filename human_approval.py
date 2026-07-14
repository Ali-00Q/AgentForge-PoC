import json

def human_approval(title, content):
    print(title)
    print(json.dumps(content, indent=2))
    print()

    answer = input("Approve? (y/n): ").strip().lower()

    if answer == "y":
        return True, None
    
    feedback = input("\nEnter feedback: ")

    return False, feedback