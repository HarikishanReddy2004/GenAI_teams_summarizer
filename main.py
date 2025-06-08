# from config import BOARD_ID
# from jira_client import jira_client
# from transcript_processor import transcript_processor
# from summarizer import summarizer
#
# def match_story_ref_to_key(ref, story_keys):
#     for key in story_keys:
#         if ref in key:
#             return key
#     return None
#
# def main():
#     with open("conversation.txt", "r") as f:
#         conversation_text = f.read()
#
#     sprint_id = jira_client.get_active_sprint(BOARD_ID)
#     if not sprint_id:
#         print("No active sprint found.")
#         return
#
#     story_map = jira_client.get_issues_in_sprint(sprint_id)
#     story_keys = list(story_map.keys())
#     print(f"Fetched {len(story_keys)} stories from sprint.")
#
#     updates = transcript_processor.extract_updates(conversation_text)
#
#     # Iterate over all updates and group them based on story ID
#     for story_id, texts in updates.items():
#         # Find the corresponding Jira story key from the sprint issues
#         story_key = match_story_ref_to_key(story_id, story_keys)
#         if not story_key:
#             print(f"Story reference {story_id} not found in active sprint.")
#             continue
#
#         # Combine all updates for the story
#         combined_text = " ".join(texts)
#         summary = summarizer.generate_summary(combined_text)
#
#         print(f"Posting comment to {story_key}: {summary}")
#
#         # Post the summary to the Jira comment section
#         status = jira_client.post_comment(story_key, summary)
#         if status == 201:
#             print(f" Successfully commented on {story_key}")
#         else:
#             print(f" Failed to comment on {story_key}")
#
# if __name__ == "__main__":
#     main()

from config import BOARD_ID
from jira_client import jira_client
from transcript_processor import transcript_processor
from summarizer import summarizer

def match_story_ref_to_key(ref, story_keys):
    for key in story_keys:
        if ref in key:
            return key
    return None

def main():
    with open("conversation.txt", "r") as f:
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
    print(f"Fetched {len(story_keys)} stories from sprint.")

    # Extract structured updates: {person: {story_id: [comments]}}
    updates = transcript_processor.extract_updates(conversation_text)

    # Define summarization instruction
    summarization_instruction = (
        "Summarize the updates in a clear, concise manner suitable for posting in a Jira comment. "
        "Make sure comments should not be repetitive and Dont consider unwanted discussions into account such as 'He is on mute i guess' which are not related to the work at all."
    )

    for person, stories in updates.items():
        for story_id, comments in stories.items():
            story_key = match_story_ref_to_key(story_id, story_keys)
            if not story_key:
                print(f"Story reference {story_id} not found in active sprint.")
                continue

            combined_text = " ".join(comments)
            summary = summarizer.generate_summary(combined_text, summarization_instruction)

            print(f"Posting comment to {story_key}: {summary}")

            status = jira_client.post_comment(story_key, summary)
            if status == 201:
                print(f"  Successfully commented on {story_key}")
            else:
                print(f"  Failed to comment on {story_key}")

if __name__ == "__main__":
    main()

