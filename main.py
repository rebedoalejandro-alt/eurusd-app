from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.core.window import Window
from kivy.clock import Clock

import threading
import requests


API_URL = "https://api.exchangerate.host/latest?base=EUR&symbols=USD"


class ConverterApp(App):
    title = "EUR → USD"

    def build(self):
        # Tamaño cómodo para escritorio; Android ignora esto y usa pantalla completa
        try:
            Window.size = (360, 640)
        except Exception:
            pass

        root = BoxLayout(orientation="vertical", padding=16, spacing=12)

        header = Label(text="Conversor EUR → USD", font_size=24, size_hint=(1, None), height=48)

        self.input_eur = TextInput(
            hint_text="Euros",
            input_filter="float",
            multiline=False,
            write_tab=False,
            size_hint=(1, None),
            height=48,
        )

        self.rate_label = Label(text="Tasa: —", font_size=16, size_hint=(1, None), height=30)
        self.result = Label(text="0.00 USD", font_size=20, size_hint=(1, None), height=40)

        buttons = BoxLayout(orientation="horizontal", size_hint=(1, None), height=48, spacing=12)
        self.btn_convert = Button(text="Convertir")
        self.btn_update = Button(text="Actualizar tasa")
        btn_clear = Button(text="Limpiar")
        self.btn_convert.bind(on_release=self.on_convert)
        self.btn_update.bind(on_release=self.on_update_rate)
        btn_clear.bind(on_release=self.on_clear)
        buttons.add_widget(self.btn_convert)
        buttons.add_widget(self.btn_update)
        buttons.add_widget(btn_clear)

        root.add_widget(header)
        root.add_widget(self.input_eur)
        root.add_widget(self.rate_label)
        root.add_widget(self.result)
        root.add_widget(buttons)

        return root

    def on_convert(self, *_):
        text = (self.input_eur.text or "").strip().replace(",", ".")
        try:
            euros = float(text)
        except ValueError:
            self.result.text = "Entrada no válida"
            return

        # Desactivar el botón mientras se consulta la tasa
        self.btn_convert.disabled = True
        self.result.text = "Consultando tasa EUR→USD..."

        threading.Thread(target=self._convert_async, args=(euros,), daemon=True).start()

    def _convert_async(self, euros: float):
        try:
            rate = self._fetch_rate()
            usd = euros * rate
            text = (
                f"{usd:,.2f} USD".replace(",", "·").replace(".", ",").replace("·", ".")
                + f"\nTasa: {rate:.4f}"
            )
        except Exception as e:
            text = "Error de conexión"

        if 'rate' in locals():
            Clock.schedule_once(lambda dt: self._set_rate_label(rate), 0)
        Clock.schedule_once(lambda dt: self._finish_convert(text), 0)

    def _finish_convert(self, text: str):
        self.result.text = text
        self.btn_convert.disabled = False

    def _set_rate_label(self, rate: float):
        self.rate_label.text = f"Tasa: {rate:.4f}"

    def _fetch_rate(self) -> float:
        resp = requests.get(API_URL, timeout=8)
        resp.raise_for_status()
        data = resp.json()
        rate = float(data["rates"]["USD"])  # type: ignore[index]
        if rate <= 0:
            raise ValueError("Tasa inválida")
        return rate

    def on_update_rate(self, *_):
        self.btn_update.disabled = True
        self.rate_label.text = "Actualizando tasa…"
        threading.Thread(target=self._update_rate_async, daemon=True).start()

    def _update_rate_async(self):
        try:
            rate = self._fetch_rate()
            Clock.schedule_once(lambda dt: self._set_rate_label(rate), 0)
        except Exception:
            Clock.schedule_once(lambda dt: setattr(self.rate_label, 'text', 'Error de conexión'), 0)
        finally:
            Clock.schedule_once(lambda dt: setattr(self.btn_update, 'disabled', False), 0)

    def on_clear(self, *_):
        self.input_eur.text = ""
        self.result.text = "0.00 USD"


if __name__ == "__main__":
    ConverterApp().run()
