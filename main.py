from kivy.app import App #Main object
from kivy.core.text import LabelBase
from kivy.core.window import Window
from kivy.lang import Builder #Connect Python File to Kivy
from kivy.uix.screenmanager import ScreenManager, Screen # to use screens for GUI
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.widget import Widget
from kivy.uix.label import Label
from kivy.properties import StringProperty
import mysql.connector
import matplotlib.pyplot as plt 

class MainApp(App):
    def build(self):

        return WindowManager()

    #Builder called from Windows Manager
    Builder.load_file('Home.kv')
    Builder.load_file('Login.kv') 
    Builder.load_file('Profile.kv')
    Builder.load_file('Help.kv')
    Builder.load_file('Dashboard.kv')
    Builder.load_file('Weight.kv')
    Builder.load_file('Happy.kv')
    Builder.load_file('Calorie.kv')
    Builder.load_file('Water.kv')
    Builder.load_file('Summary.kv')
    Builder.load_file('Graph.kv')

    #The database is initialized
    database = mysql.connector.Connect(host="localhost", user="root", password="root", database="loginform")
    cursor = database.cursor()    
    #The database cursor is established, allowing for traversal of the database
    cursor.execute("""Create Table if not exists logindata(username VARCHAR(255), password_id VARCHAR(255), name_id VARCHAR(255), height_id INT, initial_weight_id INT, age_id INT, date DATE)""")
    
    #This sends data from python to mysql
    def send_data(self, username, password_id): 
        self.cursor.execute(f"insert into logindata values('{username.text}', '{password_id.text}')")
        self.database.commit()
        
    #This sends data from python to mysql, so the summary graph can be created
    def get_data(self, username, category_input): 
        self.cursor.execute(f"SELECT {category_input.text} FROM {username.text}")
        result = self.cursor.fetchall()
        self.database.commit()
        
        #These will be the datapoints to be plotted on the graph
        int7 = result[-1][0]
        int6 = result[-2][0]
        int5 = result[-3][0]
        int4 = result[-4][0]
        int3 = result[-5][0]
        int2 = result[-6][0]
        int1 = result[-7][0]
        
        self.graph(category_input, int1, int2, int3, int4, int5, int6, int7)

    #This sends data from python to mysql, for the weight tracker
    def send_data_category(self, username, weight): 
        self.cursor.execute(f"INSERT INTO {username.text} VALUES({weight.text} , 0 , 0 , 0 , CURRENT_TIMESTAMP)")
        self.database.commit()

    #This sends data from python to mysql, for the water intake tracker
    def send_data_category_water(self, username, water): 
        self.cursor.execute(f"INSERT INTO {username.text} VALUES( 0 , {water.text} , 0 , 0 , CURRENT_TIMESTAMP)")
        self.database.commit()

    #This sends data from python to mysql, for the calorie tracker
    def send_data_category_calorie(self, username, calorie): 
        self.cursor.execute(f"INSERT INTO {username.text} VALUES( 0 , 0 , 0 , {calorie.text} , CURRENT_TIMESTAMP)")
        self.database.commit()
    
    #This sends data from python to mysql, for the happiness tracker
    def send_data_category_happy(self, username, happy, info): 
        self.cursor.execute(f"INSERT INTO {username.text} VALUES( 0 , 0 , {happy.text} , 0 , CURRENT_TIMESTAMP)")
        self.database.commit()


    #This function allows for the login info to be updated on the database
    def change_data(self, username, password_id, info):
        self.cursor.execute(f"UPDATE logindata SET password_id = '{password_id.text}' WHERE username = '{username.text}'")
        self.database.commit()
        if username == '' or password_id == '':
            info.text = '[color=#FF0000]Please fill every field required[/color]'
        else:
            if username != '' and password_id != '':
                info.text = '[color=#00FF00]Password Updated.[/color]'
            else:
                info.text = '[color=#FF000]Invalid! Please try again.[/color]'

    #This function adds a new user to profile database
    def add_user(self, username, password_id, name_id, height_id, initial_weight_id, age_id, info):
        #Makes sure that the fields are filled out before submitting the new profile to the database
        if username.text == "" or password_id.text == "" or name_id.text == "" or height_id.text == "" or initial_weight_id.text == "" or age_id.text == "":
            info.text = '[color=#FF0000]Please fill out all the fields and Press Submit or Enter when Done.[/color]'
        #When all fields are filled and form is submitted, the new profile is created on the database
        else:
            self.cursor.execute(f"""Create Table if not exists {username.text}(weight INT, water INT, happy INT, calories INT, date DATE)""")
            self.cursor.execute(f"insert into logindata values('{username.text}', '{password_id.text}', '{name_id.text}', {height_id.text}, {initial_weight_id.text}, {age_id.text}, CURRENT_TIMESTAMP)")
            self.cursor.execute(f"INSERT INTO {username.text} VALUES( 0 , 0 , 0 , 0 , CURRENT_TIMESTAMP)")
            self.cursor.execute(f"INSERT INTO {username.text} VALUES( 0 , 0 , 0 , 0 , CURRENT_TIMESTAMP)")
            self.cursor.execute(f"INSERT INTO {username.text} VALUES( 0 , 0 , 0 , 0 , CURRENT_TIMESTAMP)")
            self.cursor.execute(f"INSERT INTO {username.text} VALUES( 0 , 0 , 0 , 0 , CURRENT_TIMESTAMP)")
            self.cursor.execute(f"INSERT INTO {username.text} VALUES( 0 , 0 , 0 , 0 , CURRENT_TIMESTAMP)")
            self.cursor.execute(f"INSERT INTO {username.text} VALUES( 0 , 0 , 0 , 0 , CURRENT_TIMESTAMP)")
            self.cursor.execute(f"INSERT INTO {username.text} VALUES( 0 , 0 , 0 , 0 , CURRENT_TIMESTAMP)")
            self.database.commit()
            info.text = f'[color=#00FF00]{name_id.text}"s Profile was successfully created![/color]'

    #This is the function that creates summary graph, it takes the category and datapoints as parameters
    def graph(self, category_input, int1, int2, int3, int4, int5, int6, int7):
        
        #initializes the data to be plotted along the x-axishappy
        x1 = [1,2,3,4,5,6,7]
        #initializes the data to be plotted along the y-axis
        y1 = [int1, int2, int3, int4, int5, int6, int7]

        #plots the x and y axes
        plt.plot(x1, y1)
        #labels the y-axis
        plt.ylabel(f"{category_input.text}")
        #labels the x-axis
        plt.xlabel("Trailing Seven Days")
        
        #shows the resulting graph
        plt.show()
    
    #This function validates the inputted information, and logs them in if information is valid
    def validate_users(self, username, password_id, info):

        password_queue = []
        sql_query = f"SELECT * FROM LOGINDATA WHERE USERNAME = '{username.text}' AND password_id = '{password_id.text}'"
        try:
            self.cursor.execute(sql_query)
            results = self.cursor.fetchall()
            for row in results:
                for x in row:
                    password_queue.append(x)
        except:
            print('error occured')

        if username.text == "" and password_id.text == "":
            info.text = '[color=#00FF00]Please enter Username and Password![/color]'
            print('no data!!!')
        elif (username.text and password_id.text) in password_queue:
            info.text = '[color=#00FF00]Logged in successfully![/color]'
            print('yes!!!')
        else:
            info.text = '[color=#FF0000]Invalid Username and/or password.[/color]'

    #This function checks if the inputted information is valid
    def valid_entry(self,username, password_id, name_id, height_id, initial_weight_id, age_id, info):
        user = username
        passw = password_id
        info = info
        
        uname = user.text
        passw = passw.text
        
        if uname == '' or passw == '':
            info.text = '[color=#FF0000]Please fill every field required[/color]'
        else:
            if uname != '' and passw !='':
                info.text = '[color=#00FF00]Entry is Valid. Click Submit to create your profile.[/color]'
            else:
                info.text = '[color=#FF000]Invalid! Please try again.[/color]'
    
class Graph(BoxLayout):

    def __init__(self,):

        super().__init__(self)

        box = self.ids.box

        box.add_widget((plt.show()))

class LoginWindows(Screen):
    pass

class ProfileWindows(Screen):
    pass

class DashboardWindows(Screen):
    pass

class HelpWindows(Screen):
    pass

class WaterTrackerWindows(Screen):
    pass

class CalorieTrackerWindows(Screen):
    pass

class WeightTrackerWindows(Screen):
    pass

class HappyWindows(Screen):
    pass

class SummaryWindows(Screen):
    pass

class WindowManager(ScreenManager): # allows for transitions between windows
    pass

class BoxLayoutExample(BoxLayout):
    pass


if __name__ == "__main__":
    MainApp().run()
