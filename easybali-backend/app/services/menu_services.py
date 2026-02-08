import pandas as pd
from app.services.google_sheets import get_workbook
from app.utils.data_processing import clean_dataframe
import threading
from datetime import datetime

# Google Sheet configurations
SHEET_ID = "1tuGBnQFjDntJQglofA17uHhiyekkVyDoSInErbwfR24"
workbook = get_workbook(SHEET_ID)

# Cache for storing data
cache = {
    "menu_df": None,
    "services_df": None,
    "design_df": None,
    "last_updated": None,
    "main_menu_design":None,
    "service_providers":None
}

# Refresh thread control
should_stop = False
refresh_thread = None

def load_data_into_cache():
    """Loads data from Google Sheets into cache."""
    print(f"Refreshing data at {datetime.now()}...")
    try:
        # Load menu data
        menu_structure = workbook.get_worksheet(4)
        cache["menu_df"] = clean_dataframe(menu_structure.get_all_values())
        
        # Load services data
        services_overview = workbook.get_worksheet(0)
        cache["df"] = (services_overview.get_all_values())
        columns = cache["df"][0]
        rows = cache["df"][1:]
        cache['services_df'] = pd.DataFrame(rows, columns=columns)

        price_distribution = workbook.get_worksheet(3)
        cache["df3"] = (price_distribution.get_all_values())
        columns = cache["df3"][0]
        rows = cache["df3"][1:]
        cache['price_distribution'] = pd.DataFrame(rows, columns=columns)

        service_providers = workbook.get_worksheet(2)
        cache["df1"] = (service_providers.get_all_values())
        columns = cache["df1"][0]
        rows = cache["df1"][1:]
        cache['service_providers'] = pd.DataFrame(rows, columns=columns)

        villas = workbook.get_worksheet(5)
        cache["df2"] = (villas.get_all_values())
        columns = cache["df2"][0]
        rows = cache["df2"][1:]
        cache['villas_data'] = pd.DataFrame(rows, columns=columns)

        # Load design data
        services_design = workbook.get_worksheet(1)
        cache["design_df"] = clean_dataframe(services_design.get_all_values())

        main_menu = workbook.get_worksheet(6)
        cache["main_menu_design"] = clean_dataframe(main_menu.get_all_values())
        
        
        # Update timestamp
        cache["last_updated"] = datetime.now()
    except Exception as e:
        print(f"Error while refreshing data: {e}")

def schedule_data_refresh():
    """Runs data refresh at regular intervals."""
    global should_stop
    while not should_stop:
        load_data_into_cache()
        for _ in range(60):
            if should_stop:
                break
            threading.Event().wait(1)

def start_cache_refresh():
    """Starts the background thread for refreshing data."""
    global refresh_thread
    refresh_thread = threading.Thread(target=schedule_data_refresh, daemon=True)
    refresh_thread.start()

def stop_cache_refresh():
    """Stops the background thread for refreshing data."""
    global should_stop, refresh_thread
    should_stop = True
    if refresh_thread:
        refresh_thread.join()
        refresh_thread = None

async def get_main_menu():
    if cache["menu_df"] is None:
        raise ValueError("Data not loaded")
    return cache["menu_df"]['Main Menu'].dropna().unique().tolist()


async def get_main_menu_design():
    if cache["main_menu_design"] is None:
        raise ValueError("Data not loaded")
    return cache["main_menu_design"]


async def get_service_providers():
    if cache["service_providers"] is None:
        raise ValueError("Data not loaded")
    return cache["service_providers"]

async def get_villa_data():
    if cache["villas_data"] is None:
        raise ValueError("Data not loaded")
    return cache["villas_data"]


async def get_price_distribution():
    if cache["price_distribution"] is None:
        raise ValueError("Data not loaded")
    return cache["price_distribution"]


async def get_service_overview():
    if cache["services_df"] is None:
        raise ValueError("Data not loaded")
    return cache["services_df"]



