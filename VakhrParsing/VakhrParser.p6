#!/usr/bin/perl6

grammar article {
  rule TOP {
    <title> <part> <pos>
    <meaning-group> <example-group>
  }
}
