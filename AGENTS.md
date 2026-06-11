# Agent Operating Rules

These instructions apply to this project and all child directories.

## Product Accuracy

- Preserve original product accuracy.
- Never invent product features, dimensions, materials, claims, certifications, compatibility, or included accessories.
- Do not alter logos, labels, packaging, compliance marks, or claims in a misleading way.
- Use real product photos or real product cutouts for the actual product in every Amazon listing image.

## Amazon Main Image Rules

- Main image outputs must use a real product photo.
- Use a pure white background.
- Do not add text, icons, graphics, badges, props, comparison elements, lifestyle context, or decorative shadows that misrepresent the product.
- Center the product and make it fill the frame appropriately, usually near 85 percent when the product shape allows.

## Secondary Image Rules

- Secondary images may use infographics, callouts, dimensions, comparison graphics, benefit headlines, and lifestyle scenes.
- AI-generated backgrounds are allowed only for secondary or lifestyle images.
- Composite the real product cutout into AI or stock-style scenes; do not generate a fake replacement product.

## File Safety

- Keep originals untouched in `assets/input/`.
- Save cutouts to `assets/product-cutouts/`.
- Save final exports to `assets/output/`.
- Use clear names with workflow and version information, such as `asin-main-v01.jpg` or `asin-dimensions-v02.png`.
- Keep before/after versions when editing materially changes an image.

## MCP and Config Safety

- Do not edit `%USERPROFILE%\.codex\config.toml` without showing the exact diff and receiving explicit approval.
- Do not install global apps, enable telemetry, download model weights, or use paid APIs without explicit approval.
- Prefer project-local virtual environments and project-scoped MCP configuration examples.
- Keep secrets, API keys, tokens, customer data, and private machine paths out of committed files.
