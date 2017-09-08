#!/usr/bin/perl6
use v6;
grammar lozv {
	rule TOP {
		<number>? \s* <title_wrap> \s* <pos> \s*
		<meaning> + % (,(\s*)) %
	}
}