async def get_categories():
    if cache["design_df"] is None:
        raise ValueError("Data not loaded")
    categories = cache["design_df"].drop_duplicates(subset=["Category"])[
        ["Category", "Category Description WA"]
    ]

    result = []

    for _, category_row in categories.iterrows():
        category_name = category_row["Category"]
        category_description = category_row["Category Description WA"]

        subcategories = cache["design_df"][
            cache["design_df"]["Category"] == category_name
        ][["Sub-category", "Sub-category Description WA"]].drop_duplicates()

        section_rows = [
            {
                "id": row["Sub-category"].lower().replace(" ", "_"),
                "service_title": row["Sub-category"],
                "service_description": row["Sub-category Description WA"]
            }
            for _, row in subcategories.iterrows()
        ]
        result.append(
            {
                "title": category_name,  # Category name as header
                "description": category_description,  # Category description as body
                "sections": section_rows  # Sections contain subcategories
            }
        )

    return result



async def get_categories_only():
    if cache["design_df"] is None:
        raise ValueError("Data not loaded")
    
    categories = cache["design_df"].drop_duplicates(subset=["Category"])[
        ["Category", "Category ID", "Category Description WA"]
    ]

    result = []

    for _, category_row in categories.iterrows():
        category_id = category_row["Category ID"] 
        category_name = category_row["Category"]
        category_description = category_row["Category Description WA"]

        result.append(
            {
                "id": category_id,
                "title": category_name,
                "description": category_description
            }
        )

    return result

async def get_category_sections(category_title: str):
    if cache["design_df"] is None:
        raise ValueError("Data not loaded")
    if category_title not in cache["design_df"]["Category"].values:
        raise ValueError(f"Category '{category_title}' not found")
    subcategories = cache["design_df"][
        cache["design_df"]["Category"] == category_title
    ][["Sub-category", "Sub-category Description WA"]].drop_duplicates()

    section_rows = []

    for _, row in subcategories.iterrows():
        section_rows.append(
            {
                "id": row["Sub-category"].lower().replace(" ", "_"),
                "title": row["Sub-category"],
                "description": row["Sub-category Description WA"]
            }
        )
    result =  section_rows
    return result


async def get_sub_menu(menu_location: str):
    if cache.get("main_menu_design") is None:
        raise ValueError("Main menu design data not loaded")
    
    df = cache["main_menu_design"]
    filtered_df = df[df["Menu Location"] == menu_location]
    if filtered_df.empty:
        raise ValueError(f"Menu location '{menu_location}' not found")
    
    # Get the main title and description from the row where Title matches Menu Location
    main_row = df[df["Title"] == menu_location]
    if main_row.empty:
        main_title = menu_location
        main_description = ""
    else:
        main_title = main_row.iloc[0]["Title"]
        main_description = main_row.iloc[0].get("Description WA", "")
    
    items = [
        {
            "category": row["Title"],
            "description": row["Description"],
            "picture": row["Picture"],
            "button": row["Button"]
        }
        for _, row in filtered_df.drop_duplicates(subset=["Title"]).iterrows()
    ]
    
    return {
        "main_title": main_title,
        "main_description": main_description,
        "items": items
    }


async def get_restaurants_menu(menu_location: str):
    if cache.get("main_menu_design") is None:
        raise ValueError("Main menu design data not loaded")
    
    df = cache["main_menu_design"]
    filtered_df = df[df["Menu Location"] == menu_location]
    if filtered_df.empty:
        raise ValueError(f"Menu location '{menu_location}' not found")
    return [
        {
            "category": row["Title"],
            "description": row["Description"],
            "picture": row["Picture"],
            "button": row["Button"],
            "Description":row["Description WA"]
        }
        for _, row in filtered_df.drop_duplicates(subset=["Title"]).iterrows()
    ]



async def get_order_service_sub_menu(main_menu: str):
    if main_menu == "Order Services":
        if cache["design_df"] is None:
            raise ValueError("Services data not loaded")

        # Build JSON objects from design_df for "Order Services"
        return [
            {
                "category": row["Category"],
                "description": row["Category Description"],
                "picture": row["Category Picture"],
                "button": row["Category Button"]
            }
            for _, row in cache["design_df"].drop_duplicates(subset=["Category"]).iterrows()
        ]
    if cache["menu_df"] is None:
        raise ValueError("Menu data not loaded")
    
    filtered_df = cache["menu_df"][cache["menu_df"]['Main Menu'] == main_menu]
    if filtered_df.empty:
        raise ValueError("Main menu not found")
    return [
        {
            "category": row["Category"],
            "description": row["Category Description"],
            "picture": row["Category Picture"],
            "button": row["Category Button"]
        }
        for _, row in filtered_df.drop_duplicates(subset=["Category"]).iterrows()
    ]

