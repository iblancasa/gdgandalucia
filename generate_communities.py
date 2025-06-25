#!/usr/bin/env python3
"""
GDG Andalucía - Communities Section Generator

This script reads community data from a YAML file and generates
the communities section HTML for the GDG Andalucía website.

Usage:
    python generate_communities.py [--yaml-file communities.yaml] [--html-file index.html] [--output-file index.html]

Author: GDG Andalucía
"""

import yaml
import argparse
import re
import os
import sys
from pathlib import Path
from typing import Dict, List, Any


class CommunitiesGenerator:
    """Generates communities section HTML from YAML data."""
    
    def __init__(self, yaml_file: str = "communities.yaml", html_file: str = "index.html"):
        self.yaml_file = yaml_file
        self.html_file = html_file
        self.data = None
        
    def load_yaml_data(self) -> Dict[str, Any]:
        """Load and parse YAML data."""
        try:
            with open(self.yaml_file, 'r', encoding='utf-8') as file:
                self.data = yaml.safe_load(file)
            print(f"✅ Loaded data from {self.yaml_file}")
            return self.data
        except FileNotFoundError:
            print(f"❌ Error: YAML file '{self.yaml_file}' not found")
            sys.exit(1)
        except yaml.YAMLError as e:
            print(f"❌ Error parsing YAML file: {e}")
            sys.exit(1)
    
    def sort_communities(self, communities: List[Dict]) -> List[Dict]:
        """Sort communities based on configuration."""
        config = self.data.get('config', {})
        sort_by = config.get('sort_by', 'name')
        sort_order = config.get('sort_order', 'asc')
        
        # Define sorting key function
        def sort_key(community):
            if sort_by == 'name':
                return community.get('name', '').lower()
            elif sort_by == 'location':
                return community.get('location', '').lower()
            elif sort_by == 'featured':
                return not community.get('featured', False)  # Featured first
            else:
                return 0
        
        # Sort communities
        sorted_communities = sorted(communities, key=sort_key, reverse=(sort_order == 'desc'))
        
        # Apply max communities limit
        max_communities = config.get('max_communities', 12)
        return sorted_communities[:max_communities]
    
    def filter_communities(self, communities: List[Dict]) -> List[Dict]:
        """Filter communities based on configuration."""
        config = self.data.get('config', {})
        show_inactive = config.get('show_inactive', False)
        
        if show_inactive:
            return communities
        else:
            return [c for c in communities if c.get('active', True)]
    
    def generate_community_card(self, community: Dict) -> str:
        """Generate HTML for a single community card."""
        config = self.data.get('config', {})
        use_placeholder = config.get('logo_placeholder', True)
        
        # Extract community data
        name = community.get('name', '')
        slug = community.get('slug', '')
        description = community.get('description', '')
        logo_path = community.get('logo_path', '')
        website = community.get('website', '#')
        
        # Generate logo HTML
        if logo_path and os.path.exists(logo_path) and not use_placeholder:
            logo_html = f'<img src="{logo_path}" alt="{name} Logo" class="community-logo-img">'
        else:
            logo_html = '<span class="material-icons">location_on</span>'
        
        # Generate the card HTML (removed stats)
        card_html = f'''
                <!-- Community: {name} -->
                <div class="community-card" data-community="{slug}">
                    <div class="community-logo">
                        <div class="logo-placeholder">
                            {logo_html}
                        </div>
                    </div>
                    <div class="community-info">
                        <h3 class="community-name">{name}</h3>
                        <p class="community-description">
                            {description}
                        </p>
                    </div>
                </div>'''
        
        return card_html
    
    def generate_social_links(self, social: Dict, community_name: str) -> str:
        """Generate social media links HTML."""
        links = []
        
        if social.get('twitter'):
            links.append(f'<a href="https://twitter.com/{social["twitter"].replace("@", "")}" target="_blank" rel="noopener" aria-label="Twitter de {community_name}"><span class="material-icons">twitter</span></a>')
        
        if social.get('linkedin'):
            links.append(f'<a href="https://linkedin.com/company/{social["linkedin"]}" target="_blank" rel="noopener" aria-label="LinkedIn de {community_name}"><span class="material-icons">linkedin</span></a>')
        
        if social.get('meetup'):
            links.append(f'<a href="https://meetup.com/{social["meetup"]}" target="_blank" rel="noopener" aria-label="Meetup de {community_name}"><span class="material-icons">event</span></a>')
        
        if links:
            return f'''
                        <div class="community-social">
                            <div class="social-links">
                                {''.join(links)}
                            </div>
                        </div>'''
        
        return ""
    
    def generate_communities_section(self) -> str:
        """Generate the complete communities section HTML."""
        if not self.data:
            self.load_yaml_data()
        
        communities = self.data.get('communities', [])
        
        # Filter and sort communities
        filtered_communities = self.filter_communities(communities)
        sorted_communities = self.sort_communities(filtered_communities)
        
        if not sorted_communities:
            print("⚠️  No communities found after filtering")
            return ""
        
        # Generate community cards
        community_cards = []
        for community in sorted_communities:
            card_html = self.generate_community_card(community)
            community_cards.append(card_html)
        
        # Generate the complete section
        section_html = f'''    <!-- Communities Grid Section -->
    <section class="communities-section" id="comunidades">
        <div class="container">
            <div class="section-header">
                <h2 class="section-title">Nuestras Comunidades</h2>
                <p class="section-subtitle">
                    Descubre las comunidades GDG activas en Andalucía y únete a la conversación
                </p>
            </div>
            
            <div class="communities-grid" id="communities-grid">
{''.join(community_cards)}
            </div>
        </div>
    </section>'''
        
        print(f"✅ Generated HTML for {len(sorted_communities)} communities")
        return section_html
    
    def update_html_file(self, output_file: str = None) -> None:
        """Update the HTML file with the generated communities section."""
        if output_file is None:
            output_file = self.html_file
        
        # Generate the new communities section
        new_section = self.generate_communities_section()
        
        if not new_section:
            print("❌ No communities section generated")
            return
        
        try:
            # Read the current HTML file
            with open(self.html_file, 'r', encoding='utf-8') as file:
                html_content = file.read()
            
            # Find and replace the communities section
            # Look for the section between <!-- Communities Grid Section --> and <!-- Future Sections Placeholder -->
            pattern = r'(\s*<!-- Communities Grid Section -->.*?<!-- Future Sections Placeholder -->)'
            
            if re.search(pattern, html_content, re.DOTALL):
                # Replace the existing section
                new_html = re.sub(pattern, f'\n{new_section}\n\n    <!-- Future Sections Placeholder -->', html_content, flags=re.DOTALL)
                print(f"✅ Updated existing communities section in {self.html_file}")
            else:
                # Insert after the hero section
                hero_pattern = r'(<!-- Hero Section -->.*?</section>)'
                if re.search(hero_pattern, html_content, re.DOTALL):
                    new_html = re.sub(hero_pattern, f'\\1\n\n{new_section}', html_content, flags=re.DOTALL)
                    print(f"✅ Inserted new communities section in {self.html_file}")
                else:
                    print("❌ Could not find appropriate location to insert communities section")
                    return
            
            # Write the updated HTML
            with open(output_file, 'w', encoding='utf-8') as file:
                file.write(new_html)
            
            print(f"✅ Successfully updated {output_file}")
            
        except FileNotFoundError:
            print(f"❌ Error: HTML file '{self.html_file}' not found")
            sys.exit(1)
        except Exception as e:
            print(f"❌ Error updating HTML file: {e}")
            sys.exit(1)
    
    def validate_data(self) -> bool:
        """Validate the YAML data structure."""
        if not self.data:
            self.load_yaml_data()
        
        required_fields = ['name', 'slug', 'description']
        communities = self.data.get('communities', [])
        
        for i, community in enumerate(communities):
            missing_fields = [field for field in required_fields if field not in community]
            if missing_fields:
                print(f"❌ Community {i+1} missing required fields: {missing_fields}")
                return False
        
        print(f"✅ Validated {len(communities)} communities")
        return True


