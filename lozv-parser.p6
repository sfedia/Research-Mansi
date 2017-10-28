#!/usr/bin/perl6
use v6;
use Grammar::Tracer;

sub make_log ($file_handler, Str $message, Int $line)
{
	$file_handler.say("Line {$line}: $message\n");
}

grammar lozv_segment
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
		[ \d+ [\. || \)] \s* || \s+ ] ?
		[\s+ || <meaning>]
	}
	regex meaning { <[\x[0430] .. \x[044F]] + [Ёё] + [\s] + punct - [\;\,] - [А..Я]> + }
	regex example_wrap
	{
		<example_group> + % [ [\; || \? || \.] \s*]*
	}
	regex example_group
	{
		<example_mans>
		\s* [  [ ["." || "?"] [\s* "–"] ? ]  || "–"  ] \s+
		<example_rus> ["." || "?"] ?
	}
	regex example_mans { [ <[А..Я] + [Ё]> || <-[\s\h\(\)\d\;\,\.ё]> ] <-[–\.\?]>* }
	regex example_rus { <[А..Я] + [а..я] + [Ёё]> <-[–\.\;\?]>* }
}


my $lozv_plain = open '/home/sivan/prodotiscus/mansi-project/lozv.txt';
my $lozv_log = open '/home/sivan/prodotiscus/mansi-project/lozv-log.txt', :a;
lozv_segment.parse("вощлах сущ. ил; слякоть; Вр тӯр втат враяӈкв – Дно ручья с илом.");
