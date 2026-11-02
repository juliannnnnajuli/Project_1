from tkinter import *
from tkinter import messagebox as mb
from tkinter import ttk
import requests

# словарь криптовалют
crypto_coins = {
    "bitcoin": "Биткоин (BTC)",
    "ethereum": "Эфириум (ETH)",
    "binancecoin": "Бинанс Коин (BNB)",
    "solana": "Солана (SOL)",
    "ripple": "Рипл (XRP)",
    "cardano": "Кардано (ADA)",
    "dogecoin": "Догикоин (DOGE)",
    "tron": "Трон (TRX)",
    "polkadot": "Полкадот (DOT)",
    "litecoin": "Лайткоин (LTC)"
}


def get_price(): #функция получения курса
    """Запрашивает курс выбранной криптовалюты к USD и выводит результат."""
    coin_id = crypto_combobox.get().strip()

    if not coin_id:
        mb.showwarning("Внимание", "Выберите криптовалюту из списка")
        return

    # Ищем ключ по отображаемому названию
    selected_crypto = None
    for key, value in crypto_coins.items():
        if value == coin_id:
            selected_crypto = key
            break

    if selected_crypto is None:
        mb.showerror("Ошибка", "Криптовалюта не найдена в справочнике")
        return

    url = f"https://api.coingecko.com/api/v3/simple/price?ids={selected_crypto}&vs_currencies=usd"

    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        data = response.json()

        if selected_crypto in data and "usd" in data[selected_crypto]:
            price = data[selected_crypto]["usd"]
            formatted_price = f"{price:,.2f}".replace(",", " ").replace(".", ",")
            mb.showinfo(
                "Курс криптовалюты",
                f"Курс 1 {crypto_coins[selected_crypto]} = {formatted_price} USD"
            )
        else:
            mb.showerror("Ошибка", "Не удалось получить курс для выбранной валюты")
    except requests.exceptions.RequestException as e:
        mb.showerror("Ошибка сети", f"Не удалось выполнить запрос:\n{e}")
    except Exception as e:
        mb.showerror("Ошибка", f"Произошла ошибка:\n{e}")


root = Tk()
root.title('Криптовалютник')
root.geometry('360x180')

root.mainloop()