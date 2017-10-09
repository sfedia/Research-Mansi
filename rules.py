#!/usr/bin/python3
import grammar
# ...
rombandeeva = grammar.Container()

rombandeeva.add_element('universal:morpheme', '^та!л', 'tal_suffix').applied(
    [
        grammar.LinkSentence('universal:entity=(word) & mansi:simple_pos=(adj)'),
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
			grammar.LinkSentence('universal:entity=(word) & mansi:simple_pos=(verb) & sem:non_causative=()'),
			[ grammar.Action('sem:make_causative')]
		]
	)
rombandeeva.add_element('universal:morpheme', '^юв', 'yuv_suffix').applied(
	[
		grammar.LinkSentence('universal:entity=(word) & mansi:simple_pos=(noun)'),
		[grammar.Action('gram:make_possessive')]
	]
).add_class('lps')

container.get_system('universal:morpheme').subclasses_order(
   '.number_suffix >> .lps >> .case_suffix',
   # the next argument is optional
   parent_filter = grammar.LinkSentence(
      'universal:entity=(word) & mansi:simple_pos=(noun)',
      container
   )
)

$rombandeeva.get_system('universal:morpheme').subclasses_order(
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
