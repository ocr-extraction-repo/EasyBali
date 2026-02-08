from fastapi import APIRouter, HTTPException
from app.services.menu_services import get_main_menu, get_sub_menu, load_data_into_cache, cache, get_sub_category, get_service_items, get_service_overview, get_service_providers, get_order_service_sub_menu, get_restaurants_menu, get_villa_data, get_price_distribution
from app.models.villa_data import VillaData
from app.services.google_sheets import get_workbook
from app.utils.qrutils import generate_and_upload_qrcode
from app.utils.bucket import upload_to_s3
from fastapi import Form, File, UploadFile
from urllib.parse import unquote

# Google Sheet configurations
SHEET_ID = "1tuGBnQFjDntJQglofA17uHhiyekkVyDoSInErbwfR24"
workbook = get_workbook(SHEET_ID)

router = APIRouter(prefix="/menu", tags=["Menu"])

@router.get("/main", summary="Get main menu items")
async def main_menu():
    return {"data": await get_main_menu()}

@router.get("/sub/{main_menu}", summary="Get sub-menu items for a main menu")
async def sub_menu(main_menu: str):
    if main_menu == "Order Services":
        try:
            return {"data": await get_order_service_sub_menu(main_menu)}
        except ValueError as e:
            raise HTTPException(status_code=404, detail=str(e))
    elif main_menu == "Restaurants" or main_menu == "For the 'gram":
        try:
            return {"data": await get_restaurants_menu(main_menu)}
        except ValueError as e:
            raise HTTPException(status_code=404, detail=str(e))
    else:
        try:
            return {"data": await get_sub_menu(main_menu)}
        except ValueError as e:
            raise HTTPException(status_code=404, detail=str(e))

@router.get("/sub-category/{category}", summary="Get sub-category items for a category")
async def sub_category(category: str):
    try:
        return {"data": await get_sub_category(category)}
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    
@router.get("/service-items/{subcategory}", summary="Get service items for a sub-category")
async def sub_category(subcategory: str):
    try:
        return {"data": await get_service_items(subcategory)}
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    
@router.get("/service/{service_item_name}")
async def get_whatsapp_for_service_item(service_item_name: str):
    design_df = await get_service_overview()
    providers_df = await get_service_providers()
    
    matching_items = design_df[design_df["Service Item"].str.contains(service_item_name, case=False, na=False)]
    
    if matching_items.empty:
        raise HTTPException(status_code=404, detail="Service item not found")
    provider_ids_nested = matching_items["Service Providers"].apply(lambda x: [p.strip() for p in x.split(",")])
    
    flattened_provider_ids = [provider_id for sublist in provider_ids_nested for provider_id in sublist]
    
    unique_provider_ids = list(set(flattened_provider_ids))
    matching_providers = providers_df[providers_df["Number"].isin(unique_provider_ids)]
    
    if matching_providers.empty:
        raise HTTPException(status_code=404, detail="No service providers found for this service item")
    whatsapp_numbers = matching_providers["WhatsApp"].tolist()
    return whatsapp_numbers



    


@router.post("/refresh", summary="Refresh Google Sheets data")
async def refresh_data():
    try:
        load_data_into_cache()
        return {"message": "Data refreshed successfully", "last_updated": cache["last_updated"]}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to refresh data: {e}")


