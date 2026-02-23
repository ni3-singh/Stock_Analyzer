def calculate_score(data):

    score = 0
    if data["pe"] and data["pe"]<25:
        score +=1
    if data["roe"] and data["roe"]>0.5:
        score +=1
    if data["debt_equity"] and data["debt_equity"] < 0.5:
        score += 1

    if data["profit_margin"] and data["profit_margin"] > 0.10:
        score += 1

    if data["revenue_growth"] and data["revenue_growth"] > 0.10:
        score += 1

    return score