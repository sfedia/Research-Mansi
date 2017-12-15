#!/usr/bin/perl6

use Grammar::Tracer;

grammar gramsem {
  rule TOP {
    <authors> \s* <red>? <spl>* <year>? <spl>*
    [ <title-journal> || <title-simple> ]
  }
  token red {
    "(ред.)"
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
    <[A..Z] + [А..Я] + [Ё]> <[a..z] + [а..я] + [ё]>+
  }
  token capitals {
    [
      [ <[A..Z] + [А..Я] + [Ё]> "." | <surname>]
    ] ** ^3  % [ \s* ]
  }
  token year {
    <digit>+
  }
  token small-dot {
    <[A..Z] + [А..Я] + [a..z] + [а..я] + [\s]>
    <[\.] + [а..я] + [a..z] + [\s]>+
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
      <[А..Я] + [A..Z]><[а..я] + [a..z]>+
      [
        \s+ [<[А..Я] + [A..Z] + [а..я] + [a..z]>+]+ % [\s+]
      ]?
      \s*\.\s+
    ] +
  }
  token ext-construction-small {
    [
      [<[А..Я] + [A..Z] + [а..я] + [a..z] + [-] + :digit>+]+ % [\s+]
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
    ]
    <time-pages>? <spl>*
  }
  token journal-name {
    [
      <-[\.\:]>+ ":" <spl>* <ext-construction-small>
      |
      [
        <-[\.\:/]>+? <spl>* "," <spl>* <metadata>
        |
        <-[\.\:/]>+
      ]
    ]
  }
  token metadata {
    ["вып." | "сер."] <spl>* [ <digit>+ | <[IVX]>+ ]
  }
  token time-pages {
    "," \s* [ <pages> | <time> ] [ \s* "," \s* <pages> ] ?
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

say gramsem.parse('Гринберг, Дж. 1960. Квантитативный подход к морфологической типологии языков / Пер. с англ. // Новое в лингвистике, вып. 3. М.: ИЛ, 1963, 60-94.');
