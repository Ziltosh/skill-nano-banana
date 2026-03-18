# Generate Image with Gemini

Generate an image from a text prompt using the Gemini API.

## Instructions

1. Parse the user's request from: $ARGUMENTS

2. **Check for reference images**: If images were shared in the current conversation context:
   - Save each image to a temporary file in `/tmp/nano-banana/` (create the directory if needed)
   - Note the file paths for the `--images` flag

3. **Extract flags** from the arguments:
   - `--style <name>` — style preset to apply
   - `--model <alias>` — model to use (see models.json)
   - `--include <tag>` — resource tag to include (repeatable)

4. **Run the generation script**:

   ```bash
   cd $PROJECT_DIR && uv run python -m src.generate "$PROMPT" [--style STYLE_NAME] [--model MODEL_ALIAS] [--include TAG1] [--include TAG2] [--images /tmp/nano-banana/img1.png]
   ```

   Where `$PROJECT_DIR` is the root directory of the nano-banana project (where `pyproject.toml` is located).

5. **Handle the result**:
   - The script outputs JSON to stdout
   - On success (`"success": true`): Tell the user the image has been generated and show the absolute path
   - On failure (`"success": false`): Display the error message clearly

6. **Clean up**: Remove any temporary image files from `/tmp/nano-banana/`

## Available Options

- **Styles**: Run `cat styles.json` in the project directory. Built-in: ghibli, pixel-art, photo-realistic, watercolor.
- **Models**: Run `cat models.json` in the project directory. Built-in: flash (default), pro, banana2.
- **Resources**: Check `ls resources/` for available tags.

## Examples

- `/generate-image "a cat astronaut on the moon"`
- `/generate-image "a medieval castle" --style ghibli`
- `/generate-image "a landscape" --model pro`
- `/generate-image "portrait" --include face-kim --style watercolor`
- `/generate-image "portrait" --model pro --include face-kim --style ghibli`
- (with an image in chat) `/generate-image "transform this into pixel art"`
