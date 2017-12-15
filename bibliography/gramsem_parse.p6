#!/usr/bin/perl6

use Grammar::Tracer;

grammar gramsem {
  rule TOP {
    <authors> \s* <red>? <spl>* <year>? <spl>*
    [ <title-journal> || <title-simple> ]
  }
  token red {
    "(ред.)" | \(<[eé]>ds?\.?\)
  }
  token spl {
    <[\.\s]>
  }
  token authors {
    <author>+ % [ [" " | "&" | ";" | ","]+ ] <spl>* <et-al>?
  }
  token author {
    <surname> \s* ["," \s*]? <capitals>
  }
  token surname {
    <[A..Z] + [А..Я] + [Ё]> <[a..z] + [ÖÜÄöäüàáèéòó] + [а..я] + [ё]>+
  }
  token capitals {
    [
      [ <[A..Z] + [А..Я] + [ЁÖÜÄ]> "." ] ** ^3  % [ \s* ]
      |
      <surname> \s+ [ <[A..Z] + [А..Я] + [ЁÖÜÄ]> "." ] ** ^3  % [ \s* ]
    ]
  }
  token year {
    <digit>+ <[a..z]>?
  }
  token small-dot {
    <[A..Z] + [А..Я] + [ÖÜÄöäüàáèéòó] + [a..z] + [а..я] + [\s]>
    <[\.] + [а..я] + [ÖÜÄöäüàáèéòó] + [a..z] + [\s]>+
  }
  token title-simple {
    [ <name-simple> | <name-simple-ext> ]
    [<spl>* <part>]?
    [<spl>* "/" <spl>* <comment>]?
    <spl>*
    <place> ":" <spl>* <publisher> <spl>*
    <time-pages>? <spl>*
  }
  token name-simple-ext {
    <-[\./]>+ <spl>+ <ext-construction>
  }
  token ext-construction {
    [
      <[А..Я] + [A..Z]><[а..я] + [a..z] + [ÖÜÄöäüàáèéòó]>+
      [
        \s+ [<[А..Я] + [A..Z] + [ÖÜÄöäüàáèéòó] + [а..я] + [a..z]>+]+ % [\s+]
      ]?
      \s*\.\s+
    ] +
  }
  token ext-construction-small {
    [
      [
        <[А..Я] + [A..Z] + [а..я] + [ÖÜÄöäüàáèéòó] + [a..z] + [-] + :digit>+
      ] + % [\s+]
      \s*\.\s+
    ] +
  }
  token comment {
    <small-dot>
  }
  token editors {
    <editor> + % [ ["," | \s | "&" | " и "]+ ]
    \s* <et-al>? \s* <red>?
  }
  token et-al {
    "и"? \s* "др"\.? | "et"? \s* "al"\.?
  }
  token editor {
    <capitals> \s+ <surname> <spl>* <red>?
  }
  token title-journal {
    [ <name-simple> | <name-simple-ext> ]
    [<spl>* <part>]?
    [<spl>* "/" <spl>* <comment>]?
    <spl>*
    <spl>* "//" <spl>*
    <editors>? <spl>*
    <journal-name>
    <spl>*
    [
      <place> ":" <spl>* <publisher>
      |
      ":" <spl>* <series>
    ]?
    <spl>* <time-pages>? <spl>*
  }
  token journal-name {
    [
      <-[\.\:]>+ ":" <spl>* <ext-construction-small>
      |
      [
        <-[\.\:/]>+? <spl>* "," <spl>* <metadata-wrap>
        |
        <-[\.\:/]>+
      ]
    ]
  }
  token metadata-wrap {
    [ <section-wrap> | <metadata> ] + % [\s* "," \s*]
  }
  token metadata {
    ["вып." | "сер." | "vol"\.?] <spl>* [ <:digit + [-]>+ | <[IVX-]>+ ]
  }
  token section-wrap {
    "sec." \s* <section>
  }
  token section {
    <digit>+ "." <digit>+
  }
  token time-pages {
    "," \s* [ <pages> | <time>]+ % [ \s* "," \s* ]
  }
  token time {
    [ <digit> || "/" ] +
  }
  token pages {
    <from-page> "-" <to-page>
  }
  token from-page {
    <digit>+
  }
  token to-page {
    <digit>+
  }
  token place {
    <-[:]>+
  }
  token vol {
    "vol"\.? \s* [ <:digit + [-]>+ | <[IVX-]>+ ]
  }
  token name-simple {
    <-[/]>+? <spl>* "," \s* <vol>
    |
    <-[\./]>+
  }
  token notes-wrap {
    "(" <notes> ")"
  }
  token notes {
    <-[\)]>+
  }
  token part {
    [
      "Часть"
      ||
      "Кн."
    ]
    <-[\./]>+
  }
  token publisher-name {
    <-[,\(\)]>+
  }
  token publisher {
    <publisher-name> <spl>* <notes-wrap>?
  }
  token series {
    <-[,]>+
  }
}

