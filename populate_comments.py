from favro_request import make_request
from db_actions import populate_db, request_data
from process_attachment import get_attachment_name, download_attachment

def populate_comments():
    url = 'https://favro.com/api/v1/comments'
    request_params = {'cardCommonId': 1}
    # comments are fetched per block of 100 cards
    start_range = 0
    end_range = 100

    # fetch all cards with their sequence number
    query = "SELECT c.issue_key, c.id FROM card c ORDER BY c.issue_key"
    cards = request_data(query)

    total_range = len(cards)

    while end_range <= total_range:
        comments = []
        comment_values = []
        attachment_values = []
        for i in range(start_range,end_range):
            request_params['cardCommonId'] = cards[i][1]
            comment = make_request(url, request_params)
            if len(comment) > 0:
                comments.extend(comment)
        
        if len(comments) > 0:
            # create comment values to insert
            for c in comments:
                comment_value = (c['commentId'],c['cardCommonId'],c['comment'],c['userId'],c['created'])
                comment_values.append(comment_value)

                # create comment attachment values to insert and download attachments 
                if "attachments" in c:
                    if len(c['attachments']) > 0:
                        for a in c['attachments']:
                            name = get_attachment_name(a['fileURL'])
                            download_attachment(a['fileURL'], 'local/comment_attachments/')
                            attachment = (c['commentId'],a['fileURL'],name,'')
                            attachment_values.append(attachment)
            
            if len(comment_values) > 0:
                print('comments:', len(comment_values))
                query_comments = "INSERT INTO comment (id, card_id, comment, user_id, created) VALUES (?, ?, ?, ?, ?)"
                populate_db(query_comments, comment_values)
                print('last card sequence number for current range:', cards[end_range-1][0])

            if len(attachment_values) > 0:
                print('attachments:', len(attachment_values))
                query_attachments = "INSERT INTO comment_to_attachment (comment_id, attachment_url, name, new_url) VALUES (?, ?, ?, ?)"
                populate_db(query_attachments, attachment_values)
        else:
            print('last card sequence number for current range:', cards[end_range-1][0])
        
        start_range = end_range
        if end_range == total_range:
            end_range += 100 # just to put the end range far over the limit
        elif (end_range+100) > (total_range):
            end_range = total_range
        else:
            end_range += 100
