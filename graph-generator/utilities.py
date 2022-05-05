def add_turns(json):
    """
    ensures that each edu has a correct turn number field
    """
    for dialogue in json['dialogues']:
        turn_no = 0
        turn_id = None
        for edu in dialogue['edus']:
            if edu['turn_id'] == turn_id:
                edu['turn_no'] = turn_no
            else:
                turn_id = edu['turn_id']
                turn_no += 1
                edu['turn_no'] = turn_no
    return json