async def get_sub_sub_menu(main_menu: str, sub_menu: str):
    if cache["menu_df"] is None:
        raise ValueError("Menu data not loaded")
    filtered_df = cache["menu_df"][
        (cache["menu_df"]['Main Menu'] == main_menu) & (cache["menu_df"]['Category'] == sub_menu)
    ]
    if filtered_df.empty:
        raise ValueError("Sub-menu not found")
    return filtered_df['Sub-category'].dropna().tolist()


async def get_sub_category(category: str):
    if cache["design_df"] is None:
        raise ValueError("Services data not loaded")
    filtered_df = cache["design_df"][cache["design_df"]['Category'] == category]
    if filtered_df.empty:
        raise ValueError("Category not found")
    return [
        {
            "subcategory": row["Sub-category"],
            "description": row["Sub-category Description"],
            "picture": row["Sub-category Picture"],
            "button": row["Sub-category Button"]
        }
        for _, row in filtered_df.drop_duplicates(subset=["Sub-category"]).iterrows()
    ]


async def get_service_items(subcategory: str):
    if cache["services_df"]is None:
         raise ValueError("Services data not loaded")
    filtered_df = cache["services_df"][cache["services_df"]['Sub-category'] == subcategory]
    if filtered_df.empty:
        raise ValueError("Category not found")
    return [
        {
            "service_item": row["Service Item"],
            "description": row["Service Item Description"],
            "picture": row["Image URL"],
            "button": row["Final Price (Service Item Button)"],
        }
        for _, row in filtered_df.drop_duplicates(subset=["Service Item"]).iterrows()
    ]


async def get_service_base_price(service_name: str) -> str:
    if cache["services_df"] is None:
        raise ValueError("Services data not loaded")
    filtered_df = cache["services_df"][cache["services_df"]['Service Item'] == service_name]
    
    if filtered_df.empty:
        print(f"Warning: Service '{service_name}' not found in services data")
        return "0"
    price = filtered_df.iloc[0]["Final Price (Service Item Button)"]
    if pd.isna(price):
        return "0"
    return str(price)

async def get_service_items_for_whatsapp(subcategory_title: str):
    if cache["services_df"]is None:
         raise ValueError("Services data not loaded")
    filtered_df = cache["services_df"][cache["services_df"]['Sub-category'] == subcategory_title]
    if filtered_df.empty:
        raise ValueError("Category not found")
    return [
        {
            "title": row["Service Item"],
            "description": row["Service Item Description"],
            "button": row["Final Price (Service Item Button)"],
        }
        for _, row in filtered_df.drop_duplicates(subset=["Service Item"]).iterrows()
    ]




async def get_service_provider_by_whatsapp(whatsapp_number: str):
    try:
        providers_df = await get_service_providers()
        clean_whatsapp = whatsapp_number.lstrip('+')
        matching_provider = providers_df[
            (providers_df["WhatsApp"] == whatsapp_number) |
            (providers_df["WhatsApp"] == clean_whatsapp) |
            (providers_df["WhatsApp"] == f"+{clean_whatsapp}")
        ]
        
        if matching_provider.empty:
            return None
        return matching_provider.iloc[0]["Number"]
        
    except Exception as e:
        print(f"Error retrieving service provider: {e}")
        return None
    


async def get_villa_code_by_name(villa_name: str):
    if cache["villas_data"] is None:
        raise ValueError("Villa data not loaded")
    
    try:
        villas_df = cache["villas_data"]
        
        # Search for exact match first (case-insensitive)
        matching_villa = villas_df[
            villas_df["Name of Villa"].str.lower() == villa_name.lower()
        ]
        
        # If no exact match, try partial match
        if matching_villa.empty:
            matching_villa = villas_df[
                villas_df["Name of Villa"].str.contains(villa_name, case=False, na=False)
            ]
        
        if matching_villa.empty:
            return None
            
        # Return the villa code (Number column)
        return matching_villa.iloc[0]["Number"]
        
    except Exception as e:
        print(f"Error retrieving villa code: {e}")
        return None