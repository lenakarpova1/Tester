import sys
import os
import sqlite3
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QWidget, QMainWindow, QApplication, QMessageBox, QDialog, QTableWidgetItem

from log import Ui_Log
from one import Ui_MainWindow
from tasks import Ui_Form
from reg import Ui_Reg
from statist import Ui_Dialog


class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        #uic.loadUi('one.ui', self)
        self.user = []
        self.dict_sub = {}
        self.dict_them = {}
        self.choice = 'Тест не выбран'
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Список задач')
        self.list_test = []
        self.pixmap = QPixmap('user.png')
        self.user_im.setPixmap(self.pixmap)
        self.btn_test.clicked.connect(self.show_task)
        self.btn_log.clicked.connect(self.show_log)
        self.btn_reg.clicked.connect(self.show_reg)
        self.update_welcome()
        self.listWidget.clicked.connect(self.show_list_test)
        self.btn_filtr.clicked.connect(self.filter)

        f = open('help_sub.txt', 'r', encoding='utf-8')
        text = f.readlines()
        for el in text:
            temp = el.strip().split('=')
            self.dict_sub[temp[0]] = temp[1]
        self.list_subject = [el[:-2].split('=')[0] for el in text]
        self.sub.addItems(self.list_subject)

        f = open('help_tem.txt', 'r', encoding='utf-8')
        text = f.readlines()
        for el in text:
            temp = el.strip().split('=')
            self.dict_them[temp[0]] = temp[1]
        self.list_tem = [el[:-2].split('=')[0] for el in text]
        self.them.addItems(self.list_tem)

    def show_task(self):
        if self.choice == 'Тест не выбран':
            msg = InfoMassage('Тест не выбран', 'Вы не выбрали тест')
            retval = msg.exec_()
        else:
            self.w = Widget(self, self.choice, self.user)
            self.w.show()
            self.hide()

    def filter(self):
        self.choice = 'Тест не выбран'
        self.listWidget.clear()
        self.list_test = list(filter(lambda x: x.lower().endswith('.txt'), os.listdir(path='./test')))
        list_sub_test = list(filter(lambda x: x.startswith(self.dict_sub[self.sub.currentText()]), self.list_test))
        self.sudject = self.dict_sub[self.sub.currentText()]
        list_tem_test = list(filter(lambda x: x[4:].startswith(self.dict_them[self.them.currentText()]), list_sub_test))
        self.tem = self.dict_them[self.them.currentText()]
        list_tem_test = [i[7:-4] for i in list_tem_test]
        self.listWidget.addItems(list_tem_test)

    def show_log(self):
        self.auth = Authorization(self.user)
        self.auth.show()
        if self.auth.exec_() == QDialog.Accepted:
            self.update_welcome()

    def show_reg(self):
        self.reg = Registration(self.user)
        self.reg.show()
        if self.reg.exec_() == QDialog.Accepted:
            self.update_welcome()

    def show_list_test(self, item):
        self.choice = self.sudject + ' ' + self.tem + ' ' + item.data()

    def update_welcome(self):
        if self.user:
            self.label_user.setText(f'{self.user[0]}')
        else:
            self.label_user.setText('Войдите или зарегистрируйтесь  ')


class Widget(QWidget, Ui_Form):
    def __init__(self, last_window, choice, user):
        super().__init__()
        self.setupUi(self)
        #uic.loadUi('2.ui', self)
        self.last_win = last_window
        self.label_name_test.setText(choice[7:])
        self.user = user
        self.answers = {}
        self.TASK = {}
        f = open(f'test/{choice}.txt', 'r', encoding='utf-8')
        for i in f.read().split('&_&'):
            a, b, c = i.strip().split('&!&')
            self.TASK[int(a)] = [b, c]
        f.close()
        self.initUI()

    def initUI(self):
        self.state = 0
        self.label.setText(self.TASK[self.state][0])
        self.bttn_prev.clicked.connect(self.back)
        self.bttn_next.clicked.connect(self.forward)
        self.bttn_back.clicked.connect(self.cl_win)
        self.bttn_fin.clicked.connect(self.to_finish)
        self.bttn_check.clicked.connect(self.check)

    def back(self):
        if self.state:
            self.state = (self.state - 1) % len(self.TASK)
            self.label.setText(self.TASK[self.state][0])
            self.lineEdit.clear()
            self.lineEdit_2.clear()

    def forward(self):
        if self.state < len(self.TASK) - 1:
            self.state = (self.state + 1) % len(self.TASK)
            self.label.setText(self.TASK[self.state][0])
            self.lineEdit.clear()
            self.lineEdit_2.clear()

    def check(self):
        answer = self.lineEdit.text()
        if answer == self.TASK[self.state][1]:
            self.lineEdit_2.setText('ВЕРНО')
        else:
            self.lineEdit_2.setText('НЕВЕРНО')
        self.answers[self.TASK[self.state][0]] = [self.lineEdit.text(), self.TASK[self.state][1]]

    def cl_win(self):
        self.last_win.show()
        self.hide()

    def to_finish(self):
        self.data_fife = self.answers
        self.data_table = self.answers

        self.stat = Statistics(self.data_table)
        self.stat.show()

        f = open('answers.txt', 'w', encoding='utf-8')
        if self.user:
            f.write(f"Информация о пользователе: {self.user[0]}, {self.user[1]}, {self.user[2]}\n\n")

        for key in self.data_fife.keys():
            f.write(f'{key}\n\nДан ответ: {self.data_fife[key][0]}\tПравильный ответ: {self.data_fife[key][1]}\n\n')
        f.close()

        if not self.stat.exec_():
            self.last_win.show()
            self.hide()


