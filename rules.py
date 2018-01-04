#!/usr/bin/python3
import grammar
# ...
# first we should check if the whole token exists in dictionaries
# parent layer switching due to [time limits] like universal:token < [universal:input -> mansi:SH_MOD] (like сь -> щ)
# analytic forms: free morphemes like {A B}
#
rombandeeva = grammar.Container()

rombandeeva.need_form_parameter(
  'mansi:basic_pos',
  ['noun']
  [('mansi:basic_pos', 'noun')],
  [
    grammar.Temp.stepIter('gram:number:set_plur', 'gram:number:set_sing'),
    'grammar:case:set_main'
  ]
)

rombandeeva.need_form_parameter(
    'mansi:base_length',
    [('mansi:base_length', grammar.substComparisonValue('mansi:base_length'))],
    [
        grammar.Temp.remove_by_class('inf_suff')
    ],
    parent_filter=grammar.LinkSentence('mansi:basic_pos=(verb)')
)
# - universal:syl_count:* for VERBS, PRONOUNS etc.

# and other need-forms for other POS

#####

rombandeeva.add_element('universal:morpheme', '^та!л', 'tal_suffix').applied(
    [
        grammar.LinkSentence('# & universal:entity=(token) & mansi:simple_pos=(adj)'),
        [grammar.Action('sem:make_opposite')]
    ]
)
#
rombandeeva.add_element('universal:morpheme', '^т', 't_suffix').add_class('caus_suffixes')
rombandeeva.add_element('universal:morpheme', '^л', 'l_suffix').add_class('caus_suffixes')
rombandeeva.add_element('mansi:VowMorpheme', '^лт', 'lt_suffix').add_class('caus_suffixes')
rombandeeva.add_element('universal:morpheme', '^пт', 'pt_suffix').add_class('caus_suffixes')
for element in rombandeeva.get_by_class_name('caus_suffixes'):
    # or just element.applied ??
    rombandeeva.get_by_id(element.get_id()).applied(
        [
            grammar.LinkSentence('# & universal:entity=(token) & mansi:simple_pos=(verb) & sem:non_causative=()'),
            [ grammar.Action('sem:make_causative')]
        ]
    )

rombandeeva.get_system('universal:morpheme').subclasses_order(
   '? < .number_suffix <<>> .lps >> .case_suffix >> ?',
   # the next argument is optional
   parent_filter=grammar.LinkSentence(
      'universal:entity=(token) & mansi:simple_pos=(noun)',
      rombandeeva
   )
)

rombandeeva.get_system('universal:morpheme').subclasses_order(
    '''
        :prefix +<<
        :root >>+
        .word_building_suffix & APPLIED~=(pos:(verb)) >>+
        .word_inflection_suffix & APPLIED~=(pos:(verb))
    ''',
    parent_filter=grammar.LinkSentence(
        'universal:entity=(token) & mansi:simple_pos=(verb)',
        rombandeeva
    )
)

rombandeeva.get_system('universal:morpheme').subclasses_order(
    '? << :root >> ? >> .word_building_suffix >> .case_suffix >> ?',
    parent_filter=grammar.LinkSentence(
        'universal:entity=(token) & mansi:simple_pos=(noun)'
    )
)


#
is_noun = '# & universal:entity=(token) & mansi:basic_pos=(noun) '

rombandeeva.add_element('universal:morpheme', grammar.Temp.null(), 'number_noun_null_suffix').applied(
    [
        grammar.LinkSentence(is_noun),
        [grammar.Action('gram:number:set_sing')]
    ]    
).add_class('number_suffix')

rombandeeva.add_element('universal:morpheme', '^г', 'g_suffix').applied(
    [
        grammar.LinkSentence(is_noun + '& [ universal:end=(а) | universal:end=(е) | universal:end=(я) ]'),
        [grammar.Action('gram:number:set_dual')]
    ]
).add_class('number_suffix')

# твёрдые согласные?

rombandeeva.add_element('universal:morpheme', '^ыг', 'yg_suffix').applied(
    [
        grammar.LinkSentence(is_noun + '& [ ТВЁРДЫЕ СОГЛАСНЫЕ ]'),
        [grammar.Action('gram:number:set_dual')]
    ]
).add_class('number_suffix')

# мягкие согласные?

rombandeeva.add_element('universal:morpheme', '^яг', 'yag_suffix').applied(
    [
        grammar.LinkSentence(is_noun + '& [ МЯГКИЕ СОГЛАСНЫЕ | universal:end=(и)]'),
        [grammar.Action('gram:number:set_dual')]
    ]
).add_class('number_suffix')

lps_matrix = [
    ['sing', '1', 'ум', 'um'],
    ['sing', '2', 'ын', 'yn'],
    ['sing', '3', 'е', 'e'],
    ['dual', '1', 'ме!н', 'men'],
    ['dual', '3', 'е!н', 'en'],
    ['plur', '1', 'ув', 'uv'],
    ['plur', '3', 'а!ныл', 'anyl'],
]

for number, person, suffix, id in lps_matrix:
    rombandeeva.add_element('universal:morpheme', '^' + suffix, id + '_suffix').add_class('lps').applied(
        [
            grammar.LinkSentence(
                is_noun + '& gram:possessor:number=({0}) & gram:possessor:person=({0})'.format(number, person)
            ),
            [grammar.Action('mansi:make_lp > {0} > {1}'.format(number, person))]
        ]
    )

