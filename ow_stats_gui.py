'''
Created on Aug 10, 2016

@author: Hanna
'''
import tkinter as tk
from collections import namedtuple
import ow_database
import matplotlib.pyplot as plt
from random import random

class ow_stats_gui(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)
        self.parent = parent
        self.figure_count = 0

        self.heroes = ["Ana", "Bastion", "D.Va", "Genji", "Hanzo", "Junkrat", "Lucio", "McCree", "Mei", "Mercy", "Pharah", "Reaper", "Reinhardt", "Roadhog", "Soldier: 76", "Symmetra", "Torbjorn", "Tracer", "Widowmaker", "Winston", "Zarya", "Zenyatta"]
        self.players = ["Hanna", "Heeran", "James", "Jason", "Kyle", "Derek", "Sam", "Michael", "Brad", "Zack", "Jimmy"]
        self.maps = ["Hanamura", "Temple of Anubis", "Volskaya Industries", "Dorado", "Route 66", "Watchpoint: Gibraltar", "Hollywood", "King's Row", "Numbani", "Ilios", "Lijiang Tower", "Nepal"]
        
        #database init
        self.database = ow_database.ow_database()
        
        self.personal_game = tk.Button(self, text="Add Personal Match Result", command=self.create_personal_match)
        self.personal_game.pack(side="top")
        
        self.create_match_button = tk.Button(self, text="Add New Competitive Match Result", command=self.create_match)
        self.create_match_button.pack(side="top")
        
        self.hero_map_winrate_button = tk.Button(self, text="Find Hero Total Wins/Losses", command=self.hero_map_winrate)
        self.hero_map_winrate_button.pack(side="top")
        
        self.hero_percent_winrate_button = tk.Button(self, text="Find Hero Win Rates on All Maps", command=self.hero_win_percent)
        self.hero_percent_winrate_button.pack(side="top")
        
        self.match_history_button = tk.Button(self, text="View Match History by Player", command=self.view_match_history)
        self.match_history_button.pack(side="top")
    
    def view_match_history(self):
        self.mh = tk.Toplevel(self)
        self.mh.wm_title("Match History")
        
        self.p_name2 = tk.StringVar(self.mh)
        self.p_name2.set("Player Name")
        self.p_menu2 = tk.OptionMenu(self.mh, self.p_name2, "Player Name", "Hanna", "Heeran", "James", "Jason", "Kyle", "Derek", "Sam", "Michael", "Brad", "Zack", "Jimmy")
        self.p_menu2.grid(row=0, column=0)
        
        self.p_submit_match_button2 = tk.Button(self.mh, text="Submit", command=self.submit_match_history)
        self.p_submit_match_button2.grid(row=3, column=3)
        
    def submit_match_history(self):
        player_name = self.p_name2.get()
        history = self.database.query_match_history(player_name)
        
        mh_frame = tk.Toplevel(self)
        mh_frame.wm_title(("Match History for {}").format(player_name))
        
        mh_textbox = tk.Text(mh_frame, borderwidth=3, relief="sunken")
        mh_textbox.config(font=("consolas", 12), undo=True, wrap='word', state="disabled", width=150)
        mh_textbox.grid(row=0, column=0, sticky="nsew", padx=2, pady=2)
             
        mh_scrollbar = tk.Scrollbar(mh_frame, command=mh_textbox.yview)
        mh_scrollbar.grid(row=0, column=1, sticky='nsew')
        mh_textbox['yscrollcommand'] = mh_scrollbar.set
        header = ("| {:^15} | {:^15} | {:^15} | {:^15} | {:^15} | {:^30} | {:^15} |\r\n").format("match_id", "Player", "Hero", "Map", "Result", "Date", "Match Type")
        mh_textbox.config(state="normal")
        mh_textbox.insert("end", header)
        
        for row in history:
            if row[6] == 0:
                match_type = "Competitive"
            else:
                match_type = "Personal"
            if row[5] == 0:
                victory = "Victory"
            else:
                victory = "Defeat"
            text = ("| {:^15} | {:^15} | {:^15} | {:^15} | {:^15} | {:^30} | {:^15} |\r\n").format(row[0], row[1], row[2], row[4], victory, str(row[7]), match_type)
            #print(text)
            mh_textbox.insert("end", text)
        mh_textbox.config(state="disabled")
            
        self.mh.destroy()
        return
    
    def create_personal_match(self):
        self.cp = tk.Toplevel(self)
        self.cp.wm_title("Add Match")
        
        self.p_name = tk.StringVar(self.cp)
        self.p_name.set("Player Name")
        self.p_menu = tk.OptionMenu(self.cp, self.p_name, "Player Name", "Hanna", "Heeran", "James", "Jason", "Kyle", "Derek", "Sam", "Michael", "Brad", "Zack", "Jimmy")
        self.p_menu.grid(row=0, column=0)
        
        self.p_hero = tk.StringVar(self.cp)
        self.p_hero.set("Hero Played")
        self.p_hero_menu = tk.OptionMenu(self.cp, self.p_hero, "Hero Played", "Ana", "Bastion", "D.Va", "Genji", "Hanzo", "Junkrat", "Lucio", "McCree", "Mei", "Mercy", "Pharah", "Reaper", "Reinhardt", "Roadhog", "Soldier: 76", "Symmetra", "Torbjorn", "Tracer", "Widowmaker", "Winston", "Zarya", "Zenyatta")
        self.p_hero_menu.grid(row=0, column=1)
        
        #map name widget
        self.p_map_name = tk.StringVar(self.cp)
        self.p_map_name.set("Map")
        self.p_map_menu = tk.OptionMenu(self.cp, self.p_map_name, "Map", "Hanamura", "Temple of Anubis", "Volskaya Industries", "Dorado", "Route 66", "Watchpoint: Gibraltar", "Hollywood", "King's Row", "Numbani", "Ilios", "Lijiang Tower", "Nepal")
        self.p_map_menu.grid(row=0, column=2)
        
        #victory widget
        self.p_victory = tk.BooleanVar(self.cp)
        self.p_true_button = tk.Radiobutton(self.cp, text="Victory", variable=self.p_victory, value=True)
        self.p_false_button = tk.Radiobutton(self.cp, text="Defeat", variable=self.p_victory, value=False)
        self.p_true_button.grid(row=0, column=3)
        self.p_false_button.grid(row=1, column=3)
        
        #submit button
        self.p_submit_match_button = tk.Button(self.cp, text="Submit", command=self.personal_submit_match)
        self.p_submit_match_button.grid(row=3, column=3)
        
    def personal_submit_match(self):
        p_name = self.p_name.get()
        hero = self.p_hero.get()
        map_name = self.p_map_name.get()
        victory = self.p_victory.get()
        match_id = self.database.gen_match_id()
        
        self.database.add_personal_match(match_id, p_name, hero, map_name, victory)
        self.cp.destroy()
        
        
    def create_match(self):
        self.t = tk.Toplevel(self)
        self.t.wm_title("Add Competitive Match")
        
        #Player name drop menus
        self.name1 = tk.StringVar(self.t)
        self.name1.set("Player 1 Name")
        self.menu1 = tk.OptionMenu(self.t, self.name1, "Player 1 Name", "Hanna", "Heeran", "James", "Jason", "Kyle", "Derek", "Sam", "Michael", "Brad", "Zack", "Jimmy")
        self.menu1.grid(row=0, column=0)
        
        self.name2 = tk.StringVar(self.t)
        self.name2.set("Player 2 Name")        
        self.menu2 = tk.OptionMenu(self.t, self.name2, "Player 2 Name", "Hanna", "Heeran", "James", "Jason", "Kyle", "Derek", "Sam", "Michael", "Brad", "Zack", "Jimmy")
        self.menu2.grid(row=1, column=0)

        self.name3 = tk.StringVar(self.t)
        self.name3.set("Player 3 Name")
        self.menu3 = tk.OptionMenu(self.t, self.name3, "Player 3 Name", "Hanna", "Heeran", "James", "Jason", "Kyle", "Derek", "Sam", "Michael", "Brad", "Zack", "Jimmy")
        self.menu3.grid(row=2, column=0)
        
        self.name4 = tk.StringVar(self.t)
        self.name4.set("Player 4 Name")
        self.menu4 = tk.OptionMenu(self.t, self.name4, "Player 4 Name", "Hanna", "Heeran", "James", "Jason", "Kyle", "Derek", "Sam", "Michael", "Brad", "Zack", "Jimmy")
        self.menu4.grid(row=3, column=0)
        
        self.name5 = tk.StringVar(self.t)
        self.name5.set("Player 5 Name")
        self.menu5 = tk.OptionMenu(self.t, self.name5, "Player 5 Name", "Hanna", "Heeran", "James", "Jason", "Kyle", "Derek", "Sam", "Michael", "Brad", "Zack", "Jimmy")
        self.menu5.grid(row=4, column=0)
        
        self.name6 = tk.StringVar(self.t)
        self.name6.set("Player 6 Name")
        self.menu6 = tk.OptionMenu(self.t, self.name6, "Player 6 Name", "Hanna", "Heeran", "James", "Jason", "Kyle", "Derek", "Sam", "Michael", "Brad", "Zack", "Jimmy")
        self.menu6.grid(row=5, column=0)
        
        #Hero played boxes
        self.hero1 = tk.StringVar(self.t)
        self.hero1.set("Hero Played")
        self.hero_menu1 = tk.OptionMenu(self.t, self.hero1, "Hero Played", "Ana", "Bastion", "D.Va", "Genji", "Hanzo", "Junkrat", "Lucio", "McCree", "Mei", "Mercy", "Pharah", "Reaper", "Reinhardt", "Roadhog", "Soldier: 76", "Symmetra", "Torbjorn", "Tracer", "Widowmaker", "Winston", "Zarya", "Zenyatta")
        self.hero_menu1.grid(row=0, column=1)
        
        self.hero2 = tk.StringVar(self.t)
        self.hero2.set("Hero Played")
        self.hero_menu2 = tk.OptionMenu(self.t, self.hero2, "Hero Played", "Ana", "Bastion", "D.Va", "Genji", "Hanzo", "Junkrat", "Lucio", "McCree", "Mei", "Mercy", "Pharah", "Reaper", "Reinhardt", "Roadhog", "Soldier: 76", "Symmetra", "Torbjorn", "Tracer", "Widowmaker", "Winston", "Zarya", "Zenyatta")
        self.hero_menu2.grid(row=1, column=1)
        
        self.hero3 = tk.StringVar(self.t)
        self.hero3.set("Hero Played")
        self.hero_menu3 = tk.OptionMenu(self.t, self.hero3, "Hero Played", "Ana", "Bastion", "D.Va", "Genji", "Hanzo", "Junkrat", "Lucio", "McCree", "Mei", "Mercy", "Pharah", "Reaper", "Reinhardt", "Roadhog", "Soldier: 76", "Symmetra", "Torbjorn", "Tracer", "Widowmaker", "Winston", "Zarya", "Zenyatta")
        self.hero_menu3.grid(row=2, column=1)
        
        self.hero4 = tk.StringVar(self.t)
        self.hero4.set("Hero Played")
        self.hero_menu4 = tk.OptionMenu(self.t, self.hero4, "Hero Played", "Ana", "Bastion", "D.Va", "Genji", "Hanzo", "Junkrat", "Lucio", "McCree", "Mei", "Mercy", "Pharah", "Reaper", "Reinhardt", "Roadhog", "Soldier: 76", "Symmetra", "Torbjorn", "Tracer", "Widowmaker", "Winston", "Zarya", "Zenyatta")
        self.hero_menu4.grid(row=3, column=1)
        
        self.hero5 = tk.StringVar(self.t)
        self.hero5.set("Hero Played")
        self.hero_menu5 = tk.OptionMenu(self.t, self.hero5, "Hero Played", "Ana", "Bastion", "D.Va", "Genji", "Hanzo", "Junkrat", "Lucio", "McCree", "Mei", "Mercy", "Pharah", "Reaper", "Reinhardt", "Roadhog", "Soldier: 76", "Symmetra", "Torbjorn", "Tracer", "Widowmaker", "Winston", "Zarya", "Zenyatta")
        self.hero_menu5.grid(row=4, column=1)
        
        self.hero6 = tk.StringVar(self.t)
        self.hero6.set("Hero Played")
        self.hero_menu6 = tk.OptionMenu(self.t, self.hero6, "Hero Played", "Ana", "Bastion", "D.Va", "Genji", "Hanzo", "Junkrat", "Lucio", "McCree", "Mei", "Mercy", "Pharah", "Reaper", "Reinhardt", "Roadhog", "Soldier: 76", "Symmetra", "Torbjorn", "Tracer", "Widowmaker", "Winston", "Zarya", "Zenyatta")
        self.hero_menu6.grid(row=5, column=1)
        
        
        #map name widget
        self.map_name = tk.StringVar(self.t)
        self.map_name.set("Map")
        self.map_menu = tk.OptionMenu(self.t, self.map_name, "Map", "Hanamura", "Temple of Anubis", "Volskaya Industries", "Dorado", "Route 66", "Watchpoint: Gibraltar", "Hollywood", "King's Row", "Numbani", "Ilios", "Lijiang Tower", "Nepal")
        self.map_menu.grid(row=0, column=2)
        
        #victory widget
        self.victory = tk.BooleanVar(self.t)
        self.true_button = tk.Radiobutton(self.t, text="Victory", variable=self.victory, value=True)
        self.false_button = tk.Radiobutton(self.t, text="Defeat", variable=self.victory, value=False)
        self.true_button.grid(row=0, column=3)
        self.false_button.grid(row=1, column=3)
        
        #submit button
        self.submit_match_button = tk.Button(self.t, text="Submit", command=self.submit_match)
        self.submit_match_button.grid(row=3, column=3)
        
        #match_id entry
