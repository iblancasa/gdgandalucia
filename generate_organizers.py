#!/usr/bin/env python3
"""
GDG Andalucía - Organizers Generator

This script reads community data from communities.yaml, calls the scraper
for each community, and generates organizers.yaml with organizer information.

Usage:
    python generate_organizers.py
"""

import yaml
import json
import subprocess
import sys
import os
from typing import List, Dict, Any
from datetime import datetime


class OrganizersGenerator:
    """Generates organizers.yaml from communities data."""
    
    def __init__(self, communities_file: str = "communities.yaml", output_file: str = "organizers.yaml"):
        self.communities_file = communities_file
        self.output_file = output_file
        self.communities_data = None
        self.organizers_data = []
    
    def load_communities(self) -> Dict[str, Any]:
        """Load communities data from YAML file."""
        try:
            with open(self.communities_file, 'r', encoding='utf-8') as file:
                self.communities_data = yaml.safe_load(file)
            print(f"✅ Loaded communities from {self.communities_file}")
            return self.communities_data
        except FileNotFoundError:
            print(f"❌ Error: Communities file '{self.communities_file}' not found")
            sys.exit(1)
        except yaml.YAMLError as e:
            print(f"❌ Error parsing communities file: {e}")
            sys.exit(1)
    
    def call_scraper(self, community_slug: str) -> List[Dict]:
        """Call the scraper script for a specific community."""
        try:
            # Call the scraper script
            result = subprocess.run(
                [sys.executable, 'scrape_gdg_organizers.py', community_slug],
                capture_output=True,
                text=True,
                timeout=30  # 30 second timeout
            )
            
            if result.returncode == 0:
                # Parse the JSON output
                scraper_output = json.loads(result.stdout)
                return scraper_output.get('organizers', [])
            else:
                print(f"⚠️  Scraper failed for {community_slug}: {result.stderr}")
                return []
                
        except subprocess.TimeoutExpired:
            print(f"⚠️  Scraper timeout for {community_slug}")
            return []
        except json.JSONDecodeError:
            print(f"⚠️  Invalid JSON output from scraper for {community_slug}")
            return []
        except Exception as e:
            print(f"❌ Error calling scraper for {community_slug}: {e}")
            return []
    
    def process_community(self, community: Dict) -> List[Dict]:
        """Process a single community and get its organizers."""
        community_slug = community.get('slug')
        community_name = community.get('name')
        
        if not community_slug:
            print(f"⚠️  Skipping community without slug: {community_name}")
            return []
        
        print(f"\n🔍 Processing {community_name} ({community_slug})...")
        
        # Check if community is active
        if not community.get('active', True):
            print(f"⏭️  Skipping inactive community: {community_name}")
            return []
        
        # Check if community has a URL in the scraper
        try:
            # Import the scraper to check available URLs
            from scrape_gdg_organizers import GDGOrganizersScraper
            scraper = GDGOrganizersScraper()
            if community_slug not in scraper.gdg_urls:
                print(f"⏭️  Skipping community without URL in scraper: {community_name}")
                return []
        except ImportError:
            print(f"⚠️  Could not import scraper to check URLs for {community_name}")
            return []
        
        # Call the scraper
        organizers = self.call_scraper(community_slug)
        
        # Format organizers for output
        formatted_organizers = []
        for organizer in organizers:
            formatted_organizer = {
                'name': organizer.get('name', 'Unknown'),
                'community': community_slug,
                'affiliation': organizer.get('affiliation', f'GDG {community_slug.title()}'),
                'profile_image': organizer.get('profile_image', '')
            }
            formatted_organizers.append(formatted_organizer)
        
        print(f"✅ Found {len(formatted_organizers)} organizers for {community_name}")
        return formatted_organizers
    
    def generate_organizers(self) -> List[Dict]:
        """Generate organizers data for all communities."""
        if not self.communities_data:
            self.load_communities()
        
        communities = self.communities_data.get('communities', [])
        
        if not communities:
            print("❌ No communities found in the YAML file")
            return []
        
        print(f"🚀 Starting organizer generation for {len(communities)} communities...")
        
        all_organizers = []
        
        for i, community in enumerate(communities, 1):
            print(f"\n📋 [{i}/{len(communities)}] Processing community...")
            
            organizers = self.process_community(community)
            all_organizers.extend(organizers)
            
            # Add a small delay between communities to be respectful
            if i < len(communities):
                print("⏳ Waiting before next community...")
                import time
                time.sleep(2)
        
        self.organizers_data = all_organizers
        print(f"\n✅ Generated data for {len(all_organizers)} organizers from {len(communities)} communities")
        return all_organizers
    
    def save_to_yaml(self) -> str:
        """Save organizers data to YAML file."""
        if not self.organizers_data:
            print("❌ No organizers data to save")
            return ""
        
        # Prepare the output data structure
        output_data = {
            'metadata': {
                'generated_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                'source_file': self.communities_file,
                'total_organizers': len(self.organizers_data),
                'communities_processed': len(set(org['community'] for org in self.organizers_data))
            },
            'organizers': self.organizers_data
        }
        
        try:
            with open(self.output_file, 'w', encoding='utf-8') as file:
                yaml.dump(output_data, file, default_flow_style=False, 
                         allow_unicode=True, sort_keys=False, indent=2)
            
            print(f"✅ Organizers data saved to {self.output_file}")
            return self.output_file
            
        except Exception as e:
            print(f"❌ Error saving to YAML: {e}")
            return ""
    
    def print_summary(self):
        """Print a summary of the generated data."""
        if not self.organizers_data:
            print("❌ No organizers data to summarize")
            return
        
        print("\n" + "="*50)
        print("📊 ORGANIZERS GENERATION SUMMARY")
        print("="*50)
        
        # Count organizers by community
        community_counts = {}
        for organizer in self.organizers_data:
            community = organizer['community']
            community_counts[community] = community_counts.get(community, 0) + 1
        
        print(f"Total organizers: {len(self.organizers_data)}")
        print(f"Communities with organizers: {len(community_counts)}")
        print("\nOrganizers by community:")
        
        for community, count in sorted(community_counts.items()):
            print(f"  • {community.title()}: {count} organizers")
        
        print(f"\nOutput file: {self.output_file}")
        print("="*50)


