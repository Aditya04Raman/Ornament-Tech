"""
Website Content Scraper for Ornament Tech ML Chatbot
Extracts comprehensive website content for training data generation
"""

import json
import os
from typing import Dict, List, Any

def extract_website_content() -> Dict[str, Any]:
    """
    Extract comprehensive website content for ML training
    This function returns the complete knowledge base for the jewelry website
    """
    return {
        'brand': {
            'name': 'Ornament Tech',
            'description': 'luxury jewelry boutique specializing in bespoke jewelry creation',
            'tagline': 'bespoke jewellery with editorial presentation and an AI concierge',
            'experience': '15+ years',
            'pieces_created': '1200+ pieces created',
            'customers': '500+ happy customers',
            'values': ['Artistry', 'Partnership', 'Sustainability']
        },
        
        'bespoke_process': {
            'overview': 'From concept to creation, a guided journey tailored to you',
            'typical_timeline': '4-8 weeks depending on complexity',
            'steps': [
                {
                    'step': 1,
                    'title': 'Consultation',
                    'description': 'Share your vision and story with our designers. We\'ll discuss your budget, timeline, and unique inspirations to create the perfect foundation for your piece.',
                    'duration': 'Week 1'
                },
                {
                    'step': 2,
                    'title': 'Design',
                    'description': 'Watch your dreams take shape through hand-drawn sketches and 3D CAD models. We\'ll refine every detail together until the design is perfect.',
                    'duration': 'Weeks 2-3'
                },
                {
                    'step': 3,
                    'title': 'Craft',
                    'description': 'Our master craftspeople bring your design to life using traditional techniques and modern precision. Every piece is handmade with exceptional attention to detail.',
                    'duration': 'Weeks 4-8'
                },
                {
                    'step': 4,
                    'title': 'Delivery',
                    'description': 'Your completed masterpiece undergoes rigorous quality checks before being presented in our signature packaging. The moment you\'ve been waiting for.',
                    'duration': 'Week 9'
                }
            ]
        },
        
        'collections': [
            {
                'name': 'Engagement Rings',
                'description': 'Solitaire classics, vintage-inspired halos, and completely custom designs to mark your unique love story.',
                'pieces': '50+ designs',
                'starting_price': 'From £2,500',
                'styles': ['Solitaire', 'Halo', 'Trilogy', 'Custom designs']
            },
            {
                'name': 'Wedding Bands',
                'description': 'Perfectly paired bands in classic, textured, and shaped styles. Each designed to complement your engagement ring.',
                'pieces': '40+ designs',
                'starting_price': 'From £800',
                'styles': ['Classic', 'Shaped', 'Textured', 'Bespoke fits']
            },
            {
                'name': 'Necklaces',
                'description': 'Delicate pendants to statement pieces, each featuring carefully selected gemstones and precious metals.',
                'pieces': '35+ designs',
                'starting_price': 'From £1,200',
                'styles': ['Pendants', 'Statement designs', 'Precious stones']
            },
            {
                'name': 'Earrings',
                'description': 'From elegant studs for everyday wear to dramatic drops for special occasions, crafted with precision.',
                'pieces': '45+ designs',
                'starting_price': 'From £600',
                'styles': ['Studs', 'Hoops', 'Drops', 'Precious metals']
            },
            {
                'name': 'Bridal Collection',
                'description': 'Complete bridal sets designed to complement each other perfectly for your special day.',
                'pieces': '25+ sets',
                'starting_price': 'From £3,500'
            },
            {
                'name': 'Heritage Collection',
                'description': 'Timeless pieces inspired by classical designs, updated with contemporary craftsmanship.',
                'pieces': '30+ designs',
                'starting_price': 'From £1,800'
            }
        ],
        
        'materials': [
            {
                'name': 'Platinum',
                'description': 'The ultimate choice for luxury jewelry. Naturally white, hypoallergenic, and incredibly durable. Platinum develops a beautiful patina over time while maintaining its strength.',
                'properties': ['Hypoallergenic', 'Naturally White', 'Extremely Durable', 'Develops Patina'],
                'durability': 'Highest',
                'maintenance': 'Minimal',
                'best_for': 'Engagement rings, daily wear'
            },
            {
                'name': '18K Yellow Gold',
                'description': 'Classic and timeless with a warm, rich hue. Perfect balance of purity and durability, making it ideal for everyday wear and heirloom pieces.',
                'properties': ['Classic Beauty', 'Excellent Durability', 'Warm Tone', 'Traditional Choice'],
                'durability': 'High',
                'maintenance': 'Low',
                'best_for': 'Classic pieces, heirlooms'
            },
            {
                'name': '18K White Gold',
                'description': 'Contemporary elegance with a bright, silvery finish. Rhodium-plated for extra brilliance, though periodic re-plating may be recommended.',
                'properties': ['Modern Appeal', 'Rhodium Finished', 'Bright Appearance', 'Versatile Choice'],
                'durability': 'High',
                'maintenance': 'Moderate',
                'best_for': 'Modern designs, versatility'
            },
            {
                'name': '18K Rose Gold',
                'description': 'Romantic and distinctive with its beautiful blush tone created by copper alloys. Increasingly popular for its unique warmth and vintage appeal.',
                'properties': ['Romantic Tone', 'Unique Character', 'Vintage Appeal', 'Growing Popularity'],
                'durability': 'High',
                'maintenance': 'Low',
                'best_for': 'Romantic pieces, vintage styles'
            }
        ],
        
        'gemstones': [
            {
                'name': 'Diamonds',
                'description': 'Understand the 4Cs: cut, color, clarity, carat. The most precious and durable gemstone.',
                'characteristics': ['4Cs evaluation', 'Exceptional hardness', 'Brilliant fire', 'Timeless appeal']
            },
            {
                'name': 'Sapphires',
                'description': 'Durable corundum in a range of colors. Second only to diamonds in hardness.',
                'characteristics': ['Available in many colors', 'Excellent durability', 'Royal heritage', 'Symbolic meaning']
            },
            {
                'name': 'Emeralds',
                'description': 'Vibrant green beryl with unique inclusions that add character and authenticity.',
                'characteristics': ['Vivid green color', 'Natural inclusions', 'Requires gentle care', 'Historic significance']
            },
            {
                'name': 'Rubies',
                'description': 'Rich red corundum prized for its intensity and passion.',
                'characteristics': ['Intense red color', 'Excellent hardness', 'Symbol of love', 'Rare and valuable']
            }
        ],
        
        'services': {
            'consultations': {
                'types': ['In-Person Consultation', 'Virtual Video Call', 'Phone Consultation'],
                'locations': ['London Studio', 'Cambridge Boutique', 'Virtual Appointment'],
                'duration': '60-90 minutes',
                'cost': 'Free consultation',
                'what_to_expect': [
                    'Discovery session to understand your vision',
                    'Design exploration and material selection',
                    'Detailed proposal with timeline and pricing'
                ]
            },
            'care_guide': {
                'cleaning': 'Gentle cleaning with warm water and mild soap keeps your pieces brilliant',
                'storage': 'Individual pouches or compartments prevent scratching and tangling',
                'professional_service': 'Annual check-ups ensure settings remain secure and finishes stay fresh'
            },
            'sizing': {
                'tips': [
                    'Measure at the end of the day when fingers are warm',
                    'Consider width: wider bands feel tighter',
                    'Consult our team for printable sizing tools and advice'
                ],
                'services': ['Ring sizing', 'International conversions', 'Comfort-fit recommendations']
            }
        },
        
        'locations': [
            {
                'name': 'London Studio',
                'address': '69 Regent\'s Park Road, Primrose Hill, London NW1 8UY',
                'phone': '020 8154 9500',
                'email': 'primrosehill@ornamenttech.co.uk',
                'description': 'Flagship studio. Appointments recommended.'
            },
            {
                'name': 'Cambridge Boutique',
                'address': '6/7 Green Street, Cambridge CB2 3JU',
                'phone': '01223 461333',
                'email': 'cambridge@ornamenttech.co.uk',
                'description': 'Boutique showroom. Walk-ins welcome when available.'
            }
        ],
        
        'pricing': {
            'ranges': {
                'engagement_rings': 'From £2,500',
                'wedding_bands': 'From £800',
                'necklaces': 'From £1,200',
                'earrings': 'From £600',
                'bridal_sets': 'From £3,500',
                'heritage_pieces': 'From £1,800'
            },
            'payment_options': ['Full payment', 'Payment plans', 'Deposit system', 'Financing available'],
            'factors': ['Materials chosen', 'Gemstone quality', 'Design complexity', 'Craftsmanship level']
        },
        
        'features': [
            'Ethically sourced materials with full traceability',
            'Award-winning craftsmanship and innovative design',
            'Lifetime guarantee covering craftsmanship and materials',
            'AI concierge for 24/7 customer support',
            'Virtual and in-person consultations available',
            'Complete bespoke service from concept to creation'
        ],
        
        'testimonials': [
            {
                'text': 'Absolutely stunning ring! The bespoke process was so personal and the final piece exceeded all expectations.',
                'author': 'Sarah M.',
                'rating': 5
            },
            {
                'text': 'Professional service from start to finish. They truly understood our vision and brought it to life perfectly.',
                'author': 'James & Emma K.',
                'rating': 5
            },
            {
                'text': 'The quality is exceptional and the AI concierge made the whole experience so smooth and informative.',
                'author': 'Michael R.',
                'rating': 5
            }
        ],
        
        'faq': [
            {
                'question': 'What are typical lead times?',
                'answer': 'Bespoke projects typically take 4–8 weeks depending on complexity. Simple modifications may take 2-3 weeks, while completely custom pieces with rare gemstones can take up to 12 weeks.'
            },
            {
                'question': 'Do you resize rings?',
                'answer': 'Yes, we offer comprehensive resizing services. Most rings can be resized up or down by 2-3 sizes. Complex designs with intricate details may have limitations, which we\'ll discuss during consultation.'
            },
            {
                'question': 'What\'s a typical budget for bespoke jewelry?',
                'answer': 'Budgets vary widely based on materials and design complexity. Engagement rings start from £2,500, while elaborate custom pieces can range from £5,000 to £50,000+. We work with all budgets to create something special.'
            },
            {
                'question': 'Do you provide certificates for gemstones?',
                'answer': 'Yes, all our diamonds come with GIA or similar certification. Colored gemstones receive appropriate certifications from recognized gemological laboratories.'
            },
            {
                'question': 'What is your return policy?',
                'answer': 'Bespoke pieces are custom-made for you and generally cannot be returned. However, we offer unlimited revisions during the design phase and a satisfaction guarantee on craftsmanship.'
            }
        ],
        
        'contact': {
            'email': 'hello@ornamenttech.com',
            'phone': '+44 20 8154 9500',
            'whatsapp': 'Available for quick questions',
            'response_time': 'within 24 hours',
            'availability': 'Monday to Saturday, 9 AM to 6 PM',
            'social_media': {
                'instagram': '@ornamenttech',
                'facebook': 'OrnamentTech',
                'pinterest': 'OrnamentTech'
            }
        }
    }

def save_website_content():
    """
    Save extracted website content to JSON file
    """
    content = extract_website_content()
    
    # Save to data directory
    data_dir = os.path.join(os.path.dirname(__file__), '..', 'data')
    os.makedirs(data_dir, exist_ok=True)
    
    output_path = os.path.join(data_dir, 'website-content.json')
    
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(content, f, indent=2, ensure_ascii=False)
    
    print(f"Website content saved to {output_path}")
    return output_path

if __name__ == "__main__":
    save_website_content()
