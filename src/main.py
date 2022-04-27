import argparse
import json
import tkinter
from tkinter import messagebox

import sbi


def button_click():
    if ipo_order():
        messagebox.showinfo("Info", "IPO申込みが終わりました。")
    else:
        messagebox.showerror("Error", "IPO申込みに失敗しました。")


def ipo_order() -> bool:
    ret = False
    if config["sbi"]["is_disabled"]:
        sbi_ipo = sbi.Ipo(headless=config["is_headless"])
        if sbi_ipo.login(
            user_id=config["sbi"]["user_id"],
            user_password=config["sbi"]["user_password"],
            trading_password=config["sbi"]["trading_password"],
        ):
            sbi_ipo.order_all()
            sbi_ipo.logout()
            ret = True
        del sbi_ipo
    return ret


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", type=str, help="コンフィグファイル（.json）のパスを指定してください")
    args = parser.parse_args()

    if args.config is None:
        file = "config.json"
    else:
        file = args.config
    try:
        with open(file) as f:
            config = json.load(f)
    except FileNotFoundError as e:
        messagebox.showerror("Error", f"{e}")
    else:
        if config["display"]:
            window = tkinter.Tk()
            window.title("Automatic IPO")
            window.geometry("300x60")
            label_1 = tkinter.Label(text="IPO自動申込ツール")
            label_1.pack()
            button = tkinter.Button(text="実行", command=button_click)
            button.pack()
            window.mainloop()
        else:
            ipo_order()