def main():
    """Main function to run the organizers generator."""
    import argparse
    
    parser = argparse.ArgumentParser(
        description="Generate organizers.yaml from communities data",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python generate_organizers.py
  python generate_organizers.py --communities-file my-communities.yaml
  python generate_organizers.py --output-file my-organizers.yaml
        """
    )
    
    parser.add_argument(
        '--communities-file',
        default='communities.yaml',
        help='Communities YAML file (default: communities.yaml)'
    )
    
    parser.add_argument(
        '--output-file',
        default='organizers.yaml',
        help='Output organizers YAML file (default: organizers.yaml)'
    )
    
    parser.add_argument(
        '--dry-run',
        action='store_true',
        help='Show what would be generated without saving to file'
    )
    
    args = parser.parse_args()
    
    # Check if scraper script exists
    if not os.path.exists('scrape_gdg_organizers.py'):
        print("❌ Error: scrape_gdg_organizers.py not found")
        print("Please ensure the scraper script is in the same directory")
        sys.exit(1)
    
    # Initialize generator
    generator = OrganizersGenerator(args.communities_file, args.output_file)
    
    try:
        # Generate organizers data
        organizers = generator.generate_organizers()
        
        if not organizers:
            print("❌ No organizers data generated")
            sys.exit(1)
        
        # Print summary
        generator.print_summary()
        
        # Save to file unless dry run
        if not args.dry_run:
            output_file = generator.save_to_yaml()
            if output_file:
                print(f"\n🎉 Organizers generation completed successfully!")
                print(f"📁 Output file: {output_file}")
            else:
                print("\n❌ Failed to save organizers data")
                sys.exit(1)
        else:
            print("\n🔍 DRY RUN - No file saved")
            print("Use --dry-run to see what would be generated")
        
    except KeyboardInterrupt:
        print("\n\n⚠️  Process interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main() 