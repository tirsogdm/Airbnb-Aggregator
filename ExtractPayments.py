from Representations import Payment
import re

email_content = """
> Inicio del mensaje reenviado:
> 
> De: Airbnb <express@airbnb.com>
> Asunto: Hemos enviado un cobro de 1.964,39 €
> Fecha: 12 de julio de 2024, 13:31:28 CEST
> Para: madridrentalsmadrid@gmail.com
> 
>  <https://www.airbnb.es/?eal_exp=1723375888&eal_sig=289992144961d73889b38954140a59f78b156e7f7b12cff425431df882d691e0&eal_uid=368117770&eluid=0&euid=fe2a54b2-7298-a8dd-75dd-297cb67a6183>
> Pago de 1.964,39 € enviado
> Te hemos enviado un cobro de 1.964,39 €. Este pago debería llegar a tu cuenta antes del 19 de julio de 2024, contando con los fines de semana y los días festivos. 
> Número de identificación de la cuenta de Airbnb
> 368117770 
> *Número de identificación del pago
> G-AGR45MRTTZIQKM6LK6EZTWBO6J3MSHFY
> Tipo 
> Detalles
> Importe
> Reservation
> 07/11/2024 - 07/14/2024
> HM4FBZADWT - Mustapha Benrhamous - Céntrico Apartamento a 3 calles de Gran Vía V5C
> Número de identificación del anuncio: 862728754324018131 
> 462,45 € 
> Reservation
> 07/11/2024 - 07/14/2024
> HMTEJ5DCNK - Borja García-Fogeda Polo - Céntrico Apartamento a 3 calles de Gran Vía VBB
> Número de identificación del anuncio: 859072987646569497 
> 491,10 € 
> Reservation
> 07/11/2024 - 07/14/2024
> HMHJEMFSH2 - Felipe Castro Salvador - Céntrico Apartamento a 3 calles de Gran Vía V4B
> Número de identificación del anuncio: 858748940545303702 
> 462,45 € 
> Reservation
> 07/11/2024 - 07/15/2024
> HMDA9CDSDJ - Michelle Conde - Céntrico Apartamento a 3 calles de Gran Vía V4A
> Número de identificación del anuncio: 857908678811987992 
> 548,39 € 
> Importe pagado (EUR) 
> 1.964,39 €
> *Número de identificación del pago 
> Este es el identificador único que Airbnb transmite a tu entidad financiera. Ten en cuenta que esta información quizá no aparezca en tu extracto bancario. 
> Puedes consultar el estado de tus cobros en tu Historial de transacciones <https://www.airbnb.es/users/transaction_history/368117770?c=.pi80.pkcGF5bWVudHMvaG9zdF9wYXlvdXRfc2VudF9iYXNl&euid=fe2a54b2-7298-a8dd-75dd-297cb67a6183>. 
> Gracias,
> El equipo de Airbnb 
> Preguntas frecuentes 
> ¿Cuándo recibiré el pago?
>  <https://www.airbnb.es/help/question/425?c=.pi80.pkcGF5bWVudHMvaG9zdF9wYXlvdXRfc2VudF9iYXNl&euid=fe2a54b2-7298-a8dd-75dd-297cb67a6183>
> ¿Cómo puedo calcular el pago que recibiré?
>  <https://www.airbnb.es/help/question/459?c=.pi80.pkcGF5bWVudHMvaG9zdF9wYXlvdXRfc2VudF9iYXNl&euid=fe2a54b2-7298-a8dd-75dd-297cb67a6183>
> Puedes obtener más información en nuestro Centro de ayuda <https://www.airbnb.es/help?c=.pi80.pkcGF5bWVudHMvaG9zdF9wYXlvdXRfc2VudF9iYXNl&euid=fe2a54b2-7298-a8dd-75dd-297cb67a6183>. 
> 
> Airbnb Ireland UC, 8 Hanover Quay,
> Dublín 2, Irlanda 
> 
>
"""

