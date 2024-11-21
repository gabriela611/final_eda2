import sys
import random
from PyQt5 import QtWidgets, QtGui, QtCore
from grafos_ui import Ui_MainWindow
from PyQt5.QtWidgets import QGraphicsScene, QGraphicsEllipseItem, QGraphicsLineItem, QGraphicsTextItem, QGraphicsItem
import numpy as np


class Nodo(QGraphicsEllipseItem):
    def __init__(self, x, y, radius, id, app):
        super().__init__(-radius, -radius, 2 * radius, 2 * radius) 
        self.setBrush(QtGui.QBrush(QtGui.QColor("lightblue")))
        self.setPen(QtGui.QPen(QtCore.Qt.black))
        self.id = id
        self.setFlag(QGraphicsEllipseItem.ItemIsMovable)
        self.setFlag(QGraphicsEllipseItem.ItemSendsGeometryChanges)
        self.text_item = QGraphicsTextItem(f"Nodo {self.id}", self)
        self.text_item.setPos(-10, -10) 
        self.app = app  
        self.aristas = []  

    def agregar_arista(self, arista):
        self.aristas.append(arista)

    def itemChange(self, change, value):
        if change == QGraphicsItem.ItemPositionChange:
            
            for arista in self.aristas:
                arista.actualizar_posiciones()
        return super().itemChange(change, value)


class Arista(QGraphicsLineItem):
    def __init__(self, nodo1, nodo2, peso, scene):
        super().__init__()
        self.nodo1 = nodo1
        self.nodo2 = nodo2
        self.peso = peso
        self.scene = scene
        self.text_item = QGraphicsTextItem(str(self.peso))
        self.scene.addItem(self.text_item)
        self.actualizar_posiciones()
        self.setFlag(QGraphicsLineItem.ItemIsSelectable)
        self.setPen(QtGui.QPen(QtCore.Qt.black))

    def actualizar_posiciones(self):
        x1, y1 = self.nodo1.scenePos().x(), self.nodo1.scenePos().y()
        x2, y2 = self.nodo2.scenePos().x(), self.nodo2.scenePos().y()
        self.setLine(x1, y1, x2, y2)
        self.text_item.setPos((x1 + x2) / 2, (y1 + y2) / 2)

    def mousePressEvent(self, event):
        self.setPen(QtGui.QPen(QtCore.Qt.red, 3))  
        self.nodo1.setPen(QtGui.QPen(QtCore.Qt.red, 3))  
        self.nodo2.setPen(QtGui.QPen(QtCore.Qt.red, 3))  
        super().mousePressEvent(event)  

