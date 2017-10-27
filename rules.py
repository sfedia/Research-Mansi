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

#
is_noun = '# & universal:entity=(word) & mansi:basic_pos=(noun) '

rombandeeva.add_element('universal:morpheme', '^г', 'g_suffix').applied(
	[
		grammar.LinkSentence(is_noun + '& [ universal:end=(а) | universal:end=(е) | universal:end=(я) ]'),
		[grammar.Action('gram:number:set_dual')]
	]
)

# твёрдые согласные?

rombandeeva.add_element('universal:morpheme', '^ыг', 'yg_suffix').applied(
	[
		grammar.LinkSentence(is_noun + '& [ ТВЁРДЫЕ СОГЛАСНЫЕ ]'),
		[grammar.Action('gram:number:set_dual')]
	]
)

# мягкие согласные?

rombandeeva.add_element('universal:morpheme', '^яг', 'yag_suffix').applied(
	[
		grammar.LinkSentence(is_noun + '& [ МЯГКИЕ СОГЛАСНЫЕ | universal:end=(и)]'),
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
	rombandeeva.add_element('universal:morpheme', '^' + suffix, id + '_suffix').add_class('lps').applied(
		[
			grammar.LinkSentence(
				is_noun + '& gram:possessor:number=({0}) & gram:possessor:person=({0})'.format(number, person)
			),
			[gramar.Action('mansi:make_lp > {0} > {1}'.format(number, person))]
		]
	)

rombandeeva.add_element('universal:morpheme', '^' + suffix, 'yn_suffix').add_class('lps').applied(
	[
		grammar.LinkSentence(
			is_noun + '& gram:possessor:number=({0}) & gram:possessor:person=({0})'.format(number, person)
		),
		[
			grammar.Action('mansi:make_lp > sing > 2'),
			grammar.Action('mansi:make_lp > dual > 2'),
		]
	]
)	

rombandeeva.add_element('universal:morpheme', '^н', 'n_suffix').applied(
	[
		grammar.LinkSentence(is_noun + '& [ universal:end=(а) | universal:end=(е) | universal:end=(э) ]'),
		[grammar.Action('gram:number:set_plur')]
	]
).add_class('number_suffix')

# твёрдые согласные?

rombandeeva.add_element('universal:morpheme', '^ан', 'an_suffix').applied(
	[
		grammar.LinkSentence(is_noun + '& [ ТВЁРДЫЕ СОГЛАСНЫЕ ]'),
		[grammar.Action('gram:number:set_plur')]
	]
).add_class('number_suffix')

# мягкие согласные?

rombandeeva.add_element('universal:morpheme', '^ян', 'yan_suffix').applied(
	[
		grammar.LinkSentence(is_noun + '& [ МЯГКИЕ СОГЛАСНЫЕ | universal:end=(и)]'),
		[grammar.Action('gram:number:set_plur')]
	]
).add_class('number_suffix')

rombandeeva.add_element('universal:morpheme', '^', 'null_suffix_main_case').applied(
	[
		grammar.LinkSentence(is_noun + '& mansi:is_lemma=()'),
		[grammar.Action('gram:case:set_main')]
	]
).add_class('case_suffix')

rombandeeva.add_element('universal:morpheme', '^н', 'n_case_suffix').applied(
	[
		grammar.LinkSentence(is_noun + '& {universal:before:rx_check > [ГЛАСНЫЙ | ГЛАСНЫЙ СОГЛАСНЫЙ]$}=()'),
		[grammar.Action('gram:case:set_napr')]
	]
).add_class('case_suffix')

rombandeeva.add_element('universal:morpheme', '^ын', 'yn_case_suffix').applied(
	[
		grammar.LinkSentence(is_noun + '& {universal:before:rx_check > [СОГЛАСНЫЙ]{2}$}=()'),
		[grammar.Action('gram:case:set_napr')]
	]
).add_class('case_suffix')

rombandeeva.add_element('universal:morpheme', '^т', 't_case_suffix').applied(
	[
		grammar.LinkSentence(is_noun + '& {universal:before:rx_check > [ГЛАСНЫЙ | ГЛАСНЫЙ СОГЛАСНЫЙ]$}=()'),
		[grammar.Action('gram:case:set_loc')]
	]
).add_class('case_suffix')

rombandeeva.add_element('universal:morpheme', '^ыт', 'yt_case_suffix').applied(
	[
		grammar.LinkSentence(is_noun + '& {universal:before:rx_check > [СОГЛАСНЫЙ]{2}$}=()'),
		[grammar.Action('gram:case:set_loc')]
	]
).add_class('case_suffix')

rombandeeva.add_element('universal:morpheme', '^ныл', 'nyl_case_suffix').applied(
    [
        grammar.LinkSentence(is_noun),
        [grammar.Action('gram:case:set_ish')]
    ]    
).add_class('case_suffix')

rombandeeva.add_element('universal:morpheme', '^л', 'l_case_suffix').applied(
    [grammar.LinkSentence(is_noun + '& {universal:before:rx_check > [ГЛАСНЫЙ]$}=()'),
        [grammar.Action('gram:case:set_instr')]
    ]    
)

rombandeeva.add_element('universal:morpheme', '^ыл', 'l_case_suffix').applied(
    [grammar.LinkSentence(is_noun + '& {universal:before:rx_check > [ТВЁРДЫЙ СОГЛАСНЫЙ]$}=()'),
        [grammar.Action('gram:case:set_instr')]
    ]    
)

rombandeeva.add_element('universal:morpheme', '^л', 'l_case_suffix').applied(
    [grammar.LinkSentence(is_noun + '& {universal:before:rx_check > [МЯГКИЙ СОГЛАСНЫЙ]$}=()'),
        [grammar.Action('gram:case:set_instr')]
    ]    
)

rombandeeva.add_element('universal:morpheme', '^г', 'g_case_suffix').applied(
    [grammar.LinkSentence(is_noun + '& [ universal:end=(а) | universal:end=(е) | universal:end=(э) ]'),
        [grammar.Action('gram:case:set_transf')]
    ]    
)

rombandeeva.add_element('universal:morpheme', '^ыг', 'yg_case_suffix').applied(
    [grammar.LinkSentence(is_noun + '& {universal:before:rx_check > [ТВЁРДЫЙ СОГЛАСНЫЙ]$}=()'),
        [grammar.Action('gram:case:set_transf')]
    ]    
)

rombandeeva.add_element('universal:morpheme', '^иг', 'yg_case_suffix').applied(
    [grammar.LinkSentence(is_noun + '& [{universal:before:rx_check > [МЯГКИЙ СОГЛАСНЫЙ]$}=() | universal:end=(и)]'),
        [grammar.Action('gram:case:set_transf')]
    ]    
)

# page 70

is_verb = '# & universal:entity=(word) & mansi:basic_pos=(verb) '

## warning: mutation strategy may be applied wrong to these elements <= is_verb is too broad for that

rombandeeva.get_class('infinitive_excl_suff').added_behaviour('!override')

# infinitive!

rombandeeva.add_element('universal:morpheme', '^ун!кве', 'u_infinitive_suffix').applied(
    [
        grammar.LinkSentence(is_verb),
        [grammar.Action('gram:verb:set_infinitive')]
    ]    
).add_class('infinitive_excl_suff')

rombandeeva.add_element('universal:morpheme', '^н!кве', 'E_infinitive_suffix').applied(
    [
        grammar.LinkSentence(is_verb),
        [grammar.Action('gram:verb:set_infinitive')]
    ]    
).add_class('infinitive_excl_suff')

# уп, ап, па, пи, п

rombandeeva.add_element('universal:morpheme', '^уп', 'up_wb_suffix').applied(
    [
        grammar.LinkSentence(is_noun),
        [grammar.Action('mansi:verb_to_noun')]
    ]
).add_class('infinitive_excl_suff').add_class('word_building_suffix').add_class('subst_suffix')

rombandeeva.add_element('universal:morpheme', '^ап', 'ap_wb_suffix').applied(
    [
        grammar.LinkSentence(is_noun),
        [grammar.Action('mansi:verb_to_noun')]
    ]
).add_class('infinitive_excl_suff').add_class('word_building_suffix').add_class('subst_suffix')

rombandeeva.add_element('universal:morpheme', '^па', 'pa_wb_suffix').applied(
    [
        grammar.LinkSentence(is_noun),
        [grammar.Action('mansi:verb_to_noun')]
    ]
).add_class('infinitive_excl_suff').add_class('word_building_suffix').add_class('subst_suffix')

rombandeeva.add_element('universal:morpheme', '^пи', 'pi_wb_suffix').applied(
    [
        grammar.LinkSentence(is_noun),
        [grammar.Action('mansi:verb_to_noun')]
    ]
).add_class('infinitive_excl_suff').add_class('word_building_suffix').add_class('subst_suffix')

rombandeeva.add_element('universal:morpheme', '^п', 'p_wb_suffix').applied(
    [
        grammar.LinkSentence(is_noun),
        [grammar.Action('mansi:verb_to_noun')]
    ]
).add_class('infinitive_excl_suff').add_class('word_building_suffix').add_class('subst_suffix')

@foreach_in_class('subst_suffix')
def ss_set_mutation_link(element):
    element.provide_mutation_link(
        [grammar.LinkSentence('# & universal:entity=(word) & mansi:basic_pos=(verb)')]
    )