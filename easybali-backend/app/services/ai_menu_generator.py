# app/services/ai_menu_generator.py
from typing import Dict, List, Optional, Any
import re
from app.services.menu_services import cache
from app.services.openai_client import client
from app.settings.config import settings

class AIMenuGenerator:
    """Generate dynamic WhatsApp menus based on AI-detected intent using Google Sheets data"""
    
    def __init__(self):
        # ═══════════════════════════════════════════════════════════════
        # SUBCATEGORY IMAGE URLS - Maps subcategory to S3 image URL
        # ═══════════════════════════════════════════════════════════════
        self.subcategory_image_urls = {
            "Airport Pickup/Drop": "https://easybali.s3.ap-southeast-2.amazonaws.com/services/Airport_Pickup_Drop.jpg",
            "Boxing": "https://easybali.s3.ap-southeast-2.amazonaws.com/services/Boxing.jpg",
            "Equipment Rental": "https://easybali.s3.ap-southeast-2.amazonaws.com/services/Equipment_Rental.jpg",
            "Fast Boat": "https://easybali.s3.ap-southeast-2.amazonaws.com/services/Fast_Boat.jpg",
            "Flowers": "https://easybali.s3.ap-southeast-2.amazonaws.com/services/Flowers.jpg",
            "Helicopter Ride": "https://easybali.s3.ap-southeast-2.amazonaws.com/services/Helicopter_Ride.jpg",
            "IV Drip": "https://easybali.s3.ap-southeast-2.amazonaws.com/services/IV_Drip.jpg",
            "In-House Dining": "https://easybali.s3.ap-southeast-2.amazonaws.com/services/In_House_Dining.jpg",
            "Island Tour": "https://easybali.s3.ap-southeast-2.amazonaws.com/services/Island_Tour.jpg",
            "Kickboxing": "https://easybali.s3.ap-southeast-2.amazonaws.com/services/Kickboxing.jpg",
            "Laundry": "https://easybali.s3.ap-southeast-2.amazonaws.com/services/Laundry.jpg",
            "Massage": "https://easybali.s3.ap-southeast-2.amazonaws.com/services/Massage.jpg",
            "Movie Night": "https://easybali.s3.ap-southeast-2.amazonaws.com/services/Movie_Night.jpg",
            "Muay Thai": "https://easybali.s3.ap-southeast-2.amazonaws.com/services/Muay_Thai.jpg",
            "Photography": "https://easybali.s3.ap-southeast-2.amazonaws.com/services/Photography.jpg",
            "Physiotherapy": "https://easybali.s3.ap-southeast-2.amazonaws.com/services/Physiotherapy.jpg",
            "Private Barber": "https://easybali.s3.ap-southeast-2.amazonaws.com/services/Private_Barber.jpg",
            "Private Chef": "https://easybali.s3.ap-southeast-2.amazonaws.com/services/Private_Chef.jpg",
            "Shisha Rental": "https://easybali.s3.ap-southeast-2.amazonaws.com/services/Shisha_Rental.jpg",
            "Tour with Driver": "https://easybali.s3.ap-southeast-2.amazonaws.com/services/Tour_with_Driver.jpg",
            "Yoga": "https://easybali.s3.ap-southeast-2.amazonaws.com/services/Yoga.jpg"
        }
        
        self.service_categories = {
            "massage": {
                "category": "Health & Wellness",
                "subcategory": "Massage",
                "keywords": [
                    "massage", "spa", "balinese", "aroma", "aromatherapy", "shiatsu", "zhiatzu",
                    "reflexology", "foot massage", "head neck", "shoulder", "coconut oil",
                    "sunburn massage", "aloevera", "facial", "natural facial", "body treatment"
                ]
            },
            "yoga": {
                "category": "Health & Wellness",
                "subcategory": "Yoga",
                "keywords": ["yoga", "meditation", "mobility", "functional training", "stretch"]
            },
            "physiotherapy": {
                "category": "Health & Wellness",
                "subcategory": "Physiotherapy",
                "keywords": ["physio", "physiotherapy", "injury", "recovery", "therapy"]
            },
            "iv_drip": {
                "category": "Health & Wellness",
                "subcategory": "IV Drip",
                "keywords": ["iv drip", "iv", "vitamin drip", "hangover", "hydration", "detox", "glutathione", "nad"]
            },
            "muay_thai": {
                "category": "Health & Wellness",
                "subcategory": "Muay Thai",
                "keywords": ["muay thai", "thai boxing"]
            },
            "boxing": {
                "category": "Health & Wellness",
                "subcategory": "Boxing",
                "keywords": ["boxing", "box"]
            },
            "kickboxing": {
                "category": "Health & Wellness",
                "subcategory": "Kickboxing",
                "keywords": ["kickboxing", "kickbox"]
            },

            # ── TRANSPORTATION ─────────────────────────────────────────────
            "airport_transfer": {
                "category": "Transportation",
                "subcategory": "Airport Pickup/Drop",
                "keywords": [
                    "airport", "pickup", "drop off", "transfer", "dps", "from airport",
                    "to airport", "pick up", "drop", "arrival", "departure"
                ]
            },
            "tour_with_driver": {
                "category": "Transportation",
                "subcategory": "Tour with Driver",
                "keywords": ["tour", "driver", "day tour", "half day", "full day", "sightseeing", "explore bali"]
            },
            "fast_boat": {
                "category": "Transportation",
                "subcategory": "Fast Boat",
                "keywords": [
                    "fast boat", "boat", "nusa penida", "lembongan", "gili", "sanur", "penida",
                    "island hopper", "roundtrip", "return ticket"
                ]
            },
            "island_tour": {
                "category": "Transportation",
                "subcategory": "Island Tour",
                "keywords": ["nusa penida tour", "penida tour", "island tour", "penida day trip"]
            },

            # ── FOOD & DRINKS ─────────────────────────────────────────────
            "private_chef": {
                "category": "Food and Beverage",
                "subcategory": "Private Chef",
                "keywords": ["chef", "private chef", "breakfast", "lunch", "dinner", "bbq", "cooking", "meal"]
            },

            # ── VILLA EXPERIENCES ─────────────────────────────────────────
            "shisha_rental": {
                "category": "Villa Experiences",
                "subcategory": "Shisha Rental",
                "keywords": ["shisha", "hookah", "sheesha"]
            },
            "movie_night": {
                "category": "Villa Experiences",
                "subcategory": "Movie Night",
                "keywords": ["movie night", "projector", "outdoor cinema", "cinema", "film"]
            },

            # ── RENTAL ────────────────────────────────────────────────────
            "equipment_rental": {
                "category": "Rental",
                "subcategory": "Equipment Rental",
                "keywords": [
                    "ps5", "playstation", "vr", "projector", "soundbar", "dolby",
                    "gaming", "console", "rent ps", "play station"
                ]
            },

            # ── EXTRA SERVICES ─────────────────────────────────────────────
            "private_barber": {
                "category": "Extra Services",
                "subcategory": "Private Barber",
                "keywords": ["barber", "haircut", "hair cut", "beard", "haircolor", "lineup"]
            },
            "flowers": {
                "category": "Extra Services",
                "subcategory": "Flowers",
                "keywords": ["flower", "bouquet", "roses", "arrangement", "hb "]
            },
            "laundry": {
                "category": "Extra Services",
                "subcategory": "Laundry",
                "keywords": ["laundry", "wash", "dry clean", "express laundry"]
            },
        }
    
    async def intelligent_service_check(self, query: str) -> Dict[str, Any]:
        """
        Use AI to determine:
        1. Is the user asking for a service?
        2. What service are they asking for?
        3. Do we offer it?
        """
        
        # Get all our available services from the service_categories
        our_services = []
        for service_type, info in self.service_categories.items():
            our_services.append({
                "name": info["subcategory"],
                "category": info["category"],
                "keywords": info["keywords"][:5]  # Sample keywords for context
            })
        
        services_list = "\n".join([
            f"- {s['name']} (Category: {s['category']})" 
            for s in our_services
        ])
        
        prompt = f"""You are an intelligent service matcher for EASYBali, a luxury villa concierge service in Bali.

OUR AVAILABLE SERVICES:
{services_list}

USER QUERY: "{query}"

YOUR TASK:
Analyze if the user is requesting a service, and determine if we offer it.

Return ONLY a JSON object with this exact structure:
{{
    "is_service_request": true/false,
    "requested_service": "name of service they want" or null,
    "we_offer_it": true/false,
    "matched_service": "exact name from our list" or null,
    "confidence": 0.0-1.0
}}

EXAMPLES:

Query: "I want to book a massage"
{{
    "is_service_request": true,
    "requested_service": "massage",
    "we_offer_it": true,
    "matched_service": "Massage",
    "confidence": 0.95
}}

Query: "Can you arrange scuba diving?"
{{
    "is_service_request": true,
    "requested_service": "scuba diving",
    "we_offer_it": false,
    "matched_service": null,
    "confidence": 0.90
}}

Query: "What's the weather like?"
{{
    "is_service_request": false,
    "requested_service": null,
    "we_offer_it": false,
    "matched_service": null,
    "confidence": 0.95
}}

Query: "I need a driver to the airport"
{{
    "is_service_request": true,
    "requested_service": "airport transfer",
    "we_offer_it": true,
    "matched_service": "Airport Pickup/Drop",
    "confidence": 0.90
}}

Query: "Book me a spa treatment"
{{
    "is_service_request": true,
    "requested_service": "spa treatment",
    "we_offer_it": true,
    "matched_service": "Massage",
    "confidence": 0.85
}}

Now analyze the user query and return ONLY the JSON:"""

        try:
            response = await client.chat.completions.create(
                model=settings.OPENAI_MODEL_NAME,  # Fast and cheap for classification
                messages=[
                    {"role": "system", "content": "You are a precise service classification AI. Return only valid JSON."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.2,  # Low temperature for consistent classification
                max_tokens=150,
                response_format={"type": "json_object"}  # Force JSON output
            )
            
            import json
            result = json.loads(response.choices[0].message.content)
            
            return result
            
        except Exception as e:
            print(f"[intelligent_service_check] Error: {e}")
            # Fallback to keyword-based detection
            return {
                "is_service_request": False,
                "requested_service": None,
                "we_offer_it": False,
                "matched_service": None,
                "confidence": 0.0
            }
    
    def detect_service_intent(self, query: str) -> Optional[Dict[str, str]]:
        """KEEP EXISTING - Detect which service category user is asking about"""
        query_lower = query.lower()
        
        scores = {}
        for service_type, info in self.service_categories.items():
            score = 0
            for keyword in info["keywords"]:
                if keyword in query_lower:
                    score += len(keyword.split())
            if score > 0:
                scores[service_type] = score
        
        if scores:
            best_match = max(scores.items(), key=lambda x: x[1])
            service_type = best_match[0]
            info = self.service_categories[service_type]
            return {
                "service_type": service_type,
                "category": info["category"],
                "subcategory": info["subcategory"]
            }
        return None

    
    def extract_requirements(self, query: str) -> Dict[str, Any]:
        """Extract specific requirements from query"""
        requirements = {
            "location": None,
            "people_count": None,
            "budget": None,
            "time_preference": None,
            "date": None
        }
        
        # Extract location - check against your actual locations
        locations = [
            "canggu", "seminyak", "uluwatu", "ubud", "berawa", "umalas", 
            "kerobokan", "pererenan", "legian", "kuta", "petitenget", 
            "batubelig", "batubolong", "jimbaran", "nusa dua", "sanur"
        ]
        for loc in locations:
            if loc in query.lower():
                requirements["location"] = loc.title()
                break
        
        # Extract people count
        people_patterns = [
            r'(\d+)\s*(?:people|person|pax|guests?)',
            r'for\s*(\d+)',
            r'group\s*of\s*(\d+)',
            r'(\d+)\s*of\s*us'
        ]
        for pattern in people_patterns:
            match = re.search(pattern, query.lower())
            if match:
                requirements["people_count"] = int(match.group(1))
                break
        
        # Extract budget
        budget_patterns = [
            r'(?:under|below|max|maximum|budget)\s*(?:idr)?\s*(\d+(?:,\d{3})*(?:k|000)?)',
            r'(?:around|about)\s*(?:idr)?\s*(\d+(?:,\d{3})*(?:k|000)?)'
        ]
        for pattern in budget_patterns:
            budget_match = re.search(pattern, query.lower())
            if budget_match:
                budget_str = budget_match.group(1).replace(',', '').replace('k', '000')
                requirements["budget"] = int(budget_str)
                break
        
        # Extract time preferences
        time_keywords = {
            "morning": ["morning", "breakfast", "am"],
            "afternoon": ["afternoon", "lunch", "noon"],
            "evening": ["evening", "dinner", "night"]
        }
        for period, keywords in time_keywords.items():
            if any(kw in query.lower() for kw in keywords):
                requirements["time_preference"] = period
                break
        
        return requirements
    
    async def generate_service_menu(
        self, 
        category: str, 
        subcategory: Optional[str],
        requirements: Dict[str, Any]
    ) -> Optional[Dict[str, Any]]:
        """Generate WhatsApp list menu for services using Google Sheets data"""
        
        if cache["services_df"] is None:
            return None
        
        services_df = cache["services_df"]
        
        # Filter by category
        filtered_df = services_df[services_df['Category'] == category]
        
        # Filter by subcategory if specified
        if subcategory:
            filtered_df = filtered_df[filtered_df['Sub-category'] == subcategory]
        
        # Filter by location if specified
        if requirements.get("location"):
            location = requirements["location"]
            filtered_df = filtered_df[
                filtered_df['Locations'].str.contains(location, case=False, na=False)
            ]
        
        # Filter by people count if specified (for services with max pax)
        if requirements.get("people_count"):
            people = requirements["people_count"]
            # Check service item names for pax info
            filtered_df = filtered_df[
                filtered_df['Service Item'].str.contains(f'max {people}', case=False, na=False) |
                filtered_df['Service Item'].str.contains(f'{people} pax', case=False, na=False) |
                ~filtered_df['Service Item'].str.contains('max', case=False, na=False)
            ]
        
        if filtered_df.empty:
            return None
        
        # Filter by budget if specified
        if requirements.get("budget"):
            budget = requirements["budget"]
            # Convert price to numeric, handling potential formatting issues
            filtered_df = filtered_df.copy()
            filtered_df['Price_Numeric'] = filtered_df['Final Price (Service Item Button)'].replace(
                r'[^\d]', '', regex=True
            ).replace('', '0').astype(int)
            filtered_df = filtered_df[filtered_df['Price_Numeric'] <= budget]
        
        # ═══════════════════════════════════════════════════════════════
        # GET IMAGE URL BASED ON SUBCATEGORY
        # ═══════════════════════════════════════════════════════════════
        image_url = None
        if subcategory and subcategory in self.subcategory_image_urls:
            image_url = self.subcategory_image_urls[subcategory]
        else:
            # Fallback: log warning if no image found
            print(f"[Warning] No image URL found for subcategory: {subcategory}")
        
        # ═══════════════════════════════════════════════════════════════
        # BUILD WHATSAPP LIST MENU - SEPARATED PRICE & DESCRIPTION
        # ═══════════════════════════════════════════════════════════════
        rows = []
        for idx, (_, service) in enumerate(filtered_df.head(10).iterrows()):
            service_name = service.get("Service Item", "Unknown Service")
            price_raw = service.get("Final Price (Service Item Button)", "0")
            description = service.get("Service Item Description", "")
            
            # Clean and format price for display (with spaces like: 20 000, 500 000)
            try:
                price_clean = int(str(price_raw).replace(' ', '').replace(',', ''))
                # Format with spaces every 3 digits from right
                price_formatted = f"{price_clean:,}".replace(',', ' ')
            except:
                price_formatted = str(price_raw).replace(',', ' ')
            
            # Truncate description to fit WhatsApp limits (72 chars for description field)
            desc_short = description[:72] if len(description) > 72 else description
            
            rows.append({
                "id": f"ai_service_{idx}_{service.get('Sub-category ID', service_name.replace(' ', '_'))}",
                "title": service_name[:24],  # WhatsApp 24 char limit
                "description": desc_short,    # ONLY description now
                "price": price_formatted      # Separate price field
            })
        
        # Build header and body text
        header_text = f"{subcategory or category}"
        body_parts = [f"Found {len(rows)} service{'s' if len(rows) > 1 else ''}"]
        
        if requirements.get("location"):
            body_parts.append(f"in {requirements['location']}")
        if requirements.get("people_count"):
            body_parts.append(f"for {requirements['people_count']} people")
        if requirements.get("budget"):
            body_parts.append(f"under IDR {requirements['budget']:,}")
        
        body_text = " ".join(body_parts)
        
        return {
            "title": header_text[:60],
            "description": body_text[:1024],
            "image_url": image_url,  # S3 image URL
            "sections": [{
                "title": "Available Services",
                "rows": rows
            }]
        }
    
    async def get_service_details_by_id(self, service_id: str) -> Optional[Dict[str, Any]]:
        """Get full service details from ID"""
        if cache["services_df"] is None:
            return None
        
        services_df = cache["services_df"]
        
        # Extract subcategory ID from service_id (format: ai_service_idx_subcategory_id)
        parts = service_id.split("_")
        if len(parts) >= 3:
            subcategory_id = "_".join(parts[2:])
            
            # Try to find by subcategory ID first
            service = services_df[
                services_df['Sub-category ID'] == subcategory_id
            ]
            
            # If not found, try by service name (fallback)
            if service.empty:
                service_name = subcategory_id.replace('_', ' ')
                service = services_df[
                    services_df['Service Item'].str.contains(service_name, case=False, na=False)
                ]
            
            if not service.empty:
                row = service.iloc[0]
                return {
                    "service_name": row.get("Service Item"),
                    "description": row.get("Service Item Description"),
                    "price": row.get("Final Price (Service Item Button)"),
                    "locations": row.get("Locations"),
                    "image_url": row.get("Image URL"),
                    "category": row.get("Category"),
                    "subcategory": row.get("Sub-category"),
                    "subcategory_id": row.get("Sub-category ID")
                }
        
        return None

ai_menu_generator = AIMenuGenerator()