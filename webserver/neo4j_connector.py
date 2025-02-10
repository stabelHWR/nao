from neo4j import GraphDatabase

# Neo4j Verbindungsklasse
class Neo4jConnection:
    def __init__(self, uri, user, password):
        self.__uri = uri
        self.__user = user
        self.__password = password
        self.__driver = None
        self.__session = None

    def open(self):
        """Verbindung zur Neo4j-Datenbank öffnen."""
        self.__driver = GraphDatabase.driver(self.__uri, auth=(self.__user, self.__password))
        self.__session = self.__driver.session()

    def close(self):
        """Verbindung zur Neo4j-Datenbank schließen."""
        if self.__session:
            self.__session.close()

    def query(self, query, parameters=None):
        """Führe eine Abfrage aus und gib die Ergebnisse zurück."""
        if not parameters:
            parameters = {}
        result = self.__session.run(query, parameters)
        return [record for record in result]

    def execute_query(self, query):
        with self.__driver.session() as session:
            session.run(query)
# Verbindungseinstellungen
uri = "neo4j://localhost:7999"  # Beispiel-URI
user = "neo4j"  # Standardbenutzername
password = "password"  # Dein Passwort

# Verbindung aufbauen
neo4j_conn = Neo4jConnection(uri, user, password)
neo4j_conn.open()

# Beispielabfrage: Alle Knoten vom Typ 'Person' abfragen

query1 = """
CREATE CONSTRAINT ON (a:Answer) ASSERT a.answerID IS UNIQUE;
"""
neo4j_conn.execute_query(query1)
"""for record in result:
    print(f"Person Name: {record['generic_term']}")"""
