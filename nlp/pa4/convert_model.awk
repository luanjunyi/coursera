/^TRIGRAM/ {
    line = gensub(/(.+?):(.+?):(.+?):(.+?) /, "\\1#\\2#\\3#\\4 ", "g");
    print line;
}

/^TAG:/ {
    line = gensub(/([^:]+?):(.+?):(.+?) /, "\\1#\\2#\\3 ", "g");
    print line;
}