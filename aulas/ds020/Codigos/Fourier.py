# -*- coding: utf-8 -*-
"""
Created on Sun Aug 24 19:15:06 2025

@author: claus
"""

import numpy as np
import matplotlib.pyplot as plt

# Classe para gerenciar sinais
class SignalGenerator:
    def __init__(self, t_min=0, t_max=1, sample_rate=1000):
        self.t = np.linspace(t_min, t_max, int((t_max - t_min) * sample_rate))
        self.signals = []

    def add_sine(self, freq=1, amplitude=1, phase=0):
        """Adiciona um sinal senoidal"""
        signal = amplitude * np.sin(2 * np.pi * freq * self.t + phase)
        self.signals.append(("Seno", signal))

    def add_cosine(self, freq=1, amplitude=1, phase=0):
        """Adiciona um sinal cossenoidal"""
        signal = amplitude * np.cos(2 * np.pi * freq * self.t + phase)
        self.signals.append(("Cosseno", signal))

    def plot_signals(self):
        """Plota cada sinal e a soma de todos"""
        if not self.signals:
            print("Nenhum sinal adicionado!")
            return

        # Criar subplots para cada sinal + 1 para a soma
        fig, axes = plt.subplots(len(self.signals) + 1, 1, figsize=(10, 2*(len(self.signals)+1)))

        # Plota cada sinal individual
        for i, (label, signal) in enumerate(self.signals):
            axes[i].plot(self.t, signal, label=f"{label}")
            axes[i].legend()
            axes[i].grid(True)

        # Plota a soma dos sinais
        total = np.sum([s for _, s in self.signals], axis=0)
        axes[-1].plot(self.t, total, color="black", label="Soma dos sinais")
        axes[-1].legend()
        axes[-1].grid(True)

        plt.tight_layout()
        plt.show()


# Exemplo de uso
if __name__ == "__main__":
    sg = SignalGenerator(t_min=0, t_max=1, sample_rate=2000)

    # Adicionando sinais
    sg.add_sine(freq=5, amplitude=1)
    sg.add_cosine(freq=10, amplitude=0.5)
    sg.add_sine(freq=20, amplitude=0.8, phase=np.pi/4)

    # Visualização
    sg.plot_signals()
