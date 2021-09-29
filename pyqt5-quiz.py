from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
# from functools import partial
import sys, math, json, random

class WindowStart(QWidget):
    def __init__(self):
        super().__init__()
        # mainwindow.setWindowIcon(QtGui.QIcon('PhotoIcon.png'))
        self.label = QLabel('Would you like to start a quiz?')
        self.label.setAlignment(Qt.AlignCenter)
        self.label.setWordWrap(True)
        self.btn_start = QPushButton('Start')
        self.btn_exit = QPushButton('Exit')

        # self.layout = QuizLayout()
        self.layout = QGridLayout()
        self.layout.addWidget(self.label, 0, 0, 0, 2)
        self.layout.addWidget(self.btn_start, 1, 0)
        self.layout.addWidget(self.btn_exit, 1, 1)

        # windows
        self.setWindowTitle("Kazuya Quiz")
        self.setLayout(self.layout)

class WindowQuiz(QWidget):
    def __init__(self, number_of_questions):
        super().__init__()
        
        # self.layout.removeWidget(self.widgets['label'])
        self.label_question_number = QLabel()
        self.label_question_number.setAlignment(Qt.AlignCenter)
        self.label_question_number.setWordWrap(True)

        self.label_answer_status = QLabel()
        self.label_answer_status.setAlignment(Qt.AlignCenter)
        self.label_answer_status.setWordWrap(True)

        self.label_question = QLabel()
        self.label_question.setAlignment(Qt.AlignCenter)
        self.label_question.setWordWrap(True)
        self.btn_A = QPushButton()
        self.btn_B = QPushButton()
        self.btn_C = QPushButton()
        self.btn_D = QPushButton()
        self.btn_E = QPushButton()
        self.btn_next = QPushButton('Next')
        self.btn_prev = QPushButton('Prev')
        self.btns_nav = [QPushButton(str(i+1)) for i in range(number_of_questions)]


        self.layout = QGridLayout()        
        self.layout.addWidget(self.label_question_number, 0, 0, 1, 5)
        self.layout.addWidget(self.label_answer_status, 0, 5, 1, 5)
        self.layout.addWidget(self.label_question, 1, 1, 3, 8)
        self.layout.addWidget(self.btn_A, 4, 1, 1, 8)
        self.layout.addWidget(self.btn_B, 5, 1, 1, 8)
        self.layout.addWidget(self.btn_C, 6, 1, 1, 8)
        self.layout.addWidget(self.btn_D, 7, 1, 1, 8)
        self.layout.addWidget(self.btn_E, 8, 1, 1, 8)
        self.layout.addWidget(self.btn_prev, 9, 0, 1, 5)
        self.layout.addWidget(self.btn_next, 9, 5, 1, 5)
        # ---------------------------------- rowstart, colstart, rowspan, colspan
        for i in range(len(self.btns_nav)):
            self.layout.addWidget(self.btns_nav[i], 10 + math.floor(i / 10), i - math.floor(i / 10)*10)
        self.setLayout(self.layout)

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        width = 800
        height = 600
        self.number_of_questions = 30

        screen = app.primaryScreen()
        size = screen.size()
        self.setGeometry(
            int((size.width()-width)/2), #pos_x
            int((size.height()-height)/2), #pos_y
            width, #win_width
            height #win_height
        )
        self.setFixedSize(width, height)
        # with open('qna.json') as f:
        #    self.qna = json.load(f)
        with open('uud.json') as f:
           self.uud = json.load(f)

        self.startWindowStart()

    def startWindowStart(self):
        self.Start = WindowStart()
        self.setWindowTitle("Tes Wawasan Kebangsaan")
        self.setCentralWidget(self.Start)
        self.Start.btn_start.clicked.connect(self.startWindowQuiz)
        self.Start.btn_exit.clicked.connect(self.exit)
        self.show()

    def startWindowQuiz(self):
        self.questions = random.sample(self.uud['uud'], self.number_of_questions)
        self.answers =[random.randrange(5) for i in range(self.number_of_questions)]
        self.answered_questions = [-1 for i in range(self.number_of_questions)]
        self.Quiz = WindowQuiz(self.number_of_questions)
        self.navigateWindowQuiz(0)

        self.Quiz.btn_A.clicked.connect(lambda n, x=0:self.checkCorrectAnswer(x))
        self.Quiz.btn_B.clicked.connect(lambda n, x=1:self.checkCorrectAnswer(x))
        self.Quiz.btn_C.clicked.connect(lambda n, x=2:self.checkCorrectAnswer(x))
        self.Quiz.btn_D.clicked.connect(lambda n, x=3:self.checkCorrectAnswer(x))
        self.Quiz.btn_E.clicked.connect(lambda n, x=4:self.checkCorrectAnswer(x))

        for i in range(self.number_of_questions):
            # self.Quiz.btns_nav[i].clicked.connect(partial(self.navigateWindowQuiz, i))
            self.Quiz.btns_nav[i].clicked.connect(lambda n, x=i:self.navigateWindowQuiz(x))

    def navigateWindowQuiz(self, i):
        self.current_question_number = i
        self.setWindowTitle("Kuis no.{}".format(i+1))
        self.Quiz.label_question_number.setText("No.{}".format(i+1))
        # self.Quiz.label_answer_status.setText("{} dari {} pertanyaan terjawab".format(self.answered_questions.count(True), self.number_of_questions))
        self.Quiz.label_answer_status.setText("{} dari {} pertanyaan terjawab".format(self.number_of_questions - self.answered_questions.count(-1), self.number_of_questions))
        self.Quiz.label_question.setText("{}. Peraturan ini tercantum dalam ...".format(self.questions[i]['bunyi']))
        self.Quiz.btn_A.setText("A. UUD 1945 Pasal {} Ayat ({})".format(self.questions[i]['pasal'], self.questions[i]['ayat']))
        self.Quiz.btn_B.setText("B. UUD 1945 Pasal {} Ayat ({})".format(self.questions[i]['pasal'], self.questions[i]['ayat']))
        self.Quiz.btn_C.setText("C. UUD 1945 Pasal {} Ayat ({})".format(self.questions[i]['pasal'], self.questions[i]['ayat']))
        self.Quiz.btn_D.setText("D. UUD 1945 Pasal {} Ayat ({})".format(self.questions[i]['pasal'], self.questions[i]['ayat']))
        self.Quiz.btn_E.setText("E. UUD 1945 Pasal {} Ayat ({})".format(self.questions[i]['pasal'], self.questions[i]['ayat']))
        
        self.Quiz.btn_A.setStyleSheet("background-color : none")
        self.Quiz.btn_B.setStyleSheet("background-color : none")
        self.Quiz.btn_C.setStyleSheet("background-color : none")
        self.Quiz.btn_D.setStyleSheet("background-color : none")
        self.Quiz.btn_E.setStyleSheet("background-color : none")
        print("no.{}, your answer={}".format(self.current_question_number, self.answered_questions[self.current_question_number]))
        if self.answered_questions[self.current_question_number] == 0:
            self.Quiz.btn_A.setStyleSheet("background-color : rgb(192,208,240)")
        if self.answered_questions[self.current_question_number] == 1:
            self.Quiz.btn_B.setStyleSheet("background-color : rgb(192,208,240)")
        if self.answered_questions[self.current_question_number] == 2:
            self.Quiz.btn_C.setStyleSheet("background-color : rgb(192,208,240)")
        if self.answered_questions[self.current_question_number] == 3:
            self.Quiz.btn_D.setStyleSheet("background-color : rgb(192,208,240)")
        if self.answered_questions[self.current_question_number] == 4:
            self.Quiz.btn_E.setStyleSheet("background-color : rgb(192,208,240)")

        self.Quiz.btn_prev.setEnabled(True)
        self.Quiz.btn_next.setEnabled(True)
        if i == 0:
            self.Quiz.btn_prev.setEnabled(False)
        if i == self.number_of_questions-1:
            self.Quiz.btn_next.setEnabled(False)
        QObject.disconnect(self.Quiz.btn_prev)
        QObject.disconnect(self.Quiz.btn_next)
        self.Quiz.btn_prev.clicked.connect(lambda n, x=i-1:self.navigateWindowQuiz(x))
        self.Quiz.btn_next.clicked.connect(lambda n, x=i+1:self.navigateWindowQuiz(x))

        self.setCentralWidget(self.Quiz)
        self.show()
    
    def checkCorrectAnswer(self, answer):
        self.Quiz.btns_nav[self.current_question_number].setStyleSheet("background-color : rgb(192,208,240)")
        # if self.answers[self.current_question_number] == answer:
            # self.answered_questions[self.current_question_number] = True
        self.answered_questions[self.current_question_number] = answer
        if self.current_question_number + 1 < self.number_of_questions:
            self.navigateWindowQuiz(self.current_question_number + 1)
        else:
            self.navigateWindowQuiz(self.current_question_number)
        print("correct answers = {}".format(self.checkAllAnswer()))

    def checkAllAnswer(self):
        correct = 0
        for i in range(len(self.answers)):
            if self.answers[i] == self.answered_questions[i]:
                correct += 1
        return correct

    def exit(self):
        alert = QMessageBox(w)
        alert.setIcon(QMessageBox.Warning)
        alert.setText("Warning");
        alert.setInformativeText("Are you sure you want to exit?")
        btn_yes = alert.addButton("Yes", alert.YesRole)
        alert.addButton("No", alert.NoRole)
        alert.exec()
        if btn_yes == alert.clickedButton():
           sys.exit()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = MainWindow()
    sys.exit(app.exec_())