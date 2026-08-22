**Classification: Bounded** — this is a well-scoped change to existing code (a single Python file using sqlite), so the output will be a short design in chat, and I'll need your explicit yes before implementing. (Say the word if you'd rather treat it as a spike or something bigger.)

Before I can ask useful questions, I looked for your notes CLI in the workspace and couldn't find it — no Python file is present here.

**First question (one at a time):** Can you share the file — either paste it here or point me to its path? I need to see your current schema (does the `notes` table already exist, and what columns does it have?) and how your CLI commands are structured (argparse subcommands? a simple loop?) so the design matches your existing patterns.

Once I can see the code, my likely follow-ups will be things like whether "starred" should just be a boolean column on the existing table versus a separate table, and whether you want a separate `list --starred` flag or a new `starred` command — but I'll take them one at a time. I'll stop and wait for the file before going further.
