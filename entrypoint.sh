#!/bin/bash

if [ -n "$EXTRA_COMMANDS" ]; then
    EXTRA_COMMANDS="repo/$EXTRA_COMMANDS"
    if [ -f "$EXTRA_COMMANDS" ]; then
        echo "Execute extra commands..."
        # Zeilenumbrüche zu unix konvertieren, falls die Datei unter Windows erstellt wurde.
        dos2unix "$EXTRA_COMMANDS"
        # Ausführungsrechte setzen
        chmod +x "$EXTRA_COMMANDS"
        # Script ausführen
        ./"$EXTRA_COMMANDS"
    fi
fi

python3 testExecutor.py