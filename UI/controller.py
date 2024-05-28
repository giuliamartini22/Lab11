import flet as ft


class Controller:
    def __init__(self, view, model):
        # the view, with the graphical elements of the UI
        self._view = view
        # the model, which implements the logic of the program and holds the data
        self._model = model
        self._listYear = []
        self._listColor = []

    def fillDD(self):
        """methodo che popola la tendina con tutti gli anni in cui ci sono state vendite,
                prendendo le informazioni dal database"""
        self._listColor = self._model.getColor()
        for c in self._listColor:
            self._view._ddcolor.options.append(ft.dropdown.Option(c[0]))
        self._view.update_page()

    def read_color(self, e):
        """event handler che legge l'anno scelto dal menu a tendina ogniqualvolta viene cambiata
        la scelta, e lo memorizza in una variabile di instanza. L'anno è un intero, se si tratta di un anno,
        oppure un None se viene scelta l'opzione nessun filtro sull'anno"""
        if e.control.value == "None":
            self._color = None
        else:
            self._color = e.control.value

    def populate_dd_anno(self):
        """methodo che popola la tendina con tutti gli anni in cui ci sono state vendite,
        prendendo le informazioni dal database"""
        self._listYear = self._model.getYears()
        for anno in self._listYear:
            self._view._ddyear.options.append(ft.dropdown.Option(anno[0]))
        self._view.update_page()

    def read_anno(self, e):
        """event handler che legge l'anno scelto dal menu a tendina ogniqualvolta viene cambiata
        la scelta, e lo memorizza in una variabile di instanza. L'anno è un intero, se si tratta di un anno,
        oppure un None se viene scelta l'opzione nessun filtro sull'anno"""
        if e.control.value == "None":
            self._anno = None
        else:
            self._anno = e.control.value

    def handle_graph(self, e):
        color = self._view._ddcolor.value
        try:
            colorProduct = str(color)
        except ValueError:
            self._view.txtOut.controls.append(ft.Text("Il colore non è stato inserito"))
            self._view.update_page()
        anno = self._view._ddyear.value
        try:
            annoSelected = int(anno)
        except ValueError:
            self._view.txtOut.controls.append(ft.Text("L'anno non è stato inserito"))
            self._view.update_page()

        self._model.buildGraph(colorProduct, annoSelected)
        self._view.txtOut.controls.append(ft.Text("Grafo creato correttamente"))
        self._view.txtOut.controls.append(ft.Text(f"Num nodi: {self._model.getNumNodi()}"))
        self._view.txtOut.controls.append(ft.Text(f"Num archi: {self._model.getNumArchi()}"))
        archiPesoMaggiore = self._model.getArchiPesoMaggiore()
        conta = 0
        listaProdotti = []
        listaRipetuti = []
        for u, v, peso in archiPesoMaggiore:
            if conta < 3:
                #self._view.txtOut.controls.append(ft.Text(f"Da arco {u.getProductNumber()} ad arco {v.getProductNumber()} - peso: {peso}"))
                self._view.txtOut.controls.append(ft.Text(f"Da arco {u} ad arco {v} - peso: {peso}"))
                if u not in listaProdotti:
                    listaProdotti.append(u)
                if v not in listaProdotti:
                    listaProdotti.append(v)
                else:
                    listaRipetuti.append(u)
                    listaRipetuti.append(v)
                conta +=1
        print(listaRipetuti)
        print(listaProdotti)
        self._view.txtOut.controls.append(ft.Text(f"I nodi ripetuti sono:"))
        for n in listaRipetuti:
            self._view.txtOut.controls.append(ft.Text(f"[{n.Product_number}]"))

        self._view.update_page()



    def fillDDProduct(self):
        pass


    def handle_search(self, e):
        pass
