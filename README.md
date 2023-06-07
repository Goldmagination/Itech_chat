# ITech_Chat

Das ITech_Chat-Projekt ist ein Chatbot, der auf dem PyTorch-Framework basiert. Dieser Chatbot wurde trainiert, um spezifische Absichten oder Fragen zu erkennen, die in den gegebenen Eingabeaufforderungen vorkommen.

## Hauptkomponenten
- **ChatDataset.py**: Diese Datei definiert eine benutzerdefinierte PyTorch-Dataset-Klasse, die zum Laden und Verarbeiten der Chat-Daten verwendet wird.
- **chat.py**: Dies ist das Hauptskript für den Chatbot. Es lädt die trainierten Modelldaten, erzeugt ein Neuronales Netz und führt die eigentliche Chat-Schleife durch.
- **model.py**: Definiert die Architektur des neuronalen Netzwerkmodells, das für den Chatbot verwendet wird.
- **nltk_utils.py**: Enthält Hilfsfunktionen zum Tokenisieren von Sätzen und zum Erstellen von "Bag-of-Words"-Vektoren, die für die Eingabe in das Modell verwendet werden.
- **processDataFromDataSET.py**: Dieses Skript verarbeitet die Daten aus einer CSV-Datei und konvertiert sie in das JSON-Format, das der Chatbot verwendet.

> **Hinweis**: Der Chatbot wurde speziell für das Erkennen und Beantworten von Fragen zu bestimmten Themen trainiert. Die genauen Themen hängen von den Daten ab, die für das Training des Modells verwendet wurden.

## Trainingsprozess
Bevor Sie den Chatbot starten, müssen Sie ein Modell trainieren, das die menschlichen Eingabeaufforderungen interpretieren kann. Das Training erfolgt in mehreren Schritten:

1. **Vorbereitung der Trainingsdaten**: Die Trainingsdaten für den Chatbot sind in einer JSON-Datei mit der oben angegebenen Struktur gespeichert. Jedes Element in der JSON-Datei enthält einen "Tag", der eine spezifische Absicht darstellt, eine Liste von "Patterns", die menschliche Eingabeaufforderungen darstellen, die mit dieser Absicht korrespondieren, und eine Liste von "Responses", die der Chatbot auf diese Pattern geben kann.
2. **Verarbeitung der Trainingsdaten**: Die Patterns in der JSON-Datei werden durch ein Tokenisierungsprozess verarbeitet, der jeden Satz in eine Liste von Wörtern zerlegt. Diese Wörter werden dann "gestemmt", was bedeutet, dass sie auf ihre Wurzel reduziert werden, um Variationen in der Grammatik und Wortwahl zu berücksichtigen. Die resultierenden gestemmten Wörter werden dann in "Bag-of-Words"-Vektoren umgewandelt, die numerische Darstellungen der Wörter sind, die vom Modell verarbeitet werden können.
3. **Training des Modells**: Das trainierte Modell ist ein neuronales Netzwerk, das die Bag-of-Words-Vektoren als Eingabe nimmt und eine Liste von Wahrscheinlichkeiten für jede mögliche Absicht als Ausgabe liefert. Das Modell wird trainiert, indem es die Bag-of-Words-Vektoren zusammen mit den entsprechenden Absichten präsentiert bekommt und dann seine Gewichte anpasst, um seine Vorhersagen zu verbessern.

## Ausführung des Chatbots
Sobald das Modell trainiert ist, können Sie den Chatbot starten, indem Sie das Skript ```chat.py``` ausführen. Dieses Skript lädt das trainierte Modell und führt eine Schleife aus, in der es auf menschliche Eingabeaufforderungen wartet. Wenn es eine Eingabeaufforderung erhält, verarbeitet es den Text auf die gleiche Weise wie die Trainingsdaten und präsentiert das Ergebnis dem Modell. Das Modell gibt dann eine Liste von Wahrscheinlichkeiten für jede mögliche Absicht zurück. Das Skript wählt die Absicht mit der höchsten Wahrscheinlichkeit und gibt eine zufällige Antwort aus der Liste der Antworten für diese Absicht aus.

> **Hinweis**: Der spezifische Code, der zum Trainieren des Modells und zum Ausführen des Chatbots verwendet wird, kann von Projekt zu Projekt variieren. Der oben beschriebene Prozess ist eine allgemeine Beschreibung, wie ein auf einer JSON-Datei basierender Chatbot trainiert und ausgeführt wird.
