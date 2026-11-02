from tkinter import *
from tkinter import ttk
from tkinter import messagebox as mb
import requests


# Словарь: id монеты в CoinGecko -> отображаемое название на русском
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


def update_label(event):
    """Обновляет надпись под списком при выборе криптовалюты"""
    selected = crypto_combobox.get()
    if selected:
        # Меняем текст метки на выбранную валюту
        result_label.config(text=f"Выбрано: {selected}", foreground="black")


def get_price():
    """Запрашивает курс выбранной криптовалюты к USD и выводит результат."""
    coin_id = crypto_combobox.get()

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


# Создание графического интерфейса
window = Tk()
window.title("Курсы криптовалют")
window.geometry("400x280")
window.resizable(False, False)

# Заголовок
Label(text="Выберите криптовалюту:", font=("Arial", 11)).pack(padx=10, pady=(20, 5))

# Выпадающий список с отображаемыми названиями
crypto_combobox = ttk.Combobox(
    values=list(crypto_coins.values()),
    state="readonly",
    width=30
)
crypto_combobox.pack(padx=10, pady=5)
crypto_combobox.bind("<<ComboboxSelected>>", update_label)

# Кнопка получения курса
Button(
    text="Получить курс",
    command=get_price,
    width=20
).pack(padx=10, pady=15)

# Метка для вывода результата
result_label = ttk.Label(
    text="Выберите монету из списка",
    font=("Arial", 12),
    foreground="blue"
)
result_label.pack(padx=10, pady=10)

window.mainloop()