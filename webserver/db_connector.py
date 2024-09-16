#!/usr/bin/python
# -*- coding:utf-8 -*-

# TODO: Specify Docs of function, add Doc for File and variables
import json
from typing import Dict, List, Optional, Set, Tuple
from mariadb import Cursor


def get_all_keywords(cur: Cursor, batch_size: int = 1000) -> list:
    """
    Retrieves all unique keywords from primary_keywords and secondary_keywords
    in the matching_table, fetched in batches.

    :param cur: The database cursor.
    :param batch_size: The number of rows to fetch in each batch.
    :return: A list of unique keywords.
    """
    keywords_set = set()  # To store unique keywords

    # Query to fetch all keywords
    query = "SELECT primary_keywords, secondary_keywords FROM matching_table"
    cur.execute(query)

    while True:
        rows = cur.fetchmany(batch_size)  # Fetch a batch of rows
        if not rows:
            break  # Exit loop if no more rows are fetched

        for primary_keywords, secondary_keywords in rows:
            # Split and strip keywords from both columns, then add them to the set
            keywords_set.update(
                kword.strip() for kword in primary_keywords.split(",") + secondary_keywords.split(",")
            )

    return list(keywords_set)


# TODO: add checks for wrong returns, raise Error
def get_generic_term(synonym: str, cur: Cursor) -> str:
    # Execute the query to get the synonym ID
    cur.execute("SELECT id FROM synonyms WHERE synonym=%s", (synonym,))
    synonym_id = next((id for (id,) in cur), None)

    if synonym_id is None:
        return None

    # Execute the query to get the generic term
    cur.execute("SELECT generic_term FROM generic_terms WHERE id=%s", (synonym_id,))
    gen_term = next((generic_term for (generic_term,) in cur), None)

    return gen_term


# TODO: add check for wrong case_id, raise InvalidCaseIDError
def get_answer_from_db(case_id: int, cur: Cursor) -> str:
    """Returns the answer for a given case_id.

    :param case_id: Integer of the specific answer.
    :return: Returns the answer as a string if it exists.
    :raise InvalidCaseIDError: If case_id is not in the database table.
    """
    # Use parameterized query to prevent SQL injection
    cur.execute("SELECT answer FROM matching_table WHERE caseID = %s", (case_id,))
    result = cur.fetchone()

    if result:
        return result[0]
    else:
        # Raise an error if case_id is not found
        raise ValueError(f"case_id {case_id} is not in the database table.")


def get_caseIDs_by_keywords(words: List[str], cur: Cursor) -> Dict[str, Set[int]]:
    """
    Retrieves case IDs for a list of words.

    :param words: The list of words to look up.
    :param cur: The database cursor.
    :return: A dictionary mapping each word to a set of case IDs.
    """
    unique_words = list(set(words))
    if not unique_words:
        return {}

    # Prepare the SQL query with parameterized placeholders
    # For each word, we'll check if it exists in primary_keywords or secondary_keywords
    conditions = []
    params = []
    for word in unique_words:
        condition = "(primary_keywords LIKE %s OR secondary_keywords LIKE %s)"
        conditions.append(condition)
        # We use wildcards to match any occurrence of the word
        wildcard_word = f"%{word}%"
        params.extend([wildcard_word, wildcard_word])

    where_clause = ' OR '.join(conditions)
    query = f"SELECT caseID, primary_keywords, secondary_keywords FROM matching_table WHERE {where_clause}"
    cur.execute(query, params)
    rows = cur.fetchall()

    # Build a mapping of words to case IDs
    word_caseIDs = {word: set() for word in unique_words}
    for caseID, primary_keywords, secondary_keywords in rows:
        # Combine and split keywords
        all_keywords = primary_keywords.split(',') + secondary_keywords.split(',')
        # Clean up keywords by stripping whitespace
        all_keywords = [kw.strip() for kw in all_keywords]
        # Map each word to its corresponding case IDs
        for word in unique_words:
            if word in all_keywords:
                word_caseIDs[word].add(caseID)

    return word_caseIDs


def get_weights_of_keywords(keywords: List[str], cur: Cursor) -> Dict[str, float]:
    """
    Retrieves the weights for a list of keywords from the weights table using batch requests.
    Handles large lists by chunking.

    :param keywords: The list of keywords to look up.
    :param cur: The database cursor.
    :return: A dictionary mapping each keyword to its weight.
    """
    unique_keywords = list(set(keywords))
    if not unique_keywords:
        return {}

    keyword_weights = {}
    chunk_size = 1000  # Adjust based on database limitations
    for i in range(0, len(unique_keywords), chunk_size):
        chunk = unique_keywords[i:i+chunk_size]
        placeholders = ', '.join(['%s'] * len(chunk))
        query = f"SELECT keyword, weight FROM weights WHERE keyword IN ({placeholders})"
        try:
            cur.execute(query, chunk)
            results = cur.fetchall()
            keyword_weights.update({keyword: weight for keyword, weight in results})
        except Exception as e:
            print(f"An error occurred while fetching weights: {e}")
            continue

    return keyword_weights

def get_primary_keywords_by_caseID(caseID: int, cur: Cursor) -> Optional[str]:
    """
    Retrieves the primary keywords associated with a given caseID from the matching_table.

    :param caseID: The case ID to look up.
    :param cur: The database cursor.
    :return: The primary keywords as a string if found, otherwise None.
    """
    # Use a parameterized query to prevent SQL injection
    cur.execute("SELECT primary_keywords FROM matching_table WHERE caseID = %s", (caseID,))
    result = cur.fetchone()

    if result:
        return result[0]  # Assuming 'primary_keywords' is the first column
    else:
        return None

def get_weights(cur: Cursor) -> str:
    """
    Retrieves all keywords and their weights from the weights table and returns them as a JSON string.

    :param cur: The database cursor.
    :return: A JSON string containing a list of dictionaries with 'keyword' and 'weight'.
    """
    # Execute the query to fetch all keywords and their weights
    cur.execute("SELECT keyword, weight FROM weights")
    # Fetch all results at once
    rows = cur.fetchall()
    # Use a list comprehension to build the list of dictionaries
    weights = [{'keyword': keyword, 'weight': weight} for keyword, weight in rows]
    # Convert the list of dictionaries to a JSON string
    json_str = json.dumps(weights)
    return json_str

def insert_weights(data: List[Tuple[str, float]], cur: Cursor):
    cur.executemany("INSERT INTO weights (keyword, weight) VALUES (%s, %s)", data)