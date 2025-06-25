#!/usr/bin/env python3
"""
GDG Organizers Scraper

This script scrapes organizer information from GDG community websites.
It can be called with a community slug and returns organizer data.

Usage:
    python scrape_gdg_organizers.py <community_slug>
"""

import sys
import requests
import re
import json
from typing import List, Dict, Optional
from urllib.parse import urljoin, urlparse
import time
import random


class GDGOrganizersScraper:
    """Scrapes organizer information from GDG community websites."""
    
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        })
        
        # Common GDG community URLs
        self.gdg_urls = {
            'sevilla': 'https://gdg.community.dev/gdg-sevilla/',
            'malaga': 'https://gdg.community.dev/gdg-malaga/',
            'granada': 'https://gdg.community.dev/gdg-granada/',
            'cordoba': 'https://gdg.community.dev/gdg-cordoba/',
            'jaen': 'https://gdg.community.dev/gdg-jaen/'
        }
    
    def scrape_community_organizers(self, community_slug: str) -> List[Dict]:
        """Scrape organizers for a specific community."""
        print(f"🔍 Scraping organizers for GDG {community_slug.title()}...", file=sys.stderr)
        
        # Get the community URL
        community_url = self.gdg_urls.get(community_slug)
        if not community_url:
            print(f"❌ No URL found for community: {community_slug}")
            return []
        
        try:
            # Try to scrape the actual website
            organizers = self._scrape_website(community_url, community_slug)
            if organizers:
                return organizers
            
            # If scraping fails, try alternative methods
            organizers = self._scrape_meetup(community_slug)
            if organizers:
                return organizers
            
            # If all else fails, return empty list
            print(f"⚠️  No organizers found for {community_slug}")
            return []
            
        except Exception as e:
            print(f"❌ Error scraping {community_slug}: {e}")
            return []
    
    def _scrape_website(self, url: str, community_slug: str) -> List[Dict]:
        """Attempt to scrape organizers from the community website."""
        try:
            print(f"  📄 Fetching {url}...", file=sys.stderr)
            response = self.session.get(url, timeout=15)
            response.raise_for_status()
            
            content = response.text
            print(f"  ✅ Successfully fetched page ({len(content)} characters)", file=sys.stderr)
            
            # Look for organizer patterns in the HTML
            organizers = []
            
            # Pattern 1: Look for JSON data in script tags (GDG community sites often have this)
            json_organizers = self._extract_from_json(content, community_slug)
            if json_organizers:
                print(f"  🎯 Found {len(json_organizers)} organizers from JSON data", file=sys.stderr)
                return json_organizers
            
            # Pattern 2: Look for organizer names in the page content
            html_organizers = self._extract_from_html(content, community_slug)
            if html_organizers:
                print(f"  🎯 Found {len(html_organizers)} organizers from HTML content", file=sys.stderr)
                return html_organizers
            
            # Pattern 3: Look for social media links that might indicate organizers
            social_organizers = self._extract_from_social_links(content, community_slug)
            if social_organizers:
                print(f"  🎯 Found {len(social_organizers)} organizers from social links", file=sys.stderr)
                return social_organizers
            
            print(f"  ⚠️  No organizers found in HTML content", file=sys.stderr)
            return []
            
        except Exception as e:
            print(f"  ❌ Website scraping failed for {community_slug}: {e}", file=sys.stderr)
            return []
    
    def _extract_from_json(self, content: str, community_slug: str) -> List[Dict]:
        """Extract organizer information from embedded JSON data."""
        organizers = []
        found_json = False
        # Look for JSON data in script tags
        json_patterns = [
            r'<script[^>]*id="__NEXT_DATA__"[^>]*>(.*?)</script>',
            r'<script[^>]*type="application/json"[^>]*>(.*?)</script>',
            r'window\.__INITIAL_STATE__\s*=\s*({.*?});',
            r'window\.__PRELOADED_STATE__\s*=\s*({.*?});'
        ]
        for pattern in json_patterns:
            matches = re.findall(pattern, content, re.DOTALL | re.IGNORECASE)
            for match in matches:
                found_json = True
                try:
                    data = json.loads(match)
                    organizers.extend(self._parse_json_data(data, community_slug))
                except json.JSONDecodeError:
                    print(f"[DEBUG] JSON decode error for {community_slug}. First 500 chars:\n{match[:500]}", file=sys.stderr)
                    continue
        if not found_json:
            print(f"[DEBUG] No JSON data found in page for {community_slug}", file=sys.stderr)
        if found_json and not organizers:
            print(f"[DEBUG] JSON found but no organizers extracted for {community_slug}. Check JSON structure.", file=sys.stderr)
        return organizers
    
    def _parse_json_data(self, data: Dict, community_slug: str) -> List[Dict]:
        """Parse JSON data to find organizer information."""
        organizers = []
        
        # Common paths where organizer data might be stored
        paths_to_check = [
            ['props', 'pageProps', 'prerenderData', 'chapterTeam'],
            ['props', 'pageProps', 'chapterTeam'],
            ['chapterTeam'],
            ['team'],
            ['organizers'],
            ['members'],
            ['data', 'chapterTeam'],
            ['data', 'team'],
            ['data', 'organizers']
        ]
        
        for path in paths_to_check:
            current = data
            try:
                for key in path:
                    current = current[key]
                
                if isinstance(current, list):
                    for member in current:
                        if isinstance(member, dict):
                            organizer = self._extract_organizer_from_json_member(member, community_slug)
                            if organizer:
                                organizers.append(organizer)
            except (KeyError, TypeError):
                continue
        
        return organizers
    
    def _extract_organizer_from_json_member(self, member: Dict, community_slug: str) -> Optional[Dict]:
        """Extract organizer information from a JSON member object."""
        # Always prioritize the real person's name
        name = None
        affiliation = None
        profile_image = None

        # Check if this is a GDG community structure with 'user' object
        if 'user' in member and isinstance(member['user'], dict):
            user = member['user']
            # Get full name, or first + last name
            full_name = user.get('full_name', '').strip()
            first_name = user.get('first_name', '').strip()
            last_name = user.get('last_name', '').strip()
            if full_name:
                name = full_name
            elif first_name or last_name:
                name = f"{first_name} {last_name}".strip()
            
            # Get profile image from avatar
            if 'avatar' in user and isinstance(user['avatar'], dict):
                profile_image = user['avatar'].get('url', '')
            
            # Affiliation: title (role) or company
            title = member.get('title', '').strip()
            company = user.get('company', '').strip()
            if title:
                affiliation = title
            elif company:
                affiliation = company
            else:
                affiliation = f'GDG {community_slug.title()}'
        else:
            # Fallback to direct field extraction
            name_fields = ['full_name', 'name', 'display_name', 'first_name', 'last_name', 'username']
            for field in name_fields:
                value = member.get(field, '').strip()
                if value:
                    if field in ['first_name', 'last_name']:
                        # Try to combine first and last name
                        first = member.get('first_name', '').strip()
                        last = member.get('last_name', '').strip()
                        name = f"{first} {last}".strip()
                    else:
                        name = value
                    if name:
                        break
            
            # Get profile image from avatar or image field
            if 'avatar' in member and isinstance(member['avatar'], dict):
                profile_image = member['avatar'].get('url', '')
            elif 'image' in member:
                profile_image = member.get('image', '')
            
            # Affiliation: title, role, company, etc.
            affiliation_fields = ['title', 'role', 'affiliation', 'position', 'company']
            for field in affiliation_fields:
                value = member.get(field, '').strip()
                if value:
                    affiliation = value
                    break
            if not affiliation:
                affiliation = f'GDG {community_slug.title()}'
        
        # Only return if we have a real name (not a role/title)
        if name and len(name.split()) >= 2:
            return {
                'name': name,
                'affiliation': affiliation,
                'profile_image': profile_image
            }
        return None
    
    def _extract_from_html(self, content: str, community_slug: str) -> List[Dict]:
        """Extract organizer information from HTML content."""
        organizers = []
        
        # Look for organizer-related content in HTML
        organizer_patterns = [
            r'<h[1-6][^>]*>([^<]*organizador[^<]*)</h[1-6]>',
            r'<h[1-6][^>]*>([^<]*organizer[^<]*)</h[1-6]>',
            r'<div[^>]*class="[^"]*organizador[^"]*"[^>]*>([^<]*)</div>',
            r'<div[^>]*class="[^"]*organizer[^"]*"[^>]*>([^<]*)</div>',
            r'<span[^>]*class="[^"]*name[^"]*"[^>]*>([^<]*)</span>',
            r'<p[^>]*class="[^"]*name[^"]*"[^>]*>([^<]*)</p>'
        ]
        
        for pattern in organizer_patterns:
            matches = re.findall(pattern, content, re.IGNORECASE)
            for match in matches:
                name = match.strip()
                if len(name) > 3 and name.lower() not in ['organizador', 'organizer', 'admin', 'team']:
                    organizers.append({
                        'name': name,
                        'affiliation': f'GDG {community_slug.title()}'
                    })
        
        return organizers
    
    def _extract_from_social_links(self, content: str, community_slug: str) -> List[Dict]:
        """Extract organizer information from social media links."""
        organizers = []
        
        # Look for social media profiles that might indicate organizers
        social_patterns = [
            r'twitter\.com/([a-zA-Z0-9_]+)',
            r'linkedin\.com/in/([a-zA-Z0-9_-]+)',
            r'github\.com/([a-zA-Z0-9_-]+)',
            r'instagram\.com/([a-zA-Z0-9_.]+)'
        ]
        
        for pattern in social_patterns:
            matches = re.findall(pattern, content)
            for match in matches[:3]:  # Limit to first 3 matches
                # Clean up the username
                username = match.replace('_', ' ').replace('-', ' ').title()
                organizers.append({
                    'name': f'Organizador {username}',
                    'affiliation': f'GDG {community_slug.title()}'
                })
        
        return organizers
    
    def _scrape_meetup(self, community_slug: str) -> List[Dict]:
        """Attempt to scrape organizers from Meetup."""
        try:
            print(f"  📅 Trying Meetup for {community_slug}...", file=sys.stderr)
            meetup_url = f"https://meetup.com/gdg-{community_slug}"
            response = self.session.get(meetup_url, timeout=10)
            
            if response.status_code == 200:
                content = response.text
                
                # Look for organizer information in Meetup page
                organizers = []
                
                # Pattern for Meetup organizers
                meetup_patterns = [
                    r'organizer[^>]*>([^<]+)',
                    r'leader[^>]*>([^<]+)',
                    r'admin[^>]*>([^<]+)',
                    r'<span[^>]*class="[^"]*name[^"]*"[^>]*>([^<]*)</span>'
                ]
                
                for pattern in meetup_patterns:
                    matches = re.findall(pattern, content, re.IGNORECASE)
                    for match in matches:
                        name = match.strip()
                        if len(name) > 3 and name.lower() not in ['organizer', 'leader', 'admin']:
                            organizers.append({
                                'name': name,
                                'affiliation': f'GDG {community_slug.title()}'
                            })
                
                if organizers:
                    print(f"  ✅ Found {len(organizers)} organizers on Meetup", file=sys.stderr)
                    return organizers[:3]  # Limit to 3 organizers
            
            print(f"  ⚠️  No organizers found on Meetup", file=sys.stderr)
            return []
            
        except Exception as e:
            print(f"  ❌ Meetup scraping failed: {e}", file=sys.stderr)
            return []
    
    def get_organizers_for_community(self, community_slug: str) -> List[Dict]:
        """Main method to get organizers for a community."""
        # Add a small delay to be respectful to servers
        time.sleep(random.uniform(1, 3))
        
        organizers = self.scrape_community_organizers(community_slug)
        
        # Add community information to each organizer
        for organizer in organizers:
            organizer['community'] = community_slug
        
        # Remove duplicates based on name
        unique_organizers = []
        seen_names = set()
        for organizer in organizers:
            name = organizer['name'].lower().strip()
            if name not in seen_names:
                unique_organizers.append(organizer)
                seen_names.add(name)
        
        return unique_organizers


def main():
    """Main function to run the scraper."""
    if len(sys.argv) != 2:
        print("Usage: python scrape_gdg_organizers.py <community_slug>", file=sys.stderr)
        sys.exit(1)
    
    community_slug = sys.argv[1]
    scraper = GDGOrganizersScraper()
    
    try:
        organizers = scraper.get_organizers_for_community(community_slug)
        
        # Output as JSON for easy parsing
        result = {
            'community': community_slug,
            'organizers': organizers,
            'count': len(organizers)
        }
        
        print(json.dumps(result, indent=2, ensure_ascii=False))
        
    except Exception as e:
        print(f"❌ Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main() 