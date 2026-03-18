# Generate Image with Gemini

Generate an image from a text prompt using the Gemini API.

## Instructions

1. Parse the user's request from: $ARGUMENTS

2. **Check for reference images**: If images were shared in the current conversation context:
   - Save each image to a temporary file in `/tmp/nano-banana/` (create the directory if needed)
   - Note the file paths for the `--images` flag

3. **Extract style flag**: If the user mentioned a style (e.g., `--style ghibli`), extract it from the arguments.

4. **Run the generation script**:

   Without reference images:
   ```bash
   cd $PROJECT_DIR && uv run python -m src.generate "$PROMPT" [--style STYLE_NAME]
   ```

   With reference images:
   ```bash
   cd $PROJECT_DIR && uv run python -m src.generate "$PROMPT" [--style STYLE_NAME] --images /tmp/nano-banana/img1.png /tmp/nano-banana/img2.png
   ```

   Where `$PROJECT_DIR` is the root directory of the nano-banana project (where `pyproject.toml` is located).

5. **Handle the result**:
   - The script outputs JSON to stdout
   - On success (`"success": true`): Tell the user the image has been generated and show the absolute path
   - On failure (`"success": false`): Display the error message clearly

6. **Clean up**: Remove any temporary image files from `/tmp/nano-banana/`

## Available Styles

Run `cat styles.json` in the project directory to see available styles, or use `--style` with one of: ghibli, pixel-art, photo-realistic, watercolor.

## Examples

- `/generate-image "a cat astronaut on the moon"`
- `/generate-image "a medieval castle" --style ghibli`
- (with an image in chat) `/generate-image "transform this into pixel art"`
