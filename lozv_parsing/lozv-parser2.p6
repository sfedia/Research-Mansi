use v6;
use lib 'lib';
use DBIish;
use JSON::Tiny;

%*ENV<DBIISH_SQLITE_LIB> = "sqlitel3.dll";

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


my $lozv_plain = open 'lozv.txt';
my $lozv_log = open 'lozv-log.txt', :a;
my @lozv_data = $lozv_plain.lines();
my $lozv_data_length  = @lozv_data.elems;
constant lp_timeout = 3;
my @lp_list = [];

my $dbh = DBIish.connect("SQLite", :database<lozv.sqlite3>);
my $sth = $dbh.prepare(q:to/STATEMENT/);
    INSERT INTO dictionary (title, part, pos, meanings, examples)
    VALUES ( ?, ?, ?, ?, ? )
    STATEMENT


for 0..$lozv_data_length -> $index
{
	@lp_list[$index] = start {
		my $iter = @lozv_data[$index].trim;

		my $parsed = lozv_segment.parse($iter);
		if ( $parsed )
		{
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
			my
			Str $title = $parsed<title_wrap><title>.Str;
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
			$sth.execute($title, $part, $pos_tag, to-json($meanings), to-json($examples));
			say "$index/2100";
		}
	}
	await Promise.anyof(@lp_list[$index], Promise.in(lp_timeout));
}

$sth.finish;

$dbh.dispose;
