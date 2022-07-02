# Normaliser for Yoranish dictionary

  

Main purpose of this program is to normalise the data in csv provided by creator of Yoranish language Lukáš Tomášek. He created the whole dictionary in an app in his phone. File formatting of exported csv turned out to be suboptimal for further use.

## Main problems with original csv:

1. default csv delimiter is a colon, whereas Tomášek used also forward slash

2. Tomášek also wrote masculine and feminine versions of adjectives using a forward slash, example of this:

	> diobirayi /-raa,dobrý/pádný,dobrá/pádná

Especially second problem poses a challenge. Czech translations of yoranish words are always wrote in full, in both masculine and feminine. Their yoranish counterparts are, sadly, not. Tomášek wrote only masculine version, with forward slash and change in ending for the feminine version. One of the things this normaliser tries to do is use the masculine version and the ending provided by the creator of the language and put them together, thus forming feminine version.
