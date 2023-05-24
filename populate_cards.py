from favro_request import make_request
from db_actions import populate_db


url = 'https://favro.com/api/v1/cards'
query_params = {'unique': 'true', 'cardSequentialId': 0}
# cards are fetched in batches of 1000 cards, the last_id is a fixed number indicating the highest sequential ID in Favro
start_range = 1
last_id = 30000
end_range = 1001


while end_range <= (last_id+1) :
    cards = [] # raw cards
    card_values = [] # card values to populate card table
    cards_to_tags = [] # tag to card values to populate card_to_tag table
    cards_to_assignments = [] # assignment on card values to populate card_to_assignment table
    cards_to_attachments = [] # attachment on card values to populate card_to_attachment table
    cards_to_dependencies = [] # dependencies on card values to populate card_to_dependency table

    empty_cards = []

    for i in range(start_range,end_range):
        query_params['cardSequentialId'] = i
        card = make_request(url,query_params)
        if len(card) > 0:
            cards.extend(card)
        else:
            empty_cards.append(i)

    for c in cards:
        # populate card values
        card_value = [c['cardCommonId']]
        if "widgetCommonId" in c:
            card_value.append(c['widgetCommonId'])
        else:
            card_value.append(None)
        card_value.append(c['name'])
        if "detailedDescription" in c:
            card_value.append(c['detailedDescription'])
        else:
            card_value.append(None)
        card_value.append(c['sequentialId'])
        if "startDate" in c:
            card_value.append(c['startDate'])
        else:
            card_value.append(None)
        if "dueDate" in c:
            card_value.append(c['dueDate'])
        else:
            card_value.append(None)
        
        card_values.append(card_value)

        # populate cards to tags
        if len(c['tags']) > 0:
            for t in c['tags']:
                tag_value = (c['cardCommonId'],t)
                cards_to_tags.append(tag_value)
        
        # populate card assignments
        if len(c['assignments']) > 0:
            for a in c['assignments']:
                assignment_value = (c['cardCommonId'],a['userId'])
                cards_to_assignments.append(assignment_value)
        
        # populate card attachments
        if len(c['attachments']) > 0:
            for f in c['attachments']:
                attachment_value = (c['cardCommonId'],f['fileURL'])
                cards_to_attachments.append(attachment_value)

        # populate card dependencies
        if len(c['dependencies']) > 0:
            for d in c['dependencies']:
                # only populate if the dependency is not before the current card, this way we record the dependency in only one direction, which translates to current card blocks dependency card
                if d['isBefore'] == False:
                    dependency_value = (c['cardCommonId'],d['cardCommonId'])
                    cards_to_dependencies.append(dependency_value)


    if len(card_values) > 0:
        print("cards:", len(card_values))
        query_cards = "INSERT INTO card (id, widget_id, name, description, issue_key, start_date, due_date) VALUES (?, ?, ?, ?, ?, ?, ?)"
        populate_db(query_cards, card_values)
    if len(cards_to_tags) > 0:
        print("card to tags:", len(cards_to_tags))
        query_tags = "INSERT INTO card_to_tag (card_id, tag_id) VALUES (?, ?)"
        populate_db(query_tags, cards_to_tags)
    if len(cards_to_assignments) > 0:
        print("card to assignments:", len(cards_to_assignments))
        query_assignments = "INSERT INTO card_to_assignment (card_id, user_id) VALUES (?, ?)"
        populate_db(query_assignments, cards_to_assignments)
    if len(cards_to_attachments) > 0:
        print("card to attachments", len(cards_to_attachments))
        query_attachments = "INSERT INTO card_to_attachment (card_id, attachment_url) VALUES (?, ?)"
        populate_db(query_attachments, cards_to_attachments)
    if len(cards_to_dependencies) > 0:
        print("card to dependencies", len(cards_to_dependencies))
        query_dependencies = "INSERT INTO card_dependency (from_card_id, to_card_id) VALUES (?, ?)"
        populate_db(query_dependencies, cards_to_dependencies)

    print(empty_cards)

    start_range = end_range
    if end_range == (last_id+1):
        end_range += 1000 # just to put the end range far over the limit
    elif (end_range+1000) > (last_id+1):
        end_range = last_id+1
    else:
        end_range += 1000