# 2. Erstellen der Answer-Knoten
query2 = """
CREATE  (a1:Answer {answerID: 1, answer: 'Es gibt eine Übersicht aller Studiengänge auf der Webseite der HWR Berlin. Außerdem findest du dort alle Bewerbungs- und Zulassungsvoraussetzungen. Bei Fragen zur Studienorientierung und Studienwahl kannst du dich an die Allgemeine Studienberatung wenden. Zu vielen Themen bietet auch der Studierendenservice der HWR Berlin regelmäßig Online-Veranstaltungen an, bei denen du ins Gespräch kommen kannst. Und in unserer Instathek kannst du Studierende der HWR Berlin treffen und Infos aus erster Hand bekommen.'}),
        (a2:Answer {answerID: 2, answer: 'Du benötigst eine anerkannte Hochschulzugangsberechtigung. Diese wären die allgemeine Hochschulreife, also das Abitur, eine fachgebundene Hochschulreife oder Fachhochschulreife, auch Fachabitur genannt oder eine andere Hochschulzugangsberechtigung. Außerdem solltest du auch Interesse am Fach mitbringen.'}),
        (a3:Answer {answerID:3, answer: 'Es gibt unterschiedliche Bewerbungsverfahren. Es hängt von deinem Schulabschluss, Fachsemester und Studienziel ab, auf welchem Weg du dich an der Hochschule für Wirtschaft und Recht Berlin für ein Bachelorstudium bewirbst. Ob es dual, normal, ein Bachelor oder Masterstudium werden soll ist ebenfalls ausschlaggebend. Auf dem Onlineportal der HWR gibt es genauere Infos dazu.'}),
        (a4:Answer {answerID:4, answer: 'Die Bewerbung für duale Studiengänge läuft direkt über die Partnerunternehmen der jeweiligen Studiengänge an der HWR Berlin. Bitte beachte: Bei vielen Partnerunternehmen solltest du dich ein Jahr vor Studienbeginn bewerben. Auf der Webseite der HWR findest du auch eine Liste mit allen Partnerunternehmen für jeden Studiengang. Bei weiteren Fragen unterstützt dich auch gerne die Studienberatung.'}),
        (a5:Answer {answerID:5, answer: 'Das duale Studium der Informatik gliedert sich in den theoretischen und praktischen Teil. In der Praxis werden betriebliche Aufgaben innerhalb des Unternehmens bewältigt. Der theoretische Teil wird an der Hochschule absolviert. In den einzelnen Semestern werden Module wie mathematische Methoden, Betriebssysteme oder Datenbanken behandelt. Neben Klausuren werden auch Praxistransferberichte, Studienarbeiten oder eine Bachelorthesis verfasst.'}),
        (a6:Answer {answerID:6, answer: 'Das duale Bachelorstudium qualifiziert sowohl für Tätigkeiten in der Software- Entwicklung als auch in der Systemadministration. Absolventinnen und Absolventen des Studiengangs kommen vor allem in den folgenden Bereichen zum Einsatz: Entwicklungsabteilungen von Unternehmen aus der Softwarebranche, IT-Dienstleister oder unternehmensinterne IT-Abteilungen.'}),
        (a7:Answer {answerID:7, answer: 'Der duale Studiengang Informatik ist einer von derzeit 18 dualen Studiengängen an der HWR. Die Dauer des Studiums beträgt 6 Semester und umfasst mehrere unterschiedliche Module, die Grundwissen und fortgeschrittenes Anwendungswissen vermitteln sollen. Dazu gehören beispielsweise Betriebssysteme, Datenbanken, Software-Engineering, Programmierung und mathematische Module wie Statistik und Datenanalyse. Am Campus Lichtenberg findet der theoretische Teil statt, wobei Probleme und Lösungsmöglichkeiten, spezielle Methoden, kleine Anwendungsbeispiele und theoretisches Wissen vermittelt wird. Der Praxisteil findet im Unternehmen statt und umfasst abteilungsabhängige Aufgaben, die mit dem Theoriewissen einhergehen können.'}),
        (a8:Answer {answerID:8, answer: 'Das Informatikstudium setzt sich aus Grundlagen wie Mathematik, Programmieren, Software-Engineering und vielen weiteren Modulen zusammen. Dabei werden gesellschaftliche und juristische Aspekte, Problematiken und deren Lösungsansätze sowie grundsätzliches, fachliches Wissen vermittelt und praktisch erläutert.'}),
        (a9:Answer {answerID:9, answer: 'Ein Praxistransferbericht, kurz auch PTB genannt, ist eine schriftliche Arbeit, welche während der Praxisphase im Unternehmen geschrieben wird. Der PTB bezieht sich auf ein betriebliches Thema, welches aktuell im Unternehmen anfällt. Diese wissenschaftliche Arbeit geht in die Gesamtbewertung eines Moduls des aktuellen Semesters ein.'}),
        (a10:Answer {answerID:10, answer: 'Eine Studienarbeit ist wie ein PTB eine wissenschaftliche Arbeit, bei der von der Hochschule angebotene Themen meistens in kleinen Gruppen, aber auch alleine bearbeitet werden. Der Umfang der Arbeit ist etwa doppelt so groß wie bei einem PTB und diese wissenschaftliche Arbeit geht ebenfalls in die Gesamtbewertung eines Moduls des aktuellen Semesters ein.'}),
        (a11:Answer {answerID:11, answer: 'Eine Bachelorarbeit ist die Abschlussarbeit eines Bachelor-Studiums und wird sowohl schriftlich verfasst als auch vor einem Publikum präsentiert. Die Präsentation wird auch Kolloquium genannt. Der schriftliche Umfang beträgt etwa das dreifache eines Praxistransferberichts. Diese wissenschaftliche Arbeit geht in die Gesamtbewertung des Studiums ein.'}),
        (a12:Answer {answerID:12, answer: 'Im Verlaufe des Studiums werden drei PTBs in den ersten drei Semestern und zwei Studienarbeiten im vierten und fünften Semester geschrieben. Abhängig vom Studiengang kann anstelle der Studienarbeit im fünften Semester eine mündlichge Trasnferprüfung abgehalten werden. Im sechsten Semester wird dann eine Bachelorthesis als Abschlussarbeit verfasst.'}),
        (a13:Answer {answerID:13, answer: 'Das Informatikstudium besteht aus folgenden Modulen. Die Grundlagen bestehen aus Mathematik, Programmieren, technische Grundlagen der Informatik und theoretischer Informatik. Die übergreifenden Inhalte sind Betriebswirtschaftslehre, Gesellschaftliche und juristische Aspekte der Informatik, Projektmanagement, Softwareengineering, Betriebssysteme, Datenbanken und Netzwerke. Als Wahlpflichtfächer kann man zwischen Grafik und Multimedia, Kommunikationssysteme, Mobile Systeme und Künstliche Intelligenz.'}),
        (a14:Answer {answerID:14, answer: 'Die Hochschule für Wirtschaft und Recht ist neben der HTW und der Beuth Hochschule eine der größten Hochschulen in Berlin. Sie vereint viele Ausrichtungen und Fachbereiche in einer Hochschule. Ich kann dir gerne etwas mehr über die HWR erzählen. Du kannst mich zum Beispiel nach der Gründung, der Anzahl an Studierenden oder den Standorten fragen.'}),
            (a15:Answer {answerID:15, answer: 'Die HWR, so wie sie heute bekannt ist, gibt es seit 2009. Sie hat sich aus dem Zusammenschluss der Berlin School of Economics und der Fachhochschule für Verwaltung und Rechtspflege Berlin ergeben.'}),
        (a16:Answer {answerID:16, answer: 'An der HWR studieren zurzeit circa 11400 Menschen, wovon über 2000 ein duales Studium machen.'}),
        (a17:Answer {answerID:17, answer: 'Die Hochschule für Wirtschaft und Recht hat 2 Standorte. Diese liegen in Lichtenberg und in Schöneberg. Der Campus Schöneberg und der Standort an der Möckernbrücke werden vom Fachbereich 1 genutzt, während der Campus Lichtenberg von den anderen Fachbereichen verwendet wird.'}),
        (a18:Answer {answerID:18, answer: 'Die HWR hat 5 Fachbereiche. Diese sind Fachbereich 1 für Wirtschaftswissenschaften, Fachbereich 2 für duales Studium, Fachbereich 3 für Allgemeine Verwaltung, Fachbereich 4 für Rechtspflege und Fachbereich 5 für Polizei und Sicherheitsmanagement.'}),
        (a19:Answer {answerID:19, answer: 'Es gibt zurzeit 56 Studiengänge, welche in Bachelor, Master, Fernstudium, duales Studium und berufsbegleitendes Studium unterteilt werden. Davon sind 18 duale Studiengänge.'}),
        (a20:Answer {answerID:20, answer: 'Die Studiengänge kann man grob in technische und wirtschaftliche Studiengänge unterteilen. Zu den technischen Studiengängen gehören unter anderem Bau-ingenieurwesen, Informatik und industrielle Elektrotechnik. Im Wirtschaftsbereich gibt es zum Beispiel BWL-Industrie und Wirtschaftsinformatik.'}),
        (a21:Answer {answerID:21, answer: 'Ein Bachelorstudium hat eine Länge von 6 Semestern und dauert damit circa 3 Jahre lang. Wenn du an dein Bachelorstudium noch einen Master anhängen möchtest, verlängert sich dein Studium um 2 bis 4 Semester.'}),
        (a22:Answer {answerID:22, answer: 'Informatik ist die Wissenschaft von der systematischen Darstellung, Speicherung, Verarbeitung und Übertragung von Informationen, besonders der automatischen Verarbeitung mit Digitalrechnern. Historisch hat sich die Informatik einerseits aus der Mathematik als Strukturwissenschaft entwickelt, andererseits als Ingenieursdisziplin aus dem praktischen Bedarf nach der schnellen und insbesondere automatischen Ausführung von Berechnungen.'}),
        (a23:Answer {answerID:23, answer: 'Mein Name ist NAO. Ich bin ein humanoider Roboter.'}),
        (a24:Answer {answerID:24, answer: 'Ich wurde im Firmenhauptsitz von Softbank-Robotics in Paris entwickelt.'}),
        (a25:Answer {answerID:25, answer: 'Ich kann alles, was bei mir einprogrammiert wurde. Ich kann mich mit dir unterhalten und ich kann Dinge erkennen und sogar tanzen. Heute habe ich da aber keine Lust darauf und unterhalte mich lieber nur.'});

       """
