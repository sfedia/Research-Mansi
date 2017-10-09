#!/usr/bin/python3
import grammar
# ...
rombandeeva = grammar.Container()

rombandeeva.add_element('universal:morpheme', '^та!л', 'tal_suffix').applied(
    [
        grammar.LinkSentence('# & universal:entity=(word) & mansi:simple_pos=(adj)'),
        [grammar.Action('sem:make_opposite')]
    ]
)
#
rombandeeva.add_element('universal:morpheme', '^т', 't_suffix').add_class('caus_suffixes')
rombandeeva.add_element('universal:morpheme', '^л', 'l_suffix').add_class('caus_suffixes')
rombandeeva.add_element('universal:morpheme', '^лт', 'lt_suffix').add_class('caus_suffixes')
rombandeeva.add_element('universal:morpheme', '^пт', 'pt_suffix').add_class('caus_suffixes')
for element in rombandeeva.get_by_class_name('caus_suffixes'):
	# or just element.applied ??
	rombandeeva.get_by_id(element.get_id()).applied(
		[
			grammar.LinkSentence('# & universal:entity=(word) & mansi:simple_pos=(verb) & sem:non_causative=()'),
			[ grammar.Action('sem:make_causative')]
		]
	)

rombandeeva.get_system('universal:morpheme').subclasses_order(
   '.number_suffix >> .lps >> .case_suffix',
   # the next argument is optional
   parent_filter = grammar.LinkSentence(
      'universal:entity=(word) & mansi:simple_pos=(noun)',
      container
   )
)

rombandeeva.get_system('universal:morpheme').subclasses_order(
	'''
        :prefix +<<
        :root >>+
        .word_building_suffix & APPLIED~=(pos:(verb)) >>+
        .word_inflection_suffix & APPLIED~=(pos:(verb))
    ''',
	parent_filter = grammar.LinkSentence(
		'universal:entity=(word) & mansi:simple_pos=(verb)',
		container
	)
)

rombandeeva.add_element('universal:morpheme', '^г', 'g_suffix').applied(
	[
		grammar.LinkSentence('# & universal:entity=(word) & [ universal:end=(а) | universal:end=(е) | universal:end=(я) ]'),
		[grammar.Action('gram:number:set_dual')]
	]
)

# твёрдые согласные?

rombandeeva.add_element('universal:morpheme', '^ыг', 'yg_suffix').applied(
	[
		grammar.LinkSentence('# & universal:entity=(word) & [ ТВЁРДЫЕ СОГЛАСНЫЕ ]'),
		[grammar.Action('gram:number:set_dual')]
	]
)

# мягкие согласные?

rombandeeva.add_element('universal:morpheme', '^яг', 'yag_suffix').applied(
	[
		grammar.LinkSentence('# & universal:entity=(word) & [ МЯГКИЕ СОГЛАСНЫЕ | universal:end=(и)]'),
		[grammar.Action('gram:number:set_dual')]
	]
)

lps_matrix = [
	['sing', '1', 'ум', 'um'],
	['sing', '2', 'ын', 'yn'],
	['sing', '3', 'е', 'e'],
	['dual', '1', 'ме!н', 'men'],
	['dual', '2', 'ы!н', 'yn'],
	['dual', '3', 'е!н', 'en'],
	['plur', '1', 'ув', 'uv'],
	['plur', '2', 'ы!н', 'yn'],
	['plur', '3', 'а!ныл', 'anyl'],
]

for number, person, suffix, id in lps_matrix:
	rombandeeva.add_element('universal:morpheme', '^' + suffix, id + '_suffix').applied(
		[
			grammar.LinkSentence(
				'# & universal:entity=(word) & gram:possessor:number=({0}) & gram:possessor:person=({0})'.format(number, person)
			),
			[gramar.Action('mansi:make_lp > {0} > {1}'.format(number, person))]
		]
	)

rombandeeva.add_element('universal:morpheme', '^' + suffix, 'yn_suffix').applied(
	[
		grammar.LinkSentence(
			'# & universal:entity=(word) & gram:possessor:number=({0}) & gram:possessor:person=({0})'.format(number, person)
		),
		[
			grammar.Action('mansi:make_lp > sing > 2'),
			grammar.Action('mansi:make_lp > dual > 2'),
		]
	]
)	

# page 59