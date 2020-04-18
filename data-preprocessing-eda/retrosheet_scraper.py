# takes an action and sees how many runs scored
def compute_num_runs(running):
    runs = 0
    if ('3-H' in running): 
        # +1 RS 
        runs = runs + 1
    if ('2-H' in running): 
        # +1 RS 
        runs = runs + 1
    if ('1-H' in running): 
        # +1 RS 
        runs = runs + 1
    return runs
    
rows = []

for line in lines: 
    if (line[0:2] == 'id'):
        game_date = line.split(',')[1][3:-1]
        game_id = game_date[-1:]
        game_date = game_date[:-1]
    
    # separate info
    if (line[0:4] == 'info'):
        if (line.split(',')[1] == 'visteam'):
            away_team = line.split(',')[2][:-1]
        if (line.split(',')[1] == 'hometeam'):
            home_team = line.split(',')[2][:-1]
    if (line[0:4] == 'play'):
        row = [game_date, game_id]
        play_data = line.split(',')
        # not important to keep inning
        player_team = home_team if play_data[2] == '1' else away_team
        row.append(player_team)
        row.append(play_data[3])
        
#         'AB', 'RS', 'H', 'HR', 'TB', 'BB', 'SF'
        # record play data
        next_play = [0, 0, 0, 0, 0, 0, 0]
        play_details = play_data[6][:-1]

        ##### CASE 1: WHEN NO DIRECTION IS INDICATED
        if (len(play_details.split('/')) == 1):
            # no fielding occured
            if (len(play_details.split('.')) > 1):
                ##### CASE 1: BATTERS ON BASE AND CAN SCORE
                action = play_details.split('.')
                # we ignore walk + events
                if ((action[0] == 'W') or (action[0] == 'HP') 
                    or (action[0] == 'IW') or (action[0] == 'I')):
                    # BB
                    next_play[1] = compute_num_runs(action[1])
                    next_play[5] = 1
                    rows.append(row + next_play) # ADD TO TABLE
                elif (((action[0][0] == 'S') and ('SB' not in action[0]))
                      or ((action[0][0] == 'D') and ('DI' not in action[0]))
                      or (action[0][0] == 'T')):
                    # single, double or triple
                    next_play[0] = 1
                    next_play[1] = compute_num_runs(action[1])
                    next_play[2] = 1
                    next_play[4] = 1 if (action[0][0] == 'S') else (2 if (action[0][0] == 'D') else 3)
                    rows.append(row + next_play) # ADD TO TABLE
                else:
                    # 1 AB no result
                    if ((action[0][0:2] != 'SB') and (action[0][0:2] != 'CS') 
                        and (action[0][0:2] != 'WP') and (action[0][0:2] != 'NP')):
                        next_play[0] = 1
                    next_play[1] = compute_num_runs(action[1])
                    rows.append(row + next_play) # ADD TO TABLE
            else:
                ##### CASE 1B: NO BATTER MOVEMENT; NOBODY ON BASE
                if ((play_details == 'W') or (play_details == 'HP') 
                    or (play_details == 'IW') or (play_details == 'I')):
                    # BB
                    next_play[1] = 0 
                    next_play[5] = 1
                    rows.append(row + next_play) # ADD TO TABLE
                elif (((play_details[0] == 'S')and ('SB' not in play_details))
                      or ((play_details[0] == 'D') and ('DI' not in play_details)) 
                      or (play_details[0] == 'T')):
                    # single, double or triple
                    next_play[0] = 1
                    next_play[1] = 0 # no runs scored
                    next_play[2] = 1
                    next_play[4] = 1 if (play_details[0] == 'S') else (2 if (play_details[0] == 'D') else 3)
                    rows.append(row + next_play) # ADD TO TABLE
                else:
                    # 1 AB no result
                    if ((play_details[0:2] != 'SB') and (play_details[0:2] != 'CS') 
                        and (play_details[0:2] != 'WP') and (play_details[0:2] != 'NP')):
                        next_play[0] = 1
                    rows.append(row + next_play) # ADD TO TABLE
        
        ##### CASE 2: WHEN DIRECTION IS INDICATED
        else:
            play_detail_2 = play_details.split('/')
            if (len(play_detail_2[1].split('.')) > 1):
                ##### CASE 2a: BATTERS ON BASE AND CAN SCORE
                action = play_detail_2[0]
                runners = play_detail_2[1].split('.')[1]
                if ((action == 'H') or (action == 'H9') or (action == 'HR') or (action == 'HR9')):
                    # home runs aren't counted
                    next_play[0] = 1
                    next_play[1] = compute_num_runs(runners) + 1 # home run implicit
                    next_play[2] = 1
                    next_play[3] = 1
                    next_play[4] = 4
                    rows.append(row + next_play) # ADD TO TABLE
                elif (((action[0] == 'S') and ('SB' not in action))
                      or ((action[0] == 'D') and ('DI' not in action)) 
                      or (action[0] == 'T')):
                    # single, double or triple
                    next_play[0] = 1
                    next_play[1] = compute_num_runs(runners)
                    next_play[2] = 1
                    next_play[4] = 1 if (action[0] == 'S') else (2 if (action[0] == 'D') else 3)
                    rows.append(row + next_play) # ADD TO TABLE
                elif(play_detail_2[1].split('.')[0] == 'SF'):
                    # sacrifice fly
                    next_play[1] = 1
                    next_play[6] = 1
                    rows.append(row + next_play) # ADD TO TABLE
                elif(play_detail_2[1].split('.')[0] == 'SH'):
                    # sacrifice hit; not counted as AB or OBP though
                    next_play[1] = compute_num_runs(runners)
                    rows.append(row + next_play) # ADD TO TABLE
                else:
                    # 1 AB no result
                    if ((action[0:2] != 'SB') and (action[0:2] != 'CS') and (action[0:2] != 'WP')):
                        next_play[0] = 1
                    next_play[1] = compute_num_runs(runners)
                    rows.append(row + next_play) # ADD TO TABLE                
            else:
                ##### CASE 2b: BATTERS NOT ON BASE, NO SAC FLIES!
                action = play_detail_2[0]
                if (((action[0] == 'S') and ('SB' not in action))
                    or ((action[0] == 'D') and ('DI' not in action)) 
                    or (action[0] == 'T')):
                    # single, double or triple
                    next_play[0] = 1
                    next_play[1] = 0 # no runs scored
                    next_play[2] = 1
                    next_play[4] = 1 if (action[0] == 'S') else (2 if (action[0] == 'D') else 3)
                    rows.append(row + next_play) # ADD TO TABLE
                elif ((action == 'H') or (action == 'H9') or (action == 'HR') or (action == 'HR9')):
                    # home runs aren't counted
                    next_play[0] = 1
                    next_play[1] = 1 # home run implicit
                    next_play[2] = 1
                    next_play[3] = 1
                    next_play[4] = 4
                    rows.append(row + next_play) # ADD TO TABLE
                else:
                    # 1 AB no result
                    if ((action[0:2] != 'SB') and (action[0:2] != 'CS') and (action[0:2] != 'WP')):
                        next_play[0] = 1
                    rows.append(row + next_play) # ADD TO TABLE  