#!/usr/bin/python
# -*- coding:utf-8 -*-

import db_connector
from mariadb import Cursor

# calculate weightings of distinct keywords from input list
# TODO: check if calculation of weighting is correct


def calculate_weight(cur: Cursor) -> list:
    keywords = db_connector.get_all_keywords(cur)
    weightings = []
    keywords_amount = len(keywords)
    for word in keywords:
        weightings = distinct_list(weightings, word)
    i = 0
    while i < len(weightings):
        weightings[i]["count"] = 1 - (weightings[i]["count"] / keywords_amount)
        i += 1
    return weightings


# write distinct keywords with their count in a list and return
def distinct_list(weightings: list, keyword: str) -> list:
    if len(weightings) == 0:
        dict_record = {"keyword": keyword, "count": 1}
        weightings.append(dict_record)
        return weightings
    else:
        i = 0
        while i < len(weightings):
            if keyword == weightings[i].get("keyword"):
                weightings[i].update({"count": weightings[i].get("count") + 1})
                return weightings
            i += 1
        dict_record = {"keyword": keyword, "count": 1}
        weightings.append(dict_record)
        return weightings


def setup(cur: Cursor):
    # Calculate weights
    weights = calculate_weight(cur)
    
    # Ensure the data is in the correct format (list of tuples)
    weights_data = [(weight["keyword"], weight["count"]) for weight in weights]
    
    # Insert weights into the database
    db_connector.insert_weights(weights_data, cur)