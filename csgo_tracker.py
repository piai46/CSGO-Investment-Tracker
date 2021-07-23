import time, json, datetime
import requests
import PySimpleGUI as sg

class ControleCSGO:
    def __init__(self):
        self.window_title = "CSGO Investment Tracker"
        layout = [
            [sg.Text("")],
            [sg.Text("")],
            [sg.Text(""),sg.Button("ADICIONAR ITEM", size=(10,3), key="adicionar_item"),
             sg.Button("VER ITENS", size=(10,3), key="ver_itens")],
            [sg.Text("    "),sg.Button("EDITAR/EXCLUIR ITENS", key="editar")]
        ]

        window = sg.Window("CSGO Investment Tracker", layout, size=(250, 200))

        while True:
            event, values = window.read()
            if event == "adicionar_item":
                window.close()
                self.track_price()
            elif event == "ver_itens":
                window.close()
                self.show_items()
            elif event == "editar":
                window.close()
                self.edit_items()
            if event == sg.WIN_CLOSED or event == "Exit":
                break
        window.close()

    def track_price(self):
        layout = [
            [sg.Text("Insira o nome do item para rastrear o preço: ", size=(32,1)), sg.InputText(key="skin_name")],
            [sg.Text("Insira o preço que pagou:                        R$", size=(32,1)), sg.InputText(key="skin_price")],
            [sg.Text("Insira a data quando comprou o item: ", size=(32,1)), sg.InputText(key="skin_date")],
            [sg.Text("Insira a quantidade que comprou: ", size=(32, 1)),
            sg.Spin(values=[i for i in range(1, 1000)], initial_value=1, size=(4, 1), key="quantidade")],
            [sg.Submit(), sg.Button("Voltar", key="voltar")]
        ]

        window = sg.Window(title=self.window_title, layout=layout)
        while True:
            event, values = window.read()
            if event == "Submit":
                skin_name = values["skin_name"]
                success = self.skin_price(skin_name)
                if success["success"] == True:
                    try:
                        float(values["skin_price"])
                        item = {"item_name":skin_name,
                                "old_price": values["skin_price"],
                                "date_bought":values["skin_date"],
                                "quantidade":values["quantidade"]}
                        self.adc_items(item)
                        sg.popup("Adicionado com sucesso!", title=self.window_title)
                    except:
                        sg.popup("Número inválido!", title=self.window_title)
                elif success["success"] == False:
                    sg.popup("Falha ao adicionar item!", title=self.window_title)
                else:
                    sg.popup("Erro desconhecido.", title=self.window_title)
            elif event == "voltar":
                window.close()
                ControleCSGO()
            if event == sg.WIN_CLOSED or event == "Exit":
                break
        window.close()

    def show_items(self):
        with open("items.json") as file:
            items = json.load(file)
            file.close()
        layout = [
            [sg.Output(size=(140, 10), key="output")],
            [sg.Button("Show/Refresh", key="show"),sg.Button("Back", key="back")]
        ]

        window = sg.Window("CSGO Investment Tracker", layout)

        while True:
            event, values = window.read()
            if event == "back":
                window.close()
                ControleCSGO()
            elif event == "show":
                now_date = datetime.datetime.now()
                hour_date = f"{now_date.strftime('%d')}/{now_date.strftime('%m')}, {now_date.hour}:{now_date.minute}\t\t"
                window.FindElement("output").Update("")
                print(hour_date)
                total_gasto = 0
                total_profit = 0
                for item in items["items"].values():
                    item_info = self.skin_price(item["item_name"])
                    price_now = float(item_info["lowest_price"].strip("R$ ").replace(",", "."))
                    profit = (price_now - (price_now * 0.12)) - float(item["old_price"])
                    total_gasto += float(item["old_price"]) * int(item["quantidade"])
                    total_profit += profit * int(item["quantidade"])
                    print(f"{item['item_name']}\t\t\t\tPreço pago: R${item['old_price']}\t\t\tQuantidade: {item['quantidade']}\t\tData da compra: {item['date_bought']}"
                          f"\t\t\tPreço atual:R${price_now}\t\t\tProfit: R${profit:.2f}")
                print(f"Totais:\t\t\t\tGastos:      \tR${total_gasto:.2f} \t\t\t\t\t\t\t\t\t\tProfit: R${total_profit:.2f}")
            if event == sg.WIN_CLOSED or event == "Exit":
                break

    def edit_items(self):
        with open("items.json") as file:
            items = json.load(file)
            file.close()
        item_names = [name for name in items["items"]]
        layout = [
            [sg.Text("Listando todos os itens:")],
            [sg.Listbox(item_names, size=(50,7), key="item_name")],
            [sg.Button("Editar", key="editar"),sg.Button("Excluir", key="excluir"),sg.Button("Back", key="back")]
        ]
        window = sg.Window("CSGO Investment Tracker", layout, size=(400,200))
        while True:
            event, values = window.read()
            if event == "editar":
                layout2 = [
                    [sg.Text(f"Insira o nome do item para rastrear o preço:    {values['item_name'][0]}")],
                    [sg.Text("Insira o preço que pagou:                        R$", size=(32, 1)),
                     sg.InputText(key="skin_price")],
                    [sg.Text("Insira a data quando comprou o item: ", size=(32, 1)), sg.InputText(key="skin_date")],
                    [sg.Text("Insira a quantidade que comprou: ", size=(32, 1)),
                     sg.Spin(values=[i for i in range(1, 1000)], initial_value=1, size=(4, 1), key="quantidade")],
                    [sg.Submit(), sg.Button("Voltar", key="voltar")]
                ]
                window2 = sg.Window("CSGO Investment Tracker", layout2)
                while True:
                    event2, values2 = window2.read()
                    if event2 == "Submit":
                        skin_name = values['item_name'][0]
                        success = self.skin_price(skin_name)
                        if success["success"] == True:
                            try:
                                skin_price = float(values2["skin_price"])
                                item = {"item_name": skin_name,
                                        "old_price": skin_price,
                                        "date_bought": values2["skin_date"],
                                        "quantidade": values2["quantidade"]}
                                items["items"].pop(skin_name)
                                self.adc_items(item)
                                sg.popup("Adicionado com sucesso! Aguarde...", title=self.window_title)
                                time.sleep(3)
                                break
                            except:
                                sg.popup("Numero inválido!", title=self.window_title)
                        elif success["success"] == False:
                            sg.popup("Falha ao adicionar item!", title=self.window_title)
                        else:
                            sg.popup("Erro desconhecido.", title=self.window_title)
                    if event2 == sg.WIN_CLOSED or event2 == "Exit":
                        break
                window2.close()
            elif event == "excluir":
                confirm_delete = sg.popup_ok_cancel(f"Deseja exlcuir {values['item_name'][0]}?")
                if confirm_delete == "OK":
                    items["items"].pop(values['item_name'][0])
                    with open("D:\Documents\LUIS\programaçao\python\projetos\csgo_tracker\items.json", "w") as file:
                        json.dump(items, file)
                        file.close()
                    window.close()
                    self.edit_items()
            elif event == "back":
                window.close()
                ControleCSGO()
            if event == sg.WIN_CLOSED or event == "Exit":
                break
        window.close()

    def skin_price(self, skin_name):
        payload = {"appid": "730", "market_hash_name": skin_name, "currency": "7"}
        response = requests.get("http://steamcommunity.com/market/priceoverview", payload)
        return response.json()

    def adc_items(self, item:dict):
        item_name = item["item_name"]
        with open("items.json") as file:
            items = json.load(file)
            file.close()
        items["items"][item_name] = item
        with open("items.json", "w") as file:
            json.dump(items, file)
            file.close()


if __name__ == "__main__":
    controle = ControleCSGO()