neo4j_conn.execute_query(query2)

# 3. CREATE CONSTRAINT für GenericTerm
query3 = """
CREATE CONSTRAINT ON (g:GenericTerm) ASSERT g.id IS UNIQUE;
"""
neo4j_conn.execute_query(query3)

query4 = """
Create (g1:GenericTerm{id:1, generic_term: 'brauchen'} ),
(g2:GenericTerm{ id:2, generic_term: 'studiengang'} ),
(g3:GenericTerm{ id:3, generic_term: 'hwr'} ),
(g4:GenericTerm{ id:4, generic_term: 'ptb'} ),
(g5:GenericTerm{ id:5, generic_term: 'schreiben'} ),
(g6:GenericTerm{ id:6, generic_term: 'studienarbeit'} ),
(g7:GenericTerm{ id:7, generic_term: 'informieren'} ),
(g8:GenericTerm{ id:8, generic_term: 'aufbau'} ),
(g9:GenericTerm{ id:9, generic_term: 'bachelor'} ),
(g10:GenericTerm{ id:10, generic_term: 'beruf'} ),
(g11:GenericTerm{ id:11, generic_term: 'bachelorarbeit'} ),
(g12:GenericTerm{ id:12, generic_term: 'modul'} ),
(g13:GenericTerm{ id:13, generic_term: 'erzählen'} ),
(g14:GenericTerm{ id:14, generic_term: 'gründen'} ),
(g15:GenericTerm{ id:15, generic_term: 'student'} ),
(g16:GenericTerm{ id:16, generic_term: 'haben'} ),
(g17:GenericTerm{ id:17, generic_term: 'bewerben'} ),
(g18:GenericTerm{ id:18, generic_term: 'informatikstudium'} ),
(g19:GenericTerm{id:19, generic_term: 'brauche'} ),
(g20:GenericTerm{ id:20, generic_term: 'brauch'} ),
(g21:GenericTerm{ id:21, generic_term: 'benötigen'} ),
(g22:GenericTerm{ id:22, generic_term: 'studiengänge'} ),
(g23:GenericTerm{ id:23, generic_term: 'uni'} ),
(g24:GenericTerm{ id:24, generic_term: 'campus'} ),
(g25:GenericTerm{ id:25, generic_term: 'universität'} ),
(g26:GenericTerm{ id:26, generic_term: 'hochschule'} ),
(g27:GenericTerm{ id:27, generic_term: 'praxistransferbericht'} ),
(g28:GenericTerm{ id:28, generic_term: ' praxistransferberichte'} ),
(g29:GenericTerm{ id:29, generic_term: 'ptps'} ),
(g30:GenericTerm{ id:30, generic_term: 'verfassen'} ),
(g31:GenericTerm{ id:31, generic_term: 'studienarbeiten'} ),
(g32:GenericTerm{ id:32, generic_term: 'erkundigen'} ),
(g33:GenericTerm{ id:33, generic_term: 'schlaumachen'} ),
(g34:GenericTerm{ id:34, generic_term: 'information'} ),
(g35:GenericTerm{ id:35, generic_term: 'aufbauen'} ),
(g36:GenericTerm{ id:36, generic_term: 'zusammensetzen'} ),
(g37:GenericTerm{ id:37, generic_term: 'zusammensetzung'} ),
(g38:GenericTerm{ id:38, generic_term: 'struktur'} ),
(g39:GenericTerm{ id:39, generic_term: 'strukturieren'} ),
(g40:GenericTerm{ id:40, generic_term: 'bestehen'} ),
(g41:GenericTerm{ id:41, generic_term: 'besteht'} ),
(g42:GenericTerm{ id:42, generic_term: 'ablaufen'} ),
(g43:GenericTerm{ id:43, generic_term: 'laufen'} ),
(g44:GenericTerm{ id:44, generic_term: 'bachelorabschluss'} ),
(g45:GenericTerm{ id:45, generic_term: 'berufe'} ),
(g46:GenericTerm{ id:46, generic_term: 'berufsfeld'} ),
(g47:GenericTerm{ id:47, generic_term: 'berufsfelder'} ),
(g48:GenericTerm{ id:48, generic_term: 'bachelorthesis'} ),
(g49:GenericTerm{ id:49, generic_term: 'fach'} ),
(g50:GenericTerm{ id:50, generic_term: 'fächer'} ),
(g51:GenericTerm{ id:51, generic_term: 'module'} ),

(g52:GenericTerm{ id:52, generic_term: 'sagen'} ),
(g53:GenericTerm{ id:53, generic_term: 'sag'} ),
(g54:GenericTerm{ id:54, generic_term: 'erzähl'} ),

(g55:GenericTerm{ id:55, generic_term: 'gründung'} ),
(g56:GenericTerm{ id:56, generic_term: 'studenten'} ),
(g57:GenericTerm{ id:57, generic_term: 'studentin'} ),
(g58:GenericTerm{ id:58, generic_term: 'studierende'} ),
(g59:GenericTerm{ id:59, generic_term: 'studierender'} ),
(g60:GenericTerm{ id:60, generic_term: 'schüler'} ),
(g61:GenericTerm{ id:61, generic_term: 'schülerin'} ),
(g62:GenericTerm{ id:62, generic_term: 'person'} ),
(g63:GenericTerm{ id:63, generic_term: 'personen'} ),
(g64:GenericTerm{ id:64, generic_term: 'hat'} ),
(g65:GenericTerm{ id:65, generic_term: 'besitzt'} ),
(g66:GenericTerm{ id:66, generic_term: 'besitzen'} ),
(g67:GenericTerm{ id:67, generic_term: 'vorhanden'} ),
(g68:GenericTerm{ id:68, generic_term: 'vertreten'} ),
(g69:GenericTerm{ id:69, generic_term: 'geben'} ),

(g70:GenericTerm{ id:70, generic_term: 'bewerbung'} ),
(g71:GenericTerm{ id:71, generic_term: 'bewerbe'} ),
(g72:GenericTerm{ id:72, generic_term: 'bewirbt'} ),
(g73:GenericTerm{ id:73, generic_term: 'informatikstudiengang'} )
"""
neo4j_conn.execute_query(query4)