rombandeeva.add_element('universal:morpheme', '^ы!н', 'yn_suffix').add_class('lps').applied(
    [
        grammar.LinkSentence(
            is_noun + '& gram:possessor:number!=(sing) & gram:possessor:person=(2)'
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

rombandeeva.add_element('universal:morpheme', grammar.Temp.null(), 'null_suffix_main_case').applied(
    [
        grammar.LinkSentence(is_noun),
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
).add_class('case_suffix')

rombandeeva.add_element('universal:morpheme', '^ыл', 'l_case_suffix').applied(
    [grammar.LinkSentence(is_noun + '& {universal:before:rx_check > [ТВЁРДЫЙ СОГЛАСНЫЙ]$}=()'),
        [grammar.Action('gram:case:set_instr')]
    ]    
).add_class('case_suffix')

rombandeeva.add_element('universal:morpheme', '^л', 'l_case_suffix').applied(
    [grammar.LinkSentence(is_noun + '& {universal:before:rx_check > [МЯГКИЙ СОГЛАСНЫЙ]$}=()'),
        [grammar.Action('gram:case:set_instr')]
    ]    
).add_class('case_suffix')

rombandeeva.add_element('universal:morpheme', '^г', 'g_case_suffix').applied(
    [grammar.LinkSentence(is_noun + '& [ universal:end=(а) | universal:end=(е) | universal:end=(э) ]'),
        [grammar.Action('gram:case:set_transf')]
    ]    
).add_class('case_suffix')

rombandeeva.add_element('universal:morpheme', '^ыг', 'yg_case_suffix').applied(
    [grammar.LinkSentence(is_noun + '& {universal:before:rx_check > [ТВЁРДЫЙ СОГЛАСНЫЙ]$}=()'),
        [grammar.Action('gram:case:set_transf')]
    ]    
).add_class('case_suffix')

rombandeeva.add_element('universal:morpheme', '^иг', 'yg_case_suffix').applied(
    [grammar.LinkSentence(is_noun + '& [{universal:before:rx_check > [МЯГКИЙ СОГЛАСНЫЙ]$}=() | universal:end=(и)]'),
        [grammar.Action('gram:case:set_transf')]
    ]    
).add_class('case_suffix')

# page 70

is_verb = '# & universal:entity=(token) & mansi:basic_pos=(verb) '

## AN IMPORTANT RULE

rombandeeva.add_element('universal:char_regex', '([ГЛАСНЫЙ])с([ГЛАСНЫЙ])', 'XsX_sequence').applied(
    [
        grammar.LinkSentence('#'),
        []
    ]    
).add_class('XsX_pair')

rombandeeva.add_element('universal:char_regex:responsive', 'c\g<2>', 'XsX_sequence').applied(
    [
        grammar.LinkSentence('#'),
        [grammar.Action('seq:correction:mansi:XsX')]
    ]    
).add_class('XsX_pair')

rombandeeva.get_class('XsX_pair').added_behaviour('override')
## /

## warning: mutation strategy may be applied wrong to these elements <= is_verb is too broad for that

rombandeeva.get_class('infinitive_excl_suff').added_behaviour('override')

# infinitive!

rombandeeva.add_element('universal:morpheme', '^ун!кве', 'u+_infinitive_suffix').applied(
    [
        grammar.LinkSentence(
            is_verb + '& universal:reg_match=([СОГЛАСНЫЙ_ТВЁРД]$){pre=()} & universal:syl_count:odd=(){pre=()}'
        ),
        [grammar.Action('gram:verb:set_infinitive')]
    ]    
).add_class('infinitive_excl_suff').add_class('inf_suff')

rombandeeva.add_element('universal:morpheme', '^юн!кве', 'yu+_infinitive_suffix').applied(
    [
        grammar.LinkSentence(
            is_verb + '& universal:reg_match=(([СОГЛАСНЫЙ_МЯГК]|й)$){pre=()} & universal:syl_count:odd=(){pre=()}'
        ),
        [grammar.Action('gram:verb:set_infinitive')]
    ]
).add_class('infinitive_excl_suff').add_class('inf_suff')

rombandeeva.add_element('universal:morpheme', '^ан!кве', 'a+_infinitive_suffix').applied(
    [
        grammar.LinkSentence(
            is_verb + '& universal:reg_match=([СОГЛАСНЫЙ]$){pre=()} & universal:syl_count:even=(){pre=()}'
        ),
        [grammar.Action('gram:verb:set_infinitive')]
    ]
).add_class('infinitive_excl_suff').add_class('inf_suff')

rombandeeva.add_element('universal:morpheme', '^н!кве', 'null+_infinitive_suffix').applied(
    [
        grammar.LinkSentence(is_verb + '& universal:reg_match=([ГЛАСНЫЙ]$){pre=()} & universal:syl_count=(1)'),
        [grammar.Action('gram:verb:set_infinitive')]
    ]    
).add_class('infinitive_excl_suff').add_class('inf_suff')

# уп, ап, па, пи, п

rombandeeva.add_element('universal:morpheme', '^уп', 'up_wb_suffix').applied(
    [
        grammar.LinkSentence(is_noun),
        [
            grammar.Action('mansi:verb_to_noun'),
            grammar.Action('mansi:sem:tool-or-action')
        ]
    ]
).add_class('infinitive_excl_suff').add_class('word_building_suffix').add_class('verb_to_noun_suff')

rombandeeva.add_element('universal:morpheme', '^ап', 'ap_wb_suffix').applied(
    [
        grammar.LinkSentence(is_noun),
        [
            grammar.Action('mansi:verb_to_noun'),
            grammar.Action('mansi:sem:tool-or-action')
        ]
    ]
).add_class('infinitive_excl_suff').add_class('word_building_suffix').add_class('verb_to_noun_suff')

rombandeeva.add_element('universal:morpheme', '^па', 'pa_wb_suffix').applied(
    [
        grammar.LinkSentence(is_noun),
        [
            grammar.Action('mansi:verb_to_noun'),
            grammar.Action('mansi:sem:tool-or-action')
        ]
    ]
).add_class('infinitive_excl_suff').add_class('word_building_suffix').add_class('verb_to_noun_suff')

rombandeeva.add_element('universal:morpheme', '^пи', 'pi_wb_suffix').applied(
    [
        grammar.LinkSentence(is_noun),
        [
            grammar.Action('mansi:verb_to_noun'),
            grammar.Action('mansi:sem:tool-or-action')
        ]
    ]
).add_class('infinitive_excl_suff').add_class('word_building_suffix').add_class('verb_to_noun_suff')

rombandeeva.add_element('universal:morpheme', '^п', 'p_wb_suffix').applied(
    [
        grammar.LinkSentence(is_noun),
        [
            grammar.Action('mansi:verb_to_noun'),
            grammar.Action('mansi:sem:tool-or-action')
        ]
    ]
).add_class('infinitive_excl_suff').add_class('word_building_suffix').add_class('verb_to_noun_suff')


@rombandeeva.foreach_in_class('verb_to_noun_suff')
def ss_set_mutation_link(element):
    element.provide_mutation_link(
        [grammar.LinkSentence('# & universal:entity=(token) & mansi:basic_pos=(verb)')]
    )


rombandeeva.add_element('universal:morpheme', '^т', 't_wb_from_noun_suffix').applied(
    [
        grammar.LinkSentence(is_noun),
        [
            grammar.Action('mansi:adj_to_noun'),
            grammar.Action('mansi:sem:obj-size')
        ]
    ]
).add_class('adj_ending_excl').add_class('word_building_suffix').add_class('adj_to_noun_suff')

rombandeeva.add_element('universal:morpheme', '^ит', 'it_wb_from_noun_suffix').applied(
    [
        grammar.LinkSentence(is_noun),
        [
            grammar.Action('mansi:adj_to_noun'),
            grammar.Action('mansi:sem:obj-size')
        ]
    ]
).add_class('adj_ending_excl').add_class('word_building_suffix').add_class('adj_to_noun_suff')

rombandeeva.add_element('universal:morpheme', '^та', 'ta_wb_from_noun_suffix').applied(
    [
        grammar.LinkSentence(is_noun),
        [
            grammar.Action('mansi:adj_to_noun'),
            grammar.Action('mansi:sem:obj-size')
        ]
    ]
).add_class('adj_ending_excl').add_class('word_building_suffix').add_class('adj_to_noun_suff')


@rombandeeva.foreach_in_class('adj_to_noun_suff')
def atn_set_mutation_link(element):
    element.provide_mutation_link(
        [grammar.LinkSentence('# & universal:entity=(token) & mansi:basic_pos=(adj)')]
    )


# page 73, mutation scheme is complicated

rombandeeva.get_class('adj_ending_excl').added_behaviour('override')
# Need some universal:char_regex AS adj_ending_excl there??

rombandeeva.add_element('mansi:morphemeYU', '^т', 't_wb_from_verb_suffix').applied(
    [
        grammar.LinkSentence(is_noun),
        [
            grammar.Action('mansi:verb_to_noun'),
            grammar.Action('mansi:sem:UNKNOWN_MEANING')
        ]
    ]
).add_class('verb_to_noun').add_class('yu.verb_ending_excl').add_class('verb_to_noun_suff')

rombandeeva.add_element('mansi:morphemeYU', '^ит', 'it_wb_from_verb_suffix').applied(
    [
        grammar.LinkSentence(is_noun),
        [
            grammar.Action('mansi:verb_to_noun'),
            grammar.Action('mansi:sem:UNKNOWN_MEANING')
        ]
    ]
).add_class('verb_to_noun').add_class('yu.verb_ending_excl').add_class('verb_to_noun_suff')

rombandeeva.add_element('mansi:morphemeYU', '^та', 'ta_wb_from_verb_suffix').applied(
    [
        grammar.LinkSentence(is_noun),
        [
            grammar.Action('mansi:verb_to_noun'),
            grammar.Action('mansi:sem:UNKNOWN_MEANING')
        ]
    ]
).add_class('verb_to_noun').add_class('yu.verb_ending_excl').add_class('verb_to_noun_suff')


@rombandeeva.foreach_in_class('verb_to_noun_suff')
def vtn_set_mutation_link(element):
    element.provide_mutation_link(
        [grammar.LinkSentence('# & universal:entity=(token) & mansi:basic_pos=(verb)')]
    )

## mansi:morphemeYU ^ункве < universal:morpheme ^ункве

rombandeeva.get_class('yu.verb_ending_excl').added_behaviour('override mutate>MUTATION')

rombandeeva.add_element('universal:char_regex', 'ololo', 'random2728').applied(
    grammar.LinkSentence('something'),
    [
        grammar.Action('MUTATION')
    ]
)

# LOTS OF WORD BUILDING SUFFIXES
# ... pages 72-75
#

# page 77

rombandeeva.add_element('universal:morpheme', '^нув', 'nuv_suffix').applied(
    grammar.LinkSentence('# & universal:entity=(token) & mansi:basic_pos=(adj)'),
    [
        grammar.Action('gram:adj:comparative')
    ]
)

rombandeeva.add_element('universal:morpheme', '^нуве', 'nuve_suffix').applied(
    grammar.LinkSentence('# & universal:entity=(token) & mansi:basic_pos=(adj)'),
    [
        grammar.Action('gram:adj:comparative')
    ]
)

rombandeeva.add_element('universal:morpheme', '^кве', 'kve_suffix').applied(
    grammar.LinkSentence('# & universal:entity=(token) & mansi:basic_pos=(adj)'),
    [
        grammar.Action('sem:adj:dimin'),
        grammar.Action('sem:adj:prenebr')
    ]
)

rombandeeva.add_element('universal:morpheme', '^ысь', 'ys*-suffix').applied(
    grammar.LinkSentence('# & universal:entity=(token) & mansi:basic_pos=(adv)'),
    [
        grammar.Action('gram:adj_to_adv')
    ]
).provide_mutation_link(
    [grammar.LinkSentence('# & universal:entity=(token) & mansi:basic_pos=(adj)')]
)


rombandeeva.add_element('universal:collocation', '''
    <[gram:case=(nom)]> *1 <[gram:case=(ish)]> *1 <[mansi:basic_pos=(adj) & gram:case=(nom)]>
''', 'analytic_comp').applied(
    grammar.LinkSentence('# & universal:entity=(input)'),
    [
        grammar.Action('gram:adj:comparative')
    ]
)


rombandeeva.add_element('universal:collocation', '''
    <[universal:content=(сяр) | universal:content=(сака)]> *1 <[mansi:basic_pos=(adj) & gram:case=(nom)]>
''', 'analytic_superlative').applied(
    grammar.LinkSentence('# & universal:entity=(input)'),
    [
        grammar.Action('gram:adj:superlative')
    ]
)

rombandeeva.add_element('universal:morpheme', '^н!', 'ng_suffix').applied(
    grammar.LinkSentence('# & universal:entity=(token) & mansi:basic_pos=(adj)'),
    [
        grammar.Action('gram:noun_to_adj')
    ]
).provide_mutation_link(
    [grammar.LinkSentence('# & universal:entity=(token) & mansi:basic_pos=(noun)')]
)

rombandeeva.add_element('universal:morpheme', '^ын!', 'yng_suffix').applied(
    grammar.LinkSentence('# & universal:entity=(token) & mansi:basic_pos=(adj)'),
    [
        grammar.Action('gram:noun_to_adj')
    ]
).provide_mutation_link(
    [grammar.LinkSentence('# & universal:entity=(token) & mansi:basic_pos=(noun)')]
)

rombandeeva.add_element('universal:morpheme', '^ин!', 'ing_suffix').applied(
    grammar.LinkSentence('# & universal:entity=(token) & mansi:basic_pos=(adj)'),
    [
        grammar.Action('gram:noun_to_adj')
    ]
).provide_mutation_link(
    [grammar.LinkSentence('# & universal:entity=(token) & mansi:basic_pos=(noun)')]
)

# *** tal_suffix REF

rombandeeva.add_element('universal:morpheme', '^и', 'i_suffix').applied(
    grammar.LinkSentence('# & universal:entity=(token) & mansi:basic_pos=(adj)'),
    [
        grammar.Action('gram:noun_to_adj'),
        grammar.Action('sem:adj_to_noun_corresp')
    ]
)

rombandeeva.add_element('universal:morpheme', '^ы', 'y_suffix').applied(
    grammar.LinkSentence('# & universal:entity=(token) & mansi:basic_pos=(adj)'),
    [
        grammar.Action('gram:noun_to_adj'),
        grammar.Action('sem:adj_to_noun_corresp')
    ]
)

# PARTICIPLE -> ADJ, not actually VERB -> ADJ

rombandeeva.add_element('mansi:morphemeYU', '^м', 'm_suffix').applied(
    grammar.LinkSentence('# & universal:entity=(token) & mansi:basic_pos=(adj)'),
    [
        grammar.Action('gram:verb_to_adj')
    ]
).add_class('yu.verb_ending_excl').provide_mutation_link(
    [grammar.LinkSentence('# & universal:entity=(token) & mansi:basic_pos=(verb)')]
)

rombandeeva.add_element('mansi:morphemeYU', '^ум', 'um_suffix').applied(
    grammar.LinkSentence('# & universal:entity=(token) & mansi:basic_pos=(adj)'),
    [
        grammar.Action('gram:verb_to_adj')
    ]
).add_class('yu.verb_ending_excl').provide_mutation_link(
    [grammar.LinkSentence('# & universal:entity=(token) & mansi:basic_pos=(verb)')]
)

rombandeeva.add_element('mansi:morphemeYU', '^ам', 'am_suffix').applied(
    grammar.LinkSentence('# & universal:entity=(token) & mansi:basic_pos=(adj)'),
    [
        grammar.Action('gram:verb_to_adj')
    ]
).add_class('yu.verb_ending_excl').provide_mutation_link(
    [grammar.LinkSentence('# & universal:entity=(token) & mansi:basic_pos=(verb)')]
)

# page 83

rombandeeva.add_element('universal:morpheme', 'ий', 'iy_suffix').applied(
    grammar.LinkSentence('# & universal:entity=(token) & mansi:basic_pos=(adj)'),
    [
        grammar.Action(grammar.Temp.null()),
        grammar.Action('mansi:russian_loan_word')
    ]
)

rombandeeva.add_element('universal:morpheme', 'ый', 'iy_suffix').applied(
    grammar.LinkSentence('# & universal:entity=(token) & mansi:basic_pos=(adj)'),
    [
        grammar.Action(grammar.Temp.null()),
        grammar.Action('mansi:russian_loan_word')
    ]
)

rombandeeva.add_element('universal:collocation', '''
    <[mansi:basic_pos=(noun) | mansi:basic_pos=(numeral)]> *1 <[mansi:basic_pos=(noun) & mansi:HAS_DerP=()]>
''', 'phrase_adj').applied(
    grammar.LinkSentence('# & universal:entity=(input)'),
    [
        grammar.Action('mansi:phrase_adj')
    ]
)

rombandeeva.add_element('universal:morpheme', '^п', 'p_suffix').applied(
    grammar.LinkSentence('# & universal:entity=(token) & mansi:basic_pos=(noun)'),
    [
        grammar.Action('mansi:make_DerP') # set mansi:HAS_DerP param
    ]
)

rombandeeva.add_element('universal:morpheme', '^уп', 'up_suffix').applied(
    grammar.LinkSentence('# & universal:entity=(token) & mansi:basic_pos=(noun)'),
    [
        grammar.Action('mansi:make_DerP') # set mansi:HAS_DerP param
    ]
)

rombandeeva.add_element('universal:morpheme', '^па', 'pa_suffix').applied(
    grammar.LinkSentence('# & universal:entity=(token) & mansi:basic_pos=(noun)'),
    [
        grammar.Action('mansi:make_DerP') # set mansi:HAS_DerP param
    ]
)

rombandeeva.add_element('universal:experimental:reduplication', 'яныг', 'yanyg_redupl').applied(
    grammar.LinkSentence('# & universal:entity=(input)'),
    [
        grammar.Action('sem:magnification_colloc')
    ]
)

# ??? -ит -> -ит | -ыт ; page 87

rombandeeva.add_element('universal:morpheme', '^ит', 'it_suffix').applied(
    grammar.LinkSentence('# & universal:entity=(token) & mansi:basic_pos=(numeral)'),
    [
        grammar.Action('gram:numeral:card_to_ord')
    ]
)

rombandeeva.add_element('universal:morpheme', '^ыт', 'yt_suffix_for_nums').applied(
    grammar.LinkSentence('# & universal:entity=(token) & mansi:basic_pos=(numeral)'),
    [
        grammar.Action('gram:numeral:card_to_ord')
    ]
)

rombandeeva.add_element('universal:morpheme', '^г', 'g_suffix_for_nums').applied(
    grammar.LinkSentence('# & universal:entity=(token) & mansi:basic_pos=(numeral)'),
    [
        grammar.Action('gram:numeral:card_to_div')
    ]
)

rombandeeva.add_element('universal:morpheme', '^ыг', 'yg_suffix_for_nums').applied(
    grammar.LinkSentence('# & universal:entity=(token) & mansi:basic_pos=(numeral)'),
    [
        grammar.Action('gram:numeral:card_to_div')
    ]
)

rombandeeva.add_element('universal:morpheme', '^л', 'l_suffix_for_nums').applied(
    grammar.LinkSentence('# & universal:entity=(token) & mansi:basic_pos=(numeral)'),
    [
        grammar.Action('gram:numeral:card_to_distr')
    ]
)

rombandeeva.add_element('universal:morpheme', '^ыл', 'yl_suffix_for_nums').applied(
    grammar.LinkSentence('# & universal:entity=(token) & mansi:basic_pos=(numeral)'),
    [
        grammar.Action('gram:numeral:card_to_distr')
    ]
)

rombandeeva.add_element('universal:morpheme', '^иттыг', 'ittyg_suffix').applied(
    grammar.LinkSentence('# & universal:entity=(token) & mansi:basic_pos=(numeral)'),
    [
        grammar.Action('gram:numeral:card_to_repet')
    ]
)

rombandeeva.add_element('universal:morpheme', '^ынтыг', 'yntyg_suffix').applied(
    grammar.LinkSentence('# & universal:entity=(token) & mansi:basic_pos=(numeral)'),
    [
        grammar.Action('gram:numeral:card_to_repet')
    ]
)

rombandeeva.add_element('universal:collocation', '''
    <[mansi:basic_pos=(numeral) & [gram:numeral_cat=(cardinal) | gram:numeral_cat=(ordinal)]]>
    *1 <[universal:content=(сёс)]>
''', 'repet_numeral_colloc').applied(
    grammar.LinkSentence('# & universal:entity=(input)'),
    [
        grammar.Action('gram:numeral:co_to_repet_colloc')
    ]
)

# page 91 !!

rombandeeva.add_element('universal:morpheme', '^кем', 'kem_suffix').applied(
    grammar.LinkSentence('''# & universal:entity=(token) & mansi:basic_pos=(numeral)
    & gram:numeral_cat=(cardinal)'''),
    [
        grammar.Action('gram:numeral:cardinal_to_round')
    ]
).add_class('kem_abstraction')

rombandeeva.get_class('kem_abstraction').added_behaviour('''
    prepend <universal:morpheme> ( (^ах) | (^ман) ) -> (0.5|0.5)
''')

rombandeeva.add_element('universal:collocation', '''
    <[mansi:basic_pos=(numeral)]> *1 <[universal:content=(суп) | universal:content=(па!л)]>
''', 'num_partial_colloc').applied(
    grammar.LinkSentence('# & universal:entity=(input)'),
    [
        grammar.Action('mansi:numeral:partial_colloc')
    ]
)

# extract morphemes from tokens here

personal_pronouns = {
    '1SG': {
        'nom': 'ам',
        'acc': 'а!нум',
        'dat': 'а!нумн',
        'ish': 'а!нумныл',
        'instr': 'а!нумтыл',
    },
    '2SG': {
        'nom': 'нан!',
        'acc': 'нан!ын',
        'dat': 'нан!ынн',
        'ish': 'нан!ынныл',
        'instr': 'нан!ынтыл',
    },
    '3SG': {
        'nom': 'тав',
        'acc': 'таве',
        'dat': 'таве!н',
        'ish': 'таве!ныл',
        'instr': 'таветыл',
    },
    '1DUAL': {
        'nom': 'ме!н',
        'acc': 'ме!нме!н',
        'dat': 'ме!нме!нн',
        'ish': 'ме!нме!нныл',
        'instr': 'ме!нме!нтыл',
    },
    '2DUAL': {
        'nom': 'нэ!н',
        'acc': 'нэ!нан',
        'dat': 'нэ!нанн',
        'ish': 'нэ!нанныл',
        'instr': 'нэ!нантыл',
    },
    '3DUAL': {
        'nom': 'тэ!н',
        'acc': 'тэ!нтэ!н',
        'dat': 'тэ!нтэ!нн',
        'ish': 'тэ!нтэ!нныл',
        'instr': 'тэ!нтэ!нтыл',
    },
    '1PL': {
        'nom': 'ма!н',
        'acc': 'ма!нав',
        'dat': 'ма!навн',
        'ish': 'ма!навныл',
        'instr': 'ма!навтыл'
    },
    '2PL': {
        'nom': 'на!н',
        'acc': 'на!нан',
        'dat': 'нананн',
        'ish': 'на!нанныл',
        'instr': 'на!нантыл'
    },
    '3PL': {
        'nom': 'та!н',
        'acc': 'та!наныл',
        'dat': 'та!нанылн',
        'ish': 'та!нанылныл',
        'instr': 'та!нанылтыл'
    }
}

for person_number, cases in personal_pronouns:
    for case, value in cases:
        rombandeeva.add_element(
            'universal:token', value, 'pers_pron_{}.{}'.format(person_number, case)
        ).applied(
            grammar.LinkSentence('# & universal:entity=(input)'),
            [
                grammar.Action('mansi:pronoun:personal:' + person_number)
                grammar.Action('gram:case:' + case)
            ]
        )

rombandeeva.add_element('universal:morpheme', '^ки', 'ki_pronoun_suff').applied(
    grammar.LinkSentence('# & universal:entity=(token) & mansi:pronoun:is_personal=()'),
    [
        grammar.Action('mansi:pronoun:lich_ukaz')
    ]
).add_class('lich_ukaz')

rombandeeva.add_element('universal:morpheme', '^кке', 'kke_suffix').applied(
    grammar.LinkSentence('# & universal:entity=(token) & mansi:pronoun:is_personal=()'),
    [
        grammar.Action('mansi:pronoun:restriction')
    ]
).add_class('kke_suff')

rombandeeva.get_system('universal:morpheme').subclasses_order(
   '? <>> .kke_suff > .p_lps',
   parent_filter=grammar.LinkSentence(
      'universal:entity=(token) & mansi:simple_pos=(pronoun) & mansi:pronoun:is_personal=()',
      rombandeeva
   )
)

rombandeeva.add_element('universal:morpheme', '^на!', 'na_pr_suffix').applied(
    grammar.LinkSentence('# & mansi:simple_pos=(pronoun) & mansi:pronoun:is_personal=()'),
    [
        grammar.Action('mansi:pronoun:lich_vozvr')
    ]
).add_class('na_suff')

rombandeeva.get_system('universal:morpheme').subclasses_order(
    '? > .lich_ukaz > .na_suff > .p_lps',
    parent_filter=grammar.LinkSentence(
      'universal:entity=(token) & mansi:simple_pos=(pronoun) & mansi:pronoun:is_personal=()',
      rombandeeva
   )
)

lps_matrix_2 = [
    ['sing', '1', '^м'],
    ['sing', '3', '^тэ'],
    ['dual', '1', '^ме!н'],
    ['dual', '3', '^тэ!н'],
    ['plur', '1', '^в'],
    ['plur', '3', '^ныл']
]

p_lps_filter = '# & universal:entity=(token) & mansi:basic_pos=(pronoun) & mansi:pronoun:is_personal=()'
for number, person, suffix in lps_matrix_2:
    rombandeeva.add_element(
        'universal:morpheme',
        suffix,
        '2a_{}_{}_suff_lps'.format(number, person)
    ).applied(
        grammar.LinkSentence(p_lps_filter),
        [
            grammar.Action('mansi:make_lp', arguments=[number, person])
        ]
    ).add_class('p_lps')

rombandeeva.add_element(
    'universal:morpheme',
    '^н',
    '2a_sing/plur_2_suff_lps'
).applied(
    grammar.LinkSentence(p_lps_filter),
    [
        grammar.Action('mansi:make_lp', arguments=['sing', '2'], branching=True),
        grammar.Action('mansi:make_lp', arguments=['plur', '2'], branching=True)
    ]
).add_class('p_lps')

# page 98-99!

interrog_pronoun = [
    ['хотъют', 'хотъютыг', 'хотъютыт', 'hotyut'],
    ['хо!н!ха', 'хо!н!хаг', 'хо!н!хат', 'honha'],
    ['ма!ныр', 'ма!нарыг', 'ма!нарыт', 'manyr']
]

for sing, dual, plur, id_word in interrog_pronoun:
    rombandeeva.add_element('universal:token', sing, '{}_sing'.format(id_word)).applied(
        grammar.LinkSentence('# & universal:entity=(input)'),
        [
            grammar.Action('gram:number:set_sing')
        ]
    ).add_class('interrog_pronoun')
    rombandeeva.add_element('universal:token', dual, '{}_dual'.format(id_word)).applied(
        grammar.LinkSentence('# & universal:entity=(input)'),
        [
            grammar.Action('gram:number:set_dual')
        ]
    ).add_class('interrog_pronoun')
    rombandeeva.add_element('universal:token', sing, '{}_sing'.format(id_word)).applied(
        grammar.LinkSentence('# & universal:entity=(input)'),
        [
            grammar.Action('gram:number:set_dual')
        ]
    ).add_class('interrog_pronoun')


@rombandeeva.foreach_in_class('interrog_pronoun')
def interrog_pronouns_as_nouns(element):
    element.intrusion(
        grammar.LinkSentence('universal:entity=(noun)'),
        whitelist={
            'classes': ['case_suffixes']
        }
    )
    element.bw_list(exclude={'mutations': ['gram:case:set_loc']})

demonstr_pronoun_matrix = [
    [['ты', 'та'], ['тыиг', 'таиг'], ['тыит', 'таит']],
    [['тыи', 'таи'], ['тыиг', 'таиг'], ['тыит', 'таит']],
    [['тыин', 'таин'], ['тыигн', 'таигн'], ['тыитн', 'таитн']],
    [['тыиныл', 'таиныл'], ['тыигныл', 'таигныл'], ['тыитныл', 'таитныл']],
    [['тыил', 'таил'], ['тыигыл', 'таигыл'], ['тыитыл', 'таитыл']],
    [['тыиг', 'таиг'], [], []]
]

cases = ['nom', 'acc', 'dat', 'ish', 'instr', 'transf']
num = ['sing', 'dual', 'plur']
for j, group in enumerate(demonstr_pronoun_matrix):
    for e, number in enumerate(group):
        rombandeeva.add_element(
            'universal:token', number[0], 'pd.ty_{}_{}'.format(j, e)
        ).applied(
            grammar.LinkSentence('# & universal:entity=(input)'),
            [
                grammar.Action('gram:case:set_{}'.format(cases[j])),
                grammar.Action('gram:number:set_{}'.format(num[e])),
                grammar.Action('mansi:pronoun:demonstrative')
            ]
        )
        rombandeeva.add_element(
            'universal:token', number[1], 'pd.ta_{}_{}'.format(j, e)
        ).applied(
            grammar.LinkSentence('# & universal:entity=(input)'),
            [
                grammar.Action('gram:case:set_{}'.format(cases[j])),
                grammar.Action('gram:number:set_{}'.format(num[e])),
                grammar.Action('mansi:pronoun:demonstrative')
            ]
        )

det_pronoun_matrix = [
    ['tamle', 'тамле'],
    ['kasyn', 'ка!сын!'],
    ['pussyn', 'пуссын'],
    ['tova', 'то!ва'],
    ['tasavit', 'таса!вит']
]
for id_word, mansi_word in det_pronoun_matrix:
    rombandeeva.add_element(
        'universal:token:start',
        mansi_word,
        id_word
    ).applied(
        grammar.LinkSentence('# & universal:entity=(input)'),
        [
            grammar.Action('mansi:set_basic_pos:pronoun'),
            grammar.Action('mansi:pronoun:determinative')
        ]
    )

hotpa = ['хо!тпа', 'хо!тпаг', 'хо!тпат']
matyr = ['матыр', 'матарыг', 'матарыт']

for j in range(3):
    for s in ('hotpa', 'matyr'):
        rombandeeva.add_element(
            'universal:token', eval(s)[j], 'pi_{}_{}'.format(s, num[j])
        ).applied(
            grammar.LinkSentence('# & universal:entity=(input)'),
            [
                grammar.Action('gram:number:set_{}'.format(num[j]))
            ]
        )

matyr_hotpa_matrix = [
    ['nom', 'хо!тпа', 'матыр'],
    ['dat', 'хо!тпан', 'матарн'],
    ['ish', 'хо!тпаныл', 'матарныл'],
    ['instr', 'хо!тпал', 'матарыл'],
    ['transf', 'хо!тпаг', 'матарыг']
]

for case, h_paradigm, m_paradigm in matyr_hotpa_matrix:
    rombandeeva.add_element(
        'universal:token', h_paradigm, 'hotpa_{}'.format(case)
    ).applied(
        grammar.LinkSentence('# & universal:entity=(input)'),
        [
            grammar.Action('gram:case:set_{}'.format(case))
        ]
    )
    rombandeeva.add_element(
        'universal:token', m_paradigm, 'matyr_{}'.format(case)
    ).applied(
        grammar.LinkSentence('# & universal:entity=(input)'),
        [
            grammar.Action('gram:case:set_{}'.format(case))
        ]
    )

rombandeeva.add_element('universal:token:start', 'хо!тпа')

# negative pronouns нэ!мхо!тпа and нэ!матыр
for case, h_paradigm, m_paradigm in matyr_hotpa_matrix:
    rombandeeva.add_element(
        'universal:token', 'нэ!м' + h_paradigm, 'NEG_hotpa_{}'.format(case)
    ).applied(
        grammar.LinkSentence('# & universal:entity=(input)'),
        [
            grammar.Action('gram:case:set_{}'.format(case))
        ]
    )
    rombandeeva.add_element(
        'universal:token', 'нэ!' + m_paradigm, 'NEG_matyr_{}'.format(case)
    ).applied(
        grammar.LinkSentence('# & universal:entity=(input)'),
        [
            grammar.Action('gram:case:set_{}'.format(case))
        ]
    )

# pronouns need further description

# page 107, VERB
# `not a derivative` parameter
rombandeeva.add_element('universal:morpheme', '^ахт', 'aht_suffix').applied(
    grammar.LinkSentence('# & universal:entity=(token) & mansi:basic_pos=(verb)'),
    [
        grammar.Action('gram:make_intransitive')
    ]
).add_class('trans_suffs')

rombandeeva.add_element('universal:morpheme', '^хат', 'hat_suffix').applied(
    grammar.LinkSentence('# & universal:entity=(token) & mansi:basic_pos=(verb)'),
    [
        grammar.Action('gram:make_intransitive')
    ]
).add_class('trans_suffs')

transitive_suffs = [('lt', 'лт'), ('pt', 'пт'), ('ltt', 'лтт'), ('tt', 'тт')]
for code, suff in transitive_suffs:
    rombandeeva.add_element('universal:morpheme', '^' + suff, code + '_suffix').applied(
        grammar.LinkSentence(
            '# & universal:entity=(token) & mansi:basic_pos=(verb) & gram:intransitive=()'
        ),
        [
            grammar.Action('gram:make_transitive')
        ]
    ).add_class('trans_suffs')

rombandeeva.get_by_id('lt_suffix').add_class('lt_suff')

rombandeeva.add_element('mansi:morphemeYU', '^ыгл', 'ygl_suffix').applied(
    grammar.LinkSentence(
        '# & universal:entity=(token) & mansi:basic_pos=(verb) & gram:intransitive=()'
    ),
    [
        grammar.Action('gram:make_transitive')
    ]
).add_class('trans_suffs')

rombandeeva.add_element('mansi:morphemeYU', '^гл', 'gl_suffix').applied(
    grammar.LinkSentence(
        '# & universal:entity=(token) & mansi:basic_pos=(verb) & gram:intransitive=()'
    ),
    [
        grammar.Action('gram:make_transitive')
    ]
).add_class('trans_suffs')

rombandeeva.add_element('universal:morpheme', grammar.Temp.null(), 'null_for_trans').applied(
    grammar.LinkSentence(
        '# & universal:entity=(token) & mansi:basic_pos=(verb)'
    ),
    [
        grammar.Action('gram:make_intransitive')
    ]
).add_class('trans_suffs')

rombandeeva.get_system('universal:morpheme').subclasses_order(
    '''? < .lt_suff >> .inf_suff''',
    parent_filter=grammar.LinkSentence('universal:entity=(token) & mansi:basic_pos=(verb)')
)

rombandeeva.add_element('universal:morpheme', '^хат', 'hat_suffix').applied(
    grammar.LinkSentence(
        '# & universal:entity=(token) & mansi:basic_pos=(verb) & mansi:base_length=(1)'
    ),
    [
        grammar.Action('gram:make_reflexive')
    ]
)

rombandeeva.add_element('universal:morpheme', '^ахт', 'aht_suffix').applied(
    grammar.LinkSentence(
        '# & universal:entity=(token) & mansi:basic_pos=(verb) & mansi:base_length>(1)'
    ),
    [
        grammar.Action('gram:make_reflexive')
    ]
)

# reflexive не могут иметь при себе прямого дополнения

# page 112, побудительные глаголы - повторение предыдущего

# page 113, типы спряжения глагола

rombandeeva.add_element('universal:morpheme', '^л', 'l_oc_suffix').applied(
    grammar.LinkSentence(
        '# & universal:entity=(token) & mansi:basic_pos=(verb) & [gram:person=(1) | gram:person=(2)]'
    ),
    [
        grammar.Action('mansi:set_obj_conj')
    ]
).add_class('conj_set')

rombandeeva.add_element('universal:morpheme', '^тэ', 'te_oc_suffix').applied(
    grammar.LinkSentence(
        '# & universal:entity=(token) & mansi:basic_pos=(verb) & gram:person=(3)'
    ),
    [
        grammar.Action('mansi:conj:set_obj')
    ]
).add_class('conj_set')

rombandeeva.add_element('universal:morpheme', '^т', 't_oc_suffix').applied(
    grammar.LinkSentence(
        '# & universal:entity=(token) & mansi:basic_pos=(verb) & gram:person=(3)'
    ),
    [
        grammar.Action('mansi:conj:set_obj')
    ]
).add_class('conj_set')

rombandeeva.add_element('universal:morpheme', '^ве', 've_spc_suffix').applied(
    grammar.LinkSentence(
        '# & universal:entity=(token) & mansi:basic_pos=(verb) & gram:person=(3)'
    ),
    [
        grammar.Action('mansi:conj:set_subj_pass')
    ]
).add_class('conj_set')

rombandeeva.add_element('universal:morpheme', grammar.Temp.null(), 'conj_null').applied(
    grammar.LinkSentence('# & universal:entity=(token) & mansi:basic_pos=(verb)'),
    [
        grammar.Action('mansi:conj:set_objectless')
    ]
).add_class('conj_set')
#

present_s_consonant_suffs = [('ye!g', 'е!г'), ('i', 'и'), ('ye', 'е'), ('ye!', 'е!')]
for code, suff in present_s_consonant_suffs:
    rombandeeva.add_element(
        'universal:morpheme',
        '^' + suff,
        '{}_present_suff'.format(code)
    ).applied(
        grammar.LinkSentence(
            '''# & universal:entity=(token)
            & mansi:basic_pos=(verb)
            & universal:reg_match=([СОГЛАСНЫЙ_МЯГК]$){pre=()}
            '''
        ),
        [
            grammar.Action('gram:tense:set_present')
        ]
    )

present_h_consonant_suffs = [('eg', 'эг'), ('e!g', 'э!г'), ('y', 'ы'), ('e', 'э'), ('e!', 'э!')]
for code, suff in present_h_consonant_suffs:
    rombandeeva.add_element(
        'universal:morpheme',
        '^' + suff,
        '{}_present_suff'.format(code)
    ).applied(
        grammar.LinkSentence(
            '''# & universal:entity=(token)
            & mansi:basic_pos=(verb)
            & mansi:conj=(objectless)
            & universal:reg_match=([СОГЛАСНЫЙ_ТВЁРД]$){pre=()}'''
        ),
        [
            grammar.Action('gram:tense:set_present')
        ]
    )

rombandeeva.add_element('universal:morpheme', '^ыс', 'ys_past_suffix').applied(
    grammar.LinkSentence(
        '''# & universal:entity=(token)
            & mansi:basic_pos=(verb)
            & universal:syl_count=(1)
            & universal:reg_match([СОГЛАСНЫЙ]{1,2}$){pre=()}'''
    ),
    [
        grammar.Action('gram:tense:set_past')
    ]
).add_class('past_suffixes')

rombandeeva.add_element('universal:morpheme', '^ас', 'as_past_suffix').applied(
    grammar.LinkSentence(
        '''# & universal:entity=(token)
            & mansi:basic_pos=(verb)
            & universal:syl_count>(1)
            & universal:reg_match([СОГЛАСНЫЙ]{1,2}$){pre=()}'''
    ),
    [
        grammar.Action('gram:tense:set_past')
    ]
).add_class('past_suffixes')

# page 115

rombandeeva.add_element('universal:morpheme', '^с', 's_past_suffix').applied(
    grammar.LinkSentence(
        '''# & universal:entity=(token)
            & mansi:basic_pos=(verb)
            & universal:syl_count>(1)
            & universal:reg_match([ГЛАСНЫЙ]$){pre=()}'''
    ),
    [
        grammar.Action('gram:tense:set_past')
    ]
).add_class('past_suffixes')

rombandeeva.add_element('universal:morpheme', '^м', 'm_unob_suffix').applied(
    grammar.LinkSentence(
        '''#
        & universal:entity=(token)
        & mansi:basic_pos=(verb)
        & [ mansi:conj=(objectless) | mansi:conj=(obj) ]
        & mansi:syl_count=(1)
        & universal:reg_match=([СОГЛАСНЫЙ]$){pre=()}'''
    ),
    [
        grammar.Action('mansi:mood:set_unobvious_action'),
        grammar.Action('mansi:tense:set_past')
    ]
)

rombandeeva.add_element('universal:morpheme', '^ум', 'um_unob_suffix').applied(
    grammar.LinkSentence(
        '''#
        & universal:entity=(token)
        & mansi:basic_pos=(verb)
        & [ mansi:conj=(objectless) | mansi:conj=(obj) ]
        & mansi:syl_count=(1)
        & universal:reg_match=([СОГЛАСНЫЙ]$){pre=()}
        & universal:reg_match!=([лн]$){pre=()}'''
    ),
    [
        grammar.Action('mansi:mood:set_unobvious_action'),
        grammar.Action('mansi:tense:set_past')
    ]
)

rombandeeva.add_element('universal:morpheme', '^ам', 'am_unob_suffix').applied(
    grammar.LinkSentence(
        '''#
        & universal:entity=(token)
        & mansi:basic_pos=(verb)
        & [ mansi:conj=(objectless) | mansi:conj=(obj) ]
        & mansi:syl_count>=(1)
        & universal:reg_match=([лн]$){pre=()}'''
    ),
    [
        grammar.Action('mansi:mood:set_unobvious_action'),
        grammar.Action('mansi:tense:set_past')
    ]
)

rombandeeva.add_element('mansi:morpheme_soft', '^има', 'ima_unob_suffix').applied(
    grammar.LinkSentence(
        '''#
        & universal:entity=(token)
        & mansi:basic_pos=(verb)
        & gram:transitive=()
        & mansi:syl_count>=(1)
        & universal:reg_match=([лнст]'$){pre=()}
        & mansi:conj=(subj_pass)'''
    ),
    [
        grammar.Action('mansi:mood:set_unobvious_action')
    ]
)

rombandeeva.add_element('mansi:morpheme_soft', '^ыма', 'yma_unob_suffix').applied(
    grammar.LinkSentence(
        '''#
        & universal:entity=(token)
        & mansi:basic_pos=(verb)
        & gram:transitive=()
        & mansi:syl_count>=(1)
        & universal:reg_match=([лнст]$){pre=()}
        & mansi:conj=(subj_pass)'''
    ),
    [
        grammar.Action('mansi:mood:set_unobvious_action')
    ]
)

# page 116
# INDICATIVE


rombandeeva.add_element('universal:morpheme', '^ум', 'um_1sing_ind_objless').applied(
    grammar.LinkSentence(
        '''#
        & universal:entity=(token)
        & mansi:basic_pos=(verb)
        & mansi:conj=(objectless)'''
    ),
    [
        grammar.Action('mansi:verb:set_person', arguments=['1']),
        grammar.Action('gram:number:set_sing')
    ]
).add_class('objectless_conj_suffixes')

rombandeeva.add_element('universal:morpheme', '^н', 'n_2sing_ind_objless').applied(
    grammar.LinkSentence(
        '''#
        & universal:entity=(token)
        & mansi:basic_pos=(verb)
        & mansi:conj=(objectless)'''
    ),
    [
        grammar.Action('mansi:verb:set_person', arguments=['2']),
        grammar.Action('gram:number:set_sing')
    ]
).add_class('objectless_conj_suffixes')

rombandeeva.add_element('universal:morpheme', '^ын', 'yn_2sing_ind_objless').applied(
    grammar.LinkSentence(
        '''#
        & universal:entity=(token)
        & mansi:basic_pos=(verb)
        & mansi:conj=(objectless)'''
    ),
    [
        grammar.Action('mansi:verb:set_person', arguments=['2']),
        grammar.Action('gram:number:set_sing')
    ]
).add_class('objectless_conj_suffixes')

rombandeeva.add_element(
    'universal:morpheme',
    grammar.Temp.null(),
    'null_3sing_ind_objless'
).applied(
    grammar.LinkSentence('# & universal:entity=(token) & mansi:basic_pos=(verb) & mansi:conj=(objectless)'),
    [
        grammar.Action('mansi:verb:set_person', arguments=['3']),
        grammar.Action('gram:number:set_sing')
    ]
)

rombandeeva.add_element('universal:morpheme', '^ме!н', 'men_1dual_ind_objless').applied(
    grammar.LinkSentence(
        '''#
        & universal:entity=(token)
        & mansi:basic_pos=(verb)
        & mansi:conj=(objectless)'''
    ),
    [
        grammar.Action('mansi:verb:set_person', arguments=['1']),
        grammar.Action('gram:number:set_dual')
    ]
).add_class('objectless_conj_suffixes')

rombandeeva.add_element('universal:morpheme', '^ы!н', 'yn_2_dual/plur_ind_objless').applied(
    grammar.LinkSentence(
        '''#
        & universal:entity=(token)
        & mansi:basic_pos=(verb)
        & mansi:conj=(objectless)'''
    ),
    [
        grammar.Action('mansi:verb:set_person', arguments=['2']),
        grammar.Action('gram:number:set_dual', branching=True),
        grammar.Action('gram:number:set_plur', branching=True)
    ]
).add_class('objectless_conj_suffixes')

rombandeeva.add_element('universal:morpheme', '^ыг', 'yg_3dual_ind_objless').applied(
    grammar.LinkSentence(
        '''#
        & universal:entity=(token)
        & mansi:basic_pos=(verb)
        & mansi:conj=(objectless)'''
    ),
    [
        grammar.Action('mansi:verb:set_person', arguments=['3']),
        grammar.Action('gram:number:set_dual')
    ]
).add_class('objectless_conj_suffixes')

rombandeeva.add_element('universal:morpheme', '^г', 'g_3dual_ind_objless').applied(
    grammar.LinkSentence(
        '''#
        & universal:entity=(token)
        & mansi:basic_pos=(verb)
        & mansi:conj=(objectless)'''
    ),
    [
        grammar.Action('mansi:verb:set_person', arguments=['3']),
        grammar.Action('gram:number:set_dual')
    ]
).add_class('objectless_conj_suffixes')

rombandeeva.add_element('universal:morpheme', '^ув', 'uv_1plur_ind_objless').applied(
    grammar.LinkSentence(
        '''#
        & universal:entity=(token)
        & mansi:basic_pos=(verb)
        & mansi:conj=(objectless)'''
    ),
    [
        grammar.Action('mansi:verb:set_person', arguments=['1']),
        grammar.Action('gram:number:set_plur')
    ]
).add_class('objectless_conj_suffixes')

rombandeeva.add_element('universal:morpheme', '^в', 'v_1plur_ind_objless').applied(
    grammar.LinkSentence(
        '''#
        & universal:entity=(token)
        & mansi:basic_pos=(verb)
        & mansi:conj=(objectless)'''
    ),
    [
        grammar.Action('mansi:verb:set_person', arguments=['1']),
        grammar.Action('gram:number:set_plur')
    ]
).add_class('objectless_conj_suffixes')

rombandeeva.add_element('universal:morpheme', '^э!в', 'ev_1plur_ind_objless').applied(
    grammar.LinkSentence(
        '''#
        & universal:entity=(token)
        & mansi:basic_pos=(verb)
        & mansi:conj=(objectless)'''
    ),
    [
        grammar.Action('mansi:verb:set_person', arguments=['1']),
        grammar.Action('gram:set_number:plur')
    ]
).add_class('objectless_conj_suffixes')

rombandeeva.add_element('universal:morpheme', '^ыт', 'yt_3plur_ind_objless').applied(
    grammar.LinkSentence(
        '''#
        & universal:entity=(token)
        & mansi:basic_pos=(verb)
        & mansi:conj=(objectless)'''
    ),
    [
        grammar.Action('mansi:verb:set_person', arguments=['3']),
        grammar.Action('gram:set_number:plur'),
    ]
).add_class('objectless_conj_suffixes')

rombandeeva.get_system('universal:morpheme').subclasses_order(
    '.past_suffixes > .objectless_conj_suffixes',
    parent_filter=grammar.LinkSentence(
        'universal:entity=(token) & mansi:basic_pos=(verb) & mansi:conj=(objectless)'
    )
)

rombandeeva.add_element('universal:collocation', '''
    <[mansi:conj=(objectless)] :contains[.objectless_conj_suffixes]> *1
    тах''', 'analytic_future').applied(
    grammar.LinkSentence('# & universal:entity=(input)'),
    [
        grammar.Action('gram:tense:set_future')
    ]
)

rombandeeva.add_element(
    'universal:collocation',
    '<[gram:verb:infinitive=()]> *1 <[mansi:lemma=(патун!кве)]>',
    'future_patunkwe'
).applied(
    grammar.LinkSentence('# & universal:entity=(input)'),
    [
        grammar.Action('gram:tense:set_future')
    ]
)

# page 121

rombandeeva.add_element('mansi:morphemeYU', '^и', 'i_suffix_present').applied(
    grammar.LinkSentence('# & universal:entity=(token) & mansi:conj=(obj)'),
    [
        grammar.Action('gram:tense:set_present')
    ]
).add_class('obj_conj_tense')

rombandeeva.add_element('universal:morpheme', '^л', 'l_suffix_object_sing').applied(
    grammar.LinkSentence('# & universal:entity=(token) & mansi:conj=(obj)'),
    [
        grammar.Action('mansi:object_number:set_sing')
    ]
).add_class('obj_conj_object_number')

rombandeeva.add_element('mansi:morphemeYU', '^аг', 'ag_suffix_object_dual').applied(
    grammar.LinkSentence('# & universal:entity=(token) & mansi:conj=(obj)'),
    [
        grammar.Action('mansi:object_number:set_dual')
    ]
).add_class('obj_conj_object_number')

rombandeeva.add_element('mansi:morphemeYU', '^ан', 'an_suffix_object_plur').applied(
    grammar.LinkSentence('# & universal:entity=(token) & mansi:conj=(obj)'),
    [
        grammar.Action('mansi:object_number:set_plur')
    ]
).add_class('obj_conj_object_number')

rombandeeva.get_system('universal:morpheme').subclasses_order(
    '.obj_conj_tense > .obj_conj_object_number',
    parent_filter=grammar.LinkSentence('universal:entity=(token) & mansi:conj=(obj)')
)

rombandeeva.get_system('universal:morpheme').subclasses_order(
    '#i_suffix_present > .obj_conj_object_number > .l_friendly',
    parent_filter=grammar.LinkSentence('universal:entity=(token) & mansi:conj=(obj)')
)

rombandeeva.get_system('universal:morpheme').subclasses_order(
    '#i_suffix_present > .l_non_friendly',
    parent_filter=grammar.LinkSentence('universal:entity=(token) & mansi:conj=(obj)')
)

rombandeeva.add_element('mansi:VowMorpheme', '^ум', 'um_obj_conj').applied(
    grammar.LinkSentence('# & universal:entity=(token) & mansi:conj=(obj)'),
    [
        grammar.Action('mansi:verb:set_person', arguments=['1']),
        grammar.Action('gram:number:set_sing')
    ]
).add_class('l_friendly')

rombandeeva.add_element('mansi:VowMorpheme', '^ын', 'yn_obj_conj').applied(
    grammar.LinkSentence('# & universal:entity=(token) & mansi:conj=(obj)'),
    [
        grammar.Action('mansi:verb:set_person', arguments=['2']),
        grammar.Action('gram:number:set_sing')
    ]
).add_class('l_friendly')


rombandeeva.add_element('universal:morpheme', '^тэ', 'te_obj_conj').applied(
    grammar.LinkSentence('# & universal:entity=(token) & mansi:conj=(obj)'),
    [
        grammar.Action('mansi:verb:set_person', arguments=['3']),
        grammar.Action('gram:number:set_sing')
    ]
).add_class('l_non_friendly')

rombandeeva.add_element('mansi:VowMorpheme', '^ме!н', 'men_obj_conj').applied(
    grammar.LinkSentence('# & universal:entity=(token) & mansi:conj=(obj)'),
    [
        grammar.Action('mansi:verb:set_person', arguments=['1']),
        grammar.Action('gram:number:set_dual')
    ]
).add_class('l_friendly')

rombandeeva.add_element('mansi:VowMorpheme', '^ы!н', 'yyn_obj_conj').applied(
    grammar.LinkSentence('# & universal:entity=(token) & mansi:conj=(obj)'),
    [
        grammar.Action('mansi:verb:set_person', arguments=['2']),
        grammar.Action('gram:number:set_dual', branching=True),
        grammar.Action('gram:number:set_plur', branching=True)
    ]
).add_class('l_friendly')

rombandeeva.add_element('universal:morpheme', '^тэ!н', 'teen_obj_conj').applied(
    grammar.LinkSentence('# & universal:entity=(token) & mansi:conj=(obj)'),
    [
        grammar.Action('mansi:verb:set_person', arguments=['3']),
        grammar.Action('gram:number:set_dual')
    ]
).add_class('l_non_friendly')

rombandeeva.add_element('mansi:VowMorpheme', '^ув', 'uv_obj_conj').applied(
    grammar.LinkSentence('# & universal:entity=(token) & mansi:conj=(obj)'),
    [
        grammar.Action('mansi:verb:set_person', arguments=['1']),
        grammar.Action('gram:number:set_plur')
    ]
).add_class('l_friendly')

rombandeeva.add_element('mansi:morphemeYU', '^а!ныл', 'jaanyl_obj_conj').applied(
    grammar.LinkSentence('# & universal:entity=(token) & mansi:conj=(obj)'),
    [
        grammar.Action('mansi:verb:set_person', arguments=['3']),
        grammar.Action('gram:number:set_plur')
    ]
)

# IN PLUR ONLY:
rombandeeva.add_element('universal:morpheme', '^ныл', 'nyl_obj_conj').applied(
    grammar.LinkSentence('# & universal:entity=(tooken) & mansi:conj=(obj)'),
    [
        grammar.Action('mansi:verb:set_person', arguments=['3']),
        grammar.Action('gram:number:set_plur')
    ]
)

rombandeeva.get_system('universal:morpheme').subclasses_order(
    '#an_suffix_obj_plur > #nyl_obj_conj',
    parent_filter=grammar.LinkSentence('universal:entity=(token) & mansi:conj=(obj)'),
    strict=True
)

# page 124

rombandeeva.add_element('universal:collocation', '''
    <[mansi:conj=(obj)]> *1
    тах''', 'analytic_future_for_obj_conj').applied(
    grammar.LinkSentence('# & universal:entity=(input)'),
    [
        grammar.Action('gram:tense:set_future')
    ]
)

rombandeeva.get_system('universal:morpheme').subclasses_order(
    '#ve_spc_suffix > .subj_pass_suffixes |',
    parent_filter=grammar.LinkSentence(
        'universal:entity=(token) & mansi:conj=(subj_pass)'
    )
)

rombandeeva.add_element('mansi:VowMorpheme', '^м', 'm_suffix_subj_pass').applied(
    grammar.LinkSentence('# & universal:entity=(token) & mansi:conj=(subj_pass)'),
    [
        grammar.Action('mansi:verb:set_person', arguments=['1']),
        grammar.Action('gram:number:set_sing')
    ]
).add_class('subj_pass_suffixes')

rombandeeva.add_element('mansi:VowMorpheme', '^н', 'n_suffix_subj_pass').applied(
    grammar.LinkSentence('# & universal:entity=(token) & mansi:conj=(subj_pass)'),
    [
        grammar.Action('mansi:verb:set_person', arguments=['2']),
        grammar.Action('gram:number:set_sing', branching=True),
        grammar.Action('gram:number:set_dual', branching=True),
        grammar.Action('gram:number:set_plur', branching=True)
    ]
).add_class('subj_pass_suffixes')

rombandeeva.add_element('universal:morpheme', grammar.Temp.null(), 'null_suffix_subj_pass').applied(
    grammar.LinkSentence('# & universal:entity=(token) & mansi:conj=(subj_pass)'),
    [
        grammar.Action('mansi:verb:set_person', arguments=['3']),
        grammar.Action('gram:number:set_sing')
    ]
).add_class('subj_pass_suffixes')

rombandeeva.add_element('mansi:VowMorpheme', '^ме!н', 'men_suffix_subj_pass').applied(
    grammar.LinkSentence('# & universal:entity=(token) & mansi:conj=(subj_pass)'),
    [
        grammar.Action('mansi:verb:set_person', arguments=['1']),
        grammar.Action('gram:number:set_dual')
    ]
).add_class('subj_pass_suffixes')

rombandeeva.add_element('mansi:VowMorpheme', '^г', 'g_suffix_subj_pass').applied(
    grammar.LinkSentence('# & universal:entity=(token) & mansi:conj=(subj_pass)'),
    [
        grammar.Action('mansi:verb:set_person', arguments=['3']),
        grammar.Action('gram:number:set_dual')
    ]
).add_class('subj_pass_suffixes')

rombandeeva.add_element('mansi:VowMorpheme', '^в', 'v_suffix_subj_pass').applied(
    grammar.LinkSentence('# & universal:entity=(token) & mansi:conj=(subj_pass)'),
    [
        grammar.Action('mansi:verb:set_person', arguments=['1']),
        grammar.Action('gram:number:set_plur')
    ]
).add_class('subj_pass_suffixes')

rombandeeva.add_element('mansi:VowMorpheme', '^т', 't_suffix_subj_pass').applied(
    grammar.LinkSentence('# & universal:entity=(token) & mansi:conj=(subj_pass)'),
    [
        grammar.Action('mansi:verb:set_person', arguments=['3']),
        grammar.Action('gram:number:set_plur')
    ]
).add_class('subj_pass_suffixes')

rombandeeva.get_system('universal:morpheme').subclasses_order(
    '.past_suffixes > .subj_pass_suffixes',
    parent_filter=grammar.LinkSentence('universal:entity=(token) & mansi:conj=(subj_pass)')
)

rombandeeva.add_element('universal:collocation', '''
    <[mansi:conj=(subj_pass)]> *1
    тах''', 'analytic_future_for_subj_pass_conj').applied(
    grammar.LinkSentence('# & universal:entity=(input)'),
    [
        grammar.Action('gram:tense:set_future')
    ]
)

# page 126

rombandeeva.add_element('universal:morpheme', '^э', 'e_suffix_imperative_present').applied(
    grammar.LinkSentence('# & universal:entity=(token) & mansi:basic_pos=(verb)'),
    [
        grammar.Action('gram:tense:set_present')
    ]
).add_class('imperative_present_2sg')

rombandeeva.add_element('universal:morpheme', '^е', 'ye_suffix_imperative_present').applied(
    grammar.LinkSentence('# & universal:entity=(token) & mansi:basic_pos=(verb)'),
    [
        grammar.Action('gram:tense:set_present')
    ]
).add_class('imperative_present_2sg')

rombandeeva.get_system('universal:morpheme').subclasses_order(
    '.imperative_present_2sg > #n_suffix_imperative',
    parent_filter=grammar.LinkSentence('universal:entity=(token) & mansi:basic_pos=(verb)'),
    select_into={
        'id': 'imperative_group_2sg',
        'classes': ['imperative_group'],
        'actions': [
            grammar.Action('gram:mood:set_imperative'),
            grammar.Action('mansi:verb:set_person', arguments=['2']),
            grammar.Action('gram:number:set_sing')
        ]
    },
    strict=True
)

rombandeeva.add_element('universal:morpheme', '^н', 'n_suffix_imperative').applied(
    grammar.LinkSentence('# & universal:entity=(token) & mansi:basic_pos=(verb)'),
    [
        grammar.Action('gram:mood:set_imperative')
    ]
)

rombandeeva.add_element('universal:morpheme', '^э!', 'ee_suffix_imperative_present').applied(
    grammar.LinkSentence('# & universal:entity=(token) & mansi:basic_pos=(verb)'),
    [
        grammar.Action('gram:tense:set_present')
    ]
).add_class('imperative_present_2du_pl')

rombandeeva.add_element('universal:morpheme', '^е!', 'yee_suffix_imperative_present').applied(
    grammar.LinkSentence('# & universal:entity=(token) & mansi:basic_pos=(verb)'),
    [
        grammar.Action('gram:tense:set_present')
    ]
).add_class('imperative_present_2du_pl')

rombandeeva.get_system('universal:morpheme').subclasses_order(
    '.imperative_present_2du_pl > #n_suffix_imperative',
    parent_filter=grammar.LinkSentence('universal:entity=(token) & mansi:basic_pos=(verb)'),
    select_into={
        'id': 'imperative_group_2du_pl',
        'classes': ['imperative_group'],
        'actions': [
            grammar.Action('gram:mood:set_imperative'),
            grammar.Action('mansi:verb:set_person', arguments=['2']),
            grammar.Action('gram:number:set_dual', branching=True),
            grammar.Action('gram:number:set_plur', branching=True)
        ]
    },
    strict=True
)

### RUN seq:correction:mansi* mutation
### create mansi:morphemeYU
