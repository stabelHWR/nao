from neo4j_connection import Neo4jConnection
import json
from typing import Optional

class Neo4jConnector:
    def get_all_keywords(connection: Neo4jConnection) -> list:
        """
        Retrieves all unique keywords from primary_keywords and secondary_keywords
        in the matching_table, fetched in batches.

        :param cur: The database cursor.
        :param batch_size: The number of rows to fetch in each batch.
        :return: A list of unique keywords.
        """
        # To store unique keywords

        # Query to fetch all keywords
        query = "MATCH (a:Answer)-[r]->(g:GenericTerm) Return Distinct g.generic_term"
        keywords = connection.query(query, field_name="g.generic_term")
        return keywords

    def get_generic_term(synonym: str, connection: Neo4jConnection) -> str:
        # Execute the query to get the synonym ID
        gen_term = connection.query("MATCH (g:GenericTerm)-[IS_SYNONYM_OF]->(g2:GenericTerm) WHERE g.generic_term=\""+synonym+ "\" Return g2.generic_term" ,field_name="g2.generic_term")
        if gen_term == [] :
            return None
        return gen_term[0]

    def get_answer_from_db(case_id: int, connection: Neo4jConnection) -> str:
        """Returns the answer for a given case_id.

        :param case_id: Integer of the specific answer.
        :return: Returns the answer as a string if it exists.
        :raise InvalidCaseIDError: If case_id is not in the database table.
        """
        # Use parameterized query to prevent SQL injection
        result = connection.query("MATCH (a:Answer) WHERE a.answerID ="+ str(case_id)+" Return a.answer", field_name="a.answer")

        if result:
            return result[0]
        else:
            # Raise an error if case_id is not found
            raise ValueError(f"case_id {case_id} is not in the database table.")


    def get_caseIDs_by_keywords(words: list[str], connection: Neo4jConnection) -> dict[str, set[int]]:
        """
        Retrieves case IDs for a list of words.

        :param words: The list of words to look up.
        :param cur: The database cursor.
        :return: A dictionary mapping each word to a set of case IDs.
        """
        unique_words = list(set(words))
        if not unique_words:
            return {}
        conditions =[]
        for word in unique_words:
            condition = "g.generic_term contains \""+word+"\""
            conditions.append(condition)

        where_clause = ' OR '.join(conditions)
        records = connection.query("MATCH (a:Answer)-[r]->(g:GenericTerm) WHERE "+where_clause+"Return distinct g.generic_term, a.answerID")
        word_answer_dict = {}
        for record in records:
            try:
                word_answer_dict[record["g.generic_term"]].add(record["a.answerID"])
            except KeyError:
                word_answer_dict[record["g.generic_term"]] = set()
                word_answer_dict[record["g.generic_term"]].add(record["a.answerID"])  
        return word_answer_dict

    def get_weights_of_keywords(keywords: list[str], connection: Neo4jConnection) -> dict[str, float]:
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
        
        conditions = []
        for word in unique_keywords:
            condition = "g.generic_term contains \""+word+"\""
            conditions.append(condition)

        where_clause = ' OR '.join(conditions)
        records = connection.query("MATCH (a:Answer)-[r]->(g:GenericTerm) WHERE "+where_clause+"Return distinct g.generic_term, r.weight")
        keyword_weights = {}
        for record in records:
            keyword_weights[record["g.generic_term"]]= record["r.weight"]
        return keyword_weights
    def get_primary_keywords_by_caseID(caseID: int, connection: Neo4jConnection) -> Optional[str]:
        """
        Retrieves the primary keywords associated with a given caseID from the matching_table.

        :param caseID: The case ID to look up.
        :param cur: The database cursor.
        :return: The primary keywords as a string if found, otherwise None.
        """
        # Use a parameterized query to prevent SQL injection
        result = connection.query("MATCH (a:Answer)-[r:HAS_PRIMARY_KEY]->(g:GenericTerm) WHERE a.answerID ="+ str(caseID)+ " Return g.generic_term", field_name="g.generic_term")
        if result == []:
            result = None
        return result

    def get_weights(connection: Neo4jConnection) -> str:
        """
        Retrieves all keywords and their weights from the weights table and returns them as a JSON string.

        :param cur: The database cursor.
        :return: A JSON string containing a list of dictionaries with 'keyword' and 'weight'.
        """
        records = connection.query("MATCH (a:Answer)-[r]->(g:GenericTerm)  Return distinct g.generic_term, r.weight")
        # Use a list comprehension to build the list of dictionaries
        weights = [{'keyword': record["g.generic_term"], 'weight': record["r.weight"]} for record in records]
        # Convert the list of dictionaries to a JSON string
        json_str = json.dumps(weights)
        return json_str

    def insert_weights(data: list[tuple[str, float]], connection: Neo4jConnection):
        for tupl in data:
            connection.execute_query("MATCH (a:Answer)-[r]->(g:GenericTerm) Where g.generic_term = \""+tupl[0]+"\" SET r.weight = "+str(tupl[1]))