#         self.match_id_box = tk.Entry(self.t)
#         self.match_id_box.insert(0, "Enter Match ID")
#         self.match_id_box.grid(row=2, column=3)
        
    def submit_match(self):
        ph1 = (self.name1.get(), self.hero1.get())
        ph2 = (self.name2.get(), self.hero2.get())
        ph3 = (self.name3.get(), self.hero3.get())
        ph4 = (self.name4.get(), self.hero4.get())
        ph5 = (self.name5.get(), self.hero5.get())
        ph6 = (self.name6.get(), self.hero6.get())
        
        map_name = self.map_name.get()
        victory = self.victory.get()
        match_id = self.database.gen_match_id()
        
        match_data = namedtuple("match_data", "ph1 ph2 ph3 ph4 ph5 ph6 map_name victory match_id")
        package = match_data(ph1, ph2, ph3, ph4, ph5, ph6, map_name, victory, match_id)
        
        self.database.add_comp_match(match_id, map_name, victory)
        ph_list = []
        ph_list.append(ph1)
        ph_list.append(ph2)
        ph_list.append(ph3)
        ph_list.append(ph4)
        ph_list.append(ph5)
        ph_list.append(ph6)
        
        for ph in ph_list:
            self.database.add_player(match_id, ph[0], ph[1])
        
        #print(package)
        self.t.destroy()
        return package
    
    def hero_map_submit_check(self):
        hero = self.hero_to_check.get()
        results = self.database.query_total_hero_map_winrates(hero)
        
        wins_values = []
        wins_maps = []
        losses_values = []
        losses_maps = []
        
        for i in results.wins.keys():
            wins_maps.append(i)
        for i in results.wins.values():
            wins_values.append(i)
        for i in results.losses.keys():
            losses_maps.append(i)
        for i in results.losses.values():
            losses_values.append(i)
        
        # Data to plot
        plt.figure(self.figure_count)
        self.figure_count += 1
        labels = wins_maps
        sizes = wins_values
        colors = [(1,1,1)] + [(random(),random(),random()) for i in range(255)]
         
        # Plot
        plt.pie(sizes, labels=labels, colors=colors,
                autopct='%1.1f%%', shadow=True, startangle=140)
         
        plt.axis('equal')
        plt.title(("Wins for {}").format(hero))
        
        plt.figure(self.figure_count)
        self.figure_count += 1
        labels = losses_maps
        sizes = losses_values
        colors = [(1,1,1)] + [(random(),random(),random()) for i in range(255)]
         
        # Plot
        plt.pie(sizes, labels=labels, colors=colors,
                autopct='%1.1f%%', shadow=True, startangle=140)
         
        plt.axis('equal')
        plt.title(("Losses for {}").format(hero))
        
        plt.show()
        
        self.hmwr.destroy()
    
    def hero_map_winrate(self):
        self.hmwr = tk.Toplevel(self)
        self.hmwr.wm_title("Find Hero Win Rates By Map")
        
        self.hero_to_check = tk.StringVar(self.hmwr)
        self.hero_to_check.set("Select Hero")
        self.hero_check_menu = tk.OptionMenu(self.hmwr, self.hero_to_check, "Ana", "Bastion", "D.Va", "Genji", "Hanzo", "Junkrat", "Lucio", "McCree", "Mei", "Mercy", "Pharah", "Reaper", "Reinhardt", "Roadhog", "Soldier: 76", "Symmetra", "Torbjorn", "Tracer", "Widowmaker", "Winston", "Zarya", "Zenyatta")
        self.hero_check_menu.grid(row=0, column=0)
        
