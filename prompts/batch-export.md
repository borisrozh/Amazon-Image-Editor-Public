# Batch Export Prompt

Process images from `[INPUT_DIR]` and export Amazon-ready copies to `[OUTPUT_DIR]`.

Rules:

- Keep originals untouched.
- Export square 2000 x 2000 versions unless a different approved size is provided.
- Preserve high visual quality.
- Use clear filenames with workflow and version.
- Do not overwrite existing outputs unless explicitly approved.
- Report every file created and every file skipped.
