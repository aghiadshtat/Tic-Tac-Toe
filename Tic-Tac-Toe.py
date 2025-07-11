import os

def clear_screen():
    os.system("cls" if os.name=="nt" else "clear")



class Player:
    def __init__(self) :
        self.name=""
        self.sym=""

    def choose_name(self):
        name =input("enter your name:\n")
        while True:
            if name.isdigit() or name.isalpha():
                self.name =name
                clear_screen()
                break
            
            else:
                clear_screen()
                name=input("invaild name, enter a name please:\n")

    def choose_sym(self):
        sym=input(f"{self.name} , enter a symbol\n")

        while True:
            if sym.isalpha() and len(sym)==1:
                self.sym=sym.upper()
                clear_screen()
                break
            else:
                clear_screen()
                sym=input("invaild symbol, enter a symbol please:\n")



class Menu:
    def display_main_menu(self):
        print("""
        Welcome to my X-O game
        1. Start the game
        2. Quit the game
        """)
        choice1=int(input("Enter Your Choice : (1-2)\n"))
        while True:
            if choice1==1 or choice1==2:
                
                clear_screen()
                return choice1
            else:
                choice1=int(input("Please enter 1 or 2:\n"))
                

    def display_endgame_menu(self):
        print("""
        1. Restart the game
        2. Quit the game
        """)
        choice2=int(input("Enter Your Choice : (1-2)\n"))
        while True:
            if choice2==1 or choice2==2:
                clear_screen()
                return choice2
                
            else:
                choice2=int(input("Please Enter 1 or 2:\n"))



class Board:
    def __init__(self) :
        self.list=[str(i) for i in range(1,10)]
    def dis_board(self):
        for i in range (0,9,3):
            print("\t"+"  |  ".join(self.list[i:i+3]))
            if i<6:
                print("\t"+"-"*13)
    def update_board(self,choice,sym):
        if self.isvalid_move(choice):
            self.list[choice-1]=sym
            return True
        return False
    def isvalid_move(self,choice):
        return self.list[choice-1].isdigit()
    def reset_board(self):
        self.list=[str(i) for i in range(1,10)]



class Game:
    def __init__(self) -> None:
        self.board=Board()
        self.players=[Player(),Player()]
        self.menu=Menu()
        self.index_player_turn=0

    def start_game(self):
        choice4=self.menu.display_main_menu()
        if choice4==1:
            self.setup_players()
            self.play_game()
        else :
            self.quit_game()

    def setup_players(self):
        for number ,player in enumerate(self.players,start=1):
            clear_screen()
            print(f"player {number}, enter your details:")
            player.choose_name()
            player.choose_sym()

    def play_game(self):
        while True:
            self.player_turn()
            if self.check_drow() or self.check_win():
                choice3=self.menu.display_endgame_menu()
                if choice3==1:
                    self.restart_game()
                    break
                else:
                    self.quit_game()
                    break


    def player_turn(self):
        player=self.players[self.index_player_turn]
        self.board.dis_board()
        
        print(f"{player.name}'s turn")
        while True:
            try :
                cell_choice=int(input ("Choose a number between (1-9): "))
                if 1<=cell_choice<=9 and self.board.update_board(cell_choice,player.sym):
                    clear_screen()
                    break
                else:
                    print("invalid move , try again.")
            except ValueError:
                print("Please enter a number between (1-9).")
        self.switch_player()
    
    def switch_player(self):
        self.index_player_turn=1-self.index_player_turn

    def check_win(self):
        win_conditions=[
            [0,1,2],[3,4,5],[6,7,8],
            [0,3,6],[1,4,7],[2,5,8],
            [0,4,8],[2,4,6]
                        ]

        for win_condition in win_conditions:
            if self.board.list[win_condition[0]]==self.board.list[win_condition[1]]==self.board.list[win_condition[2]]:
                return True
            
        return False


    

    def check_drow(self):
        return all(not i.isdigit() for i in self.board.list)

    def restart_game(self):
        self.board.reset_board()
        self.index_player_turn=0
        self.play_game()
    def quit_game(self):
        print ("thanks for playing")
        
    
        
               
if __name__=="__main__":
    game=Game()
    game.start_game()
