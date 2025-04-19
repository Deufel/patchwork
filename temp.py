from pathlib import Path
import httpx
import json
import shutil
from typing import Dict, List, Optional

class CSSVendor:
    """Pull CSS dependencies from various sources and organize them into a structured repository"""

    def __init__(self, output_dir: str = "css"):
        """
        Initialize CSS Vendor.

        Args:
            output_dir: Root directory where CSS will be stored
        """
        self.output_dir = Path(output_dir)
        self.sources: Dict[str, Dict] = {}

    def add_source(self,
                   name: str,
                   base_url: str,
                   files: List[str] = None,
                   directories: Dict[str, List[str]] = None,
                   auto_pull: bool = False,
                   github_repo: str = None,
                   local_dir: str = None):
        """
        Add a source to pull CSS files from.

        Args:
            name: Name of the source (used as a subdirectory)
            base_url: Base URL to fetch files from
            files: List of files to fetch (relative to base_url)
            directories: Dictionary of directories to create with list of files to fetch in each
            auto_pull: If True, will auto-pull all files from a GitHub repository
            github_repo: GitHub repository path (e.g., "owner/repo/branch/path")
            local_dir: Local directory to copy files from (instead of fetching from URL)
        """
        self.sources[name] = {
            'base_url': base_url,
            'files': files or [],
            'directories': directories or {},
            'auto_pull': auto_pull,
            'github_repo': github_repo,
            'local_dir': local_dir
        }

    def fetch_file(self, url: str, output_path: Path) -> bool:
        """Fetch a single file from URL"""
        try:
            response = httpx.get(url)
            if response.status_code == 200:
                output_path.parent.mkdir(parents=True, exist_ok=True)
                output_path.write_text(response.text)
                print(f"✓ Fetched {output_path.relative_to(self.output_dir)}")
                return True
            else:
                print(f"✗ Failed to fetch {url}: {response.status_code}")
                return False
        except Exception as e:
            print(f"✗ Error fetching {url}: {str(e)}")
            return False

    def copy_local_file(self, source_path: Path, dest_path: Path) -> bool:
        """Copy a file from a local directory"""
        try:
            if not source_path.exists():
                print(f"✗ Source file does not exist: {source_path}")
                return False

            dest_path.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(source_path, dest_path)
            print(f"✓ Copied {dest_path.relative_to(self.output_dir)}")
            return True
        except Exception as e:
            print(f"✗ Error copying {source_path}: {str(e)}")
            return False

    def get_github_files(self, repo_path: str) -> List[dict]:
        """Get all files from a GitHub repository recursively using the GitHub API"""
        # Parse repo path
        parts = repo_path.split('/')
        if len(parts) < 3:
            print(f"Invalid GitHub repository path: {repo_path}")
            return []

        owner, repo = parts[0], parts[1]
        branch = parts[2] if len(parts) > 2 else "main"
        path = '/'.join(parts[3:]) if len(parts) > 3 else ""

        api_url = f"https://api.github.com/repos/{owner}/{repo}/git/trees/{branch}?recursive=1"

        try:
            response = httpx.get(api_url)
            if response.status_code == 200:
                data = response.json()
                # Filter for CSS files and files in the specified path
                files = []
                for item in data.get('tree', []):
                    if item['type'] == 'blob' and item['path'].endswith('.css'):
                        if not path or item['path'].startswith(path):
                            files.append(item)
                return files
            else:
                print(f"Failed to fetch GitHub repository files: {response.status_code}")
                return []
        except Exception as e:
            print(f"Error fetching GitHub repository files: {str(e)}")
            return []

    def sync_source(self, name: str) -> int:
        """
        Sync all files from a given source.

        Returns:
            Number of files successfully synced
        """
        if name not in self.sources:
            print(f"Unknown source: {name}")
            return 0

        source = self.sources[name]
        success_count = 0

        # Create source directory
        source_dir = self.output_dir / name
        source_dir.mkdir(parents=True, exist_ok=True)

        # Handle local directory copying
        if source['local_dir']:
            local_path = Path(source['local_dir'])

            # Copy root files
            for file in source['files']:
                source_path = local_path / file
                output_path = source_dir / file
                if self.copy_local_file(source_path, output_path):
                    success_count += 1

            # Copy directory files
            for dir_name, files in source['directories'].items():
                for file in files:
                    source_path = local_path / dir_name / file
                    output_path = source_dir / dir_name / file
                    if self.copy_local_file(source_path, output_path):
                        success_count += 1

            return success_count

        # Auto-pull from GitHub if specified
        if source['auto_pull'] and source['github_repo']:
            print(f"Auto-pulling files from GitHub repository: {source['github_repo']}")
            files = self.get_github_files(source['github_repo'])
            base_url = source['base_url']

            for file_info in files:
                file_path = file_info['path']
                # If path is specified in github_repo, remove it from file_path
                repo_parts = source['github_repo'].split('/')
                if len(repo_parts) > 3:
                    prefix = '/'.join(repo_parts[3:]) + '/'
                    if file_path.startswith(prefix):
                        file_path = file_path[len(prefix):]

                url = f"{base_url}/{file_path}"
                output_path = source_dir / file_path
                if self.fetch_file(url, output_path):
                    success_count += 1

            return success_count

        # Fetch files from URL
        base_url = source['base_url']

        # Sync root files
        for file in source['files']:
            url = f"{base_url}/{file}"
            output_path = source_dir / file
            if self.fetch_file(url, output_path):
                success_count += 1

        # Sync directory files
        for dir_name, files in source['directories'].items():
            dir_path = source_dir / dir_name

            for file in files:
                url = f"{base_url}/{dir_name}/{file}"
                output_path = dir_path / file
                if self.fetch_file(url, output_path):
                    success_count += 1

        return success_count

    def sync_all(self) -> Dict[str, int]:
        """
        Sync all files from all sources.

        Returns:
            Dictionary mapping source names to number of files successfully synced
        """
        results = {}
        total = 0

        for name in self.sources:
            print(f"\nSyncing {name}...")
            count = self.sync_source(name)
            results[name] = count
            total += count

        print(f"\nSync complete! Synced {total} files.")
        return results

def setup_openprops_vendor():
    """Set up a CSS vendor for OpenProps and related libraries"""
    vendor = CSSVendor("css")

    # OpenProps (Beta)
    vendor.add_source(
        name="ui/opbeta",
        base_url="https://unpkg.com/open-props@2.0.0-beta.5",
        files=["index.css", "utilities.css"],
        directories={
            "css": ["media-queries.css"],
            "css/sizes": ["media.css"],
            "css/font": ["lineheight.css"],
            "css/color": ["hues.oklch.css"]
        }
    )

    # OpenProps UI - Simplified with auto-pull
    vendor.add_source(
        name="ui",
        base_url="https://raw.githubusercontent.com/felix-bohlin/ui/main/src",
        auto_pull=True,
        github_repo="felix-bohlin/ui/main/src"
    )

    # Use the local custom directory
    vendor.add_source(
        name="custom",  # This will be created as css/custom
        base_url=None,
        local_dir="custom",  # This is the source directory at project root
        files=["layout.css", "utils.css"]
    )

    return vendor

# Example usage
if __name__ == "__main__":
    vendor = setup_openprops_vendor()
    results = vendor.sync_all()
    print(f"Results by source: {results}")
