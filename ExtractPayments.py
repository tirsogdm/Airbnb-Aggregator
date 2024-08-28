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


def extract_payments(emails):
    payments = list()

    for email in emails:
        payment = parse_html(email["forwarded-content"])
        payment.setDateTime(email["date"])
        payments.append(payment)

    return payments


def parse_html(email, verbose=False):
    # Step 1: Clean up the text to remove leading '> ' characters
    stripped_content = re.sub(r'>\s+', '', email)

    # Step 2: Extract Reservation Information
    reservation_pattern = re.compile(
        r"Reservation\s*(\d{2}/\d{2}/\d{4}) - (\d{2}/\d{2}/\d{4})\s*-*\s*(.*?)\s*-\s*(.*?)\s*-\s*(.*?)\s*Número de identificación del anuncio:\s*(\d+)\s*(\d+,\d{2}) €",
        re.DOTALL
    )

    reservations = reservation_pattern.findall(stripped_content)

    # Step 3: Extract Final Amount (Importe pagado)
    final_amount_pattern = re.compile(
        r"Importe pagado \(EUR\)\s*(\d{1,3}(\.\d{3})*,\d{2}) €")
    final_amount_match = final_amount_pattern.search(stripped_content)

    if final_amount_match:
        final_amount = final_amount_match.group(1)
    else:
        final_amount = None

    verbose and print(reservations)

    return Payment(final_amount, reservations, email)

    payment = {
        "amount": final_amount,
        "reservations": [{
            "date-in": reservation[0],
            "date-out": reservation[1],
            "reservation-id": reservation[2],
            "guest-name": reservation[3],
            "apartment-desc": reservation[4],
            "listing-id": reservation[5],
            "amount": reservation[6]
        } for reservation in reservations]
    }

    return payment


if __name__ == "__main__":
    print(parse_html(email_content, True))
