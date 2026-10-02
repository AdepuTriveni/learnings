import sqlite3
from pathlib import Path
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("task-tracker")

DB = Path(__file__).parent / "tasks.db"


def get_conn():
    conn = sqlite3.connect(DB)
    conn.execute("""CREATE TABLE IF NOT EXISTS tasks (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        done INTEGER NOT NULL DEFAULT 0)""")
    return conn


# TOOLS
@mcp.tool()
def add_task(title: str) -> str:
    """Add a new task to the to-do list"""
    with get_conn() as conn:
        cur = conn.execute("INSERT INTO tasks (title) VALUES (?)", (title,))
        return f"Added task #{cur.lastrowid}: {title}"


@mcp.tool()
def list_tasks(status: str = "all") -> str:
    """List tasks. status can be 'all', 'open', or 'done'"""
    query = "SELECT id, title, done FROM tasks"
    if status == "open":
        query += " WHERE done = 0"
    elif status == "done":
        query += " WHERE done = 1"
    elif status != "all":
        raise ValueError("status must be 'all', 'open', or 'done'")
    with get_conn() as conn:
        rows = conn.execute(query).fetchall()
    if not rows:
        return "No tasks found."
    return "\n".join(f"#{i} [{'x' if d else ' '}] {t}" for i, t, d in rows)


@mcp.tool()
def complete_task(task_id: int) -> str:
    """Mark a task as done using its id number"""
    with get_conn() as conn:
        cur = conn.execute("UPDATE tasks SET done = 1 WHERE id = ?", (task_id,))
    if cur.rowcount == 0:
        raise ValueError(f"No task with id {task_id}")
    return f"Task #{task_id} marked as done"


# RESOURCE
@mcp.resource("tasks://summary")
def summary() -> str:
    """How many tasks are done out of the total"""
    with get_conn() as conn:
        total = conn.execute("SELECT COUNT(*) FROM tasks").fetchone()[0]
        done = conn.execute("SELECT COUNT(*) FROM tasks WHERE done = 1").fetchone()[0]
    return f"{done} of {total} tasks done"


# PROMPT
@mcp.prompt()
def plan_my_day() -> str:
    """Ask the AI to plan the day from open tasks"""
    return ("Use list_tasks to see my open tasks, then suggest the order "
            "to do them today, with a short reason for each.")


if __name__ == "__main__":
    mcp.run(transport="stdio")