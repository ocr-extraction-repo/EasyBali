from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
import tempfile
import os
from datetime import datetime
from app.services.Invoice_bucket import s3_service

async def generate_and_upload_invoice(order_data: dict, payment_data: dict) -> dict:
    try:
        # Prepare invoice data
        invoice_data = {
            "receipt_no": f"INV-{order_data['order_number']}",
            "payment_date": payment_data.get('paid_at', datetime.now()).strftime('%Y-%m-%d'),
            "name": order_data.get('customer_name', 'Customer'),
            "phone": order_data.get('sender_id', ''),
            "email": order_data.get('customer_email', ''),
            "items": [
                {
                    "description": order_data['service_name'],
                    "amount": order_data['price']
                }
            ],
            "total": order_data['price'],
            "payment_method": payment_data.get('payment_method', 'Online Payment'),
            "transfer_date": payment_data.get('paid_at', datetime.now()).strftime('%Y-%m-%d'),
            "transfer_time": payment_data.get('paid_at', datetime.now()).strftime('%H:%M'),
        }
        
        # Generate PDF in temporary file
        with tempfile.NamedTemporaryFile(suffix='.pdf', delete=False) as temp_file:
            temp_path = temp_file.name
            
        # Generate the PDF
        generate_invoice_pdf(invoice_data, temp_path)
        
        # Upload to S3
        object_key = f"invoices/{order_data['order_number']}/invoice_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
        upload_result = await s3_service.upload_file_async(temp_path, object_key)
        
        # Clean up temporary file
        os.unlink(temp_path)
        
        if upload_result['success']:
            return {
                'success': True,
                'download_url': upload_result['download_url'],
                'invoice_data': invoice_data
            }
        else:
            return upload_result
            
    except Exception as e:
        print(f"Invoice generation error: {e}")
        return {'success': False, 'error': str(e)}

def generate_invoice_pdf(data, output_filename="invoice.pdf"):
    background = "EB Invoice (2).jpg"
    width, height = A4

    c = canvas.Canvas(output_filename, pagesize=A4)
    c.drawImage(background, 0, 0, width=width, height=height)

    c.setFont("Helvetica", 14)
    c.drawString(420, 648, f"{data['receipt_no']}")
    c.drawString(420, 628, f"{data['payment_date']}")

    c.setFont("Helvetica", 10)
    c.drawString(365, 593, f"{data['name']}")
    c.drawString(365, 580, f"{data['phone']}")
    c.drawString(365, 567, f"{data['email']}")

    c.setFont("Helvetica", 14)
    y = 430
    for i, item in enumerate(data['items'], start=1):
        c.drawString(75, y, str(i))                     
        c.drawString(100, y, item['description'])               
        c.drawRightString(480, y, item['amount'])              
        y -= 27
    
    c.drawRightString(480, y, data['total'])
    c.setFont("Helvetica", 14)
    c.drawString(190, 316, f"{data['payment_method']}")

    c.setFont("Helvetica", 12)
    c.drawString(135, 252, f"{data['transfer_date']}")
    c.drawString(135, 237, f"{data['transfer_time']}")

    c.save()
    print(f"✅ Invoice saved as {output_filename}")