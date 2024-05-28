from dataclasses import dataclass

from model.go_products import go_product


@dataclass
class Connessione:
    P1: go_product
    P2: go_product
    #N: int