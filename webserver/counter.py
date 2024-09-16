#!/usr/bin/python
# -*- coding:utf-8 -*-
from typing import Any, Dict, List, Optional
import db_connector
from mariadb import Cursor


def count_ids(question: List[str], cur: Cursor) -> Optional[int]:
    """
    Counts IDs based on the given question and returns the highest-scoring case ID.

    :param question: A list of words from the question.
    :param cur: The database cursor.
    :return: The case ID with the highest score, or None if no case ID is found.
    """
    counter = None

    # Remove duplicates to minimize query size
    unique_words = list(set(question))
    if not unique_words:
        return None

    # Retrieve all keyword weights at once
    keyword_weights = db_connector.get_weights_of_keywords(unique_words, cur)

    # Retrieve all case IDs for the question words at once
    word_caseIDs = db_connector.get_caseIDs_by_keywords(unique_words, cur)

    for word in unique_words:
        keyword_weight = keyword_weights.get(word, 0)
        case_ids = word_caseIDs.get(word, set())

        if not case_ids:
            continue

        for case_id in case_ids:
            counter = check_list(counter, case_id, keyword_weight)

    return check_for_highest_id(question, counter, cur)

def check_list(counter: Optional[List[Dict[str, Any]]], case_id: int, weight: float) -> List[Dict[str, Any]]:
    if counter is None:
        return [{"case_id": case_id, "count": weight}]
    else:
        updated = False
        for item in counter:
            if item["case_id"] == case_id:
                item["count"] += weight
                updated = True
                break
        if not updated:
            counter.append({"case_id": case_id, "count": weight})
        return counter


def check_for_highest_id(
    question: List[str],
    counter: List[Dict[str, Any]],
    cur: Cursor
) -> Optional[int]:
    """
    Determines the case ID with the highest count from the counter list.
    If there is a tie, it uses check_for_higher_id to resolve it.

    :param question: List of words from the question.
    :param counter: List of dictionaries with 'case_id' and 'count' keys.
    :param cur: The database cursor.
    :return: The case ID with the highest score, or None if counter is empty.
    """
    if not counter:
        return None

    # Find the maximum count value
    highest_count = max(element['count'] for element in counter)

    top_case_ids = [
        element['case_id'] for element in counter if element['count'] == highest_count
    ]

    if len(top_case_ids) == 1:
        return top_case_ids[0]
    else:
        # Resolve tie using check_for_higher_id
        current_case_id = top_case_ids[0]
        for case_id in top_case_ids[1:]:
            resolved_case_id = check_for_higher_id(question, current_case_id, case_id, cur)
            if resolved_case_id is not None and resolved_case_id != current_case_id:
                current_case_id = resolved_case_id
        return current_case_id


def check_for_higher_id(question: list, case_id: int, new_case_id: int, cur:Cursor) -> int:
    case_id_keywords = db_connector.get_primary_keywords_by_caseID(case_id, cur)
    new_case_id_keywords = db_connector.get_primary_keywords_by_caseID(new_case_id, cur)
    if case_id_keywords is None or new_case_id_keywords is None:
        return None
    
    case_id_counter = len([word for word in question if word in case_id_keywords])
    new_case_id_counter = len([word for word in question if word in new_case_id_keywords])
    
    returned_id = case_id if case_id_counter >= new_case_id_counter else new_case_id
    return returned_id
