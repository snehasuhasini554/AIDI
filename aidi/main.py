def main():
    from .floating_aidi import FloatingAIDI
    from PyQt5.QtWidgets import QApplication
    import sys
    app = QApplication(sys.argv)
    QApplication.setAttribute(23, True)  # AA_EnableHighDpiScaling
    QApplication.setAttribute(24, True)  # AA_UseHighDpiPixmaps
    window = FloatingAIDI()
    window.show()
    sys.exit(app.exec_())
