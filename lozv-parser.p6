#!/usr/bin/perl6
use v6;
grammar lozv
{
	regex TOP
	{
		<number>?
		\s*
		<title_wrap>
		\s+
		<meaning_wrap>
		<example_wrap>?
	}
   	regex number { <[I V]>+ }
	regex title_wrap { <title> \s+ <pos_tag> }
	regex title { <-[\,]>+? % [","]* }
	regex pos_tag { <[а..я] + [ё] + [\-]> + "." }
	regex meaning_wrap { <meaning_group> + % [ <[\;\,]> \s* ] * }
	regex meaning_group
	{
		[ \d+\.\s* || \s+ ] ?
		[\s+ || <meaning>]
	}
	regex meaning { <-[\;\,] - [А..Я]> + }
	regex example_wrap
	{
		<example_group> + % [ [\; || \?] \s*]*
	}
	regex example_group
	{
		<example_mans>
		\s+ "–" \s+
		<example_rus> ["." || "?"] ?
	}
	regex example_mans { <[А..Я] + [Ё]> <-[–]>* }
	regex example_rus { <[А..Я] + [Ё]> <-[–\.\;\?]>* }
}

say lozv.parse($foo);
