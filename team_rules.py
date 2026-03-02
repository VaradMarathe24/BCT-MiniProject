from collections import Counter

def validate_team(team):
    """
    Fantasy cricket simple rules:
    - Exactly 11 players
    - Max 7 from one real team
    - Total credits <= 100
    """
    if len(team) != 11:
        return False, "Team must have 11 players"

    team_count = Counter([p['team'] for p in team])
    if any(count > 7 for count in team_count.values()):
        return False, "Max 7 players allowed from one side"

    total_credits = sum(p['credit'] for p in team)
    if total_credits > 100:
        return False, f"Credit limit exceeded: {total_credits}/100"

    return True, "Team is valid"