my $parsed = gramsem.parse('Маслов, Ю. С. 1984a. Типология славянских видо-временных систем и функционирование форм «претерита» в эпическом повествовании // А. В. Бондарко (ред.). Теория грамматического значения и аспектологические исследования. Л.: Наука, 22-42.');
say $parsed;
my $output = '';
my $author_range = "A1 ";
if ($parsed<red>) {
  $author_range = "A2 ";
}
my $i = 0;
for ($parsed<authors><author>) {
  if ($parsed<red>) {
    if ($parsed<authors><author>.elems == 1) {
      if ($parsed<authors><et-al>) {
        $author_range = 'A1 ';
        $output ~= "A2 .\n"
      }
      else {
        $author_range = 'A2 ';
      }
    }
    else {
      if ($i == 0) {
        $author_range = 'A1 ';
      } else {
        $author_range = 'A2 ';
      }
      if $i == ($parsed<authors><author>.elems - 1) {
        $output ~= "A2 .\n";
      }
    }
  }
  ++ $i;
  $output ~= $author_range ~ $_<surname>.Str;
  if $_<capitals> {
    $output ~= ", " ~ $_<capitals>.Str;
  }
  $output ~= "\n";
}
my $title = $parsed<title-simple> ?? 'title-simple' !! 'title-journal';
if $parsed<year> {
  my $year = $parsed<year>;
  if $year ~~ m/(<alpha>)$/ {
    $output ~= "# $0\n";
  }
  $year ~~ s/<alpha>$//;
  if ($title eq 'title-journal' && $parsed{$title}<journal-name><time-pages><time>) {
    my $pub-time = $parsed{$title}<journal-name><time-pages><time>;
    if ($pub-time ~~ /^<digit>**4/) {
      $output ~= "FD $0\n";
    }
    else {
      $output ~= "FD $year\n"
    }
  }
  else {
    $output ~= "FD $year\n";
  }
  $output ~= "YR $year\n";
}
if ($parsed<title-simple>) {
  my $name = $parsed<title-simple><name-simple>;
  my $vol = '';
  if ($parsed<title-simple><name-simple><vol>) {
    $vol = $parsed<title-simple><name-simple><vol>.Str;
    $vol ~~ s/^\s*vol\.\s*//;
    $name ~~ s/\,\s*vol\..*//;
  }
  $output ~= "T1 $name\n";
  if ($vol ne '') {
    $output ~= "T2 Vol. $vol\n";
  }
  $output ~= "PP {$parsed<title-simple><place>}\n";
  my $publisher = $parsed<title-simple><publisher><publisher-name>;
  $publisher ~~ s/\.$//;
  $output ~= "PB $publisher\n";
}
elsif ($parsed<title-journal>) {
  my $name = $parsed<title-journal><name-simple>;
  if ($parsed<title-journal><journal-name><metadata-wrap><section-wrap>) {
    my $sec-wrap = $parsed<title-journal><journal-name><metadata-wrap><section-wrap>.Str;
    $name ~~ s/\,\s*$sec-wrap//;
    my $section = $parsed<title-journal><journal-name><metadata-wrap><section-wrap>[0]<section>;
    $output ~= "T2 Sec. $section\n";
  }
  my @metadata-buffer;
  my $journal-name = $parsed<title-journal><journal-name>.Str;
  if ($parsed<title-journal><journal-name><metadata-wrap><metadata>) {
    for ($parsed<title-journal><journal-name><metadata-wrap><metadata>) {
      if $_.Str ~~ /^([вып|vol])\.\s*(.+)/ {
        my $this = $_.Str;
        my $keyw = $0 eq 'вып' ?? 'Вып.' !! 'Vol.';
        @metadata-buffer.push: "$keyw $1";
        $journal-name ~~ s/\,\s*$this//;
      }
      elsif $_.Str ~~ /^(сер)\.\s*(.+)/ {
        my $this = $_.Str;
        @metadata-buffer.push: "Сер. $1";
        $journal-name ~~ s/\,\s*$this//;
      }
    }
  }
  $output ~= "T3 $journal-name\n";
  if @metadata-buffer.elems > 0 {
    $output ~= "T2 {@metadata-buffer.join(', ')}\n";
  }
  $output ~= "T1 {$parsed<title-journal><name-simple>}\n";
  if ($parsed<title-journal><editors>) {
    for ($parsed<title-journal><editors><editor>) {
      $output ~= "A2 {$_<surname>}";
      if ($_<capitals>) {
        $output ~= ", {$_<capitals>}";
      }
      $output ~= "\n";
    }
  }
  if ($parsed<title-journal><place>) {
    $output ~= "PP {$parsed<title-journal><place>}\n";
  }
  if ($parsed<title-journal><publisher><publisher-name>) {
    $output ~= "PB {$parsed<title-journal><publisher><publisher-name>}\n";
  }
  if ($parsed<title-journal><time-pages><pages>) {
    my $pages = $parsed<title-journal><time-pages><pages>[0];
    $output ~= "SP {$pages<from-page>}\n";
    $output ~= "OP {$pages<to-page>}\n";
  }
  if ($parsed<title-journal><comment>) {
    $output ~= "NO {$parsed<title-journal><comment>.Str}\n";
  }
}

say "";
say $output;
