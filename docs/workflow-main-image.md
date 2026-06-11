# Workflow: Main Image Cleanup

Goal: produce an Amazon-compliant main image from a real product photo.

## Inputs

- Original photo in `assets/input/`.
- Product identity and any known orientation constraints.

## Steps

1. Preserve the original file.
2. Remove the background while keeping the real product pixels.
3. Place the product on a pure white canvas.
4. Center the product.
5. Scale the product to fill the frame appropriately, usually near 85 percent when shape allows.
6. Export a square 2000 x 2000 JPG or PNG to `assets/output/`.
7. Run `verify-amazon-image.py --kind main`.

## Do Not Add

- Text
- Icons
- Badges
- Props
- Lifestyle background
- Comparison graphics
- Fake product features

## Output Naming

Use a clear versioned name:

```text
product-main-v01.jpg
```
