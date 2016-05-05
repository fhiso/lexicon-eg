#!/usr/bin/perl

use strict;
use warnings;

use FindBin;
use File::Basename;
use POSIX qw/strftime/;
use Perl6::Slurp;

sub idize($) {
    my ($s) = @_;
    $s =~ s/[^A-Za-z0-9]+/-/g;
    $s =~ s/^-?(.*?)-?$/$1/;
    return $s;
}

sub process_md($$;$) {
    my ($out, $f, $indent) = @_;

    $_ = slurp '<', "$FindBin::Bin/../$f.md";
    s%(?<!\\)\]\s*\(SOURCES\.md#([^\)/#]*)\)%'](#'.idize($1).')'%eg;
    s%(?<!\\)\]\s*\(([^\)/]*)\.md\)%'](#'.idize($1).')'%eg;

    print $out "\n\n<a id=\"".idize($f)."\"></a>\n\n";

    s/^/$indent/mg if $indent;
    print $out $_;
}

my $today = strftime "%F", gmtime;
open my $out, '>', "$FindBin::Bin/lexicon-$today.md";

print $out <<EOF;
# Lexicon snapshot ($today)

This lexicon is an auto-generated snapshot of the individual markdown files 
contained in the main directory of the lexicon exploratory group's github 
repository.  See <a href=".">the lexicon exploratory group's main page</a> 
for more.

The README for this project contains the following:

EOF
process_md($out, "README", '> ');

print $out "\n# Lexicon Entries\n\n";

foreach ( grep { ! /README|SOURCES/ } map { basename $_, '.md' } 
            glob "$FindBin::Bin/../*.md" ) {
    process_md($out, $_);
} 

process_md($out, "SOURCES");

