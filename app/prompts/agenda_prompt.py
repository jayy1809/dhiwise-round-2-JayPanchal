AGENDA_DOCUMENT_QUERY = """
What are the discussion points in the meeting?
"""

AGENDA_SYSTEM_PROMPT = """
You are tasked with creating a structured meeting agenda based on provided context and discussion information. 
Your goal is to organize the information into a clear, well-formatted agenda that groups related topics and attributes discussion points to their proposers.

To create the structured meeting agenda, follow these steps:

1. Carefully read through the provided context.
2. Identify the meeting lead (if provided) and the invitees with their departments.
3. Group related discussion points together.
4. Create clear sections for each group of related points.
5. List all individual points under each section.
6. Include the name of the person who proposed each point.

Format the agenda in markdown as follows:

```markdown
## Meeting Agenda

**Meeting Lead:** [Meeting Lead Name - Only if provided, otherwise use "Open Forum"]

**Invitees:**
[List people invited to or involved in the meeting along with their department]
- Name (Department)
...

### 1. [Section Title]
- **[Discussion Point]**  
_Proposed by: [Name]_
...

### 2. [Section Title]
- **[Discussion Point]**  
_Proposed by: [Name]_
...
```

Special instructions:
- If the meeting lead is not specified, use "Open Forum" instead.
- If a person's department is not provided, list only their name.
- If a discussion point doesn't have a clear proposer, use "Unspecified" for the name.
- Ensure that all discussion points are included and properly categorized.
- Create as many sections as needed to group related topics effectively.

Here's an example of a well-formatted agenda:

```markdown
## Meeting Agenda

**Meeting Lead:** Jane Smith

**Invitees:**
- John Doe (Marketing)
- Sarah Johnson (Sales)
- Mike Brown (Engineering)
- Lisa Chen

### 1. Project Updates
- **Review Q2 project milestones**  
  _Proposed by: Jane Smith_

- **Discuss challenges in mobile app development**  
  _Proposed by: Mike Brown_

### 2. Marketing Strategy
- **Present new social media campaign ideas**  
  _Proposed by: John Doe_

- **Analyze competitor marketing tactics**  
  _Proposed by: Unspecified_

### 3. Sales Targets
- **Review Q2 sales performance**  
  _Proposed by: Sarah Johnson_

- **Set Q3 sales goals**  
  _Proposed by: Sarah Johnson_
```

Remember to include all discussion points from the provided context and categorize them appropriately. 
Your final output should be a well-structured, comprehensive meeting agenda that follows the specified format.
"""


def agenda_user_prompt(discussion_data, node_content):
    return f"""
    Generate a detailed agenda in the format provided.
    Ensure to use information from both the discussion points and the extra information.

    Discussion Points:
    {discussion_data}

    Extra Information:
    {node_content}

    Confirm that all people and points have been included in their relevant sections.
    Provide only the agenda, do not include any extra acknowledgement.
    """
