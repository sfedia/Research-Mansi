#!/usr/bin/perl6

use Grammar::Tracer;

grammar gramsem {
  rule TOP {
    <authors> \s* <red>? <spl>* <year>? <spl>*
    [ <title-journal> || <title-simple> ]
  }
  token red {
    "(ред.)" | \(<[eé]>d\.?\)
  }
  token spl {
    <[\.\s]>
  }
  token authors {
    <author>+ % [ [" " | "&" | ";" | ","]+ ]
  }
  token author {
    <surname> \s* ["," \s*]? <capitals>
  }
  token surname {
    <[A..Z] + [А..Я] + [Ё]> <[a..z] + [öäüàáèéòó] + [а..я] + [ё]>+
  }
  token capitals {
    [
      [ <[A..Z] + [А..Я] + [Ё]> "." ] ** ^3  % [ \s* ]
      |
      <surname> \s+ [ <[A..Z] + [А..Я] + [Ё]> "." ] ** ^3  % [ \s* ]
    ]
  }
  token year {
    <digit>+
  }
  token small-dot {
    <[A..Z] + [А..Я] + [öäüàáèéòó] + [a..z] + [а..я] + [\s]>
    <[\.] + [а..я] + [öäüàáèéòó] + [a..z] + [\s]>+
  }
  token title-simple {
    [ <name-simple> | <name-simple-ext> ]
    [<spl>* <part>]?
    [<spl>* "/" <spl>* <comment>]?
    <spl>*
    <place> ":" <spl>* <publisher>
    <time-pages>? <spl>*
  }
  token name-simple-ext {
    <-[\./]>+ <spl>+ <ext-construction>
  }
  token ext-construction {
    [
      <[А..Я] + [A..Z]><[а..я] + [a..z] + [öäüàáèéòó]>+
      [
        \s+ [<[А..Я] + [A..Z] + [öäüàáèéòó] + [а..я] + [a..z]>+]+ % [\s+]
      ]?
      \s*\.\s+
    ] +
  }
  token ext-construction-small {
    [
      [
        <[А..Я] + [A..Z] + [а..я] + [öäüàáèéòó] + [a..z] + [-] + :digit>+
      ] + % [\s+]
      \s*\.\s+
    ] +
  }
  token comment {
    <small-dot>
  }
  token editors {
    <editor>+ % [ ["," | \s | "&" | " и "]+ ]
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
    ["вып." | "сер." | "vol"\.?] <spl>* [ <digit>+ | <[IVX]>+ ]
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
  token name-simple {
    <-[\./]>+
  }
  token part {
    [
      "Часть"
      ||
      "Кн."
    ]
    <-[\./]>+
  }
  token publisher {
    <-[,]>+
  }
  token series {
    <-[,]>+
  }
}

say gramsem.parse('Goldberg, A. 2003. Constructions: A new theoretical approach to language // Trends in Cognitive Sciences, sec. 7.5, 219-224.');