class Statistics(QDialog, Ui_Dialog):
    def __init__(self, data_table):
        super().__init__()
        self.setupUi(self)
        #uic.loadUi('stat.ui', self)
        self.data_table = data_table
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Ваши результаты')
        self.tableWidget.setHorizontalHeaderLabels(['Условие задачи', 'Ваш ответ', 'Правильный\n ответ'])
        self.tableWidget.setRowCount(len(self.data_table.keys()))
        self.tableWidget.setColumnCount(3)
        condition, user_answer, correct_answer = [], [], []
        for key in (self.data_table.keys()):
            condition.append(key)
            user_answer.append(self.data_table[key][0])
            correct_answer.append(self.data_table[key][1])

        for i in range(len(self.data_table.keys())):
            self.tableWidget.setItem(i, 0, QTableWidgetItem(condition[i][2:]))
            self.tableWidget.setItem(i, 1, QTableWidgetItem(user_answer[i]))
            self.tableWidget.setItem(i, 2, QTableWidgetItem(correct_answer[i]))


class Authorization(QDialog, Ui_Log):
    def __init__(self, user):
        super(Authorization, self).__init__()
        self.setupUi(self)
        #uic.loadUi('log.ui', self)
        self.initUI()
        self.user = user

    def initUI(self):
        self.setWindowTitle('Вход в систему')
        self.buttonBox.accepted.connect(self.log_user_ok)
        self.buttonBox.rejected.connect(self.log_user_not)

    def log_user_ok(self):
        login = self.line_login.text()
        password = self.line_password.text()
        if login and password:
            conn = sqlite3.connect('users.db')
            cur = conn.cursor()
            id = cur.execute(f"SELECT id FROM users WHERE login = '{login}'").fetchone()
            if id:
                cur = conn.cursor()
                password_user = cur.execute(f"SELECT password FROM users WHERE id = {id[0]}").fetchone()[0]
                if password != str(password_user):
                    msg = InfoMassage('Неверный пароль',
                                      'Вы ввели неверный пароль \nПопробуйте войти еще раз ')
                    retval = msg.exec_()
                else:
                    cur = conn.cursor()
                    name_user = cur.execute(f"SELECT name_user FROM users WHERE id = {id[0]}").fetchone()[0]
                    school = cur.execute(f"SELECT name_school FROM schools WHERE id = {id[0]}").fetchone()[0]
                    grade = cur.execute(f"SELECT name_class FROM classes WHERE id = {id[0]}").fetchone()[0]
                    self.user.extend([
                        name_user, grade, school
                    ])
            else:
                msg = InfoMassage('Неверный логин или пароль',
                                  'Такого пользователя нет \nПопробуйте войти еще раз или зарегистрируйтесь ')
                retval = msg.exec_()
        else:
            msg = InfoMassage('Ошибка входа',
                              'Все поля должны быть обязательно запонены ')
            retval = msg.exec_()

    def log_user_not(self):
        pass


class Registration(QDialog, Ui_Reg):
    def __init__(self, user):
        super(Registration, self).__init__()
        self.setupUi(self)
        #uic.loadUi('reg.ui', self)
        self.user = user
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Регистрация')

        self.con = sqlite3.connect('users.db')
        cur = self.con.cursor()
        self.school.addItems([i[0] for i in cur.execute("SELECT name_school FROM schools").fetchall()])
        self.num_class.addItems([i[0] for i in cur.execute("SELECT name_class FROM classes").fetchall()])

        self.buttonBox.accepted.connect(self.reg_user_ok)
        self.buttonBox.rejected.connect(self.reg_user_not)

    def reg_user_ok(self):
        login = self.login.text()
        password = self.password.text()
        user = self.name_user.text()
        school = self.__get_id_school(self.school.currentText())
        grade = self.__get_id_class(self.num_class.currentText())
        if login and password and user:
            conn = sqlite3.connect('users.db')
            cur = conn.cursor()
            cur.execute(f"INSERT INTO users(name_user,login,password,school,class)"
                        f" VALUES('{user}', '{login}', '{password}', {school[0]}, {grade[0]})")
            conn.commit()
            conn.close()
            self.user.extend([
                user, self.num_class.currentText(), self.school.currentText()
            ])
        else:
            msg = InfoMassage('Ошибка регистрации',
                              'Все поля должны быть обязательно заполнены \nПопробуйте зарегистрироваться еще раз ')
            retval = msg.exec_()

    def __get_id_school(self, name: str):
        conn = sqlite3.connect('users.db')
        cur = conn.cursor()
        return cur.execute(f"SELECT id FROM schools WHERE name_school = '{name}'").fetchone()

    def __get_id_class(self, name: str):
        conn = sqlite3.connect('users.db')
        cur = conn.cursor()
        return cur.execute(f"SELECT id FROM classes WHERE name_class = '{name}'").fetchone()

    def reg_user_not(self):
        pass


class InfoMassage(QMessageBox):
    def __init__(self, title, text):
        super().__init__()
        self.setWindowTitle(title)
        self.setIcon(QMessageBox.Information)
        self.setText(text)
        self.setStandardButtons(QMessageBox.Ok)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MainWindow()
    ex.show()
    sys.exit(app.exec())
