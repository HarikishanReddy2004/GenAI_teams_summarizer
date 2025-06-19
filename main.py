import os,re
from datetime import datetime
from config import BOARD_ID
from jira_client import jira_client
from transcript_processor import transcript_processor
from summarizer import summarizer

def match_story_ref_to_key(ref, story_keys):
    for key in story_keys:
        if ref in key:
            return key
    return None

def replace_summary_with_person(summary, person_name):
    return summary.replace("**Summary:**", f"{person_name}:")


def main():
    with open("D:\\teams_genai\\venv\\conversation.txt", "r") as f:
        conversation_text = f.read()
    print(BOARD_ID)
    print(conversation_text)
    sprint_id = jira_client.get_active_sprint(BOARD_ID)
    print(sprint_id)
    if not sprint_id:
        print("No active sprint found.")
        return

    story_map = jira_client.get_issues_in_sprint(sprint_id)
    story_keys = list(story_map.keys())
    story_values = list(story_map.values())
    print(f"Fetched {len(story_keys)} stories from sprint.")

    # Extract structured updates: {person: {story_id: [comments]}}
    updates = transcript_processor.extract_updates(conversation_text)

    # Define summarization instruction
    summarization_instruction = (
        "Summarize the updates in a clear, concise manner suitable for posting in a Jira comment. "
        "Make sure comments should not be repetitive and Dont consider unwanted discussions into account such as 'He is on mute i guess' which are not related to the work at all."
    )

    todays_content=[];weekly_content=[]
    for person, stories in updates.items():
        for story_id, comments in stories.items():
            story_key = match_story_ref_to_key(story_id, story_keys)
            if not story_key:
                print(f"Story reference {story_id} not found in active sprint.")
                continue

            combined_text = " ".join(comments)
            summary = summarizer.generate_summary(combined_text, summarization_instruction)
            # summary=replace_summary_with_person(summary, person)
            summary=summarizer.generate_summary(str(summary))
            print(f"Posting comment to {story_key}: {summary}")

            status = jira_client.post_comment(story_key, summary)
            if status == 201:
                print(f"  Successfully commented on {story_key}")
            else:
                print(f"  Failed to comment on {story_key}")
            # Collect today's content for further processing or output  

            todays_content.append(f"{summary}")
            weekly_content.append(f"{story_map[story_key]}:{summary}")
# Save daily summary as before
    output_dir = os.path.join(os.path.dirname(__file__), '.', 'weekly_summary_inputs')
    os.makedirs(output_dir, exist_ok=True)
    date_str = datetime.now().strftime('%Y-%m-%d')
    filename = f'{date_str}_summary.txt'
    filepath = os.path.join(output_dir, filename)
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write('\n'.join(todays_content))
    print(f"All summaries written to {filepath}")

    # Append today's content to the weekly file
    weekly_dir = os.path.join(os.path.dirname(__file__), '.', 'weekly_data')
    os.makedirs(weekly_dir, exist_ok=True)
    weekly_file = os.path.join(weekly_dir, 'current_week.txt')
    with open(weekly_file, 'w', encoding='utf-8') as f:
        f.write('\n'.join(weekly_content))
    print(f"All summaries written to {weekly_file}")