#         self.map_to_check = tk.StringVar(self.hmwr)
#         self.map_to_check.set("Select Map")
#         self.map_check_menu = tk.OptionMenu(self.hmwr, self.map_to_check, "Hanamura", "Temple of Anubis", "Volskaya Industries", "Dorado", "Route 66", "Watchpoint: Gibraltar", "Hollywood", "King's Row", "Numbani", "Ilios", "Lijiang Tower", "Nepal")
#         self.map_check_menu.grid(row=0, column=1)
        
        self.submit_button = tk.Button(self.hmwr, text="Submit", command=self.hero_map_submit_check)
        self.submit_button.grid(row=0, column=1)
        
        
    def hero_win_percent(self):
        self.hmwr2 = tk.Toplevel(self)
        self.hmwr2.wm_title("Find Hero Win Rates By Map")
        
        self.hero_to_check2 = tk.StringVar(self.hmwr2)
        self.hero_to_check2.set("Select Hero")
        self.hero_check_menu2 = tk.OptionMenu(self.hmwr2, self.hero_to_check2, "Ana", "Bastion", "D.Va", "Genji", "Hanzo", "Junkrat", "Lucio", "McCree", "Mei", "Mercy", "Pharah", "Reaper", "Reinhardt", "Roadhog", "Soldier: 76", "Symmetra", "Torbjorn", "Tracer", "Widowmaker", "Winston", "Zarya", "Zenyatta")
        self.hero_check_menu2.grid(row=0, column=0)
        
        self.submit_button2 = tk.Button(self.hmwr2, text="Submit", command=self.hero_percent_submit_check)
        self.submit_button2.grid(row=0, column=1)
        
        
    def hero_percent_submit_check(self):
        hero = self.hero_to_check2.get()
        results = self.database.query_win_percent(hero)
        
        wins_values = []
        wins_maps = []
        for i in results.values():
            wins_values.append(i)
        for i in results.keys():
            wins_maps.append(i)
        
        # Data to plot
        plt.figure(self.figure_count)
        self.figure_count += 1
        labels = wins_maps
        sizes = wins_values
        colors = [(1,1,1)] + [(random(),random(),random()) for i in range(255)]
         
        # Plot
        patches, texts = plt.pie(sizes, colors=colors, shadow=True, startangle=90)
        plt.pie(sizes, colors=colors,
                autopct='%1.1f%%', shadow=True, startangle=140)
        plt.legend(patches, labels, loc="best")
        plt.axis('equal')
        plt.title(("Win %'s for {}").format(hero))
        plt.tight_layout()
        plt.show()
        
        self.hmwr2.destroy()
        
# if __name__ == "__main__":
#     root = tk.Tk()
#     ow_stats_gui(root).pack(side="top", fill="both", expand=True)
#     root.mainloop() 