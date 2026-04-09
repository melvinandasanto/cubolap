import sys
import os

# Compatibilidad con PyQt6 para Matplotlib
os.environ["QT_API"] = "pyqt6"

import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QPushButton, QFrame, QScrollArea, QComboBox, QMessageBox,
    QTableWidget, QTableWidgetItem, QHeaderView
)
from PyQt6.QtCore import Qt


class PantallaAnalisisDinamico(QMainWindow):
    def __init__(self, modelo_datos=None):
        super().__init__()
        self.setWindowTitle("Sistema OLAP - Dashboard Adaptativo")
        self.resize(1400, 900)

        self.modelo_datos = modelo_datos

        self.df_hechos = None
        self.df_analisis = None

        self.entidad_hechos_actual = None
        self.entidad_dim1_actual = None
        self.entidad_dim2_actual = None

        self.relacion_dim1 = None
        self.relacion_dim2 = None

        self.setStyleSheet("""
            QMainWindow { background-color: #0d1b2a; }
            QWidget { color: white; font-family: 'Segoe UI'; }

            QFrame#PanelControl {
                background-color: #1b263b; border-right: 2px solid #3d85c6;
            }

            QLabel#TituloSeccion {
                font-weight: bold; color: #3d85c6; font-size: 14px;
                text-transform: uppercase; margin-bottom: 5px;
            }

            QTableWidget#TablaPivot {
                background-color: #1b263b; border: 1px solid #3d85c6;
                gridline-color: #243447; color: #ffffff;
                border-radius: 8px;
            }

            QHeaderView::section {
                background-color: #243447; color: #3d85c6;
                font-weight: bold; border: 1px solid #0d1b2a;
            }

            QFrame#GraficoCard {
                background-color: #1b263b; border-radius: 12px; border: 1px solid #243447;
            }

            QComboBox {
                background-color: #415a77; border: 1px solid #3d85c6;
                border-radius: 5px; padding: 8px; color: white;
            }

            QPushButton#BtnAplicar {
                background-color: #2ecc71; color: white; font-weight: bold;
                padding: 15px; border-radius: 5px;
            }

            QPushButton#BtnSalir {
                background-color: #c63d3d; font-weight: bold; padding: 10px; border-radius: 5px;
            }
        """)

        self.init_ui()
        self.cargar_modelo()

    # =========================================================
    # UI
    # =========================================================
    def init_ui(self):
        central = QWidget()
        self.setCentralWidget(central)
        layout_principal = QHBoxLayout(central)
        layout_principal.setSpacing(0)
        layout_principal.setContentsMargins(0, 0, 0, 0)

        # PANEL LATERAL
        self.panel_config = QFrame()
        self.panel_config.setObjectName("PanelControl")
        self.panel_config.setFixedWidth(320)
        ly_config = QVBoxLayout(self.panel_config)
        ly_config.setContentsMargins(20, 20, 20, 20)

        lbl_campos = QLabel("CONFIGURACIÓN OLAP")
        lbl_campos.setObjectName("TituloSeccion")
        ly_config.addWidget(lbl_campos)

        ly_config.addSpacing(15)

        ly_config.addWidget(QLabel("TABLA DE HECHOS:"))
        self.combo_hechos = QComboBox()
        self.combo_hechos.currentIndexChanged.connect(self.cambiar_configuracion_modelo)
        ly_config.addWidget(self.combo_hechos)

        ly_config.addSpacing(12)

        ly_config.addWidget(QLabel("DIMENSIÓN 1:"))
        self.combo_dim1_entidad = QComboBox()
        self.combo_dim1_entidad.currentIndexChanged.connect(self.cambiar_configuracion_modelo)
        ly_config.addWidget(self.combo_dim1_entidad)

        ly_config.addSpacing(12)

        ly_config.addWidget(QLabel("DIMENSIÓN 2 (OPCIONAL):"))
        self.combo_dim2_entidad = QComboBox()
        self.combo_dim2_entidad.currentIndexChanged.connect(self.cambiar_configuracion_modelo)
        ly_config.addWidget(self.combo_dim2_entidad)

        ly_config.addSpacing(12)

        ly_config.addWidget(QLabel("CAMPO EN FILAS:"))
        self.combo_filas = QComboBox()
        ly_config.addWidget(self.combo_filas)

        ly_config.addSpacing(12)

        ly_config.addWidget(QLabel("CAMPO EN COLUMNAS:"))
        self.combo_columnas = QComboBox()
        ly_config.addWidget(self.combo_columnas)

        ly_config.addSpacing(12)

        ly_config.addWidget(QLabel("VALOR:"))
        self.combo_valor = QComboBox()
        ly_config.addWidget(self.combo_valor)

        ly_config.addSpacing(12)

        ly_config.addWidget(QLabel("AGREGACIÓN:"))
        self.combo_agregacion = QComboBox()
        self.combo_agregacion.addItems(["suma", "promedio", "conteo", "máximo", "mínimo"])
        ly_config.addWidget(self.combo_agregacion)

        ly_config.addSpacing(12)

        ly_config.addWidget(QLabel("FILTRO 1 (OPCIONAL):"))
        self.combo_filtro_campo = QComboBox()
        self.combo_filtro_campo.currentIndexChanged.connect(self.actualizar_valores_filtro)
        ly_config.addWidget(self.combo_filtro_campo)

        ly_config.addSpacing(12)

        ly_config.addWidget(QLabel("VALOR DEL FILTRO:"))
        self.combo_filtro_valor = QComboBox()
        ly_config.addWidget(self.combo_filtro_valor)

        ly_config.addSpacing(20)

        self.lbl_estado = QLabel("Configure hechos, dimensiones, valor, agregación y filtro.")
        self.lbl_estado.setStyleSheet("color: #a0aeba; font-size: 12px;")
        self.lbl_estado.setWordWrap(True)
        ly_config.addWidget(self.lbl_estado)

        ly_config.addSpacing(20)

        self.btn_aplicar = QPushButton("ACTUALIZAR VISTA")
        self.btn_aplicar.setObjectName("BtnAplicar")
        self.btn_aplicar.clicked.connect(self.refrescar_analisis)
        ly_config.addWidget(self.btn_aplicar)

        ly_config.addStretch()

        self.btn_salir = QPushButton("Cerrar Dashboard")
        self.btn_salir.setObjectName("BtnSalir")
        self.btn_salir.clicked.connect(self.close)
        ly_config.addWidget(self.btn_salir)

        layout_principal.addWidget(self.panel_config)

        # ÁREA CENTRAL
        container_central = QWidget()
        self.layout_central = QVBoxLayout(container_central)

        self.lbl_modelo = QLabel("MODELO CARGADO")
        self.lbl_modelo.setObjectName("TituloSeccion")
        self.layout_central.addWidget(self.lbl_modelo)

        lbl_resumen_tit = QLabel("VISTA DE RESUMEN (TABLA DINÁMICA)")
        lbl_resumen_tit.setObjectName("TituloSeccion")
        self.layout_central.addWidget(lbl_resumen_tit)

        self.tabla_resumen = QTableWidget()
        self.tabla_resumen.setObjectName("TablaPivot")
        self.tabla_resumen.setFixedHeight(240)
        self.tabla_resumen.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.layout_central.addWidget(self.tabla_resumen)

        self.layout_central.addSpacing(20)

        self.scroll = QScrollArea()
        self.scroll.setWidgetResizable(True)
        self.scroll.setStyleSheet("border: none; background: transparent;")

        self.widget_graficos = QWidget()
        self.layout_grid = QVBoxLayout(self.widget_graficos)

        self.lbl_info = QLabel("Configure filas, columnas, valor y filtro; luego presione 'Actualizar vista'.")
        self.lbl_info.setStyleSheet("font-size: 16px; color: #3d85c6;")
        self.layout_grid.addWidget(self.lbl_info, alignment=Qt.AlignmentFlag.AlignCenter)

        self.scroll.setWidget(self.widget_graficos)
        self.layout_central.addWidget(self.scroll)

        layout_principal.addWidget(container_central)

    # =========================================================
    # CARGA DEL MODELO
    # =========================================================
    def cargar_modelo(self):
        if not self.modelo_datos or not self.modelo_datos.get("entidades"):
            QMessageBox.warning(self, "Aviso", "No se recibió un modelo de datos válido.")
            return

        entidades_cargadas = []
        for nombre, entidad in self.modelo_datos["entidades"].items():
            df = entidad.get("dataframe")
            if df is not None and not df.empty:
                entidades_cargadas.append(nombre)

        if not entidades_cargadas:
            QMessageBox.warning(self, "Aviso", "No hay entidades con datos cargados.")
            return

        self.combo_hechos.clear()
        self.combo_dim1_entidad.clear()
        self.combo_dim2_entidad.clear()
        self.combo_filas.clear()
        self.combo_columnas.clear()
        self.combo_valor.clear()
        self.combo_filtro_campo.clear()
        self.combo_filtro_valor.clear()

        self.combo_hechos.addItems(entidades_cargadas)
        self.combo_dim1_entidad.addItems(entidades_cargadas)
        self.combo_dim2_entidad.addItem("(Ninguna)")
        self.combo_dim2_entidad.addItems(entidades_cargadas)

        self.lbl_modelo.setText(
            f"MODELO CARGADO: {self.modelo_datos.get('nombre_origen', 'Origen desconocido')}"
        )

        if len(entidades_cargadas) >= 2:
            self.combo_hechos.setCurrentIndex(0)
            self.combo_dim1_entidad.setCurrentIndex(1)
        else:
            self.combo_hechos.setCurrentIndex(0)
            self.combo_dim1_entidad.setCurrentIndex(0)

        self.combo_dim2_entidad.setCurrentIndex(0)
        self.cambiar_configuracion_modelo()

    # =========================================================
    # RELACIONES
    # =========================================================
    def obtener_relaciones_entre(self, entidad_a, entidad_b):
        relaciones_encontradas = []

        if not self.modelo_datos:
            return relaciones_encontradas

        for rel in self.modelo_datos.get("relaciones", []):
            origen = rel.get("origen_entidad")
            destino = rel.get("destino_entidad")

            if (origen == entidad_a and destino == entidad_b) or (origen == entidad_b and destino == entidad_a):
                relaciones_encontradas.append(rel)

        return relaciones_encontradas

    def obtener_primera_relacion(self, entidad_a, entidad_b):
        relaciones = self.obtener_relaciones_entre(entidad_a, entidad_b)
        return relaciones[0] if relaciones else None

    # =========================================================
    # CONFIGURACIÓN
    # =========================================================
    def cambiar_configuracion_modelo(self):
        hechos = self.combo_hechos.currentText().strip()
        dim1 = self.combo_dim1_entidad.currentText().strip()
        dim2 = self.combo_dim2_entidad.currentText().strip()

        self.combo_filas.clear()
        self.combo_columnas.clear()
        self.combo_valor.clear()
        self.combo_filtro_campo.clear()
        self.combo_filtro_valor.clear()

        self.relacion_dim1 = None
        self.relacion_dim2 = None
        self.df_hechos = None
        self.df_analisis = None

        if not hechos:
            return

        entidad_hechos = self.modelo_datos["entidades"].get(hechos)
        if not entidad_hechos:
            return

        self.df_hechos = entidad_hechos.get("dataframe")
        self.entidad_hechos_actual = hechos
        self.entidad_dim1_actual = dim1 if dim1 else None
        self.entidad_dim2_actual = None if dim2 == "(Ninguna)" else dim2

        if self.df_hechos is None or self.df_hechos.empty:
            self.lbl_estado.setText("La tabla de hechos no tiene datos.")
            return

        medidas = self.df_hechos.select_dtypes(include=["number"]).columns.tolist()
        self.combo_valor.addItems(medidas)

        campos_filas = []
        campos_columnas = []

        if dim1:
            self.relacion_dim1 = self.obtener_primera_relacion(hechos, dim1)
            if self.relacion_dim1:
                df_dim1 = self.modelo_datos["entidades"][dim1]["dataframe"]
                cols_dim1 = self.obtener_campos_dimensionales(df_dim1)
                campos_filas.extend([f"{dim1}.{c}" for c in cols_dim1])
            else:
                self.lbl_estado.setText(f"No se detectó relación entre {hechos} y {dim1}.")

        if self.entidad_dim2_actual:
            self.relacion_dim2 = self.obtener_primera_relacion(hechos, self.entidad_dim2_actual)
            if self.relacion_dim2:
                df_dim2 = self.modelo_datos["entidades"][self.entidad_dim2_actual]["dataframe"]
                cols_dim2 = self.obtener_campos_dimensionales(df_dim2)
                campos_columnas.extend([f"{self.entidad_dim2_actual}.{c}" for c in cols_dim2])

        cols_hechos_dim = self.obtener_campos_dimensionales(self.df_hechos)
        campos_filas.extend([f"{hechos}.{c}" for c in cols_hechos_dim])
        campos_columnas = ["(Ninguna)"] + campos_columnas + [f"{hechos}.{c}" for c in cols_hechos_dim]

        campos_filas = list(dict.fromkeys(campos_filas))
        campos_columnas = list(dict.fromkeys(campos_columnas))

        self.combo_filas.addItems(campos_filas)
        self.combo_columnas.addItems(campos_columnas)

        self.actualizar_campos_filtro()

        texto_estado = f"Hechos: {hechos} | Dim1: {dim1 if dim1 else 'N/A'}"
        if self.entidad_dim2_actual:
            texto_estado += f" | Dim2: {self.entidad_dim2_actual}"
        self.lbl_estado.setText(texto_estado)

    def obtener_campos_dimensionales(self, df):
        if df is None or df.empty:
            return []

        campos = df.select_dtypes(include=["object", "category", "datetime64[ns]"]).columns.tolist()

        if not campos:
            columnas_numericas = df.select_dtypes(include=["number"]).columns.tolist()
            campos = [c for c in df.columns if c not in columnas_numericas]

        return campos

    # =========================================================
    # FILTROS
    # =========================================================
    def actualizar_campos_filtro(self):
        self.combo_filtro_campo.clear()
        self.combo_filtro_valor.clear()

        self.combo_filtro_campo.addItem("(Ninguno)")

        campos_disponibles = []
        campos_disponibles.extend([self.combo_filas.itemText(i) for i in range(self.combo_filas.count())])

        for i in range(self.combo_columnas.count()):
            texto = self.combo_columnas.itemText(i)
            if texto != "(Ninguna)":
                campos_disponibles.append(texto)

        campos_disponibles = list(dict.fromkeys(campos_disponibles))

        for campo in campos_disponibles:
            self.combo_filtro_campo.addItem(campo)

    def actualizar_valores_filtro(self):
        self.combo_filtro_valor.clear()

        campo_filtro = self.combo_filtro_campo.currentText().strip()

        if not campo_filtro or campo_filtro == "(Ninguno)":
            self.combo_filtro_valor.addItem("(Todos)")
            return

        try:
            df_temp = self.construir_dataframe_analisis()
            if campo_filtro not in df_temp.columns:
                self.combo_filtro_valor.addItem("(Todos)")
                return

            self.combo_filtro_valor.addItem("(Todos)")

            valores = (
                df_temp[campo_filtro]
                .dropna()
                .astype(str)
                .sort_values()
                .unique()
                .tolist()
            )

            for valor in valores:
                self.combo_filtro_valor.addItem(valor)

        except Exception:
            self.combo_filtro_valor.addItem("(Todos)")

    def aplicar_filtro(self, df):
        campo_filtro = self.combo_filtro_campo.currentText().strip()
        valor_filtro = self.combo_filtro_valor.currentText().strip()

        if not campo_filtro or campo_filtro == "(Ninguno)":
            return df

        if not valor_filtro or valor_filtro == "(Todos)":
            return df

        if campo_filtro not in df.columns:
            return df

        return df[df[campo_filtro].astype(str) == valor_filtro].copy()

    # =========================================================
    # MERGES
    # =========================================================
    def aplicar_relacion(self, df_base, entidad_origen_base, entidad_destino, relacion):
        if not relacion:
            return df_base

        df_destino = self.modelo_datos["entidades"][entidad_destino]["dataframe"]

        if df_destino is None or df_destino.empty:
            raise Exception(f"La entidad '{entidad_destino}' no tiene datos.")

        if relacion["origen_entidad"] == entidad_origen_base and relacion["destino_entidad"] == entidad_destino:
            left_on = relacion["origen_columna"]
            right_on = relacion["destino_columna"]
        elif relacion["origen_entidad"] == entidad_destino and relacion["destino_entidad"] == entidad_origen_base:
            left_on = relacion["destino_columna"]
            right_on = relacion["origen_columna"]
        else:
            raise Exception(f"La relación no coincide con {entidad_origen_base} y {entidad_destino}")

        if left_on not in df_base.columns:
            raise Exception(f"La columna '{left_on}' no existe en la tabla base")

        if right_on not in df_destino.columns:
            raise Exception(f"La columna '{right_on}' no existe en '{entidad_destino}'")

        columnas_destino = []
        for col in df_destino.columns:
            if col == right_on:
                columnas_destino.append(col)
            else:
                columnas_destino.append(f"{entidad_destino}.{col}")

        df_destino_ren = df_destino.copy()
        df_destino_ren.columns = columnas_destino

        right_on_ren = right_on

        df_merge = df_base.merge(
            df_destino_ren,
            left_on=left_on,
            right_on=right_on_ren,
            how="left"
        )

        return df_merge

    def construir_merge_con_hechos(self, df_hechos, entidad_hechos, entidad_dim, relacion):
        df_dim = self.modelo_datos["entidades"][entidad_dim]["dataframe"]

        if df_dim is None or df_dim.empty:
            raise Exception(f"La entidad '{entidad_dim}' no tiene datos.")

        if relacion["origen_entidad"] == entidad_hechos and relacion["destino_entidad"] == entidad_dim:
            left_on = relacion["origen_columna"]
            right_on = relacion["destino_columna"]
        elif relacion["origen_entidad"] == entidad_dim and relacion["destino_entidad"] == entidad_hechos:
            left_on = relacion["destino_columna"]
            right_on = relacion["origen_columna"]
        else:
            raise Exception("La relación seleccionada no coincide con las entidades elegidas.")

        if left_on not in df_hechos.columns:
            raise Exception(f"La columna '{left_on}' no existe en la tabla de hechos.")

        if right_on not in df_dim.columns:
            raise Exception(f"La columna '{right_on}' no existe en la tabla de dimensión.")

        columnas_dim_ren = []
        for col in df_dim.columns:
            if col == right_on:
                columnas_dim_ren.append(col)
            else:
                columnas_dim_ren.append(f"{entidad_dim}.{col}")

        df_dim_ren = df_dim.copy()
        df_dim_ren.columns = columnas_dim_ren

        df_merge = df_hechos.merge(
            df_dim_ren,
            left_on=left_on,
            right_on=right_on,
            how="left"
        )

        return df_merge

    def construir_dataframe_analisis(self):
        if self.df_hechos is None or self.df_hechos.empty:
            raise Exception("La tabla de hechos no tiene datos.")

        df_original_hechos = self.modelo_datos["entidades"][self.entidad_hechos_actual]["dataframe"].copy()

        if self.entidad_dim1_actual and self.relacion_dim1:
            df = self.construir_merge_con_hechos(
                df_original_hechos,
                self.entidad_hechos_actual,
                self.entidad_dim1_actual,
                self.relacion_dim1
            )
        else:
            df = df_original_hechos.copy()

        if self.entidad_dim2_actual and self.relacion_dim2:
            df = self.aplicar_relacion(
                df,
                self.entidad_hechos_actual,
                self.entidad_dim2_actual,
                self.relacion_dim2
            )

        cols_finales = []
        for col in df.columns:
            if "." in str(col):
                cols_finales.append(col)
            elif col in df_original_hechos.columns:
                cols_finales.append(f"{self.entidad_hechos_actual}.{col}")
            else:
                cols_finales.append(col)
        df.columns = cols_finales

        return df

    # =========================================================
    # AGREGACIONES
    # =========================================================
    def obtener_aggfunc(self):
        opcion = self.combo_agregacion.currentText().strip().lower()

        mapa = {
            "suma": "sum",
            "promedio": "mean",
            "conteo": "count",
            "máximo": "max",
            "mínimo": "min"
        }

        return mapa.get(opcion, "sum")

    def formatear_valor(self, valor):
        try:
            return f"{float(valor):,.2f}"
        except Exception:
            return str(valor)

    # =========================================================
    # ANÁLISIS
    # =========================================================
    def refrescar_analisis(self):
        campo_filas = self.combo_filas.currentText().strip()
        campo_columnas = self.combo_columnas.currentText().strip()
        valor = self.combo_valor.currentText().strip()
        aggfunc = self.obtener_aggfunc()

        if not campo_filas:
            QMessageBox.warning(self, "Aviso", "Debe seleccionar un campo en filas.")
            return

        if not valor:
            QMessageBox.warning(self, "Aviso", "Debe seleccionar un valor.")
            return

        try:
            self.df_analisis = self.construir_dataframe_analisis()
            self.df_analisis = self.aplicar_filtro(self.df_analisis)

            valor_real = valor if "." in valor else f"{self.entidad_hechos_actual}.{valor}"
            if valor_real not in self.df_analisis.columns and valor in self.df_analisis.columns:
                valor_real = valor

            if campo_filas not in self.df_analisis.columns:
                raise Exception(f"El campo de filas '{campo_filas}' no existe.")

            if valor_real not in self.df_analisis.columns:
                raise Exception(f"El valor '{valor}' no existe.")

            if campo_columnas and campo_columnas != "(Ninguna)":
                if campo_columnas not in self.df_analisis.columns:
                    raise Exception(f"El campo de columnas '{campo_columnas}' no existe.")

                resumen = pd.pivot_table(
                    self.df_analisis,
                    index=campo_filas,
                    columns=campo_columnas,
                    values=valor_real,
                    aggfunc=aggfunc,
                    fill_value=0
                )
                self.mostrar_pivot_completa(resumen)
                self.regenerar_graficos_desde_pivot(resumen, campo_filas, valor_real, aggfunc)
            else:
                resumen = (
                    self.df_analisis
                    .groupby(campo_filas, dropna=False)[valor_real]
                    .agg(aggfunc)
                    .reset_index()
                )
                self.mostrar_resumen_simple(resumen, campo_filas, valor_real, aggfunc)
                self.regenerar_graficos_simple(campo_filas, valor_real, aggfunc)

        except Exception as e:
            QMessageBox.critical(self, "Error", f"No se pudo generar el análisis.\n\n{str(e)}")

    def mostrar_resumen_simple(self, resumen, campo_filas, valor_real, aggfunc):
        self.tabla_resumen.clear()
        self.tabla_resumen.setColumnCount(2)
        self.tabla_resumen.setRowCount(len(resumen))
        self.tabla_resumen.setHorizontalHeaderLabels(
            [f"ETIQUETA: {campo_filas}", f"{aggfunc.upper()} DE {valor_real}"]
        )

        for i, row in resumen.iterrows():
            self.tabla_resumen.setItem(i, 0, QTableWidgetItem(str(row[campo_filas])))
            item_valor = QTableWidgetItem(self.formatear_valor(row[valor_real]))
            item_valor.setTextAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
            self.tabla_resumen.setItem(i, 1, item_valor)

    def mostrar_pivot_completa(self, pivot_df):
        self.tabla_resumen.clear()

        filas = pivot_df.shape[0]
        columnas = pivot_df.shape[1] + 1

        self.tabla_resumen.setRowCount(filas)
        self.tabla_resumen.setColumnCount(columnas)

        encabezados = [str(pivot_df.index.name)] + [str(c) for c in pivot_df.columns]
        self.tabla_resumen.setHorizontalHeaderLabels(encabezados)

        for i in range(filas):
            self.tabla_resumen.setItem(i, 0, QTableWidgetItem(str(pivot_df.index[i])))
            for j in range(pivot_df.shape[1]):
                valor = pivot_df.iat[i, j]
                item = QTableWidgetItem(self.formatear_valor(valor))
                item.setTextAlignment(Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)
                self.tabla_resumen.setItem(i, j + 1, item)

    # =========================================================
    # GRÁFICOS
    # =========================================================
    def regenerar_graficos_simple(self, campo_filas, valor_real, aggfunc):
        self.limpiar_layout(self.layout_grid)

        f1 = QHBoxLayout()
        f2 = QHBoxLayout()

        f1.addWidget(self.crear_canvas_simple(f"Comparativo de {valor_real}", "bar", campo_filas, valor_real, aggfunc))
        f1.addWidget(self.crear_canvas_simple("Distribución %", "pie", campo_filas, valor_real, aggfunc))
        f2.addWidget(self.crear_canvas_simple("Evolución", "line", campo_filas, valor_real, aggfunc))
        f2.addWidget(self.crear_canvas_simple("Análisis de Puntos", "scatter", campo_filas, valor_real, aggfunc))

        self.layout_grid.addLayout(f1)
        self.layout_grid.addLayout(f2)

    def regenerar_graficos_desde_pivot(self, pivot_df, campo_filas, valor_real, aggfunc):
        self.limpiar_layout(self.layout_grid)

        serie = pivot_df.sum(axis=1)

        f1 = QHBoxLayout()
        f2 = QHBoxLayout()

        f1.addWidget(self.crear_canvas_serie(f"Comparativo de {valor_real}", "bar", serie, campo_filas, valor_real))
        f1.addWidget(self.crear_canvas_serie("Distribución %", "pie", serie, campo_filas, valor_real))
        f2.addWidget(self.crear_canvas_serie("Evolución", "line", serie, campo_filas, valor_real))
        f2.addWidget(self.crear_canvas_serie("Análisis de Puntos", "scatter", serie, campo_filas, valor_real))

        self.layout_grid.addLayout(f1)
        self.layout_grid.addLayout(f2)

    def limpiar_layout(self, layout):
        while layout.count():
            item = layout.takeAt(0)

            if item.widget():
                item.widget().deleteLater()
            elif item.layout():
                self.limpiar_layout(item.layout())

    def crear_canvas_simple(self, titulo, tipo, eje_x, eje_y, aggfunc):
        resumen = self.df_analisis.groupby(eje_x, dropna=False)[eje_y].agg(aggfunc)
        return self.crear_canvas_serie(titulo, tipo, resumen, eje_x, eje_y)

    def crear_canvas_serie(self, titulo, tipo, serie, eje_x, eje_y):
        card = QFrame()
        card.setObjectName("GraficoCard")
        ly = QVBoxLayout(card)
        ly.addWidget(QLabel(titulo))

        plt.rcParams.update({
            "text.color": "white",
            "axes.labelcolor": "white",
            "xtick.color": "#a0aeba",
            "ytick.color": "#a0aeba",
            "axes.facecolor": "#1b263b",
            "figure.facecolor": "#1b263b"
        })

        fig, ax = plt.subplots(figsize=(5, 3), dpi=85)

        try:
            if tipo == "bar":
                serie.plot(kind='bar', ax=ax, color='#3d85c6')
                ax.set_xlabel(eje_x)
                ax.set_ylabel(eje_y)

            elif tipo == "line":
                serie.plot(kind='line', ax=ax, marker='o', color='#2ecc71')
                ax.set_xlabel(eje_x)
                ax.set_ylabel(eje_y)

            elif tipo == "pie":
                if len(serie) > 0:
                    serie.plot(kind='pie', ax=ax, autopct='%1.1f%%')
                    ax.set_ylabel("")

            elif tipo == "scatter":
                ax.scatter(range(len(serie)), serie.values, color='#e67e22')
                ax.set_xlabel(eje_x)
                ax.set_ylabel(eje_y)
                ax.set_xticks(range(len(serie)))
                ax.set_xticklabels([str(i) for i in serie.index], rotation=45, ha="right")

        except Exception:
            ax.text(0.5, 0.5, "No se pudo generar", ha='center', va='center')
            ax.set_axis_off()

        plt.tight_layout()
        ly.addWidget(FigureCanvas(fig))
        return card


