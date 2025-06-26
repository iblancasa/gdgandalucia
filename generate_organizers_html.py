#!/usr/bin/env python3
"""
GDG Andalucía - Organizers HTML Generator

This script reads organizer data from organizers.yaml and generates
the HTML for the organizers section to be inserted into index.html.

Usage:
    python generate_organizers_html.py
"""

import yaml
import re
import sys
from typing import List, Dict, Any
from datetime import datetime


class OrganizersHTMLGenerator:
    """Generates HTML for organizers section from YAML data."""
    
    def __init__(self, organizers_file: str = "organizers.yaml", output_file: str = "index.html"):
        self.organizers_file = organizers_file
        self.output_file = output_file
        self.organizers_data = None
    
    def load_organizers(self) -> Dict[str, Any]:
        """Load organizers data from YAML file."""
        try:
            with open(self.organizers_file, 'r', encoding='utf-8') as file:
                self.organizers_data = yaml.safe_load(file)
            print(f"✅ Loaded organizers from {self.organizers_file}")
            return self.organizers_data
        except FileNotFoundError:
            print(f"❌ Error: Organizers file '{self.organizers_file}' not found")
            print("💡 Run 'python generate_organizers.py' first to create organizers.yaml")
            sys.exit(1)
        except yaml.YAMLError as e:
            print(f"❌ Error parsing organizers file: {e}")
            sys.exit(1)
    
    def generate_organizer_card(self, organizer: Dict) -> str:
        """Generate HTML for a single organizer card."""
        name = organizer.get('name', 'Unknown')
        community = organizer.get('community', 'unknown')
        affiliation = organizer.get('affiliation', f'GDG {community.title()}')
        profile_image = organizer.get('profile_image', '')
        
        # Use a default avatar if no profile image
        if not profile_image:
            profile_image = "https://via.placeholder.com/150x150/4CAF50/FFFFFF?text=" + name[0].upper()
        
        # Clean the name for alt text
        alt_text = name.replace('"', '&quot;')
        
        card_html = f'''                <div class="organizer-card" data-community="{community}">
                    <div class="organizer-photo">
                        <img src="{profile_image}" alt="{alt_text}" loading="lazy">
                    </div>
                    <div class="organizer-info">
                        <h3 class="organizer-name">{name}</h3>
                        <p class="organizer-affiliation">{affiliation}</p>
                        <span class="organizer-community">GDG {community.title()}</span>
                    </div>
                </div>'''
        
        return card_html
    
    def generate_organizers_section(self) -> str:
        """Generate the complete organizers section HTML."""
        if not self.organizers_data:
            self.load_organizers()
        
        organizers = self.organizers_data.get('organizers', [])
        
        if not organizers:
            print("⚠️  No organizers found in the YAML file")
            return ""
        
        print(f"🎨 Generating HTML for {len(organizers)} organizers...")
        
        # Generate organizer cards
        organizer_cards = []
        for organizer in organizers:
            card_html = self.generate_organizer_card(organizer)
            organizer_cards.append(card_html)
        
        # Combine all cards
        cards_html = '\n'.join(organizer_cards)
        
        # Generate the complete section
        section_html = f'''    <!-- Organizers Grid Section -->
    <section class="organizers-section" id="organizadores">
        <div class="container">
            <div class="section-header">
                <h2 class="section-title">Organizadores</h2>
                <p class="section-subtitle">
                    Conoce a los organizadores de las comunidades GDG en Andalucía
                </p>
            </div>
            <div class="organizers-grid">
                <!-- Organizers Cards -->
                <!-- AUTO-GENERATED: Begin organizers -->
{cards_html}
                <!-- AUTO-GENERATED: End organizers -->
            </div>
        </div>
    </section>
    <!-- End Organizers Grid Section -->'''
        
        return section_html
    
    def update_index_html(self, organizers_section: str) -> bool:
        """Update index.html with the new organizers section."""
        try:
            # Read the current index.html
            with open(self.output_file, 'r', encoding='utf-8') as file:
                content = file.read()
            
            # Check if organizers section already exists
            if '<!-- AUTO-GENERATED: Begin organizers -->' in content:
                # Replace existing organizers section
                pattern = r'(\s*<!-- Organizers Grid Section -->.*?<!-- End Organizers Grid Section -->\s*)'
                replacement = f'\n{organizers_section}\n'
                new_content = re.sub(pattern, replacement, content, flags=re.DOTALL)
            else:
                # Insert organizers section before the "Future Sections Placeholder"
                pattern = r'(\s*<!-- Future Sections Placeholder -->)'
                replacement = f'\n{organizers_section}\n\n    <!-- Future Sections Placeholder -->'
                new_content = re.sub(pattern, replacement, content, flags=re.DOTALL)
            
            # Add organizers link to navigation if it doesn't exist
            if 'href="#organizadores"' not in new_content:
                # Find the navigation list and add organizers link
                nav_pattern = r'(<ul class="nav-list">\s*<li><a href="#inicio" class="nav-link">Inicio</a></li>\s*<li><a href="#comunidades" class="nav-link">Comunidades</a></li>\s*<li><a href="#eventos" class="nav-link">Eventos</a></li>\s*<li><a href="#contacto" class="nav-link">Contacto</a></li>)'
                nav_replacement = r'\1\n                <li><a href="#organizadores" class="nav-link">Organizadores</a></li>'
                new_content = re.sub(nav_pattern, nav_replacement, new_content)
            
            # Write the updated content
            with open(self.output_file, 'w', encoding='utf-8') as file:
                file.write(new_content)
            
            print(f"✅ Updated {self.output_file} with organizers section")
            return True
            
        except FileNotFoundError:
            print(f"❌ Error: {self.output_file} not found")
            return False
        except Exception as e:
            print(f"❌ Error updating {self.output_file}: {e}")
            return False
    
    def print_summary(self):
        """Print a summary of the generated HTML."""
        if not self.organizers_data:
            print("❌ No organizers data to summarize")
            return
        
        organizers = self.organizers_data.get('organizers', [])
        
        print("\n" + "="*50)
        print("🎨 ORGANIZERS HTML GENERATION SUMMARY")
        print("="*50)
        
        # Count organizers by community
        community_counts = {}
        for organizer in organizers:
            community = organizer['community']
            community_counts[community] = community_counts.get(community, 0) + 1
        
        print(f"Total organizers: {len(organizers)}")
        print(f"Communities with organizers: {len(community_counts)}")
        print("\nOrganizers by community:")
        
        for community, count in sorted(community_counts.items()):
            print(f"  • {community.title()}: {count} organizers")
        
        metadata = self.organizers_data.get('metadata', {})
        if metadata:
            print(f"\nGenerated from: {metadata.get('source_file', 'unknown')}")
            print(f"Last updated: {metadata.get('generated_at', 'unknown')}")


def main():
    """Main function to run the organizers HTML generator."""
    print("🎨 GDG Andalucía - Organizers HTML Generator")
    print("=" * 50)
    
    generator = OrganizersHTMLGenerator()
    
    # Generate the organizers section HTML
    organizers_section = generator.generate_organizers_section()
    
    if organizers_section:
        # Update the index.html file
        success = generator.update_index_html(organizers_section)
        
        if success:
            generator.print_summary()
            print(f"\n✅ Successfully updated {generator.output_file}")
            print("🌐 Open the file in your browser to see the organizers section!")
        else:
            print(f"\n❌ Failed to update {generator.output_file}")
            sys.exit(1)
    else:
        print("\n❌ No organizers section generated")
        sys.exit(1)


if __name__ == "__main__":
    main() 