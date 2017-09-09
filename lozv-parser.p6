#!/usr/bin/perl6
use v6;

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
	regex meaning { <-[\;\,] - [А..Я]> + }
	regex example_wrap
	{
		<example_group> + % [ [\; || \? || \.] \s*]*
	}
	regex example_group
	{
		<example_mans>
		\s+ "–" \s+
		<example_rus> ["." || "?"] ?
	}
	regex example_mans { [ <[А..Я] + [Ё]> || <-[\s\h\(\)\d\;\,\.ё]-[а..я]> ] <-[–]>* }
	regex example_rus { <[А..Я] + [Ё]> <-[–\.\;\?]>* }
}


my $lozv_plain = open '/home/sivan/prodotiscus/mansi-project/lozv.txt';
my $lozv_log = open '/home/sivan/prodotiscus/mansi-project/lozv-log.txt', :a;
my @lozv_data = $lozv_plain.lines();

say @lozv_data.elems;

my Int $line_number = 0;
for @lozv_data -> $iter is copy
{
	say $line_number;

	$iter = $iter.trim;

	say $iter;

	if ( $iter eq '' )
	{
		++ $line_number;
		next;
	}
	my $parsed = lozv_segment.parse($iter);
	if ( !$parsed )
	{
		make_log($lozv_log, "Parsing failed", $line_number);
		++ $line_number;
		next;
	}
	my Int $part = -1;
	if ( $parsed<number> )
	{
		given ( $parsed<number>.Str )
		{
			when "I" { $part = 1; }
			when "II" { $part = 2; }
			when "III" { $part = 3; }
			when "IV" { $part = 4; }
			when "V" { $part = 5; }
			when "VI" { $part = 6; }
			default { $part = 0; }
		}
	}
	my Str $title = $parsed<title_wrap><title>.Str;
	my Str $pos_tag = $parsed<title_wrap><pos_tag>.Str;
	my $meanings = [];
	my $examples = [];
	for $parsed<meaning_wrap><meaning_group>
	{
		if ($_<meaning>)
		{
			$meanings.push: $_<meaning>.Str;
		}
	}
	for $parsed<example_wrap><example_group>
	{
		$examples.push: (
			$_<example_mans>.Str,
			$_<example_rus>.Str
		);
	}

	$lozv_log.say: $title;
	$lozv_log.say: $part;
	$lozv_log.say: $pos_tag;
	$lozv_log.say: $meanings;
	$lozv_log.say: $examples;
	$lozv_log.say: "--";
	
	++ $line_number;
}