def main():
    """Main function to run the communities generator."""
    parser = argparse.ArgumentParser(
        description="Generate communities section HTML from YAML data",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python generate_communities.py
  python generate_communities.py --yaml-file my-communities.yaml
  python generate_communities.py --html-file template.html --output-file index.html
        """
    )
    
    parser.add_argument(
        '--yaml-file',
        default='communities.yaml',
        help='YAML file containing community data (default: communities.yaml)'
    )
    
    parser.add_argument(
        '--html-file',
        default='index.html',
        help='HTML file to update (default: index.html)'
    )
    
    parser.add_argument(
        '--output-file',
        help='Output HTML file (default: same as html-file)'
    )
    
    parser.add_argument(
        '--validate-only',
        action='store_true',
        help='Only validate YAML data without updating HTML'
    )
    
    parser.add_argument(
        '--preview',
        action='store_true',
        help='Preview the generated HTML without updating the file'
    )
    
    args = parser.parse_args()
    
    # Initialize generator
    generator = CommunitiesGenerator(args.yaml_file, args.html_file)
    
    # Validate data
    if not generator.validate_data():
        sys.exit(1)
    
    if args.validate_only:
        print("✅ Validation completed successfully")
        return
    
    # Generate communities section
    if args.preview:
        section_html = generator.generate_communities_section()
        print("\n" + "="*50)
        print("PREVIEW: Generated Communities Section")
        print("="*50)
        print(section_html)
        print("="*50)
    else:
        # Update HTML file
        generator.update_html_file(args.output_file)
        print("\n🎉 Communities section generation completed!")


if __name__ == "__main__":
    main() 