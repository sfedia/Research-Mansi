import grammar
rombandeeva = grammar.Container()
# ...
rombandeeva.add_element('universal:morpheme', '^та!л', 'tal_suffix').applied(
    [
        grammar.LinkSentence('entity:(word) & pos:(adj)'),
        [grammar.Action('sem:make_opposite:*')]
    ]
)

rombandeeva.add_element('universal:morpheme', '^т').add_class('caus_suffixes')
rombandeeva.add_element('universal:morpheme', '^л').add_class('caus_suffixes')
rombandeeva.add_element('universal:morpheme', '^лт').add_class('caus_suffixes')
rombandeeva.add_element('universal:morpheme', '^пт').add_class('caus_suffixes')
for el in rombandeeva.get_by_class_name('caus_suffixes'):
    el.applied(
        [grammar.LinkSentence('entity:(word) & pos:(verb) & non_causative?')]
    )
$rombandeeva:'caus_suffixes'.applied (
    [
        MG_LINK entity:(word) & pos:(verb) & non_causative? MG_LINK,
        [ MG_ACTION sem:make_causative MG_ACTION ]
    ]
)
$rombandeeva.append(MORPHO ^юв MORPHO, 'yuv_suffix')
$rombandeeva:'yuv_suffix'.applied (
    [
        MG_LINK entity:(word) & pos:(noun) MG_LINK,
        [ MG_ACTION gram:make_possessive MG_ACTION ]
    ]
)
$rombandeeva:'yuv_suffix'.add_class('lps')

$rombandeeva.append(
    MG_ORDER
        class:(number_suffix) >> class:(lps) >> class:(case_suffix)
    MG_ORDER,
    'noun_suff_order_1'
)
$rombandeeva:'noun_suff_order_1'.applied (
    [
        MG_LINK entity:(word) & pos:(noun) MG_LINK,
        []
    ]
)

$rombandeeva.append(
    MG_ORDER
        entity:(morpheme) & morpheme_type:(prefix) + <<
        entity:(morpheme) & morpheme_type:(root) >>
        class:(word_building_suffix) & applied*:(pos:(verb)) + >>
        class:(word_inflection_suffix) & applied*:(pos:(verb)) +
    MG_ORDER
)

# POS
$rombandeeva.append(MG_POS noun MG_POS, MG_CL noun, pos MG_CL)
$rombandeeva:'noun'.applied(
    [
        MG_LINK entity:(word) & dictionary_recognized_pos:(noun),
        [ MG_ACTION [syntax|morphology]:set_basic_pos:noun MG_ACTION ]
    ]
)

$rombandeeva.append(MG_POS adj MG_POS, MG_CL adj, pos MG_CL)
$rombandeeva:'adj'.applied(
    [
        MG_LINK entity:(word) & dictionary_recognized_pos:(adj),
        [ MG_ACTION [syntax|morphology]:set_basic_pos:adj MG_ACTION ]
    ]
)

$rombandeeva.append(MG_POS adj MG_POS, MG_CL adj, pos MG_CL)
$rombandeeva:'adj'.applied(
    [
        MG_LINK entity:(word) & dictionary_recognized_pos:(adj),
        [ MG_ACTION [syntax|morphology]:set_basic_pos:adj MG_ACTION ]
    ]
)

$rombandeeva.append(MG_POS pronoun MG_POS, MG_CL pronoun, pos MG_CL)
$rombandeeva:'pronoun'.applied(
    [
        MG_LINK entity:(word) & dictionary_recognized_pos:(pronoun),
        [ MG_ACTION [syntax|morphology]:set_basic_pos:pronoun MG_ACTION ]
    ]
)

$rombandeeva.append(MG_POS verb MG_POS, MG_CL verb, pos MG_CL)
$rombandeeva:'verb'.applied(
    [
        MG_LINK entity:(word) & dictionary_recognized_pos:(verb),
        [ MG_ACTION [syntax|morphology]:set_basic_pos:verb MG_ACTION ]
    ]
)

$rombandeeva.append(MG_POS adverb MG_POS, MG_CL adverb, pos MG_CL)
$rombandeeva:'adverb'.applied(
    [
        MG_LINK entity:(word) & dictionary_recognized_pos:(adverb),
        [ MG_ACTION [syntax|morphology]:set_basic_pos:adverb MG_ACTION ]
    ]
)


$rombandeeva.append(MG_POS postposition MG_POS, MG_CL postposition, pos MG_CL)
$rombandeeva:'postposition'.applied(
    [
        # should this one have another entity?
        MG_LINK entity:(word) & dictionary_recognized_pos:(postposition),
        [ MG_ACTION [syntax|morphology]:set_basic_pos:postposition MG_ACTION ]
    ]
)
# postposition is special by default

$rombandeeva.append(MG_POS particle MG_POS, MG_CL particle, pos MG_CL)
$rombandeeva:'particle'.applied(
    [
        MG_LINK entity:(word) & dictionary_recognized_pos:(particle),
        [ MG_ACTION [syntax|morphology]:set_basic_pos:particle MG_ACTION ]
    ]
)
    
$rombandeeva.append(MG_POS particle MG_POS, MG_CL conjunction, pos MG_CL)
$rombandeeva:'conjunction'.applied(
    [
        MG_LINK entity:(word) & dictionary_recognized_pos:(conjunction),
        [ MG_ACTION [syntax|morphology]:set_basic_pos:conjunction MG_ACTION ]
    ]
)
# существительное

$rombandeeva.append(
    MG_ACTION
        [syntax|morphology]:basic_pos:noun:question->clear;
        [syntax|morphology]:basic_pos:noun:set_question >
            [gram|sem]:question:WHO <
        ;        
    MG_ACTION,
    'who_question_for_nouns'
)
$rombandeeva:'who_question_for_nouns'.applied(
    [
        MG_LINK entity:(word) & sem:semcat_check > human <; MG_LINK,
        []
    ]
)

$rombandeeva.append(
    MG_ACTION
        [syntax|morphology]:basic_pos:noun:question->clear;
        [syntax|morphology]:basic_pos:noun:set_question >
            [gram|sem]:question:WHAT <
        ;        
    MG_ACTION,
    'what_question_for_nouns'
)
$rombandeeva:'what_question_for_nouns'.applied(
    [
        MG_LINK entity:(word) &! sem:semcat_check > human <; MG_LINK,
        []
    ]
)