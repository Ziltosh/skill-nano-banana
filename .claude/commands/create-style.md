# Create Style Preset

Create a new style preset for image generation.

## Instructions

1. Parse the user's request from: $ARGUMENTS
   - Extract the style name (first argument) and description (second argument)
   - If arguments are missing, explain usage: `/create-style "style-name" "description of the style"`

2. **Run the creation script**:

   ```bash
   cd $PROJECT_DIR && uv run python -m src.create_style "STYLE_NAME" "STYLE_DESCRIPTION"
   ```

   Where `$PROJECT_DIR` is the root directory of the nano-banana project.

3. **Handle the result**:
   - The script outputs JSON to stdout
   - On success (`"action": "created"`): Confirm the style was created and is ready to use via `--style STYLE_NAME`
   - On conflict (`"code": "STYLE_EXISTS"`): Tell the user the style already exists, show the current description, and ask if they want to overwrite it
   - If user confirms overwrite, re-run with `--force`:
     ```bash
     cd $PROJECT_DIR && uv run python -m src.create_style "STYLE_NAME" "STYLE_DESCRIPTION" --force
     ```

## Examples

- `/create-style "cyberpunk" "cyberpunk style with bright neon lights, dark background, wet surface reflections"`
- `/create-style "manga" "Japanese manga style, black and white ink drawing, dramatic shading"`
