from pathlib import Path
import re
import sys

def validate_css_imports(main_css_path: str, base_dir: str = "."):
    """
    Validate that all files imported in main.css exist in the expected locations

    Args:
        main_css_path: Path to the main.css file
        base_dir: Base directory for resolving import paths

    Returns:
        tuple: (is_valid, list of missing files)
    """
    base_path = Path(base_dir)
    main_css = Path(main_css_path)

    if not main_css.exists():
        print(f"Error: Main CSS file {main_css} does not exist")
        return False, []

    content = main_css.read_text()

    # Find all @import statements
    import_pattern = r'@import\s+[\'"]([^\'"]+)[\'"]'
    imports = re.findall(import_pattern, content)

    missing_files = []
    all_valid = True

    print(f"Validating {len(imports)} imports in {main_css_path}...")

    for import_path in imports:
        # Handle absolute paths (starting with /)
        if import_path.startswith('/'):
            # Remove the leading slash for file system path
            file_path = base_path / import_path[1:]
        else:
            # Handle relative paths
            file_path = main_css.parent / import_path

        if not file_path.exists():
            print(f"❌ Missing file: {import_path} (expected at {file_path})")
            missing_files.append(import_path)
            all_valid = False
        else:
            print(f"✅ Found: {import_path}")

    if all_valid:
        print("\n✅ All imports are valid!")
    else:
        print(f"\n❌ {len(missing_files)} missing files found.")

    return all_valid, missing_files

def analyze_css_structure(css_dir: str = "css"):
    """
    Analyze the CSS directory structure and provide information about file locations

    Args:
        css_dir: CSS directory to analyze
    """
    css_path = Path(css_dir)

    if not css_path.exists():
        print(f"Error: CSS directory {css_dir} does not exist")
        return

    print(f"\nAnalyzing CSS directory structure in {css_dir}...")

    # Get all CSS files
    all_files = list(css_path.glob('**/*.css'))

    print(f"Found {len(all_files)} CSS files")

    # Categorize files by directory
    dirs = {}
    for file in all_files:
        rel_path = file.relative_to(css_path)
        parent = str(rel_path.parent)
        if parent == '.':
            parent = 'root'

        if parent not in dirs:
            dirs[parent] = []

        dirs[parent].append(str(rel_path))

    # Print directory structure
    print("\nDirectory structure:")
    for dir_name, files in sorted(dirs.items()):
        print(f"\n{dir_name}/")
        for file in sorted(files):
            print(f"  - {file}")

    # Look for main.css
    main_css_files = [f for f in all_files if f.name == 'main.css']

    if main_css_files:
        print("\nFound main.css files:")
        for main_css in main_css_files:
            rel_path = main_css.relative_to(css_path)
            print(f"  - {rel_path}")

            # Optionally validate the main.css imports
            validate_css_imports(str(main_css), css_dir)
    else:
        print("\nNo main.css files found.")

if __name__ == "__main__":
    # If a specific main.css path is provided, validate it
    if len(sys.argv) > 1:
        main_css_path = sys.argv[1]
        base_dir = sys.argv[2] if len(sys.argv) > 2 else "."
        validate_css_imports(main_css_path, base_dir)
    else:
        # Otherwise analyze the whole CSS structure
        analyze_css_structure()
