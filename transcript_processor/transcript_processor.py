import re
from collections import defaultdict

def clean_comment(comment, story_id):
    # Remove phrases like 'regarding SCRUM-3', 'as far as SCRUM-4 is concerned'
    pattern = re.compile(r"(regarding|as far as|about|concerning)?\s*{}\b[:,]?\s*".format(re.escape(story_id)), re.IGNORECASE)
    return pattern.sub("", comment).strip()

def extract_updates(conversation_text):
    updates = {}
    last_story_by_person = {}
    story_keywords = defaultdict(set)
    ignore_people = {'Suman', 'Ankur'}

    keyword_memory = defaultdict(lambda: defaultdict(set))  # person -> story -> set of keywords

    lines = conversation_text.split("\n")
    for line in lines:
        line = line.strip()
        if not line:
            continue

        person_match = re.match(r"^([^:]+):", line)
        if not person_match:
            continue

        person = person_match.group(1).strip()
        if person.lower() in [p.lower() for p in ignore_people]:
            continue
        if person.lower() in [p.lower() for p in ignore_people]:
            if person not in updates:
                updates[person] = {}
            continue

        if person not in updates:
            updates[person] = {}

        comment_text = line[len(person)+1:].strip()
        story_match = re.search(r"\b(SCRUM-\d+)\b", line, re.IGNORECASE)
        matched_story = None

        if story_match:
            matched_story = story_match.group(1).upper()
            last_story_by_person[person] = matched_story
            cleaned_comment = clean_comment(comment_text, matched_story)
            updates[person].setdefault(matched_story, []).append(cleaned_comment)

            # Record keywords for this story and person
            for word in cleaned_comment.split():
                keyword_memory[person][matched_story].add(word.lower())
                story_keywords[matched_story].add(word.lower())
        else:
            # No explicit story mentioned, infer based on keywords
            words = set(comment_text.lower().split())
            best_story = None
            max_overlap = 0
            for story, keywords in keyword_memory[person].items():
                overlap = len(words & keywords)
                if overlap > max_overlap:
                    max_overlap = overlap
                    best_story = story

            matched_story = best_story or last_story_by_person.get(person)
            if matched_story:
                cleaned_comment = comment_text.strip()
                updates[person].setdefault(matched_story, []).append(cleaned_comment)
                for word in cleaned_comment.split():
                    keyword_memory[person][matched_story].add(word.lower())
                    story_keywords[matched_story].add(word.lower())

    # Convert defaultdicts to normal dicts
    final_output = {}
    for person, stories in updates.items():
        final_output[person] = {story: comments for story, comments in stories.items()}

    return final_output




# def summarize_updates(updates_dict):
#     summarized = {}
#     for person, stories in updates_dict.items():
#         summarized[person] = {}
#         for story_id, messages in stories.items():
#             combined_text = " ".join(messages)
#             summary = generate_summary(combined_text)
#             summarized[person][story_id] = summary
#     return summarized
