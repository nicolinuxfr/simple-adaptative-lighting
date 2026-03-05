# Vereinfachte adaptive Beleuchtung

Dieser *Blueprint* für Home Assistant ist vom [Adaptive Lighting Integration](https://github.com/basnijholt/adaptive-lighting) inspiriert und passt verbundene Leuchten automatisch den ganzen Tag und sogar nachts an. Im Vergleich zur Integration ist er viel einfacher und bietet deutlich weniger Optionen.

## Blueprint verwenden

Sie können diesen *Blueprint* zu Ihrer Home Assistant-Instanz mit diesem direkten Link hinzufügen:

[![Open your Home Assistant instance and show the blueprint import dialog with a specific blueprint pre-filled.](https://my.home-assistant.io/badges/blueprint_import.svg)](https://my.home-assistant.io/redirect/blueprint_import/?blueprint_url=https%3A%2F%2Fraw.githubusercontent.com%2Fnicolinuxfr%2Fsimple-adaptive-lighting-blueprint%2Fgh-pages%2Fde%2Fadaptive_lighting.yaml)

Alternativ können Sie diesen Link kopieren, um ihn in Home Assistant beim Hinzufügen eines Blueprints einzufügen :

	https://raw.githubusercontent.com/nicolinuxfr/simple-adaptive-lighting-blueprint/gh-pages/de/adaptive_lighting.yaml

## Konfiguration

Die aus dem Blueprint erstellte Automatisierung benötigt nur einen Parameter: eine oder mehrere Leuchten. Sie können mehrere verschiedene Entitäten oder eine Home Assistant-Gruppe eingeben. Die anderen Parameter können in der Standardkonfiguration belassen oder nach Ihren Bedürfnissen angepasst werden.

Hier ist die Liste der Optionen mit einigen Erklärungen, wo nötig:

- **Haupteinstellungen**: Auswahl der minimalen und maximalen Helligkeit sowie der minimalen und maximalen Weißtemperatur für die Leuchten.
- **Steuerung per Entität**: Durch Auswahl einer booleschen Entität (vom Typ `input_boolean` oder `binary_sensor`) können Sie eine Steuerung der Automatisierung hinzufügen, ohne sie zu deaktivieren. Die Entität muss aktiv sein, damit die Automatisierung die Leuchten anpasst, und wenn sie deaktiviert ist, bleiben die Leuchten bei der letzten automatischen Einstellung.
- **Wetter**: Durch Auswahl einer Wetterentität wird das Verhalten der Automatisierung je nach Wetterbedingungen angepasst. Die Idee ist, die Parameter leicht zu variieren, um bei schlechten Wetterbedingungen eine schwächere und wärmere Beleuchtung zu haben.
- **Nachtmodus**: Durch Auswahl einer booleschen Entität (vom Typ `input_boolean` oder `binary_sensor`) können Sie eine spezifische feste Beleuchtung für die Nacht einrichten. Wenn die Entität aktiv ist, werden automatische Anpassungen deaktiviert und stattdessen die Helligkeits- und Farbtemperatureinstellungen verwendet. Dies ermöglicht Tageseinstellungen, die hell genug zum komfortablen Wohnen sind, während die Nachtbeleuchtung deutlich schwächer bleibt.

Für alle drei optionalen Funktionen (Steuerung per Entität, Wetter und Nachtmodus) deaktiviert ein leeres Feld die Funktion vollständig.

## Funktionsweise

Die Automatisierung aktiviert sich, sobald die ausgewählten Leuchten eingeschaltet werden. Von da an wird sie alle fünf Minuten ausgelöst, um die Helligkeit und Weißtemperatur basierend auf den definierten Parametern, der Tageszeit und der automatisch berechneten Kurve anzupassen. Jeder Übergang wird über zehn Sekunden verteilt, um sichtbare Änderungen zu vermeiden. Um Probleme mit bestimmten Leuchten zu begrenzen, verwendet die Automatisierung eine Zwei-Schritte-Strategie und wechselt bei jeder Aktualisierung zwischen Helligkeit und Weißtemperatur ab.

Wenn eine Steuerungsentität verwendet wird, stoppt die Anpassung automatisch, sobald die Entität deaktiviert wird, und nimmt sie wieder auf, wenn sie reaktiviert wird. In diesem Fall gibt es keine Verzögerung — die richtigen Werte werden sofort gesendet, mit einer sanften Progression über 10 Sekunden.

Wenn die Wetteranpassung aktiviert ist, wird die Kurve leicht basierend auf den aktuellen Wetterbedingungen angepasst. Diese Information wird nur beim ersten Einschalten der Leuchten aktualisiert, um Ressourcen zu sparen.

Es gibt mehrere Strategien, um das Verhalten der Automatisierung je nach Situation leicht anzupassen. Zum Beispiel ist die Kurve unterschiedlich, wenn nur eine Leuchte konfiguriert ist, im Vergleich zu einer Automatisierung, die mehrere Leuchten steuert.

## Einschränkungen

Dieser Blueprint verwaltet bestimmte Funktionen absichtlich nicht:

- Keine Farbverwaltung, nur Weißtemperatur;
- Keine Kurvenanpassung — die behaltenen Parameter sind diejenigen, die meinen Bedürfnissen entsprechen;
- Keine möglichen Anpassungen für Start- und Endzeiten — nur Sonnenaufgangs- und Sonnenuntergangszeiten an Ihrem Wohnort werden verwendet;
- Keine manuelle Steuerung der Leuchten bei individuellen Änderungen — die Automatisierung wird immer alle fünf Minuten ausgelöst und Änderungen überschreiben;
- Sicherlich noch viele andere.

## Hinweis

Ich habe diesen *Blueprint* nicht direkt selbst kodiert — ich habe Werkzeuge wie Codex und Claude Code verwendet, um ihn zu erstellen. Er wird daher ohne Garantie angeboten, außer dass er bei mir einwandfrei funktioniert. Ich habe ihn mit mehreren Konfigurationen und vielen Leuchten getestet und keine Probleme festgestellt.

Die Übersetzungen werden ebenfalls automatisch von diesen Werkzeugen generiert — ich habe alle Texte auf Französisch geschrieben.

## Beiträge

Alle Beiträge sind willkommen, um Fehler zu beheben oder Funktionen hinzuzufügen. Dennoch möchte ich die Konfiguration so einfach wie möglich halten — meine Absicht ist es nicht, die Adaptive Lighting Integration zu reproduzieren.
