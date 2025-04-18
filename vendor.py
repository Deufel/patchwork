from pathlib import Path
import httpx
import shutil
from typing import Dict, List, Optional, Tuple

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
                   directories: Dict[str, List[str]] = None):
        """
        Add a source to pull CSS files from.
        
        Args:
            name: Name of the source (used as a subdirectory)
            base_url: Base URL to fetch files from
            files: List of files to fetch (relative to base_url)
            directories: Dictionary of directories to create with list of files to fetch in each
        """
        self.sources[name] = {
            'base_url': base_url,
            'files': files or [],
            'directories': directories or {}
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
        base_url = source['base_url']
        success_count = 0
        
        # Create source directory
        source_dir = self.output_dir / name
        source_dir.mkdir(parents=True, exist_ok=True)
        
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
        name="openprops",
        base_url="https://unpkg.com/open-props@2.0.0-beta.5",
        files=["index.css", "utilities.css"],
        directories={
            "css": ["media-queries.css"],
            "css/sizes": ["media.css"],
            "css/font": ["lineheight.css"],
            "css/color": ["hues.oklch.css"]
        }
    )
    
    # OpenProps UI
    vendor.add_source(
        name="ui",
        base_url="https://raw.githubusercontent.com/felix-bohlin/ui/refs/heads/main/src",
        files=["normalize.css", "utils.css", "theme.css", "main.css"],
        directories={
            "actions": ["button.css", "button-group.css", "icon-button.css", "toggle-button-group.css"],
            "data-display": ["avatar.css", "badge.css", "card.css", "chip.css", "definition-list.css",
                           "divider.css", "link.css", "table.css", "accordion.css", "list.css"],
            "feedback": ["progress.css", "spinner.css", "alert.css", "dialog.css", "snackbar.css"],
            "inputs": ["checkbox-radio.css", "switch.css", "range.css", "field-group.css", "field.css",
                      "select.css", "text-field.css", "textarea.css"],
            "text": ["typography.css", "rich-text.css"]
        }
    )
    
    # Custom directory for your own styles
    custom_dir = vendor.output_dir / "custom"
    custom_dir.mkdir(parents=True, exist_ok=True)
    
    return vendor

# Example usage
from pathlib import Path
import httpx
import shutil
from typing import Dict, List, Optional, Tuple

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
                   directories: Dict[str, List[str]] = None):
        """
        Add a source to pull CSS files from.
        
        Args:
            name: Name of the source (used as a subdirectory)
            base_url: Base URL to fetch files from
            files: List of files to fetch (relative to base_url)
            directories: Dictionary of directories to create with list of files to fetch in each
        """
        self.sources[name] = {
            'base_url': base_url,
            'files': files or [],
            'directories': directories or {}
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
        base_url = source['base_url']
        success_count = 0
        
        # Create source directory
        source_dir = self.output_dir / name
        source_dir.mkdir(parents=True, exist_ok=True)
        
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
        name="openprops",
        base_url="https://unpkg.com/open-props@2.0.0-beta.5",
        files=["index.css", "utilities.css"],
        directories={
            "css": ["media-queries.css"],
            "css/sizes": ["media.css"],
            "css/font": ["lineheight.css"],
            "css/color": ["hues.oklch.css"]
        }
    )
    
    # OpenProps UI
    vendor.add_source(
        name="ui",
        base_url="https://raw.githubusercontent.com/felix-bohlin/ui/refs/heads/main/src",
        files=["normalize.css", "utils.css", "theme.css", "main.css"],
        directories={
            "actions": ["button.css", "button-group.css", "icon-button.css", "toggle-button-group.css"],
            "data-display": ["avatar.css", "badge.css", "card.css", "chip.css", "definition-list.css",
                           "divider.css", "link.css", "table.css", "accordion.css", "list.css"],
            "feedback": ["progress.css", "spinner.css", "alert.css", "dialog.css", "snackbar.css"],
            "inputs": ["checkbox-radio.css", "switch.css", "range.css", "field-group.css", "field.css",
                      "select.css", "text-field.css", "textarea.css"],
            "text": ["typography.css", "rich-text.css"]
        }
    )
    
    # Custom directory for your own styles
    custom_dir = vendor.output_dir / "custom"
    custom_dir.mkdir(parents=True, exist_ok=True)
    
    return vendor

# Example usage
if __name__ == "__main__":
    vendor = setup_openprops_vendor()
    results = vendor.sync_all()
    print(f"Results by source: {results}")
if __name__ == "__main__":
    vendor = setup_openprops_vendor()
    results = vendor.sync_all()
    print(f"Results by source: {results}")
