'''
Created on Aug 2, 2016

@author: Hanna
'''

import mysql.connector
from collections import namedtuple

        
class ow_database():
    def __init__(self):
        self.status = "Online"
        self.match_id = 0
        file = open("login.txt", "r")
        for line in file:
            tup = line.split("=")
            if tup[0] == "username":
                self.user = tup[1]
            if tup[0] == "password":
                self.password = tup[1]
            
    def query_total_hero_map_winrates(self, hero):
        win_maps = dict()
        lose_maps = dict()
         
        cnx = mysql.connector.connect(user=self.user, password=self.password, host='127.0.0.1', database='ow_stats')
        cursor = cnx.cursor()
        query = ("SELECT map_name FROM comp_match cm, player p WHERE p.hero = '{}' and cm.victory = true and cm.match_id = p.match_id").format(hero)
        cursor.execute(query)
        result = cursor.fetchall()
        for row in result:
            if row[0] not in win_maps.keys():
                win_maps[row[0]] = 1
            else:
                win_maps[row[0]] += 1 
        #print(win_maps)
         
        query = ("SELECT map_name FROM comp_match cm, player p WHERE p.hero = '{}' and cm.victory = false and cm.match_id = p.match_id").format(hero)
        cursor.execute(query)
        result = cursor.fetchall()
        for row in result:
            if row[0] not in lose_maps.keys():
                lose_maps[row[0]] = 1
            else:
                lose_maps[row[0]] += 1 
        #print(lose_maps)
         
        wins_losses = namedtuple("wins_losses", "wins losses")
        package = wins_losses(win_maps, lose_maps)
         
        cursor.close()
        cnx.close()
        return package
    
        
    def query_win_percent(self, hero):
        maps =  ["Hanamura", "Temple of Anubis", "Volskaya Industries", "Dorado", "Route 66", "Watchpoint: Gibraltar", "Hollywood", "King's Row", "Numbani", "Ilios", "Lijiang Tower", "Nepal"]
        win_maps = dict()
        lose_maps = dict()
        win_percent = dict()
        for i in maps:
            win_percent[i] = 0.0
            win_maps[i] = 0
            lose_maps[i] = 0
        
        cnx = mysql.connector.connect(user=self.user, password=self.password, host='127.0.0.1', database='ow_stats')
        cursor = cnx.cursor()
        query = ("SELECT map_name FROM comp_match cm, player p WHERE p.hero = '{}' and cm.victory = true and cm.match_id = p.match_id").format(hero)
        cursor.execute(query)
        result = cursor.fetchall()
        for row in result:
            if row[0] not in win_maps.keys():
                win_maps[row[0]] = 1
            else:
                win_maps[row[0]] += 1 
        #print(win_maps)
        
        query = ("SELECT map_name FROM comp_match cm, player p WHERE p.hero = '{}' and cm.victory = false and cm.match_id = p.match_id").format(hero)
        cursor.execute(query)
        result = cursor.fetchall()
        for row in result:
            if row[0] not in lose_maps.keys():
                lose_maps[row[0]] = 1
            else:
                lose_maps[row[0]] += 1 
        #print(lose_maps)
        
        for i in win_maps.keys():
            if win_maps[i] != 0 or lose_maps[i] != 0:
                win_percent[i] = win_maps[i] / (win_maps[i] + lose_maps[i])
                
        cursor.close()
        cnx.close()
        return win_percent
    
    
    def query_hero_map_winrate(self, map_name, hero):
        cnx = mysql.connector.connect(user=self.user, password=self.password, host='127.0.0.1', database='ow_stats')
        cursor = cnx.cursor()
        query = ("SELECT count(victory) FROM comp_match cm, player p WHERE p.hero = '{}' and cm.victory = true and cm.map_name = '{}' and cm.match_id = p.match_id").format(hero, map_name)
        cursor.execute(query)
        result = cursor.fetchall()
        for row in result:
            win_total = row[0]
        
        query = ("SELECT count(victory) FROM comp_match cm, player p WHERE p.hero = '{}' and cm.victory = false and cm.map_name = '{}' and cm.match_id = p.match_id").format(hero, map_name)
        cursor.execute(query)
        result = cursor.fetchall()
        for row in result:
            lose_total = row[0]
            
        win_loss = namedtuple("win_loss", "map_name hero wins losses")
        rate = win_loss(map_name, hero, win_total, lose_total)
        
        
        cursor.close()
        cnx.close()
          
        #print(rate)
        return rate
    
    def add_comp_match(self, match_id, map_name, victory):
        cnx = mysql.connector.connect(user=self.user, password=self.password, host='127.0.0.1', database='ow_stats')
        cursor = cnx.cursor()
        query = ("INSERT INTO comp_match(match_id, map_name, victory) VALUES ({}, '{}', {})").format(match_id, map_name, victory)
        cursor.execute(query)
        
        cnx.commit()
        cursor.close()
        cnx.close()
        
    def add_player(self, match_id, player_name, hero):
        cnx = mysql.connector.connect(user=self.user, password=self.password, host='127.0.0.1', database='ow_stats')
        cursor = cnx.cursor()
        query = ("INSERT INTO player(match_id, player_name, hero) VALUES ({}, '{}', '{}')").format(match_id, player_name, hero)
        cursor.execute(query)
        
        cnx.commit()
        cursor.close()
        cnx.close()    
        
    def add_personal_match(self, match_id, player_name, hero, map_name, victory):
        cnx = mysql.connector.connect(user=self.user, password=self.password, host='127.0.0.1', database='ow_stats')
        cursor = cnx.cursor()
        # query = ("INSERT INTO personal_game(player_name, hero, map_name, victory) VALUES ('{}', '{}', '{}', {})").format(player_name, hero, map_name, victory)
        query = ("INSERT INTO comp_match(match_id, map_name, victory, is_personal) VALUES ({}, '{}', {}, {})").format(match_id, map_name, victory, True)
        cursor.execute(query)
        
        cnx.commit()
        query = ("INSERT INTO player(match_id, player_name, hero) VALUES ({}, '{}', '{}')").format(match_id, player_name, hero)
        cursor.execute(query)
        
        cnx.commit()
        cursor.close()
        cnx.close()
    
    def gen_match_id(self):
        cnx = mysql.connector.connect(user=self.user, password=self.password, host='127.0.0.1', database='ow_stats')
        cursor = cnx.cursor()
        query = ("SELECT cm.match_id FROM comp_match cm, player ORDER BY cm.match_id DESC LIMIT 0, 1")
        cursor.execute(query)
        
        result = cursor.fetchall()
        for row in result:
            self.match_id = row[0]
            
        self.match_id += 1
        
        cursor.close()
        cnx.close()
        return self.match_id
    
    def query_match_history(self, player_name):
        cnx = mysql.connector.connect(user=self.user, password=self.password, host='127.0.0.1', database='ow_stats')
        cursor = cnx.cursor()
        query = ("SELECT * from player p, comp_match cm WHERE cm.match_id = p.match_id and p.player_name = '{}'").format(player_name, player_name)
        cursor.execute(query)
        
        result = cursor.fetchall()
        
        cursor.close()
        cnx.close()
        return result

        
#if __name__ == '__main__':
#     database = ow_database()
#     database.add_comp_match(1, "Numbani", True)
#     database.add_comp_match(2, "Numbani", True)
#     database.add_comp_match(3, "Numbani", True)
#     database.add_comp_match(4, "Numbani", True)
#      
#     database.add_player(1, "Hanna", "Lucio")
#     database.add_player(2, "Hanna", "Lucio")
#     database.add_player(3, "Hanna", "Lucio")
#     database.add_player(4, "Hanna", "Lucio")
#     
#     database.add_comp_match(5, "Numbani", False)
#     database.add_comp_match(6, "Numbani", False)
# 
#      
#     database.add_player(5, "Hanna", "Lucio")
#     database.add_player(6, "Hanna", "Lucio")

    #database = ow_database()
    #database.query_hero_map_winrate("Numbani", "Lucio")    
        