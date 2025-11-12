# 1.0 Function: Get a 4 digit year from the 'Aired' column
def get_start_year(aired):
    '''
    Clean the Aired column to get a 4-digit year
    
    Args:
        column aired

    Returns:
        returns a 4-char
    '''
    if ' - ?' in str(aired):
        # Extract year from the start date
        start_part = aired.split(' - ?')[0] # get the 1st element after spliting by ' - ?'
        return start_part[-4:]  # Get year
    else:
        return aired[-4:]  # jsut take the lat 4 chars
    


 # 2.0 Function Get the User RAtings Base Numberic
def get_users_base(score):
    '''
    Get the user rating base number from the Score column
    
    Args:
        column score

    Returns:
        returns the numeric between (numeric) element after locating 'by' 
    '''
    score_split = score.split(' ')
    try:
        by_index = score_split.index('by') # find the index of the 'by' word

        user_str = score_split[by_index + 1]  # get the element after 'by'

        return user_str.replace(',', '')  # remove any thousand separator
    
    except (ValueError, IndexError):
        return '0'
   