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


def update_label(event):  # функция обновления надписи с выбранной криптовалютой
    selected = crypto_combobox.get().strip()
    if selected:
        result_label.config(
            text=f"Выбрано: {selected}",
            bg="#1E1E24", fg="#F3BA2F",
            font=("Arial", 11, "bold")
        )


def get_price():  # функция получения курса
    coin_id = crypto_combobox.get().strip()

    if not coin_id:
        mb.showwarning("Внимание", "Выберите криптовалюту из списка")
        return

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


window = Tk()
window.title("Криптовалютник")
window.geometry("400x330")
window.configure(bg="#1E1E24")

Label(
    text="Выберите криптовалюту:",
    font=("Arial", 12, "bold"),
    bg="#1E1E24",
    fg="#FFFFFF"
).pack(padx=10, pady=(25, 5))

# Выпадающий список валют
crypto_combobox = ttk.Combobox(
    values=list(crypto_coins.values()),
    state="readonly",
    width=30,
    font=("Arial", 11)
)
crypto_combobox.pack(padx=10, pady=5)
crypto_combobox.bind("<<ComboboxSelected>>", update_label)

result_label = Label(
    text="Монета не выбрана",
    font=("Arial", 11),
    bg="#1E1E24",
    fg="gray"
)
result_label.pack(padx=10, pady=10)

# Кнопка получения курса
Button(
    text="Получить курс",
    command=get_price,
    width=20,
    font=("Arial", 11, "bold"),
    bg="#2EBD85",
    fg="white",
    activebackground="#26a674",
    activeforeground="white",
    relief=FLAT,
    cursor="hand2"
).pack(padx=10, pady=10)

# кнопка Выхода
Button(
    text="Выйти",
    command=window.destroy,
    width=20,
    font=("Arial", 11, "bold"),
    bg="#F6465D",
    fg="white",
    activebackground="#d13a4f",
    activeforeground="white",
    relief=FLAT,
    cursor="hand2"
).pack(padx=10, pady=10)

window.bind('<Return>', lambda event: get_price())
window.bind('<KP_Enter>', lambda event: get_price())

window.mainloop()
