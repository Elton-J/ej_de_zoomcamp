import pandas as pd
import sys

print(sys.argv)

dia = sys.argv[1]

print(f"(Deu certo - VINDO DA IMAGEM! DIA: {dia}) pandas version: {pd.__version__}")