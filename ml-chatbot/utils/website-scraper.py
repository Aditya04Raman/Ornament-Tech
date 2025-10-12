import json
import os

def extract_website_content():
    """
    Extract all content from the Ornament Tech website for ML training
    """
    
    website_content = {
        "brand": {
            "name": "Ornament Tech",
            "tagline": "Bespoke jewellery with editorial presentation and an AI concierge",
            "description": "Where traditional craftsmanship meets cutting-edge technology. Creating jewelry that tells your unique story.",
            "experience": "15+ years",
            "customers": "500+ happy customers", 
            "pieces_created": "1200+ pieces created",
            "values": ["Artistry", "Partnership", "Sustainability"]
        },
        
        "bespoke_process": {
            "overview": "From concept to creation, a guided journey tailored to you",
            "steps": [
                {
                    "step": 1,
                    "title": "Consultation",
                    "description": "Share your vision and story with our designers. We'll discuss your budget, timeline, and unique inspirations to create the perfect foundation for your piece.",
                    "duration": "Week 1",
                    "details": "Discovery session to understand your vision, lifestyle, and preferences"
                },
                {
                    "step": 2, 
                    "title": "Design",
                    "description": "Watch your dreams take shape through hand-drawn sketches and 3D CAD models. We'll refine every detail together until the design is perfect.",
                    "duration": "Weeks 2-3",
                    "details": "View our collections, explore materials, and begin sketching your unique design concept"
                },
                {
                    "step": 3,
                    "title": "Craft", 
                    "description": "Our master craftspeople bring your design to life using traditional techniques and modern precision. Every piece is handmade with exceptional attention to detail.",
                    "duration": "Weeks 4-8",
                    "details": "Expert goldsmithing and gemstone setting in our atelier with quality control"
                },
                {
                    "step": 4,
                    "title": "Delivery",
                    "description": "Your completed masterpiece undergoes rigorous quality checks before being presented in our signature packaging.",
                    "duration": "Week 9", 
                    "details": "Final quality checks, presentation, and delivery of your bespoke piece"
                }
            ],
            "typical_timeline": "4-8 weeks depending on complexity"
        },
        
        "collections": [
            {
                "name": "Engagement Rings",
                "description": "Solitaire classics, vintage-inspired halos, and completely custom designs to mark your unique love story.",
                "pieces": "50+ designs",
                "starting_price": "From £2,500",
                "styles": ["Solitaire", "Halo", "Trilogy", "Custom designs"],
                "popular_choices": ["Diamond solitaire", "Sapphire halo", "Vintage-inspired"]
            },
            {
                "name": "Wedding Bands",
                "description": "Perfectly paired bands in classic, textured, and shaped styles. Each designed to complement your engagement ring.",
                "pieces": "40+ designs", 
                "starting_price": "From £800",
                "styles": ["Classic", "Shaped", "Textured", "Bespoke fits"],
                "popular_choices": ["Matching sets", "Rose gold bands", "Textured finish"]
            },
            {
                "name": "Necklaces",
                "description": "Delicate pendants to statement pieces, each featuring carefully selected gemstones and precious metals.",
                "pieces": "35+ designs",
                "starting_price": "From £1,200", 
                "styles": ["Pendants", "Statement designs", "Precious stones"],
                "popular_choices": ["Diamond tennis", "Gemstone pendants", "Gold chains"]
            },
            {
                "name": "Earrings",
                "description": "From elegant studs for everyday wear to dramatic drops for special occasions, crafted with precision.",
                "pieces": "45+ designs",
                "starting_price": "From £600",
                "styles": ["Studs", "Hoops", "Drops", "Precious metals"],
                "popular_choices": ["Diamond studs", "Gold hoops", "Gemstone drops"]
            },
            {
                "name": "Bridal Collection",
                "description": "Complete bridal sets designed to complement each other perfectly for your special day.",
                "pieces": "25+ sets",
                "starting_price": "From £3,500",
                "includes": ["Engagement ring", "Wedding band", "Matching earrings", "Optional necklace"]
            },
            {
                "name": "Heritage Collection",
                "description": "Timeless pieces inspired by classical designs, updated with contemporary craftsmanship.",
                "pieces": "30+ designs", 
                "starting_price": "From £1,800",
                "inspiration": ["Art Deco", "Victorian", "Edwardian", "Contemporary classical"]
            }
        ],
        
        "materials": [
            {
                "name": "Platinum",
                "description": "The ultimate choice for luxury jewelry. Naturally white, hypoallergenic, and incredibly durable.",
                "properties": ["Hypoallergenic", "Naturally White", "Extremely Durable", "Develops Patina"],
                "durability": "Highest",
                "maintenance": "Minimal",
                "best_for": "Engagement rings, daily wear",
                "care": "Simple cleaning with warm soapy water"
            },
            {
                "name": "18K Yellow Gold",
                "description": "Classic and timeless with a warm, rich hue. Perfect balance of purity and durability.",
                "properties": ["Classic Beauty", "Excellent Durability", "Warm Tone", "Traditional Choice"],
                "durability": "High",
                "maintenance": "Low", 
                "best_for": "Classic pieces, heirlooms",
                "care": "Regular gentle cleaning maintains luster"
            },
            {
                "name": "18K White Gold", 
                "description": "Contemporary elegance with a bright, silvery finish. Rhodium-plated for extra brilliance.",
                "properties": ["Modern Appeal", "Rhodium Finished", "Bright Appearance", "Versatile Choice"],
                "durability": "High",
                "maintenance": "Moderate",
                "best_for": "Modern designs, versatility",
                "care": "Periodic rhodium re-plating recommended"
            },
            {
                "name": "18K Rose Gold",
                "description": "Romantic and distinctive with its beautiful blush tone created by copper alloys.",
                "properties": ["Romantic Tone", "Unique Character", "Vintage Appeal", "Growing Popularity"],
                "durability": "High",
                "maintenance": "Low",
                "best_for": "Romantic pieces, vintage styles", 
                "care": "Gentle cleaning preserves color"
            }
        ],
        
        "gemstones": [
            {
                "name": "Diamonds",
                "description": "The most precious gemstone, evaluated by the 4Cs: cut, color, clarity, carat.",
                "characteristics": ["Exceptional hardness", "Brilliant fire", "Timeless appeal", "Investment value"],
                "grading": "4Cs system (Cut, Color, Clarity, Carat)",
                "durability": "Hardest natural material",
                "care": "Professional cleaning recommended"
            },
            {
                "name": "Sapphire",
                "description": "Durable corundum available in many colors, second only to diamonds in hardness.",
                "characteristics": ["Available in many colors", "Excellent durability", "Royal heritage", "Symbolic meaning"],
                "colors": ["Blue", "Pink", "Yellow", "White", "Padparadscha"],
                "durability": "Excellent",
                "symbolism": "Wisdom, loyalty, nobility"
            },
            {
                "name": "Emerald",
                "description": "Vibrant green beryl with unique inclusions that add character and authenticity.",
                "characteristics": ["Vivid green color", "Natural inclusions", "Requires gentle care", "Historic significance"],
                "origin": "Colombia, Zambia, Brazil",
                "care": "Gentle handling required",
                "symbolism": "Growth, renewal, wisdom"
            },
            {
                "name": "Ruby",
                "description": "Rich red corundum prized for its intensity and passion.",
                "characteristics": ["Intense red color", "Excellent hardness", "Symbol of love", "Rare and valuable"],
                "origin": "Myanmar, Madagascar, Mozambique",
                "grading": "Color intensity most important",
                "symbolism": "Love, passion, courage"
            }
        ],
        
        "services": {
            "consultations": {
                "types": ["In-Person Consultation", "Virtual Video Call", "Phone Consultation"],
                "locations": ["London Studio", "Cambridge Boutique", "Virtual Appointment"],
                "duration": "60-90 minutes",
                "cost": "Free consultation",
                "what_to_expect": [
                    "Discovery session to understand your vision",
                    "Design exploration and material selection",
                    "Detailed proposal with timeline and pricing"
                ],
                "booking": "Available through website form or phone"
            },
            
            "care_services": {
                "cleaning": "Professional cleaning and polishing services",
                "repair": "Expert repair and restoration",
                "resizing": "Ring resizing and adjustment services", 
                "maintenance": "Regular check-ups and maintenance",
                "warranty": "Lifetime guarantee on craftsmanship"
            },
            
            "sizing": {
                "process": "Professional ring sizing consultation",
                "tips": [
                    "Measure at end of day when fingers are warm",
                    "Consider band width in sizing",
                    "Account for seasonal finger size changes"
                ],
                "international": "International size conversions available",
                "tools": "Professional sizing rings and tools"
            }
        },
        
        "locations": [
            {
                "name": "London Studio",
                "address": "69 Regent's Park Road, Primrose Hill, London NW1 8UY",
                "phone": "020 8154 9500",
                "email": "primrosehill@ornamenttech.com",
                "description": "Flagship studio with full design and crafting facilities",
                "services": ["Consultations", "Design", "Crafting", "Repairs"],
                "hours": "Mon-Sat 10am-6pm, Sun by appointment"
            },
            {
                "name": "Cambridge Boutique",
                "address": "6/7 Green Street, Cambridge CB2 3JU", 
                "phone": "01223 461333",
                "email": "cambridge@ornamenttech.com",
                "description": "Boutique showroom with curated collection displays",
                "services": ["Consultations", "Collection viewing", "Repairs"],
                "hours": "Mon-Sat 10am-6pm, Sun 12pm-4pm"
            }
        ],
        
        "pricing": {
            "engagement_rings": {"min": 2500, "max": 20000, "average": 5000},
            "wedding_bands": {"min": 800, "max": 5000, "average": 1500},
            "necklaces": {"min": 1200, "max": 15000, "average": 3000},
            "earrings": {"min": 600, "max": 8000, "average": 2000},
            "consultations": {"cost": 0, "note": "Free initial consultation"},
            "payment_options": ["Full payment", "Payment plans", "Deposit system"]
        },
        
        "faq": [
            {
                "question": "What are typical lead times?",
                "answer": "Bespoke projects typically take 4-8 weeks depending on complexity. Simple pieces may be ready in 3-4 weeks, while complex designs can take up to 12 weeks.",
                "category": "Timeline"
            },
            {
                "question": "Do you resize rings?",
                "answer": "Yes, we offer comprehensive resizing services. Most rings can be resized up or down by 2-3 sizes. Complex designs may have limitations.",
                "category": "Services"
            },
            {
                "question": "What's a typical budget?",
                "answer": "Budgets vary widely based on materials and complexity. Engagement rings typically start from £2,500, while earrings start from £600. We work with all budgets.",
                "category": "Pricing"
            },
            {
                "question": "Do you offer payment plans?",
                "answer": "Yes, we offer flexible payment options including payment plans and deposit systems to make your dream piece more accessible.",
                "category": "Payment"
            },
            {
                "question": "What warranty do you provide?",
                "answer": "We provide a lifetime guarantee on craftsmanship and a comprehensive warranty covering materials and settings.",
                "category": "Warranty"
            }
        ],
        
        "testimonials": [
            {
                "text": "Absolutely stunning ring! The bespoke process was so personal and the final piece exceeded all expectations.",
                "author": "Sarah M.",
                "rating": 5,
                "service": "Engagement Ring"
            },
            {
                "text": "Professional service from start to finish. They truly understood our vision and brought it to life perfectly.",
                "author": "James & Emma K.",
                "rating": 5,
                "service": "Wedding Set"
            },
            {
                "text": "The quality is exceptional and the AI concierge made the whole experience so smooth and informative.",
                "author": "Michael R.",
                "rating": 5,
                "service": "Consultation"
            }
        ],
        
        "contact": {
            "email": "hello@ornamenttech.com",
            "phone": "+44 20 8154 9500", 
            "whatsapp": "https://wa.me/1234567890",
            "social_media": {
                "instagram": "@ornamenttech",
                "facebook": "OrnamentTech",
                "pinterest": "OrnamentTech"
            },
            "response_time": "Within 24 hours",
            "availability": "Mon-Sat 9am-6pm GMT"
        }
    }
    
    # Save to JSON file
    output_path = os.path.join(os.path.dirname(__file__), '..', 'data', 'website-content.json')
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(website_content, f, indent=2, ensure_ascii=False)
    
    print(f"Website content extracted and saved to {output_path}")
    return website_content

if __name__ == "__main__":
    extract_website_content()
