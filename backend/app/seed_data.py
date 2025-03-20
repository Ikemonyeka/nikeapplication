from sqlalchemy.orm import Session
from .schemas import ItemCreate, OrderCreate  # Import schemas
from .services import create_item, create_order  # Import existing function
from .models import Item, Order
from sqlalchemy import func

#seeded data for items database.
SEED_ITEMS = [
    {
        'name': 'Nike G.T. Cut 3', 
        'description': "How can you separate your game when it''s winning time? Start by lacing up in the G.T. Cut 3. Designed to help you create space for stepback jumpers and backdoor cuts, its sticky multicourt traction helps you stop on a dime and shift gears at will. And when you''re making all those game-changing plays, the newly added, ultra-responsive ZoomX foam helps keep you fresh for four quarters.", 
        'category': 'gym exercise', 
        'price': 144.97, 
        'gender': 'Men', 
        'image_url': 'https://i.imgur.com/g1EK29f.png'
    }, 
    {
        'name': 'Nike Pegasus 41 - F', 
        'description': 'Responsive cushioning in the Pegasus provides an energized ride for everyday road running. Experience lighter-weight energy return with dual Air Zoom units and a ReactX foam midsole. Plus, improved engineered mesh on the upper decreases weight and increases breathability.', 
        'category': 'running jogging', 
        'price': 140.0, 
        'gender': 'Women', 
        'image_url': 'https://i.imgur.com/fjHLWVY.png'
    }, 
    {
        'name': 'Nike Free Metcon 6', 
        'description': "From power lifts to ladders, from grass blades to grainy platforms, from the turf to the track your workout has a certain purpose, a specific focus. The Free Metcon 6 supports every grunt, growl and 'got it!' We added even more forefoot flexibility to our most adaptable trainer and reinforced the heel with extra foam. That means more freedom for dynamic movements during plyos and cardio classes, plus the stable base you need for weights.", 
        'category': 'gym exercise', 
        'price': 120.0, 
        'gender': 'Men', 
        'image_url': 'https://i.imgur.com/hW3tcLO.png'
    }, 
    {
        'name': 'Nike Pegasus 41', 
        'description': 'Responsive cushioning in the Pegasus provides an energized ride for everyday road running. Experience lighter-weight energy return with dual Air Zoom units and a ReactX foam midsole. Plus, improved engineered mesh on the upper decreases weight and increases breathability.', 
        'category': 'running jogging', 
        'price': 140.0, 
        'gender': 'Men', 
        'image_url': 'https://i.imgur.com/XdIpyTd.png'
    }, 
    {
        'name': 'Nike Invincible 3', 
        'description': 'Maximum cushioning provides our most comfortable ride for everyday runs. Experience a breathable Flyknit upper and the robust platform of lightweight ZoomX foam that softens impact. Plus, the midsole of this model is wider and taller than the last for even more cushioned comfort.', 'category': 'trail walking running', 'price': 180.0, 'gender': 'Men', 'image_url': 'https://i.imgur.com/LLonsyQ.png'}, {'name': 'Nike Cortez', 'description': "Was 1972. Now 2023. Sometimes more is better. Recrafting the revered look, we've refreshed the design with a wider toe area and firmer side panels so you can comfortably wear them day in, day out. Reengineered materials help prevent warping and add durability while maintaining the classic '72 shape you fell in love with. Lace up, because tradition keeps getting better.", 
        'category': 'walking', 
        'price': 180.0, 
        'gender': 'Men', 
        'image_url': 'https://i.imgur.com/LLonsyQ.png'
    }, 
    {
        'name': 'Nike Cortez', 
        'description': 'Was 1972. Now 2023. Sometimes more is better. Recrafting the revered look, we''ve refreshed the design with a wider toe area and firmer side panels so you can comfortably wear them day in, day out. Reengineered materials help prevent warping and add durability while maintaining the classic ''72 shape you fell in love with. Lace up, because tradition keeps getting better.', 
        'category': 'walking', 
        'price': 90.0, 
        'gender': 'Men', 
        'image_url': 'https://i.imgur.com/ZgImDHA.png'
    }, 
    {
        'name': 'Nike Motiva', 
        'description': 'The Nike Motiva helps you step through whatever the day brings, at your pace. Its uniquely patterned outsole and exaggerated rocker combine to give you a super-smooth, cushioned and comfortable ride. This means you can walk, jog or run comfortably and come back for your next leisurely stroll confidently. It gives you optimal support for your every move, every day.', 
        'category': 'gym exercise', 
        'price': 110.0, 
        'gender': 'Women', 
        'image_url': 'https://i.imgur.com/PhIwWjl.png'
    }, 
    {
        'name': 'Nike InfinityRN 4', 
        'description': 'Maximum cushioning provides elevated comfort for everyday runs. Experience a soft, rocker-shaped platform made with new ReactX foam underfoot and an ultra-comfortable collar and tongue for a snug feel. Plus, a water-resistant membrane was added to this version to help keep you dry.', 
        'category': 'jogging', 
        'price': 160.0, 
        'gender': 'Women', 
        'image_url': 'https://i.imgur.com/zuRpyBF.png'
    }, 
    {
        'name': 'Nike Phoenix Waffle', 
        'description': 'The iconic Nike Swoosh brings heritage style to a streamlined sneaker boasting a monochromatic design and a Waffle-textured sole for ultimate traction.', 
        'category': 'walking', 
        'price': 88.0, 
        'gender': 'Women', 
        'image_url': 'https://i.imgur.com/PDTB1G9.png'
    }, 
    {
        'name': 'Nike Air Max 270', 
        'description': "Nike's first lifestyle Air Max brings you style, comfort and big attitude in the Nike Air Max 270. The design draws inspiration from Air Max icons, showcasing Nike's greatest innovation with its large window and fresh array of colors.", 
        'category': 'walking', 
        'price': 160.0, 
        'gender': 'Women', 
        'image_url': 'https://i.imgur.com/t1skpSg.png'
    },
    {
        'name': 'Nike Dunk Low', 
        'description': "Created for the hardwood but taken to the streets, this '80s basketball icon returns with classic details and throwback hoops flair. Synthetic leather overlays help the Nike Dunk channel vintage style while its padded, low-cut collar lets you take your game anywhere—in comfort.", 
        'category': 'walking', 
        'price': 79.0, 
        'gender': 'Women', 
        'image_url': 'https://i.imgur.com/KvPrxLH.png'
    }, 
    {
        'name': 'Nike Dunk High', 
        'description': "Created for the hardwood but taken to the streets, the '80s b-ball icon returns with crisp leather and retro colors. The classic hoops design channels '80s vintage back onto the streets while the padded, high-top collar adds an old-school look rooted to comfort.", 
        'category': 'walking', 
        'price': 92.0, 
        'gender': 'Women', 
        'image_url': 'https://i.imgur.com/v4POfY5.png'
    }, 
    {
        'name': 'Jordan Stadium 90', 
        'description': 'Evolve your game. The Stadium 90 takes elements from the greats and forges them into something entirely unique. Combining iconic design elements from the AJ1 and AJ5, this is a new classic with an emphasis on comfort, durability and stability.', 
        'category': 'gym exercise', 
        'price': 120.0, 
        'gender': 'Women', 
        'image_url': 'https://i.imgur.com/Wju9xAc.png'
    }, 
    {
        'name': 'Nike Zegama 2', 
        'description': 'Up the mountain, through the woods, to the top of the trail you can go. Equipped with an ultra-responsive ZoomX foam midsole, the Zegama 2 is designed to conquer steep ridges, jagged rocks and races from trailhead to tip. Optimal cushioning complements a rugged outsole made for your trail running journey.', 
        'category': 'trail walking', 
        'price': 180.0, 
        'gender': 'Women', 
        'image_url': 'https://i.imgur.com/nxMgHP0.png'
    }, 
    {
        'name': 'Nike Pegasus Trail 4 GORE-TEX', 
        'description': "The Nike Pegasus Trail 4 GORE-TEX is made for those moments when you don't want to turn back, no matter what. Feel confident even in the most unforeseen weather conditions with waterproof GORE-TEX keeping you dry, so you can run harder for longer and take your wet run from the road to the trail without breaking stride. A waterproof layer paired with a higher ankle gaiter gives you extra coverage so you stay dry. This special design takes you to trail #440 in the Pacific Northwest, one of nature's playground's more distinctive gems, as part of our ongoing #IYKYK series.", 
        'category': 'trail walking', 
        'price': 137.0, 
        'gender': 'Women', 
        'image_url': 'https://i.imgur.com/ID7KJFl.png'
    }, 
    {
        'name': 'Nike Ultrafly', 
        'description': "Manifest your mountainous best, when the trail ahead is skiddy and uncertain. Our all-new championship trail racing shoe melds our best speed components from the running world with what you need to plant your flag first at the finish line. It offers peak performance, sleek speed and endurance for those who want to summit nature's playground.", 
        'category': 'trail walking', 
        'price': 260.0, 
        'gender': 'Women', 
        'image_url': 'https://i.imgur.com/XwnjQVu.png'
    }, 
    {
        'name': 'Nike Juniper Trail 2 GORE-TEX', 
        'description': 'The Juniper Trail 2 has waterproof GORE-TEX on the upper, grippy traction and a soft, cushiony midsole. It helps keep your toes dry when the trail conditions are splashy. This special design is part of our ongoing #IYKYK series. It traverses the Pyrenees mountains via the GR 11, using the coastal lighthouses as your guide from the Mediterranean Sea to the Cantabrian Sea.', 
        'category': 'trail walking', 
        'price': 130.0, 
        'gender': 'Men', 
        'image_url': 'https://i.imgur.com/ZpeiKUz.png'
    }
]

