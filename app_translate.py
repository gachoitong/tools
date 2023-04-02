import sys
import clipboard
from PyQt5 import QtCore, QtGui, QtWidgets
# from bxv.dictzh import translate
from app_tranlsate_lib import translate


def paste_translate():
    ui.plainTextEdit.setPlainText(clipboard.paste())
    translateTextFromInput()
    pass


def translateText(text):
    if not text:
        return '<h1>nothing<h1>'
    # text = '暮色起看天边斜阳'
    ss = []
    zh, py, vi, hv, zhvi, vph = translate(
        text, adv=True, cols=['py', 'zh', 'vi', 'hv'])
    # print(vph)
    ss.append('<h1>{}</h1>'.format(zhvi))
    ss.append("""
<style>
    .c0 {
        font-family: sans-serif;
        padding: 4px 16px;
        margin: 4px;
    }

    .c2 {
        font-size: 28px;
        color: #000;
        padding: 4px;
        background:#eee;
    }

    .c1 {
        font-size: 17px;
        padding: 4px;
        color: #a33;
    }

    .c4 {
        font-size: 15px;
        padding: 4px;
        color: #6a6;}

    .c3 {
        font-size: 15px;
        padding: 4px;
        color: #66a;}
</style>""")
    ss.append('<table>')
    for i in vph:
        ss.append(
            '<tr class="c0">\n<td class="c1">{}</td>\n<td class="c2">{}</td>\n<td class="c3">{}</td>\n<td class="c4">{}</td>\n</tr>'.format(*i))
    ss.append('</table>')
    ss = '\n'.join(ss)
    return ss


def translateTextFromInput():
    text = ui.plainTextEdit.toPlainText()
    try:
        transText = translateText(text)

    except Exception as e:
        transText = str(e)
    ui.textBrowser.setHtml(transText)
    pass


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(480, 640)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName("verticalLayout")
        self.plainTextEdit = QtWidgets.QPlainTextEdit(self.centralwidget)
        self.plainTextEdit.setObjectName("plainTextEdit")
        self.verticalLayout.addWidget(self.plainTextEdit)
        self.pushButton_2 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_2.setObjectName("pushButton_2")
        self.verticalLayout.addWidget(self.pushButton_2)
        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setObjectName("pushButton")
        self.verticalLayout.addWidget(self.pushButton)
        self.textBrowser = QtWidgets.QTextBrowser(self.centralwidget)
        self.textBrowser.setObjectName("textBrowser")
        self.verticalLayout.addWidget(self.textBrowser)
        self.verticalLayout.setStretch(0, 1)
        self.verticalLayout.setStretch(1, 1)
        self.verticalLayout.setStretch(2, 1)
        self.verticalLayout.setStretch(3, 5)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 480, 21))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "translate zhvi"))
        self.plainTextEdit.setPlaceholderText(
            _translate("MainWindow", "MANDARIN"))
        self.pushButton_2.setText(_translate("MainWindow", "PASTE+TRANSLATE"))
        self.pushButton.setText(_translate("MainWindow", "TRANSLATE"))


app = QtWidgets.QApplication(sys.argv)
MainWindow = QtWidgets.QMainWindow()

MainWindow.setWindowFlags(QtCore.Qt.WindowStaysOnTopHint)
ui = Ui_MainWindow()
ui.setupUi(MainWindow)
ui.pushButton_2.clicked.connect(paste_translate)
ui.pushButton.clicked.connect(translateTextFromInput)
MainWindow.show()
sys.exit(app.exec_())
