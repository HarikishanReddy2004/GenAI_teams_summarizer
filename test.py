from summarizer import summarizer
sample_text = """
I completed the bug fix in the backend logic for SCRUM-2, ensuring the system handles edge cases more reliably. While validating the changes, I took the opportunity to test the GitHub Copilot integration using two different repositories, both of which responded well to the suggestions and workflows. The integration worked smoothly and didn’t show any major inconsistencies. During these tests, I noticed a small issue with the API response validation, which could have caused minor misinterpretations under certain conditions. I dug deeper into the validation logic and identified the root cause. After isolating the issue, I implemented a quick fix to stabilize the response behavior. Following this, I re-ran the test scenarios and confirmed that the fix worked as expected without side effects. The Copilot testing remained consistent post-fix, which was a good indicator of overall stability. I'm wrapping up this cycle of changes and documentation. I will be raising a PR today to merge all these improvements into the main branch.
"""

summary = summarizer.generate_summary(sample_text)
print(summary)