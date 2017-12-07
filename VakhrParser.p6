#!/usr/bin/perl6

grammar Vakhr {
  rule TOP {
      ^^ <title> <pos> <meaning_group> $$
  }
  token title {
    <
    [\-ЁАБВГДЕЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯабвгдежзийклмнопрстуфхцчшщъыьэюяёӇӈӓәӛӦӧӨөӰӱ]
    > +
  }
}
