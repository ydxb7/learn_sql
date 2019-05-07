#!/usr/bin/env python
# 
# tournament.py -- implementation of a Swiss-system tournament
#

#import psycopg2
import mysql.connector


def connect():
    """Connect to the PostgreSQL database.  Returns a database connection."""
    return mysql.connector.connect(host="localhost", user="learner", passwd="abcd1234", database="tournament")


def deleteMatches():
    """Remove all the match records from the database."""
    db = connect()
    c = db.cursor()
    c.execute("delete from matches")
    db.commit()
    db.close()
    return


def deletePlayers():
    """Remove all the player records from the database."""
    db = connect()
    c = db.cursor()
    c.execute("delete from players")
    db.commit()
    db.close()
    return


def countPlayers():
    """Returns the number of players currently registered."""
    db = connect()
    c = db.cursor()
    c.execute("select count(*) from tournament.players;")
    ans = c.fetchall()[0][0]
    db.close()
    return ans


def registerPlayer(name):
    """Adds a player to the tournament database.
  
    The database assigns a unique serial id number for the player.  (This
    should be handled by your SQL database schema, not in your Python code.)
  
    Args:
      name: the player's full name (need not be unique).
    """
    db = connect()
    c = db.cursor()
    c.execute("insert into players (fullname) values (%s)", (name,))
    db.commit()
    db.close()
    return


def playerStandings():
    """Returns a list of the players and their win records, sorted by wins.

    The first entry in the list should be the player in first place, or a player
    tied for first place if there is currently a tie.

    Returns:
      A list of tuples, each of which contains (id, name, wins, matches):
        id: the player's unique id (assigned by the database)
        name: the player's full name (as registered)
        wins: the number of matches the player has won
        matches: the number of matches the player has played
    """
    db = connect()
    c = db.cursor()
    query = '''
    select players.player_id, players.fullname, subq1.wins as wins, subq1.wins + subq2.loses as matches
    from players 
    	left join (select players.player_id, count(matches.winner_id) as wins from players left join matches on players.player_id = matches.winner_id 
    				group by players.player_id) as subq1
    		on players.player_id = subq1.player_id
    	left join (select players.player_id, count(matches.loser_id) as loses from players left join matches on players.player_id = matches.loser_id 
    				group by players.player_id) as subq2
    		on players.player_id = subq2.player_id
    	order by wins desc;'''
    c.execute(query)
    ans = c.fetchall()
    db.close()
    return ans


def reportMatch(winner, loser):
    """Records the outcome of a single match between two players.

    Args:
      winner:  the id number of the player who won
      loser:  the id number of the player who lost
    """
    db = connect()
    c = db.cursor()
    c.execute("insert into matches (winner_id, loser_id) values (%s, %s)", (winner, loser))
    db.commit()
    db.close()
    return
 
def swissPairings():
    """Returns a list of pairs of players for the next round of a match.
  
    Assuming that there are an even number of players registered, each player
    appears exactly once in the pairings.  Each player is paired with another
    player with an equal or nearly-equal win record, that is, a player adjacent
    to him or her in the standings.
  
    Returns:
      A list of tuples, each of which contains (id1, name1, id2, name2)
        id1: the first player's unique id
        name1: the first player's name
        id2: the second player's unique id
        name2: the second player's name
    """
    p = playerStandings()
    N = len(p)
    ans = []
    for i in range(N // 2):
        ans.append((p[i * 2][0], p[i * 2][1], p[i * 2 + 1][0], p[i * 2 + 1][1]))
    return ans
