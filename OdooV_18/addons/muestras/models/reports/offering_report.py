
import os 
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader
from reportlab.lib import colors
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.platypus import Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet,ParagraphStyle
from reportlab.lib.colors import black,white
from io import BytesIO
from odoo.http import request 
from odoo import models, api

class PDF_Generator(models.Model):
    _name="muestras.generate_pdf"


    def _pdf_generating(self):

        current_dir=os.path.dirname(os.path.abspath(__file__))

        pdfmetrics.registerFont(TTFont('Lato',os.path.join(current_dir,'Lato-Regular.ttf') ))
        pdfmetrics.registerFont(TTFont('Arial-Bold', os.path.join(current_dir,'ARIALBD.ttf') ))
        pdfmetrics.registerFont(TTFont('Lato-Bold-Italic', os.path.join(current_dir,'Lato-BoldItalic.ttf')))
        pdfmetrics.registerFont(TTFont('Lato-Bold', os.path.join(current_dir,'Lato-Bold.ttf')))
        title_centered = ParagraphStyle(
            name='Centrado',
            alignment=1,  # 0=izquierda, 1=centro, 2=derecha, 4=justificado
            fontName='Arial-Bold',
            fontSize=36,
            textColor='#ccc1af',  
            leading=36
        )

        request_centered = ParagraphStyle(
            name='Centrado_3',
            alignment=1,  # 0=izquierda, 1=centro, 2=derecha, 4=justificado
            fontName='Arial-Bold',
            fontSize=32,
            textColor=white,  
            leading=32
        )

        mail_centered = ParagraphStyle(
            name='Centrado_5',
            alignment=1,  # 0=izquierda, 1=centro, 2=derecha, 4=justificado
            fontName='Arial-Bold',
            fontSize=20,
            textColor=white,  
            leading=20
        )
        bold_end_text = ParagraphStyle(
            name='Centrado_Italico',
            alignment=1,  # 0=izquierda, 1=centro, 2=derecha, 4=justificado
            fontName='Lato-Bold-Italic',
            fontSize=16,
            textColor='white', 
            leading=16
        )

        lato_text = ParagraphStyle(
            name='Centrado_Lato',
            alignment=1,  # 0=izquierda, 1=centro, 2=derecha, 4=justificado
            fontName='Lato',
            fontSize=16,
            textColor='white',
            leading=16
        )

        buffer = BytesIO()  
        page_x=612
        page_y=1000.08
        custom_size = (page_x, page_y)    
        c = canvas.Canvas(buffer, pagesize=custom_size)
        width, height = custom_size
        

        imagen_fondo = ImageReader(os.path.join(current_dir,"offering_background.png"))
        c.drawImage(imagen_fondo, 0, 0, width=width, height=height)

        styles = getSampleStyleSheet()
        style_normal = styles['Normal']

            # Modificar el estilo para justificar el texto
        style_justificado = ParagraphStyle(
            name='Justificado',
            parent=style_normal,
            alignment=4  # 4 es el código para justificar
        )



        # --------- Datos de la tabla ---------

        data = {
            "commercial_user":"Angelica Garrido",
            "customer": "MvsM GmbH",
            "offering_seq":"OFF-0001",
            "date": "15/5/2025",
            "coffees":[
                {
                "sku":"MC0015",
                "main_category":"Farm Selection Microlots",
                "Origin":"Risaralda",
                "Process":"Termo Shock Washed",
                "Variety":"Variedad",
                "sca":"89.7",
                "fob_us":"NYC+0.8",
                "fob_eu":"9,67",
                "spot_us":"8l,7",
                "spot_eu":"8,89",
                "macroprofile":"Floral, Citrus, Aromatic",
                "aval_35":"1000",
            },
            {
                "sku": "MC0016",
                # "main_category": "Farm Selection Microlots",
                "main_category":"Everyday Blends",
                "Origin": "Antioquia",
                "Process": "Natural",
                "Variety": "Yellow Bourbon",
                "sca": "88.3",
                "fob_us": "NYC+1.0",
                "fob_eu": "10,20",
                "spot_us": "9,0",
                "spot_eu": "9,5",
                "macroprofile": "Fruity",
                "aval_35": "500"
            },
            {
                "sku": "MC0039",
                # "main_category": "Farm Selection Microlots",
                "main_category":"Everyday Blends",
                "Origin": "Nariño",
                "Process": "Natural",
                "Variety": "Catuai",
                "sca": "88.3",
                "fob_us": "NYC+1.0",
                "fob_eu": "10,20",
                "spot_us": "9,0",
                "spot_eu": "9,5",
                "macroprofile": "Fruity",
                "aval_35": "500"
            }
            ]
        }
        datos = [
            ["Nombre", "Edad", "Ciudad"],
            ["Ana", "28", "Bogotá"],
            ["Luis", "34", "Medellín"],
            ["María", "22", "Cali"],
        ]

        categories_data={
            'categories':[
                {
                "title":"Everyday Blends",
                "description":"The Everyday Blends category offers high-volume, quality consistent coffees that are reliable and accessible. These blends are crafted by combining lots from various farms within a specific region, ensuring an even and balanced cup profile. Ideal for roasters seeking steady supply with quality flavor profiles, they are perfect for daily use and reliable for consistent quality year-round.",
                "image":"Everyday_Blends.png",
                "color":"#f6f0e2",
                },
                {
                "title":"Farm Selection Microlots",
                "description":"Small batches of specialty coffee with traceability down to the individual farm. With scores of 85+ points, these coffees showcase distinct flavor profiles and refined characteristics, celebrating the dedication of each grower. Perfect for roasters looking to highlight the craftsmanship of a specific region and farm, these lots offer an elevated experience without the premium pricing of exotic varieties.",
                "image":"Farm_Select.png",
                "color":"#272735",
                },
                {
                "title":"Avant-Grade Experimentals",
                "description":"Features coffees processed with groundbreaking techniques, including cultured bacteria inoculation and controlled fermentation environments, both during washing and drying stages. These experimental methods yield distinct and unconventional flavor profiles, catering to adventurous buyers who seek innovation and a deeper exploration of coffee’s sensory possibilities. ",
                "image":"Farm_Select.png",
                "color":"#6d5448",
                },
                {
                "title":"Decaf Collection",
                "description":"A diverse decaf collection that preserves the vibrant flavors of our specialty coffees. Using the Sugar Cane Decaf Process (EA)—a natural method with locally sourced sugar cane—we gently remove caffeine without high pressure or extreme heat, keeping the coffee’s rich taste. Whether you enjoy the sweetness of a washed decaf or the complexity of a honey process, our Decaf Collection delivers a full-flavored, caffeine-free experience.",
                "image":"Farm_Select.png",
                "color":"#e0c7b6",
                },
                {
                "title":"Rare Exotic",
                "description":"Are small-lot single origin coffees from unique and rare varieties like Java, SL28, Geisha, Sidra, and many others. Grown in carefully curated microclimates, these coffees offer unparalleled complexity and are prized for their unique flavors and exceptional cup scores (86+ points). Rare Exotics are aimed at roasters looking for exclusive, standout coffees that push the boundaries of traditional specialty coffee.",
                "image":"Farm_Select.png",
                "color":"#4c5f66",
                }
            ]
        }

        pos_x=30
        pos_y=836
        sep_section=50

        categories_unique=set()
        for coffee in data['coffees']:
            categories_unique.add(coffee['main_category'])

        for category in categories_unique:
            cat_data={}
            coffees_print={
                'coffees':[]
            }
            for coffee in data['coffees']:
                if coffee['main_category']==category:
                    coffees_print['coffees'].append(coffee)
            
            for cat in categories_data['categories']:
                if cat['title']==category:
                    cat_data=cat
            act_x,act_y=self.category_print(cat_data,coffees_print,c,styles,pos_x,pos_y,page_x,page_y,current_dir)
            pos_x=act_x
            pos_y=act_y-sep_section
            print(category)
            print(coffees_print)
            print(cat_data)

        c.showPage()
        c.setFillColor(black)
        c.rect(0, 0, width, height, fill=1, stroke=0)


        title_final = Paragraph("Important Information and Details", title_centered)
        x_title,y_title=title_final.wrap(400, 500)  # Ajustar el texto al tamaño del cuadro
        title_final.drawOn(c, (width-x_title)/2, 900-y_title)  # Dibujar el párrafo en la posición indicada

        sep_h2_h3=20
        
        pricing_title = Paragraph ("Pricing and Availability Validity:",bold_end_text)
        pt_x,pt_y=pricing_title.wrap(400,500)
        pricing_title.drawOn(c,(width-pt_x)/2,900-y_title-pt_y-50)

        tx1 = Paragraph ("The prices and availability in this offering are valid from ",lato_text)
        tx1_x,tx1_y=tx1.wrap(400,500)
        tx1.drawOn(c,(width-tx1_x)/2,900-y_title-pt_y-50-tx1_y-sep_h2_h3)

        tx2 = Paragraph ("<u>February 17, 2025, to February 24, 2025.</u>",lato_text)
        tx2_x,tx2_y=tx2.wrap(400,500)
        tx2.drawOn(c,(width-tx2_x)/2,900-y_title-pt_y-50-tx1_y-sep_h2_h3-tx2_y)

        tx3 = Paragraph ("Standard Packaging Included:",bold_end_text)
        tx3_x,tx3_y=tx3.wrap(400,500)
        tx3.drawOn(c,(width-tx3_x)/2,900-y_title-pt_y-50-tx1_y-sep_h2_h3-tx2_y-tx3_y-sep_h2_h3)

        text_4="Prices include packaging in fique sacks with multilayer bags and standard markings for <b><u>35 kg or 70 kg </u></b> sacks. If you require a different type of sack, bag, or custom markings, this may affect the price and delivery times."
        tx4 = Paragraph (text_4,lato_text)
        tx4_x,tx4_y=tx4.wrap(450,500)
        tx4.drawOn(c,(width-tx4_x)/2,900-y_title-pt_y-50-tx1_y-sep_h2_h3-tx2_y-tx3_y-sep_h2_h3-sep_h2_h3-tx4_y)

        tx5 = Paragraph ("Purchase Conditions:",bold_end_text)
        tx5_x,tx5_y=tx5.wrap(400,500)
        tx5.drawOn(c,(width-tx5_x)/2,900-y_title-pt_y-50-tx1_y-sep_h2_h3-tx2_y-tx3_y-sep_h2_h3-2*sep_h2_h3-tx4_y-tx5_y)

        text_6="The prices are based on the purchase of a full container (275 sacks of 70 kg). For smaller quantities, prices may vary."
        tx6 = Paragraph (text_6,lato_text)
        tx6_x,tx6_y=tx6.wrap(450,500)
        tx6.drawOn(c,(width-tx6_x)/2,900-y_title-pt_y-50-tx1_y-sep_h2_h3-tx2_y-tx3_y-sep_h2_h3-3*sep_h2_h3-tx4_y-tx5_y-tx6_y)

        tx7 = Paragraph ("Support and Assistance:",bold_end_text)
        tx7_x,tx7_y=tx7.wrap(400,500)
        tx7.drawOn(c,(width-tx7_x)/2,900-y_title-pt_y-50-tx1_y-sep_h2_h3-tx2_y-tx3_y-sep_h2_h3-4*sep_h2_h3-tx4_y-tx5_y-tx6_y-tx7_y)

        text_8="If you have any questions or need more information, please contact the @EquationCoffee commercial team."
        tx8 = Paragraph (text_6,lato_text)
        tx8_x,tx8_y=tx8.wrap(450,500)
        tx8.drawOn(c,(width-tx8_x)/2,900-y_title-pt_y-50-tx1_y-sep_h2_h3-tx2_y-tx3_y-sep_h2_h3-5*sep_h2_h3-tx4_y-tx5_y-tx6_y-tx7_y-tx8_y)

        tx9 = Paragraph (". _ . _ . _ . _ . _ . _ . _ . _ . _ . _ . _ . _ . _. _ . _ . _ . _ . _ . _ . _ . _ . _ . _ . _ . _ . _ . _. _ . _ . _ . _ . _ . _ . _ . _ . _ .",bold_end_text)
        tx9_x,tx9_y=tx9.wrap(550,500)
        tx9.drawOn(c,(width-tx9_x)/2,900-y_title-pt_y-50-tx1_y-sep_h2_h3-tx2_y-tx3_y-sep_h2_h3-7*sep_h2_h3-tx4_y-tx5_y-tx6_y-tx7_y-tx8_y-tx9_y)

        commercial_photo=ImageReader(os.path.join(current_dir,'angelica.png'))
        logo_width, logo_height = commercial_photo.getSize()
        c.drawImage(commercial_photo,0,0,width=None, height=None, preserveAspectRatio=True, mask='auto')

        request_par = Paragraph("Request Sample", request_centered)
        x_request_pa,y_request_par=request_par.wrap(400, 500)  # Ajustar el texto al tamaño del cuadro
        request_par.drawOn(c, 230, 200)  # Dibujar el párrafo en la posición indicada

        mail = Paragraph("nombre@equationcoffee.com", mail_centered)
        mail_x,mail_y=mail.wrap(400, 500)  # Ajustar el texto al tamaño del cuadro
        mail.drawOn(c, 230, 150)  # Dibujar el párrafo en la posición indicada

        eq = Paragraph("www.equationcoffee.com", mail_centered)
        x_eq,y_eq=eq.wrap(400, 500)  # Ajustar el texto al tamaño del cuadro
        eq.drawOn(c, 230, 100)  # Dibujar el párrafo en la posición indicada



        # c.setFillColor('#ccf1af')
        # c.setFont("Arial-Bold", 34)  # Usa 'Arial' si registraste Arial.ttf
        
        # x_centro = width / 2
        # y_pos = height / 2
        # c.drawCentredString(x_centro, y_pos, text)
        # x_inicio = 100
        # y_inicio = 700
        # ancho_celda = 120
        # alto_celda = 20

        # for fila_idx, fila in enumerate(datos):
        #     for col_idx, valor in enumerate(fila):
        #         x = x_inicio + col_idx * ancho_celda
        #         y = y_inicio - fila_idx * alto_celda

        #         # Fondo de celda
        #         if fila_idx == 0:
        #             c.setFillColor(colors.lightgrey)
        #         else:
        #             c.setFillColor(colors.whitesmoke if fila_idx % 2 == 0 else colors.white)

        #         c.setStrokeColor(colors.white)
        #         c.rect(x, y, ancho_celda, alto_celda, fill=1, stroke=1)

        #         # Texto centrado
        #         c.setFillColor(colors.black)
        #         c.setFont("Lato", 8)
        #         x_centro = x + ancho_celda / 2
        #         y_centro = y + (alto_celda / 2) - 3  # ajusta -3 para mejor vertical
        #         c.drawCentredString(x_centro, y_centro, str(valor))

        c.save()
        pdf_data = buffer.getvalue()
        buffer.close()
        return pdf_data
        # return request.make_response(pdf_data, headers=[
        #         ('Content-Type', 'application/pdf'),
        #         ('Content-Disposition', 'attachment; filename="reporte.pdf"'),
        #     ])

        # generar_pdf("mi_pdf_con_fondo_imagen.pdf")


    def category_print(self,data,coffee_table,doc,st,x_0,y_0,x_page,y_page,current_dir):
            styles = getSampleStyleSheet()
            style_normal = styles['Normal']
            style_justificado = ParagraphStyle(
                name='Justificado',
                parent=style_normal,
                fontName='Lato',
                fontSize=10,
                leading=12,
                alignment=4  
            )
            category_logo=ImageReader(os.path.join(current_dir,data.get('image')))
            logo_width, logo_height = category_logo.getSize()
            doc.drawImage(category_logo,x_0,y_0-logo_height,width=None, height=None, preserveAspectRatio=True, mask='auto')
            title_size=26
            doc.setFont("Lato", title_size)
            doc.setFillColorRGB(0, 0, 0)
            imgLim_x=x_0+logo_width
            imgLim_y=y_0+logo_height

            sepImgText_x=60
            text_x=imgLim_x+sepImgText_x
            title_y=y_0-title_size
            doc.drawString(text_x, title_y,  data.get('title', 'Sin título'))

            paragraph = Paragraph(data.get('description'), style_justificado)
            sep_title_text=5
            x_par, y_par = text_x, 740
            par_width = x_page-30-x_par
            par_height = 100        
            real_par_x,real_par_y=paragraph.wrap(par_width, par_height) 
            print('Dimensiones reales del parrafo',real_par_x,real_par_y)
            text_y=title_y-sep_title_text-real_par_y
            paragraph.drawOn(doc, x_par, text_y)  

            sep_table_text=50

            rows=[]
            coffees = coffee_table['coffees']
            for coffee in coffee_table["coffees"]:
                row = [
                    coffee.get("sku", ""),

                    coffee.get("Origin", ""),
                    coffee.get("Process", ""),
                    coffee.get("Variety", ""),
                    coffee.get("sca", ""),
                ]
                rows.append(row)

            cols_width={
                'sku':40,
                'Origin':50,
                'Process':90,
                'Variety':70,
                'sca':30, ## Posibilidad de 20 de ancho
                'fob_us':40,
                'fob_eu':40,
                'spot_us':40,
                'spot_eu':40,
                'macroprofile':90,
                'aval_35':40,

                
            }

            headers = [header for header in coffees[0].keys() if header != "main_category"]
            print(headers)
            table_data=[headers]+rows
            row_height=20
            ancho_total_tabla = sum(cols_width.get(header,80) for header in headers)  
            x_start = (612 - ancho_total_tabla) / 2  
            y_start = text_y-sep_table_text
            x=x_start
            doc.setFillColorRGB(0.9, 0.9, 0.9)  
            for col_num, header in enumerate(headers):
                col_width=cols_width.get(header,1)
                doc.setFillColor(data.get('color'))
                doc.rect(x, y_start, col_width, row_height, fill=1, stroke=0)
                doc.setFont('Lato',8)
                doc.setFillColorRGB(0,0,0)
                doc.drawCentredString(x + col_width / 2, y_start + row_height / 2, str(header))
                x=x+col_width

            # Dibujar filas
            for row_num, item in enumerate(coffees):
                y = y_start - (row_num + 1) * row_height
                y_final=y
                x=x_start
                for col_num, header in enumerate(headers):
                    col_width=cols_width.get(header,1)
                    doc.setFillColorRGB(1, 1, 1)  
                    doc.rect(x, y, col_width, row_height, fill=1, stroke=0)
                    doc.setFillColorRGB(0, 0, 0)
                    doc.drawCentredString(x + col_width / 2, y + row_height / 2, str(item.get(header, "")))
                    x = x+ col_width
            return x_0,y
        

        # def generar_pdf(nombre_archivo):
        #     buffer = BytesIO()  
        #     page_x=612
        #     page_y=1000.08
        #     custom_size = (page_x, page_y)    
        #     c = canvas.Canvas(buffer, pagesize=custom_size)
        #     width, height = custom_size
            

        #     imagen_fondo = ImageReader(os.path.join(current_dir,"offering_background.png"))
        #     c.drawImage(imagen_fondo, 0, 0, width=width, height=height)

        #     styles = getSampleStyleSheet()
        #     style_normal = styles['Normal']

        #         # Modificar el estilo para justificar el texto
        #     style_justificado = ParagraphStyle(
        #         name='Justificado',
        #         parent=style_normal,
        #         alignment=4  # 4 es el código para justificar
        #     )



        #     # --------- Datos de la tabla ---------

        #     data = {
        #         "commercial_user":"Angelica Garrido",
        #         "customer": "MvsM GmbH",
        #         "offering_seq":"OFF-0001",
        #         "date": "15/5/2025",
        #         "coffees":[
        #             {
        #             "sku":"MC0015",
        #             "main_category":"Farm Selection Microlots",
        #             "Origin":"Risaralda",
        #             "Process":"Termo Shock Washed",
        #             "Variety":"Variedad",
        #             "sca":"89.7",
        #             "fob_us":"NYC+0.8",
        #             "fob_eu":"9,67",
        #             "spot_us":"8l,7",
        #             "spot_eu":"8,89",
        #             "macroprofile":"Floral, Citrus, Aromatic",
        #             "aval_35":"1000",
        #         },
        #         {
        #             "sku": "MC0016",
        #             # "main_category": "Farm Selection Microlots",
        #             "main_category":"Everyday Blends",
        #             "Origin": "Antioquia",
        #             "Process": "Natural",
        #             "Variety": "Yellow Bourbon",
        #             "sca": "88.3",
        #             "fob_us": "NYC+1.0",
        #             "fob_eu": "10,20",
        #             "spot_us": "9,0",
        #             "spot_eu": "9,5",
        #             "macroprofile": "Fruity",
        #             "aval_35": "500"
        #         },
        #         {
        #             "sku": "MC0039",
        #             # "main_category": "Farm Selection Microlots",
        #             "main_category":"Everyday Blends",
        #             "Origin": "Nariño",
        #             "Process": "Natural",
        #             "Variety": "Catuai",
        #             "sca": "88.3",
        #             "fob_us": "NYC+1.0",
        #             "fob_eu": "10,20",
        #             "spot_us": "9,0",
        #             "spot_eu": "9,5",
        #             "macroprofile": "Fruity",
        #             "aval_35": "500"
        #         }
        #         ]
        #     }
        #     datos = [
        #         ["Nombre", "Edad", "Ciudad"],
        #         ["Ana", "28", "Bogotá"],
        #         ["Luis", "34", "Medellín"],
        #         ["María", "22", "Cali"],
        #     ]

        #     categories_data={
        #         'categories':[
        #             {
        #             "title":"Everyday Blends",
        #             "description":"The Everyday Blends category offers high-volume, quality consistent coffees that are reliable and accessible. These blends are crafted by combining lots from various farms within a specific region, ensuring an even and balanced cup profile. Ideal for roasters seeking steady supply with quality flavor profiles, they are perfect for daily use and reliable for consistent quality year-round.",
        #             "image":"Everyday_Blends.png",
        #             "color":"#f6f0e2",
        #             },
        #             {
        #             "title":"Farm Selection Microlots",
        #             "description":"Small batches of specialty coffee with traceability down to the individual farm. With scores of 85+ points, these coffees showcase distinct flavor profiles and refined characteristics, celebrating the dedication of each grower. Perfect for roasters looking to highlight the craftsmanship of a specific region and farm, these lots offer an elevated experience without the premium pricing of exotic varieties.",
        #             "image":"Farm_Select.png",
        #             "color":"#272735",
        #             },
        #             {
        #             "title":"Avant-Grade Experimentals",
        #             "description":"Features coffees processed with groundbreaking techniques, including cultured bacteria inoculation and controlled fermentation environments, both during washing and drying stages. These experimental methods yield distinct and unconventional flavor profiles, catering to adventurous buyers who seek innovation and a deeper exploration of coffee’s sensory possibilities. ",
        #             "image":"Farm_Select.png",
        #             "color":"#6d5448",
        #             },
        #             {
        #             "title":"Decaf Collection",
        #             "description":"A diverse decaf collection that preserves the vibrant flavors of our specialty coffees. Using the Sugar Cane Decaf Process (EA)—a natural method with locally sourced sugar cane—we gently remove caffeine without high pressure or extreme heat, keeping the coffee’s rich taste. Whether you enjoy the sweetness of a washed decaf or the complexity of a honey process, our Decaf Collection delivers a full-flavored, caffeine-free experience.",
        #             "image":"Farm_Select.png",
        #             "color":"#e0c7b6",
        #             },
        #             {
        #             "title":"Rare Exotic",
        #             "description":"Are small-lot single origin coffees from unique and rare varieties like Java, SL28, Geisha, Sidra, and many others. Grown in carefully curated microclimates, these coffees offer unparalleled complexity and are prized for their unique flavors and exceptional cup scores (86+ points). Rare Exotics are aimed at roasters looking for exclusive, standout coffees that push the boundaries of traditional specialty coffee.",
        #             "image":"Farm_Select.png",
        #             "color":"#4c5f66",
        #             }
        #         ]
        #     }

        #     pos_x=30
        #     pos_y=836
        #     sep_section=50

        #     categories_unique=set()
        #     for coffee in data['coffees']:
        #         categories_unique.add(coffee['main_category'])

        #     for category in categories_unique:
        #         cat_data={}
        #         coffees_print={
        #             'coffees':[]
        #         }
        #         for coffee in data['coffees']:
        #             if coffee['main_category']==category:
        #                 coffees_print['coffees'].append(coffee)
                
        #         for cat in categories_data['categories']:
        #             if cat['title']==category:
        #                 cat_data=cat
        #         act_x,act_y=category_print(cat_data,coffees_print,c,styles,pos_x,pos_y,page_x,page_y)
        #         pos_x=act_x
        #         pos_y=act_y-sep_section
        #         print(category)
        #         print(coffees_print)
        #         print(cat_data)

        #     c.showPage()
        #     c.setFillColor(black)
        #     c.rect(0, 0, width, height, fill=1, stroke=0)


        #     title_final = Paragraph("Important Information and Details", title_centered)
        #     x_title,y_title=title_final.wrap(400, 500)  # Ajustar el texto al tamaño del cuadro
        #     title_final.drawOn(c, (width-x_title)/2, 900-y_title)  # Dibujar el párrafo en la posición indicada

        #     sep_h2_h3=20
            
        #     pricing_title = Paragraph ("Pricing and Availability Validity:",bold_end_text)
        #     pt_x,pt_y=pricing_title.wrap(400,500)
        #     pricing_title.drawOn(c,(width-pt_x)/2,900-y_title-pt_y-50)

        #     tx1 = Paragraph ("The prices and availability in this offering are valid from ",lato_text)
        #     tx1_x,tx1_y=tx1.wrap(400,500)
        #     tx1.drawOn(c,(width-tx1_x)/2,900-y_title-pt_y-50-tx1_y-sep_h2_h3)

        #     tx2 = Paragraph ("<u>February 17, 2025, to February 24, 2025.</u>",lato_text)
        #     tx2_x,tx2_y=tx2.wrap(400,500)
        #     tx2.drawOn(c,(width-tx2_x)/2,900-y_title-pt_y-50-tx1_y-sep_h2_h3-tx2_y)

        #     tx3 = Paragraph ("Standard Packaging Included:",bold_end_text)
        #     tx3_x,tx3_y=tx3.wrap(400,500)
        #     tx3.drawOn(c,(width-tx3_x)/2,900-y_title-pt_y-50-tx1_y-sep_h2_h3-tx2_y-tx3_y-sep_h2_h3)

        #     text_4="Prices include packaging in fique sacks with multilayer bags and standard markings for <b><u>35 kg or 70 kg </u></b> sacks. If you require a different type of sack, bag, or custom markings, this may affect the price and delivery times."
        #     tx4 = Paragraph (text_4,lato_text)
        #     tx4_x,tx4_y=tx4.wrap(450,500)
        #     tx4.drawOn(c,(width-tx4_x)/2,900-y_title-pt_y-50-tx1_y-sep_h2_h3-tx2_y-tx3_y-sep_h2_h3-sep_h2_h3-tx4_y)

        #     tx5 = Paragraph ("Purchase Conditions:",bold_end_text)
        #     tx5_x,tx5_y=tx5.wrap(400,500)
        #     tx5.drawOn(c,(width-tx5_x)/2,900-y_title-pt_y-50-tx1_y-sep_h2_h3-tx2_y-tx3_y-sep_h2_h3-2*sep_h2_h3-tx4_y-tx5_y)

        #     text_6="The prices are based on the purchase of a full container (275 sacks of 70 kg). For smaller quantities, prices may vary."
        #     tx6 = Paragraph (text_6,lato_text)
        #     tx6_x,tx6_y=tx6.wrap(450,500)
        #     tx6.drawOn(c,(width-tx6_x)/2,900-y_title-pt_y-50-tx1_y-sep_h2_h3-tx2_y-tx3_y-sep_h2_h3-3*sep_h2_h3-tx4_y-tx5_y-tx6_y)

        #     tx7 = Paragraph ("Support and Assistance:",bold_end_text)
        #     tx7_x,tx7_y=tx7.wrap(400,500)
        #     tx7.drawOn(c,(width-tx7_x)/2,900-y_title-pt_y-50-tx1_y-sep_h2_h3-tx2_y-tx3_y-sep_h2_h3-4*sep_h2_h3-tx4_y-tx5_y-tx6_y-tx7_y)

        #     text_8="If you have any questions or need more information, please contact the @EquationCoffee commercial team."
        #     tx8 = Paragraph (text_6,lato_text)
        #     tx8_x,tx8_y=tx8.wrap(450,500)
        #     tx8.drawOn(c,(width-tx8_x)/2,900-y_title-pt_y-50-tx1_y-sep_h2_h3-tx2_y-tx3_y-sep_h2_h3-5*sep_h2_h3-tx4_y-tx5_y-tx6_y-tx7_y-tx8_y)

        #     tx9 = Paragraph (". _ . _ . _ . _ . _ . _ . _ . _ . _ . _ . _ . _ . _. _ . _ . _ . _ . _ . _ . _ . _ . _ . _ . _ . _ . _ . _. _ . _ . _ . _ . _ . _ . _ . _ . _ .",bold_end_text)
        #     tx9_x,tx9_y=tx9.wrap(550,500)
        #     tx9.drawOn(c,(width-tx9_x)/2,900-y_title-pt_y-50-tx1_y-sep_h2_h3-tx2_y-tx3_y-sep_h2_h3-7*sep_h2_h3-tx4_y-tx5_y-tx6_y-tx7_y-tx8_y-tx9_y)

        #     commercial_photo=ImageReader(os.path.join(current_dir,'angelica.png'))
        #     logo_width, logo_height = commercial_photo.getSize()
        #     c.drawImage(commercial_photo,0,0,width=None, height=None, preserveAspectRatio=True, mask='auto')

        #     request = Paragraph("Request Sample", request_centered)
        #     x_request,y_request=request.wrap(400, 500)  # Ajustar el texto al tamaño del cuadro
        #     request.drawOn(c, 230, 200)  # Dibujar el párrafo en la posición indicada

        #     mail = Paragraph("nombre@equationcoffee.com", mail_centered)
        #     mail_x,mail_y=mail.wrap(400, 500)  # Ajustar el texto al tamaño del cuadro
        #     mail.drawOn(c, 230, 150)  # Dibujar el párrafo en la posición indicada

        #     eq = Paragraph("www.equationcoffee.com", mail_centered)
        #     x_eq,y_eq=eq.wrap(400, 500)  # Ajustar el texto al tamaño del cuadro
        #     eq.drawOn(c, 230, 100)  # Dibujar el párrafo en la posición indicada



        #     # c.setFillColor('#ccf1af')
        #     # c.setFont("Arial-Bold", 34)  # Usa 'Arial' si registraste Arial.ttf
            
        #     # x_centro = width / 2
        #     # y_pos = height / 2
        #     # c.drawCentredString(x_centro, y_pos, text)
        #     # x_inicio = 100
        #     # y_inicio = 700
        #     # ancho_celda = 120
        #     # alto_celda = 20

        #     # for fila_idx, fila in enumerate(datos):
        #     #     for col_idx, valor in enumerate(fila):
        #     #         x = x_inicio + col_idx * ancho_celda
        #     #         y = y_inicio - fila_idx * alto_celda

        #     #         # Fondo de celda
        #     #         if fila_idx == 0:
        #     #             c.setFillColor(colors.lightgrey)
        #     #         else:
        #     #             c.setFillColor(colors.whitesmoke if fila_idx % 2 == 0 else colors.white)

        #     #         c.setStrokeColor(colors.white)
        #     #         c.rect(x, y, ancho_celda, alto_celda, fill=1, stroke=1)

        #     #         # Texto centrado
        #     #         c.setFillColor(colors.black)
        #     #         c.setFont("Lato", 8)
        #     #         x_centro = x + ancho_celda / 2
        #     #         y_centro = y + (alto_celda / 2) - 3  # ajusta -3 para mejor vertical
        #     #         c.drawCentredString(x_centro, y_centro, str(valor))

        #     # c.save()
        #     pdf_data = buffer.getvalue()
        #     buffer.close()
        #     return request.make_response(pdf_data, headers=[
        #             ('Content-Type', 'application/pdf'),
        #             ('Content-Disposition', 'attachment; filename="reporte.pdf"'),
        #         ])

        # # generar_pdf("mi_pdf_con_fondo_imagen.pdf")