query5 = """
MATCH (a1:Answer {answerID: 1}), (a2:Answer {answerID: 2}),(a3:Answer {answerID: 3}),(a4:Answer {answerID: 4}),(a5:Answer {answerID: 5}),(a6:Answer {answerID: 6}),(a7:Answer {answerID: 7}),(a9:Answer {answerID: 9}),(a10:Answer {answerID: 10}),(a11:Answer {answerID: 11}),(a12:Answer {answerID: 12}),(a13:Answer {answerID: 13}),(a14:Answer {answerID: 14}),(a15:Answer {answerID: 15}),(a16:Answer {answerID: 16}),(a19:Answer {answerID: 19}), (a20:Answer {answerID: 20}), (a22:Answer {answerID: 22}), (g1:GenericTerm {id: 1}),(g2:GenericTerm {id: 2}),(g3:GenericTerm {id: 3}),(g4:GenericTerm {id: 4}),(g5:GenericTerm {id: 5}),(g6:GenericTerm {id: 6}),(g7:GenericTerm {id: 7}),(g8:GenericTerm {id: 8}),(g9:GenericTerm {id: 9}),(g11:GenericTerm {id: 11}),(g12:GenericTerm {id: 12}),(g13:GenericTerm {id: 13}),(g14:GenericTerm {id: 14}),(g15:GenericTerm {id: 15}),(g16:GenericTerm {id: 16}),(g17:GenericTerm {id: 17}),(g44:GenericTerm {id: 44})
CREATE (a1)-[:HAS_PRIMARY_KEY]->(g2),
((a1) -[:HAS_PRIMARY_KEY]->(g7)),	
((a2) -[:HAS_PRIMARY_KEY]->(g1)),
((a3) -[:HAS_PRIMARY_KEY]->(g17)),
((a3) -[:HAS_PRIMARY_KEY]->(g2)),
((a4) -[:HAS_PRIMARY_KEY]->(g2)),
((a4) -[:HAS_PRIMARY_KEY]->(g17)),
((a5) -[:HAS_PRIMARY_KEY]->(g8)),
((a6) -[:HAS_PRIMARY_KEY]->(g9)),
((a6) -[:HAS_PRIMARY_KEY]->(g44)),
((a7) -[:HAS_PRIMARY_KEY]->(g2)),
((a9) -[:HAS_PRIMARY_KEY]->(g4)),
((a10) -[:HAS_PRIMARY_KEY]->(g6)),
((a11) -[:HAS_PRIMARY_KEY]->(g11)),
((a12) -[:HAS_PRIMARY_KEY]->(g5)),
((a13) -[:HAS_PRIMARY_KEY]->(g12)),
((a13) -[:HAS_PRIMARY_KEY]->(g16)),
((a14) -[:HAS_PRIMARY_KEY]->(g13)),
((a14) -[:HAS_PRIMARY_KEY]->(g3)),
((a15) -[:HAS_PRIMARY_KEY]->(g14)),
((a16) -[:HAS_PRIMARY_KEY]->(g15)),
((a19) -[:HAS_PRIMARY_KEY]->(g2)),
((a20) -[:HAS_PRIMARY_KEY]->(g2)),
((a22) -[:HAS_PRIMARY_KEY]->(g13));
"""
query6 = """
MATCH (g:GenericTerm {generic_term: 'brauchen'})
WITH g
MATCH (s:GenericTerm)
WHERE s.generic_term IN ['brauche', 'brauch', 'bräuchte', 'benötigen']
MERGE (s)-[:IS_SYNONYM_OF]->(g);
"""
query7 = """
// Beziehungen für 'studiengang'
MATCH (g:GenericTerm {generic_term: 'studiengang'})
WITH g
MATCH (s:GenericTerm)
WHERE s.generic_term IN ['studiengänge']
MERGE (s)-[:IS_SYNONYM_OF]->(g);
"""
query8= """
// Beziehungen für 'hwr'
MATCH (g:GenericTerm {generic_term: 'hwr'})
WITH g
MATCH (s:GenericTerm)
WHERE s.generic_term IN ['uni', 'campus', 'universität', 'hochschule']
MERGE (s)-[:IS_SYNONYM_OF]->(g);
"""
query9= """
// Beziehungen für 'ptb'
MATCH (g:GenericTerm {generic_term: 'ptb'})
WITH g
MATCH (s:GenericTerm)
WHERE s.generic_term IN ['praxistransferbericht', 'praxistransferberichte', 'ptbs']
MERGE (s)-[:IS_SYNONYM_OF]->(g);
"""
query10= """
// Beziehungen für 'schreiben'
MATCH (g:GenericTerm {generic_term: 'schreiben'})
WITH g
MATCH (s:GenericTerm)
WHERE s.generic_term IN ['verfassen']
MERGE (s)-[:IS_SYNONYM_OF]->(g);
"""
query11 = """
// Beziehungen für 'studienarbeit'
MATCH (g:GenericTerm {generic_term: 'studienarbeit'})
WITH g
MATCH (s:GenericTerm)
WHERE s.generic_term IN ['studienarbeiten']
MERGE (s)-[:IS_SYNONYM_OF]->(g);
"""
query12 = """
// Beziehungen für 'informieren'
MATCH (g:GenericTerm {generic_term: 'informieren'})
WITH g
MATCH (s:GenericTerm)
WHERE s.generic_term IN ['erkundigen', 'schlaumachen', 'information']
MERGE (s)-[:IS_SYNONYM_OF]->(g);
"""
query13 = """
// Beziehungen für 'aufbau'
MATCH (g:GenericTerm {generic_term: 'aufbau'})
WITH g
MATCH (s:GenericTerm)
WHERE s.generic_term IN ['aufbauen', 'zusammensetzen', 'zusammensetzung', 'strukturieren', 'struktur', 'bestehen', 'besteht', 'ablaufen', 'laufen']
MERGE (s)-[:IS_SYNONYM_OF]->(g);
"""
query14 ="""
// Beziehungen für 'bachelor'
MATCH (g:GenericTerm {generic_term: 'bachelor'})
WITH g
MATCH (s:GenericTerm)
WHERE s.generic_term IN ['bachelorabschluss']
MERGE (s)-[:IS_SYNONYM_OF]->(g);
"""
query15 = """
// Beziehungen für 'beruf'
MATCH (g:GenericTerm {generic_term: 'beruf'})
WITH g
MATCH (s:GenericTerm)
WHERE s.generic_term IN ['berufe', 'berufsfeld', 'berufsfelder']
MERGE (s)-[:IS_SYNONYM_OF]->(g);
"""
query16 = """
// Beziehungen für 'bachelorarbeit'
MATCH (g:GenericTerm {generic_term: 'bachelorarbeit'})
WITH g
MATCH (s:GenericTerm)
WHERE s.generic_term IN ['bachelorthesis']
MERGE (s)-[:IS_SYNONYM_OF]->(g);
"""
query17 = """
// Beziehungen für 'modul'
MATCH (g:GenericTerm {generic_term: 'modul'})
WITH g
MATCH (s:GenericTerm)
WHERE s.generic_term IN ['fach', 'fächer', 'module']
MERGE (s)-[:IS_SYNONYM_OF]->(g);
"""
query18 = """
// Beziehungen für 'erzählen'
MATCH (g:GenericTerm {generic_term: 'erzählen'})
WITH g
MATCH (s:GenericTerm)
WHERE s.generic_term IN ['sagen', 'sag', 'erzähl']
MERGE (s)-[:IS_SYNONYM_OF]->(g);
"""
query19 = """
// Beziehungen für 'gründen'
MATCH (g:GenericTerm {generic_term: 'gründen'})
WITH g
MATCH (s:GenericTerm)
WHERE s.generic_term IN ['gründung']
MERGE (s)-[:IS_SYNONYM_OF]->(g);
"""
query20 = """
// Beziehungen für 'student'
MATCH (g:GenericTerm {generic_term: 'student'})
WITH g
MATCH (s:GenericTerm)
WHERE s.generic_term IN ['studenten', 'studentin', 'studierende', 'studierender', 'schüler', 'schülerin', 'person', 'personen']
MERGE (s)-[:IS_SYNONYM_OF]->(g);
"""
query21 = """
// Beziehungen für 'haben'
MATCH (g:GenericTerm {generic_term: 'haben'})
WITH g
MATCH (s:GenericTerm)
WHERE s.generic_term IN ['hat', 'besitzt', 'besitzen', 'vorhanden', 'vertreten', 'geben']
MERGE (s)-[:IS_SYNONYM_OF]->(g);
"""
query22 = """
// Beziehungen für 'bewerben'
MATCH (g:GenericTerm {generic_term: 'bewerben'})
WITH g
MATCH (s:GenericTerm)
WHERE s.generic_term IN ['bewerbung', 'bewerbe', 'bewirbt']
MERGE (s)-[:IS_SYNONYM_OF]->(g);
"""
query23 = """
// Beziehungen für 'informatikstudium'
MATCH (g:GenericTerm {generic_term: 'informatikstudium'})
WITH g
MATCH (s:GenericTerm)
WHERE s.generic_term IN ['informatikstudiengang']
MERGE (s)-[:IS_SYNONYM_OF]->(g);
"""
query24 = """
WITH [
{answerID: 1, secondary_keywords: ['wie', 'und', 'wo', 'über', 'hwr', 'kenntnis', 'dual']},
{answerID: 2, secondary_keywords: ['welch', 'studiengang', 'informatik', 'informatikstudium', 'mitbringen', 'studieren', 'wissen']},
{answerID: 3, secondary_keywords: ['wie', 'und', 'wo', 'für', 'an', 'hwr', 'informatikstudium']},
{answerID: 4, secondary_keywords: ['wie', 'für', 'wo', 'und', 'informatikstudium', 'informatik', 'an', 'hwr']},
{answerID: 5, secondary_keywords: ['wie', 'studium', 'informatik', 'informatikstudium', 'woraus']},
{answerID: 6, secondary_keywords: ['welch', 'beruf', 'qualifizieren', 'was', 'wofür', 'machen', 'studium']},
{answerID: 7, secondary_keywords: ['studiengang', 'erzählen', 'informatik', 'informatikstudium', 'über', 'was']},
{answerID: 8, secondary_keywords: ['studieninhalte', 'inhalte', 'studium', 'was', 'haben', 'welch', 'machen', 'im', 'in', 'dies', 'dual', 'enthalten']},
{answerID: 9, secondary_keywords: ['ptb', 'was', 'bedeuten', 'vorstellen']},
{answerID: 10, secondary_keywords: ['studienarbeit', 'was', 'bedeuten', 'vorstellen']},
{answerID: 11, secondary_keywords: ['bachelorarbeit', 'was', 'bedeuten', 'vorstellen']},
{answerID: 12, secondary_keywords: ['viel', 'schreiben', 'oft', 'wie', 'ptb', 'studienarbeit', 'studium', 'während']},
{answerID: 13, secondary_keywords: ['modul', 'haben', 'welch', 'studium', 'existieren', 'was', 'für']},
{answerID: 14, secondary_keywords: ['erzählen', 'hwr', 'wissen', 'über', 'was']},
{answerID: 15, secondary_keywords: ['wann', 'gründen', 'jahr', 'lang', 'hwr', 'öffnen', 'haben', 'seit', 'viel']},
{answerID: 16, secondary_keywords: ['viel', 'student', 'wie', 'an', 'hwr', 'studieren']},
{answerID: 17, secondary_keywords: ['standort', 'wo', 'viel', 'welch', 'hwr', 'wie', 'haben', 'überall']},
{answerID: 18, secondary_keywords: ['viel', 'fachbereich', 'wie', 'hwr', 'welch', 'haben', 'an', 'was', 'für', 'existieren']},
{answerID: 19, secondary_keywords: ['viel', 'studiengang', 'wie', 'haben', 'an', 'hwr', 'existieren']},
{answerID: 20, secondary_keywords: ['welch', 'studiengang', 'was', 'haben', 'an', 'hwr', 'für', 'bieten', 'existieren']},
{answerID: 21, secondary_keywords: ['dauern', 'lang', 'jahr', 'wie', 'studium', 'gehen', 'viel', 'studieren', 'informatikstudium', 'informatik']},
{answerID: 22, secondary_keywords: ['informatik', 'erzählen', 'über', 'was', 'machen', 'in']},
{answerID: 23, secondary_keywords: ['heißen', 'name', 'wie', 'was', 'lauten', 'wer', 'nennen']},
{answerID: 24, secondary_keywords: ['woher', 'kommen', 'wo', 'werden', 'gebären', 'herstellen', 'erzeugen', 'bauen']},
{answerID: 25, secondary_keywords: ['können', 'fähigkeit', 'was', 'machen', 'hier']}
] AS answers
UNWIND answers AS answer
WITH answer.answerID AS answerID, answer.secondary_keywords AS secondary_keywords
MATCH (a:Answer {answerID: answerID})
UNWIND secondary_keywords AS keyword
MATCH (g:GenericTerm {generic_term: keyword})
MERGE (a)-[:HAS_SECONDARY_KEY]->(g);

"""
neo4j_conn.execute_query(query5)
neo4j_conn.execute_query(query6)
neo4j_conn.execute_query(query7)
neo4j_conn.execute_query(query8)
neo4j_conn.execute_query(query9)
neo4j_conn.execute_query(query10)
neo4j_conn.execute_query(query11)
neo4j_conn.execute_query(query12)
neo4j_conn.execute_query(query13)
neo4j_conn.execute_query(query14)
neo4j_conn.execute_query(query15)
neo4j_conn.execute_query(query16)
neo4j_conn.execute_query(query17)
neo4j_conn.execute_query(query18)
neo4j_conn.execute_query(query19)
neo4j_conn.execute_query(query20)
neo4j_conn.execute_query(query21)
neo4j_conn.execute_query(query22)
neo4j_conn.execute_query(query23)
neo4j_conn.execute_query(query24)

# Verbindung schließen
neo4j_conn.close()
