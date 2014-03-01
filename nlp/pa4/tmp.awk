BEGIN {
    prev = "";
}
{
    if (prev != "" && tolower($1) != $1) {
        print $0;
    }
    prev = $0;
}