@router.post("/add-villa-data")
async def add_villa_data(
    name_of_villa: str = Form(...),
    address: str = Form(...),
    google_maps_link: str = Form(...),
    directions: str = Form(...),
    entrance_picture: UploadFile = File(...),
    location: str = Form(...),
    contact_vm: str = Form(...),
    contact_mt: str = Form(...),
    passport_collection: str = Form(...),
    number_of_bdr: str = Form(...),
    website_url: str = Form(""),
    whatsapp_url: str = Form(""),
    messenger_url: str = Form(""),
    instagram_url: str = Form("")
):
    try:
        # Upload entrance picture to S3
        entrance_picture_url = await upload_to_s3(entrance_picture)

        # Prepare data for QR code generation
        qr_data = {
            "name_of_villa": name_of_villa,
            "address": address,
            "google_maps_link": google_maps_link,
            "directions": directions,
            "entrance_picture": entrance_picture_url,
            "location": location,
            "contact_vm": contact_vm,
            "contact_mt": contact_mt,
            "passport_collection": passport_collection,
            "number_of_bdr": number_of_bdr,
            "website_url": website_url,
            "whatsapp_url": whatsapp_url,
            "messenger_url": messenger_url,
            "instagram_url": instagram_url,
        }

        # Generate and upload the QR code
        qr_code_url = await generate_and_upload_qrcode(qr_data)

        # Access worksheet (Google Sheets)
        worksheet = workbook.get_worksheet(3)  # Adjust this index based on your sheet structure

        # Find the next available row number
        existing_rows = len(worksheet.get_all_values())
        next_number = f"V{existing_rows}"

        # Prepare row data
        row_data = [
            next_number,
            name_of_villa,
            address,
            google_maps_link,
            directions,
            entrance_picture_url,
            location,
            contact_vm,
            contact_mt,
            passport_collection,
            number_of_bdr,
            website_url,
            whatsapp_url,
            messenger_url,
            instagram_url,
            qr_code_url
        ]

        # Append data to Google Sheets
        worksheet.append_row(row_data, value_input_option="USER_ENTERED")

        return {"status": "success", "message": "Villa data added successfully!"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error adding villa data: {str(e)}")



# Routes for Payment Distribution and accocunt details for SP and villa

@router.get("/service-provider-bank")
async def get_bank_details_for_provider(provider_code: str):
    providers_df = await get_service_providers()
    matching_provider = providers_df[providers_df["Number"].str.contains(provider_code, case=False, na=False)]
    
    if matching_provider.empty:
        raise HTTPException(status_code=404, detail=f"Service provider '{provider_code}' not found")
    
    # Extract the first matching provider's bank details
    provider_row = matching_provider.iloc[0]
    
    bank_details = {
        "provider_code": provider_code,
        "bank_code": provider_row.get("Bank", ""),
        "account_number": provider_row.get("Account Number", ""),
        "account_holder_name": provider_row.get("Name", ""),
        "swift_code": provider_row.get("Swift Code", "")
    }
    
    return bank_details


@router.get("/villa-bank")
async def get_bank_details_for_villa(provider_code: str):
    villa_df = await get_villa_data()
    matching_villa = villa_df[villa_df["Number"].str.contains(provider_code, case=False, na=False)]
    
    if matching_villa.empty:
        raise HTTPException(status_code=404, detail=f"Villa '{provider_code}' not found")
    
    # Extract the first matching provider's bank details
    villa_row = matching_villa.iloc[0]
    
    bank_details = {
        "provider_code": provider_code,
        "bank_code": villa_row.get("Bank", ""),
        "account_number": villa_row.get("Account Number", ""),
        "account_holder_name": villa_row.get("Name", ""),
        "swift_code": villa_row.get("Swift Code", "")
    }
    
    return bank_details


@router.get("/price_distribution")
async def get_price_distribution_details(service_item: str):
    try:
        price_df = await get_price_distribution()

        available_services = price_df["Service Item"].unique()
        
        exact_match = price_df[price_df["Service Item"].str.lower() == service_item.lower()]
        if not exact_match.empty:
            price_row = exact_match.iloc[0]
        else:
            # Strategy 2: Contains match (case-insensitive)
            contains_match = price_df[price_df["Service Item"].str.contains(service_item, case=False, na=False)]
            if not contains_match.empty:
                price_row = contains_match.iloc[0]
            else:
                # Strategy 3: Try partial matching with key terms
                key_terms = service_item.split()
                
                partial_matches = price_df
                for term in key_terms:
                    if len(term) > 2:  # Only use meaningful terms
                        partial_matches = partial_matches[partial_matches["Service Item"].str.contains(term, case=False, na=False)]
                
                if not partial_matches.empty:
                    price_row = partial_matches.iloc[0]
                else:
                    raise HTTPException(
                        status_code=404, 
                        detail=f"Service '{service_item}' not found. Available services: {available_services.tolist()}"
                    )
        
        # Extract and return the data
        price_details = {
            "service_item": service_item,
            "matched_service": price_row.get("Service Item", ""),
            "service_provider_price": price_row.get("Vendor Price", ""),
            "villa_price": price_row.get("Villa Comm", ""),
        }
        return price_details
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")