class GrafoApp(QtWidgets.QMainWindow):
    def __init__(self):
        super(GrafoApp, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        
        self.lblTitulo2 = QtWidgets.QLabel(self)
        self.lblTitulo2.setGeometry(10, 10, 100, 100)  

        pixmap = QtGui.QPixmap("Recurso-1-8.png")

        pixmap = pixmap.scaled(100, 100, QtCore.Qt.KeepAspectRatio)

        self.graphicsView = self.ui.graphicsView

        self.scene = QGraphicsScene()
        self.graphicsView.setScene(self.scene)

        self.ui.btnPintarGrafo.clicked.connect(self.dibujar_grafo)

         # Conectar el clic en el encabezado de tableWidget para generar una matriz aleatoria
        self.ui.tableWidget.horizontalHeader().sectionClicked.connect(self.llenar_matriz_aleatoria)

        #conectar boton para genear matriz adyacencia
        self.ui.btnAdyacencia.clicked.connect(self.generar_tabla_adyacencia)

        # botones para llenar trayectoria 2 y 3
        self.ui.pushButton.clicked.connect(self.llenar_k2)
        self.ui.pushButton_2.clicked.connect(self.llenar_k3)

        self.nodos = []
        self.aristas = []

    def dibujar_grafo(self):

            self.scene.clear()
            self.nodos.clear()
            self.aristas.clear()

            matriz = self.obtener_matriz()

            self.dibujar_nodos_y_aristas(matriz)

    def obtener_matriz(self):
            filas = self.ui.tableWidget.rowCount()
            columnas = self.ui.tableWidget.columnCount()
            matriz = []
            for i in range(filas):
                fila = []
                for j in range(columnas):
                    item = self.ui.tableWidget.item(i, j)
                    valor = int(item.text()) if item and item.text().isdigit() else 0
                    fila.append(valor)
                matriz.append(fila)
            return matriz
        

    def dibujar_nodos_y_aristas(self, matriz):
            num_nodos = len(matriz)
            radius = 20
            width = self.graphicsView.width() - 100
            height = self.graphicsView.height() - 100

          
            for i in range(num_nodos):
                x = random.randint(50, width)  
                y = random.randint(50, height)  
                nodo = Nodo(x, y, radius, i + 1, self)
                nodo.setPos(x, y) 
                self.scene.addItem(nodo)
                self.nodos.append(nodo)

            for i in range(num_nodos):
                for j in range(i + 1, num_nodos):
                    peso = matriz[i][j]
                    if peso > 0:
                        nodo1 = self.nodos[i]
                        nodo2 = self.nodos[j]

                        arista = Arista(nodo1, nodo2, peso, self.scene)
                        self.aristas.append(arista)
                        self.scene.addItem(arista)

                        nodo1.agregar_arista(arista)
                        nodo2.agregar_arista(arista)


    def llenar_matriz_aleatoria(self, index):
        """Llena toda la matriz con valores aleatorios entre 0 y 100, con 0 en las diagonales."""
        filas = self.ui.tableWidget.rowCount()
        columnas = self.ui.tableWidget.columnCount()

        for i in range(filas):
            for j in range(columnas):
                if i == j:
                    self.ui.tableWidget.setItem(i, j, QtWidgets.QTableWidgetItem('0'))  
                else:
                    valor = random.choice([0, random.randint(1, 100)]) 
                    self.ui.tableWidget.setItem(i, j, QtWidgets.QTableWidgetItem(str(valor)))
    


    def generar_tabla_adyacencia(self):
          
            matriz_pesos = self.obtener_matriz()
            filas = len(matriz_pesos)
            columnas = len(matriz_pesos[0]) if filas > 0 else 0
            self.ui.tableWidget_2.setRowCount(filas)
            self.ui.tableWidget_2.setColumnCount(columnas)

            for i in range(filas):
                for j in range(columnas):
                    if matriz_pesos[i][j] > 0:
                        self.ui.tableWidget_2.setItem(i, j, QtWidgets.QTableWidgetItem('1'))  
                    else:
                        self.ui.tableWidget_2.setItem(i, j, QtWidgets.QTableWidgetItem('0'))  

    def obtener_matriz_adyacencia(self):
            filas = self.ui.tableWidget_2.rowCount()
            columnas = self.ui.tableWidget_2.columnCount()
            matriz = []
            for i in range(filas):
                fila = []
                for j in range(columnas):
                    item = self.ui.tableWidget_2.item(i, j)  
                    valor = int(item.text()) if item and item.text().isdigit() else 0
                    fila.append(valor)
                matriz.append(fila)
            return matriz
        

    def calcular_k_trayectoria(self, k):

            # Obtener la matriz de adyacencia a través del método de la clase
            matriz_adyacencia = self.obtener_matriz_adyacencia()

            if not matriz_adyacencia:
                print("La matriz de adyacencia está vacía.")
                return None

            # Convertir la matriz de adyacencia a un arreglo de numpy
            A = np.array(matriz_adyacencia)
            A_k = np.linalg.matrix_power(A, k)  # Elevar la matriz a la potencia k
            return A_k



    def llenar_k2(self):
        k2 = self.calcular_k_trayectoria(2)
        filas = len(k2)
        columnas = len(k2[0]) if filas > 0 else 0

        self.ui.tableWidget_3.setRowCount(filas)
        self.ui.tableWidget_3.setColumnCount(columnas)

        for i in range(filas):
            for j in range(columnas):
                item = QtWidgets.QTableWidgetItem(str(k2[i][j]))
                self.ui.tableWidget_3.setItem(i, j, item)

    def llenar_k3(self):
        k3 = self.calcular_k_trayectoria(3)
        filas = len(k3)
        columnas = len(k3[0]) if filas > 0 else 0

        self.ui.tableWidget_4.setRowCount(filas)
        self.ui.tableWidget_4.setColumnCount(columnas)

        for i in range(filas):
            for j in range(columnas):
                item = QtWidgets.QTableWidgetItem(str(k3[i][j]))
                self.ui.tableWidget_4.setItem(i, j, item)


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = GrafoApp()
    window.show()
    sys.exit(app.exec_())