email_content2 = """
> Inicio del mensaje reenviado:
> 
> De: Airbnb <express@airbnb.com>
> Asunto: Hemos enviado un cobro de 931,48 €
> Fecha: 14 de agosto de 2024, 13:16:27 CEST
> Para: madridrentalsmadrid@gmail.com
> 
>  <https://www.airbnb.es/?eal_exp=1726226187&eal_sig=78a1c3571dd6cc1043683ac84b50b0f60471c50369a2b0b257065b05a803fe67&eal_uid=368117770&eluid=0&euid=1aca20ca-bbaa-62d9-5b16-7adae565f9bf>
> Pago de 931,48 € enviado
> Te hemos enviado un cobro de 931,48 €. Este pago debería llegar a tu cuenta antes del 21 de agosto de 2024, contando con los fines de semana y los días festivos. 
> Número de identificación de la cuenta de Airbnb
> 368117770
> *Número de identificación del pago
> G-CKUKQ6IFOTKAN2EG4GEKH5NBYR5GKCEO
> Tipo
> Detalles
> Importe
> Reservation
> 08/13/2024 - 08/15/2024
> HMJ3SE8RF4 - Laila Haq - Céntrica Buhardilla a 3 calles de Gran Vía V5B
> Número de identificación del anuncio: 868531576895533962
> 209,56 € 
> Reservation
> 08/13/2024 - 08/15/2024
> HMSMSNYKMM - Nery Gordillo Gutierrez - Céntrico Apartamento a 3 calles de Gran Vía V2A
> Número de identificación del anuncio: 857670063427347471
> 165,34 € 
> Reservation
> 08/13/2024 - 08/16/2024
> HMBBJ8F8NE - Lynnsey Henry - Céntrico Apartamento a 3 calles de Gran Vía V3B
> Número de identificación del anuncio: 847596666234953296 
> 278,29 € 
> Reservation
> 08/13/2024 - 08/16/2024
> HMQJJFKHD2 - 수린 이 - Céntrico Apartamento a 3 calles de Gran Vía V3C
> Número de identificación del anuncio: 848281662432761392 
> 278,29 € 
> Importe pagado (EUR)
> 931,48 €
> *Número de identificación del pago
> Este es el identificador único que Airbnb transmite a tu entidad financiera. Ten en cuenta que esta información quizá no aparezca en tu extracto bancario.
> Puedes consultar el estado de tus cobros en tu Historial de transacciones <https://www.airbnb.es/users/transaction_history/368117770?c=.pi80.pkcGF5bWVudHMvaG9zdF9wYXlvdXRfc2VudF9iYXNl&euid=1aca20ca-bbaa-62d9-5b16-7adae565f9bf>. 
> Gracias,
> El equipo de Airbnb
> Preguntas frecuentes
> ¿Cuándo recibiré el pago?
>  <https://www.airbnb.es/help/question/425?c=.pi80.pkcGF5bWVudHMvaG9zdF9wYXlvdXRfc2VudF9iYXNl&euid=1aca20ca-bbaa-62d9-5b16-7adae565f9bf>
> ¿Cómo puedo calcular el pago que recibiré?
>  <https://www.airbnb.es/help/question/459?c=.pi80.pkcGF5bWVudHMvaG9zdF9wYXlvdXRfc2VudF9iYXNl&euid=1aca20ca-bbaa-62d9-5b16-7adae565f9bf>
> Puedes obtener más información en nuestro Centro de ayuda <https://www.airbnb.es/help?c=.pi80.pkcGF5bWVudHMvaG9zdF9wYXlvdXRfc2VudF9iYXNl&euid=1aca20ca-bbaa-62d9-5b16-7adae565f9bf>. 
> 
> Airbnb Ireland UC, 8 Hanover Quay,
> Dublín 2, Irlanda 
> 
>
"""


def extract_payments(emails):
    payments = list()

    for email in emails:
        raw_content = email["forwarded-content"]
        date = email["date"]
        subject = email["subject"]
        building = get_building_str(subject)
        payment_amount, payment_reservations = parse_email(raw_content, date)
        payment = Payment(payment_amount, payment_reservations,
                          date, building, raw_content)
        payments.append(payment)

    return payments

def parse_email(email, date, verbose=False):
    # Step 1: Clean up the text to remove leading '> ' characters NOTE REVIEW THIS!!!
    stripped_content = re.sub(r'\n>\s*', '\n', email)
    stripped_content = re.sub('>', ' ', stripped_content)

    # r"Reservation\s*(\d{2}/\d{2}/\d{4}) - (\d{2}/\d{2}/\d{4})\s*-*\s*(.*?)\s*-\s*(.*?)\s*-\s*(.*?)\s*Número de identificación del anuncio:\s*(\d+)\s*([\d,.]+,\d{2}) €",
    # Step 2: Extract Reservation Information
    # !!! In english messages all that changes is "Número de identificación del anuncio" to "Listing ID"
    # Break down the pattern into smaller parts so it can be easily fixed.
    reservation_pattern = re.compile(
        r"Reservation\s*(\d{2}/\d{2}/\d{4}) - (\d{2}/\d{2}/\d{4})\s*-*\s*(.*?)\s*-\s*(.*?)\s*-\s*(.*?)\s*Número de identificación del anuncio:\s*([\d\w\s]+)(?:\s*\(.*?\))?\n\s*(\d{1,3}(?:\.\d{3})*,\d{2}) €",
        re.DOTALL
    )

    reservations = reservation_pattern.findall(stripped_content)

    if not reservations:
        print(date)
        print(stripped_content)
        print("-"*50)
    
    # Step 3: Extract Final Amount (Importe pagado)
    # !!! In english messages this is simply "Amount paid"
    final_amount_pattern = re.compile(
        r"Importe pagado \(EUR\)\s*(\d{1,3}(\.\d{3})*,\d{2}) €")
    final_amount_match = final_amount_pattern.search(stripped_content)

    if final_amount_match:
        final_amount = final_amount_match.group(1)
    else:
        final_amount = None

    verbose and print(reservations)

    return final_amount, reservations

def get_building_str(subject):
    bldg_pattern = re.compile(r"([A-Za-z]+\d+):?\s+.*") # Some subjects don't have a colon!
    bldg_match = re.search(bldg_pattern, subject)
    return bldg_match.group(1)

if __name__ == "__main__":
    print(parse_email(email_content2, True))