SEED_ORDERS = [
    {
        "order_number": "3620",
        "order_images": "https://i.imgur.com/qFDbRIY.png"
    },
    {
        "order_number": "4620",
        "order_images": "https://i.imgur.com/LubKjJ9.jpeg"
    },
    {
        "order_number": "5620",
        "order_images": "https://i.imgur.com/HEMXH3o.png"
    },
    {
        "order_number": "6620",
        "order_images": "https://i.imgur.com/uBqBIAm.png"
    },
    {
        "order_number": "7620",
        "order_images": "https://i.imgur.com/rtAHFey.png"
    },
    {
        "order_number": "8620",
        "order_images": "https://i.imgur.com/DNLZWCt.png"
    },
    {
        "order_number": "9620",
        "order_images": "https://i.imgur.com/u0OvKHZ.png"
    }
]

# Check if the tables are empty
async def is_table_empty(db: Session, table):
    """Check if a given table is empty."""
    count = db.query(func.count()).select_from(table).scalar()
    return count == 0

# Seed items into the database
async def seed_items(db: Session):
    """Seed the database with items if it's empty."""
    if await is_table_empty(db, Item):
        for item_data in SEED_ITEMS:
            item = ItemCreate(**item_data)  # Convert dictionary to Pydantic model
            await create_item(item, db)
            print(f"Item added: {item.name}")
    else:
        print("Items table is not empty, skipping item seeding.")

# Seed orders into the database
async def seed_orders(db: Session):
    """Seed the database with orders if it's empty."""
    if await is_table_empty(db, Order):
        for order_data in SEED_ORDERS:
            order = OrderCreate(**order_data)  # Convert dictionary to Pydantic model
            await create_order(order, db)
            print(f"Order added: {order.order_number}")
    else:
        print("Orders table is not empty, skipping order seeding.")