import sys
from PyQt6.QtWidgets import (QApplication, QMainWindow,
                             QLabel, QPushButton, QDockWidget,
                             QStatusBar, QTabWidget, QWidget, QHBoxLayout,
                             QVBoxLayout,QGridLayout, QListWidget, QFileDialog, QListWidgetItem,
                            QSlider)
from PyQt6.QtMultimedia import QMediaPlayer, QAudioOutput
from PyQt6.QtCore import QUrl
from PyQt6.QtGui import QPixmap, QAction, QKeySequence, QIcon
from PyQt6.QtCore import Qt, QStandardPaths
import os
import random

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        
        self.initialize_ui()
        self.setWindowIcon(QIcon("images/headphones_logo.png"))
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)
        self.current_music_folder = ""
        with open("styles/estilos.css", 'r') as file:
            style = file.read()
        
        self.setStyleSheet(style)
        self.player = None
        self.playing_reproductor = False
        self.tipo_reproduccion = ""
        self.volumen = 0.5
    
    def initialize_ui(self):
        self.setGeometry(300,50,700,650)
        self.setMaximumSize(700,650)
        self.setMinimumSize(700, 650)
        self.setWindowTitle("Reproductor de Musica")
        self.generate_main_window()
        self.create_dock()
        self.create_action()
        self.create_menu()
        self.show()
        
    def generate_main_window(self):
        tab_bar = QTabWidget(self)
        self.reproductor_container = QWidget()
        self.reproductor_container.setObjectName("reproductor")
        self.settings_container = QWidget()
        self.settings_container.setObjectName("settings")
        tab_bar.addTab(self.reproductor_container, "Reproductor")
        tab_bar.addTab(self.settings_container, "Settings")
        
        self.generate_reproductor_tab()
        self.generate_settings_tab()
        
        tab_h_box = QHBoxLayout()
        tab_h_box.addWidget(tab_bar)
        
        main_container = QWidget()
        main_container.setLayout(tab_h_box)
        self.setCentralWidget(main_container)
        
    def generate_reproductor_tab(self):
        main_v_box = QVBoxLayout()
        buttons_h_box = QHBoxLayout()
        
        song_image  = QLabel()
        
        song_image.setMaximumSize(700,480)
        song_image.setMinimumSize(450,450)
        pixmap = QPixmap("images/song.png").scaled(512, 512)
        song_image.setPixmap(pixmap)
        song_image.setScaledContents(True)
        
        self.button_repeat = QPushButton()
        self.button_repeat.setObjectName("repeat")
        self.button_repeat.setFixedSize(40,40)
        self.button_repeat.clicked.connect(self.repeat_songs)
        self.button_before = QPushButton()
        self.button_before.setObjectName("before")
        self.button_before.setFixedSize(40,40)
        self.button_before.clicked.connect(self.before_song)
        self.button_play = QPushButton()
        self.button_play.setObjectName("play")
        self.button_play.setFixedSize(50,50)
        self.button_play.clicked.connect(self.play_pause_song)
        self.button_next = QPushButton()
        self.button_next.setObjectName("next")
        self.button_next.setFixedSize(40,40)
        self.button_next.clicked.connect(self.next_song)
        self.button_random = QPushButton()
        self.button_random.setObjectName("random")
        self.button_random.setFixedSize(40,40)
        self.button_random.clicked.connect(self.random_song)
        buttons_h_box.addWidget(self.button_repeat)
        buttons_h_box.addWidget(self.button_before)
        buttons_h_box.addWidget(self.button_play)
        buttons_h_box.addWidget(self.button_next)
        buttons_h_box.addWidget(self.button_random)
        buttons_container = QWidget()
        buttons_container.setLayout(buttons_h_box)
        
        main_v_box.addWidget(song_image)
        main_v_box.addWidget(buttons_container)
        
        self.reproductor_container.setLayout(main_v_box)
        
    def generate_settings_tab(self):
        main_v_box = QVBoxLayout()
        grid_layout = QGridLayout()
        buttons_h_box = QHBoxLayout()
        
        lbl_volume = QLabel("Volumen:")
        lbl_volume.setObjectName("lbl_volume")
        self.volume_scale = QSlider(Qt.Orientation.Horizontal)
        self.volume_scale.setObjectName("volume")
        self.volume_scale.setMinimum(0)
        self.volume_scale.setMaximum(100)
        self.volume_scale.setValue(50)
        self.volume_scale.setTickInterval(10)
        self.volume_scale.valueChanged.connect(self.cambiar_volumen)
        self.lbl_porcentaje = QLabel("50%")
        self.lbl_porcentaje.setObjectName("lbl_porcentaje")
        
        lbl_tipo_de_reproduccion = QLabel("reproducción: ")
        lbl_tipo_de_reproduccion.setObjectName("lbl_tipo_de_reproduccion")
        
        self.button_automatic = QPushButton()
        self.button_automatic.setObjectName("btn_automatic")
        self.button_automatic.setToolTip("Automatico")
        self.button_automatic.setFixedSize(40,40)
        self.button_automatic.clicked.connect(self.tipo_reproduccion_automatic)
        
        self.button_random = QPushButton()
        self.button_random.setObjectName("btn_random")
        self.button_random.setToolTip("Aleatorio")
        self.button_random.setFixedSize(40,40)
        self.button_random.clicked.connect(self.tipo_reproduccion_random)
        
        self.button_none = QPushButton()
        self.button_none.setObjectName("btn_none")
        self.button_none.setToolTip("Ninguno")
        self.button_none.setFixedSize(40,40)
        self.button_none.clicked.connect(self.tipo_reproduccion_none)
        
        grid_layout.addWidget(lbl_volume, 0, 0, 1, 1)
        grid_layout.addWidget(self.volume_scale, 0, 1, 1, 1)
        grid_layout.addWidget(self.lbl_porcentaje, 0, 2, 1, 1)
        buttons_h_box.addWidget(self.button_automatic)
        buttons_h_box.addWidget(self.button_random)
        buttons_h_box.addWidget(self.button_none)
        buttons_container = QWidget()
        buttons_container.setLayout(buttons_h_box)
        grid_layout.addWidget(lbl_tipo_de_reproduccion, 1, 0, 1, 1)
        grid_layout.addWidget(buttons_container, 1, 1, 1, 2)
        volume_container = QWidget()
        volume_container.setFixedHeight(130)
        volume_container.setLayout(grid_layout)
        
        main_v_box.addWidget(volume_container)
        
        self.settings_container.setLayout(main_v_box)
    
    def create_action(self):
        self.listar_musica_action = QAction('Listar Musica', self, checkable=True)
        self.listar_musica_action.setShortcut(QKeySequence("Ctrl+L"))
        self.listar_musica_action.setStatusTip("Aquí puedes listar o no la música")
        self.listar_musica_action.triggered.connect(self.list_music)
        self.listar_musica_action.setChecked(True)
        
        self.open_folder_music_action = QAction('Abrir Carpeta', self)
        self.open_folder_music_action.setShortcut(QKeySequence("Ctrl+O"))
        self.open_folder_music_action.setStatusTip("Aquí puedes abrir tu carpeta de música")
        self.open_folder_music_action.triggered.connect(self.open_folder_music)
    
    def create_menu(self):
        self.menuBar()
        menu_file = self.menuBar().addMenu("File")
        menu_file.addAction(self.open_folder_music_action)
        
        menu_view = self.menuBar().addMenu("View")
        menu_view.addAction(self.listar_musica_action)
        
    def create_dock(self):
        self.songs_list = QListWidget()
        self.dock = QDockWidget()
        self.dock.setWindowTitle("Lista de canciones")
        self.dock.setAllowedAreas(
            Qt.DockWidgetArea.LeftDockWidgetArea |
            Qt.DockWidgetArea.RightDockWidgetArea 
        )
        self.songs_list.itemSelectionChanged.connect(self.handle_song_selection)
        self.dock.setWidget(self.songs_list)
        self.addDockWidget(Qt.DockWidgetArea.LeftDockWidgetArea, self.dock)
    
    def list_music(self):
        if self.listar_musica_action.isChecked():
            self.dock.show()
        else:
            self.dock.hide()
            
    def open_folder_music(self):
        initial_dir = QStandardPaths.writableLocation(
            QStandardPaths.StandardLocation.MusicLocation
        )
        try:
            self.current_music_folder = QFileDialog.getExistingDirectory(None, "Seleccionar una carpeta", initial_dir)
            mp3_icon = QIcon('images/mp3_icon.png')
            if self.current_music_folder:
                self.songs_list.clear()
                if self.player:
                    self.player.deleteLater()
                    self.create_player()
                
            for archivo in os.listdir(self.current_music_folder):
                ruta_archivo = os.path.join(self.current_music_folder, archivo)
                if ruta_archivo.endswith('.mp3'):
                    item = QListWidgetItem(archivo)
                    item.setIcon(mp3_icon)
                    self.songs_list.addItem(item)
                
            
        except FileNotFoundError as e:
            return
   
    def create_player(self):
        if self.player:
            self.player.deleteLater()
        
        self.player = QMediaPlayer()
        self.audioOutput = QAudioOutput()
        self.player.setAudioOutput(self.audioOutput)
        self.player.mediaStatusChanged.connect(self.media_status_changed)
        self.audioOutput.setVolume(self.volumen)
        
    def play_pause_song(self):
        #sí se está reproduciendo la musica el icono
        #cambia a pausa.
        selected_items = self.songs_list.selectedItems()
        if self.songs_list.currentItem() is None or selected_items == []:
            index = self.songs_list.indexFromItem(self.songs_list.item(0))
            self.songs_list.setCurrentIndex(index)
            return
        
        if self.songs_list.count() != 0:
            if self.playing_reproductor:
                self.button_play.setStyleSheet("image: url(images/stop.png);")
                self.player.pause()
                self.playing_reproductor = False
            else:
                self.button_play.setStyleSheet("image: url(images/play.png);")
                if self.player and self.songs_list.currentItem():
                    self.player.play()
                    self.playing_reproductor = True
                    return
                
                if self.tipo_reproduccion == "automatic":
                    index = self.songs_list.indexFromItem(self.songs_list.item(0))
                    self.songs_list.setCurrentIndex(index)
                elif self.tipo_reproduccion == "random":
                    self.random_song()
                else:
                    index = self.songs_list.indexFromItem(self.songs_list.item(0))
                    self.songs_list.setCurrentIndex(index)
                
                self.playing_reproductor = True
            
    def repeat_songs(self):
        if self.songs_list.count() != 0:
            index = self.songs_list.indexFromItem(self.songs_list.item(0))
            self.songs_list.setCurrentIndex(index)
            
            self.button_play.setStyleSheet("image: url(images/play.png);")
            self.player.play()
            self.playing_reproductor = True
        
    def before_song(self):
        if self.songs_list.count() != 0:
            current_row = self.songs_list.currentRow() - 1
            if current_row < 0:
                elements_list = self.songs_list.count() - 1
                index = self.songs_list.indexFromItem(self.songs_list.item(int(elements_list)))
                self.songs_list.setCurrentIndex(index)
                self.button_play.setStyleSheet("image: url(images/play.png);")
                self.player.play()
                self.playing_reproductor = True
                return
            
            index = self.songs_list.indexFromItem(self.songs_list.item(int(current_row)))
            self.songs_list.setCurrentIndex(index)
            self.button_play.setStyleSheet("image: url(images/play.png);")
            self.player.play()
            self.playing_reproductor = True
        
    def next_song(self):
        if self.songs_list.count() != 0:
            elements_list = self.songs_list.count() - 1
            current_row = self.songs_list.currentRow() + 1
            
            if current_row > elements_list:
                index = self.songs_list.indexFromItem(self.songs_list.item(0))
                self.songs_list.setCurrentIndex(index)
                
                self.button_play.setStyleSheet("image: url(images/play.png);")
                self.player.play()
                self.playing_reproductor = True
                return
                
            index = self.songs_list.indexFromItem(self.songs_list.item(int(current_row)))
            self.songs_list.setCurrentIndex(index)
            
            self.button_play.setStyleSheet("image: url(images/play.png);")
            self.player.play()
            self.playing_reproductor = True
            
        
    def random_song(self):
        if self.songs_list.count() != 0:
            while True:
                position = random.randint(0,self.songs_list.count() - 1)
                if position == self.songs_list.currentRow():
                    continue
                
                index = self.songs_list.indexFromItem(self.songs_list.item(position))
                self.songs_list.setCurrentIndex(index)
                break
                
            self.button_play.setStyleSheet("image: url(images/play.png);")
            self.player.play()
            self.playing_reproductor = True
            
    def cambiar_volumen(self):
        self.volumen = self.volume_scale.value() / 100
        porcentaje = f'{self.volume_scale.value()}%'
        
        if self.player:
            self.audioOutput.setVolume(self.volumen)
            self.lbl_porcentaje.setText(porcentaje)
        else:
            self.create_player()
            self.audioOutput.setVolume(self.volumen)
            
    def reiniciar_botones_reproduccion(self):
        self.button_automatic.setStyleSheet("""QPushButton#btn_automatic{background-color: gray;
                                            image: url(images/repeat.png);
                                            border-radius: 20px;
                                            padding: 7px;
                                            }""")
        
        self.button_random.setStyleSheet("""QPushButton#btn_random{background-color: gray;
                                            image: url(images/random.png);
                                            border-radius: 20px;
                                            padding: 7px;
                                            }""")
        
        self.button_none.setStyleSheet("""QPushButton#btn_none{
                                            background-color: gray;
                                            image: url(images/none.png);
                                            border-radius: 20px;
                                            padding: 7px;
                                        }""")
                                            
    def tipo_reproduccion_automatic(self):
        self.tipo_reproduccion = "automatic"
        self.reiniciar_botones_reproduccion()
        self.button_automatic.setStyleSheet("background-color: rgb(27,24,24)")
    
    def tipo_reproduccion_random(self):
        self.tipo_reproduccion = "random"
        self.reiniciar_botones_reproduccion()
        self.button_random.setStyleSheet("background-color: rgb(27,24,24)")
    
    def tipo_reproduccion_none(self):
        self.tipo_reproduccion = "none"
        self.reiniciar_botones_reproduccion()
        self.button_none.setStyleSheet("background-color: rgb(27,24,24)")
            

    #SLOT HANDLING.
    
    def media_status_changed(self, status):
        print('status:', status)
        if status == QMediaPlayer.MediaStatus.LoadedMedia:
            self.playing_reproductor = True
            self.player.play()
            self.button_play.setStyleSheet("image: url(images/play.png);")
            
        if status == QMediaPlayer.MediaStatus.EndOfMedia:
            self.playing_reproductor = False
            self.button_play.setStyleSheet("image: url(images/stop.png);")
            if self.tipo_reproduccion == "automatic":
                current_row = self.songs_list.currentRow() + 1
                elements = self.songs_list.count()
                
                if current_row == elements:
                    current_row = 0
                
                index = self.songs_list.indexFromItem(self.songs_list.item(current_row))
                self.songs_list.setCurrentIndex(index)
                
            if self.tipo_reproduccion == "random":
                self.random_song()
                
    def handle_song_selection(self):
        if self.player:
            self.player.deleteLater()
        
        selected_item = self.songs_list.currentItem()
        if selected_item:
            song_name = selected_item.data(0)
            song_folder_path = os.path.join(self.current_music_folder, song_name)
            #Reproduce song with the path
            self.create_player()
            source = QUrl.fromLocalFile(song_folder_path)
            self.player.setSource(source)
            self.button_play.setStyleSheet("image: url(images/play.png);")
            self.playing_reproductor = True
            
        if not self.playing_reproductor:
            self.button_play.setStyleSheet("image: url(images/play.png);")
            self.player.play()
            self.playing_reproductor = True
            
    
if __name__ == '__main__':
    app = QApplication(sys.argv)
    ventana = MainWindow()
    sys.exit(app.exec())