if __name__ == "__main__":
    app = QApplication(sys.argv)

    df_ventas = pd.DataFrame({
        "id_venta": [1, 2, 3, 4, 5],
        "id_cliente": [10, 10, 20, 30, 20],
        "id_producto": [100, 200, 100, 300, 200],
        "monto": [100, 150, 200, 80, 120]
    })

    df_clientes = pd.DataFrame({
        "id_cliente": [10, 20, 30],
        "region": ["Norte", "Sur", "Centro"],
        "tipo_cliente": ["Minorista", "Mayorista", "Minorista"]
    })

    df_productos = pd.DataFrame({
        "id_producto": [100, 200, 300],
        "categoria": ["Bebidas", "Snacks", "Limpieza"],
        "marca": ["A", "B", "C"]
    })

    modelo_prueba = {
        "tipo_origen": "conexion",
        "nombre_origen": "prueba_relacional",
        "entidades": {
            "ventas": {
                "nombre": "ventas",
                "tipo": "tabla",
                "columnas": [],
                "filas": len(df_ventas),
                "preview": df_ventas.head(),
                "dataframe": df_ventas
            },
            "clientes": {
                "nombre": "clientes",
                "tipo": "tabla",
                "columnas": [],
                "filas": len(df_clientes),
                "preview": df_clientes.head(),
                "dataframe": df_clientes
            },
            "productos": {
                "nombre": "productos",
                "tipo": "tabla",
                "columnas": [],
                "filas": len(df_productos),
                "preview": df_productos.head(),
                "dataframe": df_productos
            }
        },
        "relaciones": [
            {
                "nombre_relacion": "ventas_clientes",
                "origen_entidad": "ventas",
                "origen_columna": "id_cliente",
                "destino_entidad": "clientes",
                "destino_columna": "id_cliente"
            },
            {
                "nombre_relacion": "ventas_productos",
                "origen_entidad": "ventas",
                "origen_columna": "id_producto",
                "destino_entidad": "productos",
                "destino_columna": "id_producto"
            }
        ]
    }

    win = PantallaAnalisisDinamico(modelo_prueba)
    win.show()
    sys.exit(app.exec())