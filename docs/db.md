# DB設計（MVP）

## tables

### projects
- id
- name
- description
- created_at
- updated_at

### minutes
- id
- project_id
- date
- agenda
- decisions_summary
- pending
- todo_note
- created_at
- updated_at

### tasks
- id
- project_id
- title
- description
- assignee
- due_date
- status (todo/doing/done)
- created_at
- updated_at

### decisions
- id
- project_id
- title
- decided_at
- decided_by
- reason
- tags
- created_at
- updated_at

### decision_options
- id
- decision_id
- label (A/B/C)
- content

### decision_criteria
- id
- decision_id
- name
- note

### links（汎用リンク）
- id
- from_type (decision/task/minutes)
- from_id
- to_type (decision/task/minutes)
- to_id
- created_at
