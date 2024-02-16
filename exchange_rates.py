import bcchapi
import os
from datetime import date, timedelta
from dotenv import load_dotenv

load_dotenv()

# Load up credentials
email = os.getenv("BCCH_EMAIL")
password = os.getenv("BCCH_PASSWORD")

def get_exchange_rates() -> dict[str, float|int]: 

    # Exchange rates dict
    exchange_rates = {}

    # Create a session
    session = bcchapi.Siete(email, password)

    exchanges_df = session.cuadro(
                series=["F073.TCO.PRE.Z.D", "F073.UFF.PRE.Z.D"],
                nombres=["USD", "UF"],
                desde=f"{date.today() - timedelta(days=7)}",  # Fetch the last 7 days, countermeasure for dates with no data
                hasta=f"{date.today()}",
                frecuencia="D",
                observado={"USD": "mean", "UF": "mean"},
            ).dropna()
    
    exchange_rates["USD"] = exchanges_df["USD"].iloc[-1]
    exchange_rates["UF"] = exchanges_df["UF"].iloc[-1]

    return exchange_rates

